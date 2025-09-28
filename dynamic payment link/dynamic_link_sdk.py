import json
import requests
import base64
from encryption import EncryptionUtils
from constants import YagoutPayConstants
from typing import Dict, Any
from datetime import datetime, timedelta
import re

class YagoutPaySDK:
    def __init__(self, merchant_id: str, encryption_key: str):
        """Initialize SDK with merchant credentials."""
        if not merchant_id or not encryption_key:
            raise ValueError("Merchant ID and encryption key are required.")
        try:
            key_bytes = base64.b64decode(encryption_key)
            if len(key_bytes) != 32:
                raise ValueError(f"Encryption key must decode to 32 bytes, got {len(key_bytes)}")
        except base64.binascii.Error:
            raise ValueError("Encryption key must be a valid base64-encoded string")
        self.merchant_id = merchant_id
        self.encryption_key = encryption_key
        self.utils = EncryptionUtils()
        self.base_url = YagoutPayConstants.BASE_URL_TEST

    def encrypt(self, text: str) -> str:
        """Encrypt text using AES-256-CBC."""
        try:
            return self.utils.encrypt(text, self.encryption_key)
        except ValueError as e:
            raise ValueError(f"Encryption failed: {str(e)}")

    def decrypt(self, encrypted: str) -> str:
        """Decrypt encrypted text using AES-256-CBC."""
        try:
            return self.utils.decrypt(encrypted, self.encryption_key)
        except ValueError as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def create_dynamic_link(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a dynamic payment link with customizable payload."""
        required_fields = {"req_user_id", "me_id", "amount", "mobile_no", "expiry_date",
                          "media_type", "order_id", "first_name", "last_name", "product",
                          "dial_code", "failure_url", "success_url", "country", "currency", "customer_email"}
        if not all(field in payload for field in required_fields):
            return {"status": "error", "message": "Missing required payload fields"}

        # Validate expiry date (within 30 days)
        expiry_date = datetime.strptime(payload["expiry_date"], "%Y-%m-%d")
        max_date = datetime.now() + timedelta(days=30)
        if expiry_date > max_date:
            return {"status": "error", "message": "Expiry date must be within 30 days"}

        try:
            json_str = json.dumps(payload)
            encrypted_request = self.encrypt(json_str)
            response = requests.post(
                f"{self.base_url}{YagoutPayConstants.DYNAMIC_LINK_ENDPOINT}",
                headers={"me_id": self.merchant_id, "Content-Type": "application/json"},
                json={"request": encrypted_request},
                timeout=30,
                verify=False
            )
            response.raise_for_status()
            response_text = response.text
            print(f"Raw Response (Dynamic): {response_text}")  # Debug
            print(f"Status Code: {response.status_code}")  # Debug
            print(f"Headers: {response.headers}")  # Debug
            decrypted_response = self.decrypt(response_text)
            # Extract PaymentLink from decrypted response
            link_match = re.search(r'"PaymentLink":"([^"]+)"', decrypted_response)
            if link_match:
                return {"status": "success", "link": link_match.group(1)}
            message_match = re.search(r"message\s*=\s*([^,]+)", decrypted_response)
            if message_match:
                return {"status": "error", "message": message_match.group(1).strip()}
            return {"status": "success", "link": decrypted_response}
        except requests.RequestException as e:
            return {"status": "error", "message": f"API request failed: {str(e)}"}
        except ValueError as e:
            return {"status": "error", "message": str(e)}
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}

if __name__ == "__main__":
    sdk = YagoutPaySDK("me id", "aes key")
    dynamic_payload = {
        "req_user_id": "yagou381",
        "me_id": "your me id",
        "amount": "500",
        "customer_email": "",
        "mobile_no": "0909260339",
        "expiry_date": "2025-10-23",
        "media_type": ["API"],
        "order_id": "DYN_20250923_150",  # Unique dynamic order ID
        "first_name": "YagoutPay",
        "last_name": "DynamicLink",
        "product": "Premium Subscription",
        "dial_code": "+251",
        "failure_url": "http://localhost:3000/failure",
        "success_url": "http://localhost:3000/success",
        "country": "ETH",
        "currency": "ETB"
    }
    print("Dynamic Link Response:", sdk.create_dynamic_link(dynamic_payload))
