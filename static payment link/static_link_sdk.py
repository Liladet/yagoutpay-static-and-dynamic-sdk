import json
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import warnings
from urllib3.exceptions import InsecureRequestWarning
import qrcode

# Suppress InsecureRequestWarning for UAT testing (remove in production)
warnings.simplefilter('ignore', InsecureRequestWarning)

def encrypt(text, key_b64):
    """Encrypt text using AES-256-CBC with PKCS7 padding"""
    try:
        key = base64.b64decode(key_b64)
        if len(key) != 32:
            raise ValueError(f"Invalid key length: {len(key)} bytes, expected 32")
        iv = b"0123456789abcdef"
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(text.encode()) + padder.finalize()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(ct).decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        raise

def decrypt(crypt_b64, key_b64):
    """Decrypt text using AES-256-CBC with PKCS7 unpadding"""
    try:
        key = base64.b64decode(key_b64)
        if len(key) != 32:
            raise ValueError(f"Invalid key length: {len(key)} bytes, expected 32")
        iv = b"0123456789abcdef"
        crypt = base64.b64decode(crypt_b64)
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        padtext = decryptor.update(crypt) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padtext) + unpadder.finalize()
        return data.decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        raise

def generate_qr_code(data, filename):
    """Generate a QR code image from the given data and save it to filename"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print(f"QR code saved as {filename}")
    except Exception as e:
        print(f"Failed to generate QR code: {e}")
        raise

# Step 1: Prepare payload
payload = {
    "ag_id": "",
    "ag_code": "",
    "ag_name": "",
    "req_user_id": "yagou381",
    "me_code": "202508080001",
    "me_name": "",
    "qr_code_id": "",
    "brandName": "Lidiya",
    "qr_name": "",
    "status": "ACTIVE",
    "storeName": "YP",
    "store_id": "",
    "token": "",
    "qr_transaction_amount": "1",
    "logo": "",
    "store_email": "",
    "mobile_no": "",
    "udf": "",
    "udfmerchant": "",
    "file_name": "",
    "from_date": "",
    "to_date": "",
    "file_extn": "",
    "file_url": "",
    "file": "",
    "original_file_name": "",
    "successURL": "",
    "failureURL": "",
    "addAll": "",
    "source": ""
}
payload_json = json.dumps(payload)

# Step 2: Encrypt payload
key_b64 = "IG3CNW5uNrUO2mU2htUOWb9rgXCF7XMAXmL63d7wNZo="  # Replace with actual key
try:
    encrypted_payload = encrypt(payload_json, key_b64)
    print("Encrypted payload:", encrypted_payload)
    request_body = {"request": encrypted_payload}
except Exception as e:
    print(f"Failed to encrypt payload: {e}")
    exit()

# Step 3: Send API request
url = "https://uatcheckout.yagoutpay.com/ms-transaction-core-1-0/sdk/staticQRPaymentResponse"
headers = {
    "Content-Type": "application/json",
    "me_id": "202508080001"
}
try:
    # Disable SSL verification for UAT (remove in production)
    response = requests.post(url, json=request_body, headers=headers, verify=False)
except Exception as e:
    print(f"API request failed: {e}")
    exit()

# Step 4: Process response
if response.status_code == 200:
    print("Raw API response:", response.text)
    try:
        response_data = response.json()
        print("Parsed JSON response:", response_data)
        encrypted_response = response_data.get("responseData")
        if encrypted_response is None:
            print("Error: 'responseData' key not found in API response")
            exit()
    except ValueError as e:
        print(f"Error: Failed to parse JSON response: {e}")
        print("Raw response:", response.text)
        exit()
else:
    print(f"API request failed with status {response.status_code}: {response.text}")
    exit()

# Step 5: Decrypt response
try:
    decrypted_response = decrypt(encrypted_response, key_b64)
    print("Decrypted response:", decrypted_response)
    decrypted_json = json.loads(decrypted_response)
    print("Parsed decrypted JSON:", decrypted_json)
    # Extract payment link and QR ID from responseData
    response_data = decrypted_json.get("responseData", {})
    payment_link = response_data.get("staticLink")
    qr_id = response_data.get("qrId")
    if payment_link:
        print(f"Payment Link: {payment_link}")
        print(f"QR ID: {qr_id}")
        # Step 6: Generate QR code for the payment link
        qr_filename = f"payment_qr_{qr_id}.png"
        generate_qr_code(payment_link, qr_filename)
    else:
        print("Error: 'staticLink' not found in decrypted responseData")
except Exception as e:
    print(f"Failed to decrypt response: {e}")