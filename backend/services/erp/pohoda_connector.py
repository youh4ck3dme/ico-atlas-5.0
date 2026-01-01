"""
Pohoda ERP connector
Slovenský ERP systém - API integrácia
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests

from .base_connector import BaseErpConnector


class PohodaConnector(BaseErpConnector):
    """Connector pre Pohoda ERP systém"""

    def __init__(self, connection_data: Dict):
        super().__init__(connection_data)
        self.api_key = connection_data.get("api_key")
        self.company_id = connection_data.get("company_id")
        self.base_url = connection_data.get("base_url", "https://api.pohoda.sk")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def test_connection(self) -> Dict:
        """Test pripojenia k Pohoda API"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/company/info", headers=self.headers, timeout=10
            )

            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Pohoda connection successful",
                    "data": response.json(),
                }
            else:
                return {
                    "success": False,
                    "message": f"Pohoda API error: {response.status_code}",
                    "error": response.text,
                }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Connection error: {str(e)}",
                "error": str(e),
            }

    def get_company_info(self) -> Dict:
        """Získa informácie o firme z Pohoda"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/company/info", headers=self.headers, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "company_name": data.get("name", ""),
                    "company_id": data.get("id", ""),
                    "ico": data.get("ico", ""),
                    "address": data.get("address", ""),
                    "erp_type": "pohoda",
                }
            else:
                return {"error": f"API error: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_suppliers(self, limit: int = 100) -> List[Dict]:
        """Získa zoznam dodávateľov z Pohoda"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/suppliers?limit={limit}",
                headers=self.headers,
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                suppliers = data.get("data", [])

                result = []
                for supplier in suppliers:
                    result.append(
                        {
                            "ico": supplier.get("ico", ""),
                            "name": supplier.get("name", ""),
                            "address": supplier.get("address", ""),
                            "total_invoices": supplier.get("invoice_count", 0),
                            "total_amount": supplier.get("total_amount", 0),
                        }
                    )

                return result
            else:
                return []
        except requests.exceptions.RequestException:
            return []

    def get_supplier_payment_history(
        self, supplier_ico: str, days: int = 365
    ) -> List[Dict]:
        """Získa históriu platieb pre dodávateľa"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            response = requests.get(
                f"{self.base_url}/api/v1/invoices",
                headers=self.headers,
                params={
                    "supplier_ico": supplier_ico,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                invoices = data.get("data", [])

                result = []
                for invoice in invoices:
                    result.append(
                        {
                            "invoice_number": invoice.get("number", ""),
                            "amount": invoice.get("amount", 0),
                            "due_date": invoice.get("due_date", ""),
                            "paid_date": invoice.get("paid_date"),
                            "status": invoice.get(
                                "status", ""
                            ),  # paid, unpaid, overdue
                            "days_paid_early": invoice.get("days_paid_early", 0),
                            "days_paid_late": invoice.get("days_paid_late", 0),
                        }
                    )

                return result
            else:
                return []
        except requests.exceptions.RequestException:
            return []

    def get_invoices(
        self, supplier_ico: Optional[str] = None, status: Optional[str] = None
    ) -> List[Dict]:
        """Získa faktúry z Pohoda"""
        try:
            params = {}
            if supplier_ico:
                params["supplier_ico"] = supplier_ico
            if status:
                params["status"] = status

            response = requests.get(
                f"{self.base_url}/api/v1/invoices",
                headers=self.headers,
                params=params,
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
            else:
                return []
        except requests.exceptions.RequestException:
            return []
