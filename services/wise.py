import uuid

import requests
from decouple import config
from fastapi import HTTPException
import json


class WiseService:
    def __init__(self):
        self.main_url = config("WISE_URL")
        self.headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}"
        }
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self):
        url = self.main_url + "/v2/profiles"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            response = response.json()
            return [el["id"] for el in response if el["type"] == "PERSONAL"]
        print(response)
        raise HTTPException(500, "Payment provider is not available at the moment")

    def create_quote(self, amount):
        url = self.main_url + f"/v3/profiles/{self.profile_id[0]}/quotes"
        data = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "sourceAmount": amount,
            "targetAmount": None
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        print(resp.json())
        raise HTTPException(500, "Payment provider is not available at the moment")

    def create_recipient_account(self, full_name, iban):
        url = self.main_url + "/v1/accounts"
        data = {
            "currency": "EUR",
            "type": "IBAN",
            "profile": self.profile_id[0],
            "ownedByCustomer": True,
            "accountHolderName": full_name,
            "details": {
                "legalType": "PRIVATE",
                "iban": iban
            }
        }

        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        print(resp.json())
        raise HTTPException(500, "Payment provider is not available at the moment")

    def create_transfer(self, target_account_id, quote_id):
        customer_transaction_id = str(uuid.uuid4())
        url = self.main_url + "/v1/transfers"
        data = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id,

        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        print(resp.json())
        raise HTTPException(500, "Payment provider is not available at the moment")

    def fund_transfer(self, transfer_id):
        url = self.main_url + f"/v3/profiles/{self.profile_id[0]}/transfers/{transfer_id}/payments"
        data = {
            "type": "BALANCE"
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        if resp.status_code == 201:
            resp = resp.json()
            return resp
        print(resp.json())
        raise HTTPException(500, "Payment provider is not available at the moment")

    def cancel_fund(self, transfer_id):
        url = self.main_url + f"/v1/transfers/{transfer_id}/cancel"
        resp = requests.put(url, headers=self.headers)
        if resp.status_code == 200:
            resp = resp.json()
            return resp
        print(resp.json())
        raise HTTPException(500, "Payment provider is not available at the moment")


