"""
SAP ERP connector
SAP Business One / SAP ERP - API integrácia
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests

from .base_connector import BaseErpConnector


class SapConnector(BaseErpConnector):
    """Connector pre SAP ERP systém"""

    def __init__(self, connection_data: Dict):
        super().__init__(connection_data)
        self.server_url = connection_data.get("server_url")
        self.username = connection_data.get("username")
        self.password = connection_data.get("password")
        self.company_db = connection_data.get("company_db")
        self.base_url = f"{self.server_url}/b1s/v1"

        # SAP OData API authentication
        self.session = requests.Session()
        self._authenticate()

    def _authenticate(self) -> bool:
        """Autentifikácia v SAP systéme"""
        try:
            response = self.session.post(
                f"{self.base_url}/Login",
                json={
                    "CompanyDB": self.company_db,
                    "UserName": self.username,
                    "Password": self.password,
                },
                timeout=10,
            )

            if response.status_code == 200:
                # SAP vráti session cookie
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False

    def test_connection(self) -> Dict:
        """Test pripojenia k SAP API"""
        try:
            if not self._authenticate():
                return {
                    "success": False,
                    "message": "SAP authentication failed",
                    "error": "Invalid credentials",
                }

            response = self.session.get(f"{self.base_url}/CompanyService", timeout=10)

            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "SAP connection successful",
                    "data": response.json(),
                }
            else:
                return {
                    "success": False,
                    "message": f"SAP API error: {response.status_code}",
                    "error": response.text,
                }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Connection error: {str(e)}",
                "error": str(e),
            }

    def get_company_info(self) -> Dict:
        """Získa informácie o firme z SAP"""
        try:
            if not self._authenticate():
                return {"error": "Authentication failed"}

            response = self.session.get(f"{self.base_url}/CompanyService", timeout=10)

            if response.status_code == 200:
                data = response.json()
                return {
                    "company_name": data.get("CompanyName", ""),
                    "company_id": data.get("CompanyDB", ""),
                    "ico": data.get("TaxIdNum", ""),
                    "address": data.get("Address", ""),
                    "erp_type": "sap",
                }
            else:
                return {"error": f"API error: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_suppliers(self, limit: int = 100) -> List[Dict]:
        """Získa zoznam dodávateľov z SAP"""
        try:
            if not self._authenticate():
                return []

            response = self.session.get(
                f"{self.base_url}/BusinessPartners",
                params={
                    "$filter": "CardType eq 'S'",  # S = Supplier
                    "$top": limit,
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                suppliers = data.get("value", [])

                result = []
                for supplier in suppliers:
                    result.append(
                        {
                            "ico": supplier.get("TaxIdNum", ""),
                            "name": supplier.get("CardName", ""),
                            "address": supplier.get("Address", ""),
                            "total_invoices": 0,  # SAP neposkytuje priamo
                            "total_amount": 0,
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
            if not self._authenticate():
                return []

            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # SAP query pre faktúry dodávateľa
            response = self.session.get(
                f"{self.base_url}/PurchaseInvoices",
                params={
                    "$filter": f"TaxIdNum eq '{supplier_ico}' and DocDate ge {start_date.strftime('%Y-%m-%d')}",
                    "$expand": "DocumentLines",
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                invoices = data.get("value", [])

                result = []
                for invoice in invoices:
                    result.append(
                        {
                            "invoice_number": invoice.get("DocNum", ""),
                            "amount": invoice.get("DocTotal", 0),
                            "due_date": invoice.get("DocDueDate", ""),
                            "paid_date": invoice.get("PaidToDate"),
                            "status": "paid" if invoice.get("PaidToDate") else "unpaid",
                            "days_paid_early": 0,
                            "days_paid_late": 0,
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
        """Získa faktúry z SAP"""
        try:
            if not self._authenticate():
                return []

            filter_parts = []
            if supplier_ico:
                filter_parts.append(f"TaxIdNum eq '{supplier_ico}'")
            if status:
                if status == "paid":
                    filter_parts.append("PaidToDate ne null")
                elif status == "unpaid":
                    filter_parts.append("PaidToDate eq null")

            filter_str = " and ".join(filter_parts) if filter_parts else None

            params = {}
            if filter_str:
                params["$filter"] = filter_str

            response = self.session.get(
                f"{self.base_url}/PurchaseInvoices", params=params, timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("value", [])
            else:
                return []
        except requests.exceptions.RequestException:
            return []
