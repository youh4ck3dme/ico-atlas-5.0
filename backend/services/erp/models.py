"""
Database models pre ERP integrácie
"""

import enum
from datetime import datetime
from typing import Dict

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from services.database import Base


class ErpType(str, enum.Enum):
    """Typy ERP systémov"""

    SAP = "sap"
    POHODA = "pohoda"
    MONEY_S3 = "money_s3"


class ErpConnectionStatus(str, enum.Enum):
    """Status ERP pripojenia"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    SYNCING = "syncing"


class ErpConnection(Base):
    """ERP pripojenie používateľa"""

    __tablename__ = "erp_connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    erp_type = Column(SQLEnum(ErpType), nullable=False)
    status = Column(
        SQLEnum(ErpConnectionStatus),
        default=ErpConnectionStatus.INACTIVE,
        nullable=False,
    )

    # Connection credentials (encrypted)
    # V produkcii by sme použili šifrovanie (napr. Fernet)
    connection_data = Column(JSON, nullable=False)  # API keys, URLs, etc.

    # Sync settings
    sync_enabled = Column(Boolean, default=True, nullable=False)
    sync_frequency = Column(String(50), default="daily")  # daily, weekly, manual
    last_sync_at = Column(DateTime, nullable=True)
    next_sync_at = Column(DateTime, nullable=True)

    # Metadata
    company_name = Column(String(255), nullable=True)  # Názov firmy v ERP
    company_id = Column(String(100), nullable=True)  # ID firmy v ERP

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'erp_type': self.erp_type.value,
            'status': self.status.value,
            'sync_enabled': self.sync_enabled,
            'sync_frequency': self.sync_frequency,
            'last_sync_at': self.last_sync_at.isoformat() if self.last_sync_at else None,
            'next_sync_at': self.next_sync_at.isoformat() if self.next_sync_at else None,
            'company_name': self.company_name,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    # Relationships
    user = relationship("User", backref="erp_connections")
    sync_logs = relationship(
        "ErpSyncLog", back_populates="connection", cascade="all, delete-orphan"
    )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "erp_type": self.erp_type.value,
            "status": self.status.value,
            "sync_enabled": self.sync_enabled,
            "sync_frequency": self.sync_frequency,
            "last_sync_at": self.last_sync_at.isoformat()
            if self.last_sync_at
            else None,
            "next_sync_at": self.next_sync_at.isoformat()
            if self.next_sync_at
            else None,
            "company_name": self.company_name,
            "company_id": self.company_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ErpSyncLog(Base):
    """Log synchronizácií ERP dát"""

    __tablename__ = "erp_sync_logs"

    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(
        Integer, ForeignKey("erp_connections.id"), nullable=False, index=True
    )

    # Sync details
    sync_type = Column(String(50), nullable=False)  # full, incremental, manual
    status = Column(String(50), nullable=False)  # success, error, partial
    records_synced = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)

    # Error details
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True)

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    # Relationships
    connection = relationship("ErpConnection", back_populates="sync_logs")

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "connection_id": self.connection_id,
            "sync_type": self.sync_type,
            "status": self.status,
            "records_synced": self.records_synced,
            "records_failed": self.records_failed,
            "error_message": self.error_message,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat()
            if self.completed_at
            else None,
            "duration_seconds": self.duration_seconds,
        }
