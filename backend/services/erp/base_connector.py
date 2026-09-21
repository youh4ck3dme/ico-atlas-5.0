"""
Base class pre ERP connectors
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class BaseErpConnector(ABC):
    """Base class pre všetky ERP connectors"""

    def __init__(self, connection_data: Dict):
        """
        Args:
            connection_data: Dict s credentials (API keys, URLs, etc.)
        """
        self.connection_data = connection_data
        self.erp_type = self.__class__.__name__.lower().replace("connector", "")

    @abstractmethod
    def test_connection(self) -> Dict:
        """
        Test pripojenia k ERP systému

        Returns:
            Dict s výsledkom testu
        """
        pass

    @abstractmethod
    def get_company_info(self) -> Dict:
        """
        Získa informácie o firme z ERP

        Returns:
            Dict s informáciami o firme
        """
        pass

    @abstractmethod
    def get_suppliers(self, limit: int = 100) -> List[Dict]:
        """
        Získa zoznam dodávateľov z ERP

        Args:
            limit: Maximálny počet výsledkov

        Returns:
            List[Dict] so zoznamom dodávateľov
        """
        pass

    @abstractmethod
    def get_supplier_payment_history(
        self, supplier_ico: str, days: int = 365
    ) -> List[Dict]:
        """
        Získa históriu platieb pre dodávateľa

        Args:
            supplier_ico: IČO dodávateľa
            days: Počet dní späť

        Returns:
            List[Dict] s históriou platieb
        """
        pass

    @abstractmethod
    def get_invoices(
        self, supplier_ico: Optional[str] = None, status: Optional[str] = None
    ) -> List[Dict]:
        """
        Získa faktúry z ERP

        Args:
            supplier_ico: IČO dodávateľa (None = všetky)
            status: Status faktúry (paid, unpaid, overdue)

        Returns:
            List[Dict] s faktúrami
        """
        pass

    def validate_connection_data(self) -> bool:
        """
        Validuje connection data

        Returns:
            True ak sú dáta platné
        """
        return bool(self.connection_data)
