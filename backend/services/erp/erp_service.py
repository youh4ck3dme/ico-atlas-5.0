"""
ERP Service Manager
Spravuje ERP pripojenia a synchronizácie
"""

class ErpService:
    """ERP Service class for managing ERP connections and synchronizations"""
    
    @staticmethod
    def get_connector(erp_type, connection_data):
        """Vytvorí správny connector podľa typu ERP"""
        from .models import ErpType
        from .money_s3_connector import MoneyS3Connector
        from .pohoda_connector import PohodaConnector
        from .sap_connector import SapConnector
        
        if erp_type == ErpType.POHODA:
            return PohodaConnector(connection_data)
        elif erp_type == ErpType.MONEY_S3:
            return MoneyS3Connector(connection_data)
        elif erp_type == ErpType.SAP:
            return SapConnector(connection_data)
        else:
            raise ValueError(f"Unknown ERP type: {erp_type}")

from datetime import datetime, timedelta
from typing import Dict, List

from sqlalchemy.orm import Session

from .models import ErpConnection, ErpConnectionStatus, ErpSyncLog, ErpType
from .money_s3_connector import MoneyS3Connector
from .pohoda_connector import PohodaConnector
from .sap_connector import SapConnector


def get_connector(erp_type: ErpType, connection_data: Dict):
    """Vytvorí správny connector podľa typu ERP"""
    if erp_type == ErpType.POHODA:
        return PohodaConnector(connection_data)
    elif erp_type == ErpType.MONEY_S3:
        return MoneyS3Connector(connection_data)
    elif erp_type == ErpType.SAP:
        return SapConnector(connection_data)
    else:
        raise ValueError(f"Unknown ERP type: {erp_type}")


@staticmethod
def create_erp_connection(
    db, user_id, erp_type, connection_data
) -> ErpConnection:
    """Vytvorí nové ERP pripojenie"""
    from .models import ErpConnection, ErpConnectionStatus
    
    connection = ErpConnection(
        user_id=user_id,
        erp_type=erp_type,
        connection_data=connection_data,
        status=ErpConnectionStatus.INACTIVE,
    )
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


@staticmethod
def test_erp_connection(erp_type, connection_data) -> Dict:
    """Testuje ERP pripojenie"""
    try:
        connector = ErpService.get_connector(erp_type, connection_data)
        result = connector.test_connection()
        return result
    except Exception as e:
        return {
            "success": False,
            "message": f"Connection test failed: {str(e)}",
            "error": str(e),
        }


@staticmethod
def activate_erp_connection(db, connection_id, user_id) -> bool:
    """Aktivuje ERP pripojenie"""
    from .models import ErpConnection, ErpConnectionStatus
    
    connection = (
        db.query(ErpConnection)
        .filter(ErpConnection.id == connection_id, ErpConnection.user_id == user_id)
        .first()
    )

    if not connection:
        return False

    # Test pripojenia
    test_result = ErpService.test_erp_connection(connection.erp_type, connection.connection_data)

    if test_result.get("success"):
        connection.status = ErpConnectionStatus.ACTIVE

        # Získať info o firme
        connector = ErpService.get_connector(connection.erp_type, connection.connection_data)
        company_info = connector.get_company_info()

        if "error" not in company_info:
            connection.company_name = company_info.get("company_name")
            connection.company_id = company_info.get("company_id")

        db.commit()
        return True
    else:
        connection.status = ErpConnectionStatus.ERROR
        db.commit()
        return False


@staticmethod
def deactivate_erp_connection(db, connection_id, user_id) -> bool:
    """Deaktivuje ERP pripojenie"""
    from .models import ErpConnection, ErpConnectionStatus
    
    connection = (
        db.query(ErpConnection)
        .filter(ErpConnection.id == connection_id, ErpConnection.user_id == user_id)
        .first()
    )

    if not connection:
        return False

    connection.status = ErpConnectionStatus.INACTIVE
    connection.sync_enabled = False
    db.commit()
    return True


@staticmethod
def get_user_erp_connections(db, user_id) -> List:
    """Získa všetky ERP pripojenia používateľa"""
    from .models import ErpConnection
    
    return (
        db.query(ErpConnection)
        .filter(ErpConnection.user_id == user_id)
        .order_by(ErpConnection.created_at.desc())
        .all()
    )


@staticmethod
def sync_erp_data(
    db, connection_id, user_id, sync_type="incremental"
) -> Dict:
    """Synchronizuje dáta z ERP"""
    from .models import ErpConnection, ErpConnectionStatus, ErpSyncLog
    
    connection = (
        db.query(ErpConnection)
        .filter(ErpConnection.id == connection_id, ErpConnection.user_id == user_id)
        .first()
    )

    if not connection:
        return {"success": False, "message": "Connection not found"}

    if connection.status != ErpConnectionStatus.ACTIVE:
        return {"success": False, "message": "Connection is not active"}

    # Vytvoriť sync log
    sync_log = ErpSyncLog(
        connection_id=connection_id,
        sync_type=sync_type,
        status="running",
        started_at=datetime.utcnow(),
    )
    db.add(sync_log)
    db.commit()

    try:
        connector = ErpService.get_connector(connection.erp_type, connection.connection_data)

        # Synchronizovať dodávateľov
        suppliers = connector.get_suppliers(limit=1000)
        records_synced = len(suppliers)
        records_failed = 0

        # TODO: Uložiť dáta do databázy alebo cache
        # Pre teraz len logujeme

        sync_log.status = "success"
        sync_log.records_synced = records_synced
        sync_log.records_failed = records_failed
        sync_log.completed_at = datetime.utcnow()
        sync_log.duration_seconds = int(
            (sync_log.completed_at - sync_log.started_at).total_seconds()
        )

        connection.last_sync_at = datetime.utcnow()

        # Nastaviť ďalšiu synchronizáciu
        if connection.sync_frequency == "daily":
            connection.next_sync_at = datetime.utcnow() + timedelta(days=1)
        elif connection.sync_frequency == "weekly":
            connection.next_sync_at = datetime.utcnow() + timedelta(weeks=1)

        db.commit()

        return {
            "success": True,
            "message": "Sync completed",
            "records_synced": records_synced,
            "records_failed": records_failed,
            "sync_log_id": sync_log.id,
        }
    except Exception as e:
        sync_log.status = "error"
        sync_log.error_message = str(e)
        sync_log.completed_at = datetime.utcnow()
        sync_log.duration_seconds = int(
            (sync_log.completed_at - sync_log.started_at).total_seconds()
        )
        db.commit()

        return {"success": False, "message": f"Sync failed: {str(e)}", "error": str(e)}


@staticmethod
def get_supplier_payment_history_from_erp(
    db, connection_id, user_id, supplier_ico, days=365
) -> List[Dict]:
    """Získa históriu platieb dodávateľa z ERP"""
    from .models import ErpConnection, ErpConnectionStatus
    
    connection = (
        db.query(ErpConnection)
        .filter(
            ErpConnection.id == connection_id,
            ErpConnection.user_id == user_id,
            ErpConnection.status == ErpConnectionStatus.ACTIVE,
        )
        .first()
    )

    if not connection:
        return []

    try:
        connector = ErpService.get_connector(connection.erp_type, connection.connection_data)
        return connector.get_supplier_payment_history(supplier_ico, days)
    except Exception as e:
        print(f"Error getting payment history: {e}")
        return []


@staticmethod
def get_erp_sync_logs(
    db, connection_id, user_id, limit=50
) -> List:
    """Získa logy synchronizácií"""
    from .models import ErpConnection, ErpSyncLog
    
    connection = (
        db.query(ErpConnection)
        .filter(ErpConnection.id == connection_id, ErpConnection.user_id == user_id)
        .first()
    )

    if not connection:
        return []

    return (
        db.query(ErpSyncLog)
        .filter(ErpSyncLog.connection_id == connection_id)
        .order_by(ErpSyncLog.started_at.desc())
        .limit(limit)
        .all()
    )
