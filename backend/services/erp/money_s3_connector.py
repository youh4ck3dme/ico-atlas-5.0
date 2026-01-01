"""
Money S3 ERP connector
Český ERP systém - API integrácia
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests

from .base_connector import BaseErpConnector


class MoneyS3Connector(BaseErpConnector):
    """Connector pre Money S3 ERP systém"""

    def __init__(self, connection_data: Dict):
        super().__init__(connection_data)
        self.api_key = connection_data.get("api_key")
        self.company_id = connection_data.get("company_id")
        self.base_url = connection_data.get("base_url", "https://api.moneys3.cz")
        self.headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}

    def test_connection(self) -> Dict:
        """Test pripojenia k Money S3 API"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/company", headers=self.headers, timeout=10
            )

            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Money S3 connection successful",
                    "data": response.json(),
                }
            else:
                return {
                    "success": False,
                    "message": f"Money S3 API error: {response.status_code}",
                    "error": response.text,
                }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Connection error: {str(e)}",
                "error": str(e),
            }

    def get_company_info(self) -> Dict:
        """Získa informácie o firme z Money S3"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/company", headers=self.headers, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "company_name": data.get("nazev", ""),
                    "company_id": data.get("id", ""),
                    "ico": data.get("ico", ""),
                    "address": data.get("adresa", ""),
                    "erp_type": "money_s3",
                }
            else:
                return {"error": f"API error: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_suppliers(self, limit: int = 100) -> List[Dict]:
        """Získa zoznam dodávateľov z Money S3"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/dodavatele?limit={limit}",
                headers=self.headers,
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                suppliers = data.get("dodavatele", [])

                result = []
                for supplier in suppliers:
                    result.append(
                        {
                            "ico": supplier.get("ico", ""),
                            "name": supplier.get("nazev", ""),
                            "address": supplier.get("adresa", ""),
                            "total_invoices": supplier.get("pocet_faktur", 0),
                            "total_amount": supplier.get("celkova_castka", 0),
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
                f"{self.base_url}/api/v1/faktury",
                headers=self.headers,
                params={
                    "ico": supplier_ico,
                    "datum_od": start_date.strftime("%Y-%m-%d"),
                    "datum_do": end_date.strftime("%Y-%m-%d"),
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                invoices = data.get("faktury", [])

                result = []
                for invoice in invoices:
                    result.append(
                        {
                            "invoice_number": invoice.get("cislo", ""),
                            "amount": invoice.get("castka", 0),
                            "due_date": invoice.get("datum_splatnosti", ""),
                            "paid_date": invoice.get("datum_uhrady"),
                            "status": invoice.get(
                                "stav", ""
                            ),  # zaplaceno, nezaplaceno, po_splatnosti
                            "days_paid_early": invoice.get("dni_pred_platbou", 0),
                            "days_paid_late": invoice.get("dni_po_splatnosti", 0),
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
        """Získa faktúry z Money S3"""
        try:
            params = {}
            if supplier_ico:
                params["ico"] = supplier_ico
            if status:
                params["stav"] = status

            response = requests.get(
                f"{self.base_url}/api/v1/faktury",
                headers=self.headers,
                params=params,
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("faktury", [])
            else:
                return []
        except requests.exceptions.RequestException:
            return []
