# YagoutPay Payment SDK

A lightweight Python SDK for YagoutPay's dynamic payment links and static QR code payments, with an optional HTML demo. Generates secure payment URLs and QR codes using AES-256-CBC encryption.

## Features

- **Dynamic Payment Links**: Generate unique, one-time payment URLs for e-commerce transactions.
- **Static QR Code Payments**: Create reusable payment links and QR codes for fixed-amount payments, ideal for store displays or printed materials.
- **Secure**: Uses AES-256-CBC encryption with a merchant-provided key.
- **Easy Integration**: Simple Python scripts for both payment methods.

# Quick Start

## ✅ Prerequisites

- Python 3.8+
- Git
- YagoutPay credentials (`MERCHANT_ID`, `MERCHANT_KEY`)
- ngrok (for dynamic payment callback testing)
- Flask (optional, for dynamic payment demo server)
- A QR code reader (for testing static QR codes)

## 🔒 Encryption

Uses AES-256-CBC with a 32-byte key and static IV (`0123456789abcdef`) for secure payloads. Contact YagoutPay for your encryption key.

## ⚡ Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Liladet/yagoutpay-dynamic-payment-sdk.git
   cd yagoutpay-dynamic-payment-sdk


- Install Dependencies
```bash
pip install requests cryptography qrcode pillow
pip install flask  # Optional, for dynamic payment demo
```

- requests: For HTTP requests to YagoutPay API.
- cryptography: For AES-256-CBC encryption/decryption.
- qrcode and pillow: For generating QR code images (static payments).
- flask: For running the demo server (dynamic payments).



# Dynamic Payment Links

- Configure Credentials
 Update dynamic_link_sdk.py with your YagoutPay credentials:
```bash
from dynamic_link_sdk import YagoutPaySDK
sdk = YagoutPaySDK("your mid", "aes key")
```

- Run the Server (Optional)
 For callback testing, run the Flask server and expose it with ngrok:
```bash
python app.py
ngrok http 3000
```
Update success_url and failure_url in the payload with ngrok URLs.

- Generate a Payment Link
  
Run dynamic_link_sdk.py or app.py to generate a payment link. See docs/usage.md for details.


# Static QR Code Payments

-Configure Credentials
 Update static_link_sdk.py with your YagoutPay credentials:
 ```bash
key_b64 = "aes key"  # Replace with your key
headers = {"Content-Type": "application/json", "me_id": "me id"}
```

- Generate Payment Link and QR Code
 Run static_link_sdk.py to generate a reusable payment link and QR code image:
```bash
python static_link_sdk.py
```

- Outputs a payment link (staticLink) and QR ID (qrId).
- Saves a QR code image (e.g., payment_qr_6495373221.png) encoding the payment link.
- Share the QR code or link via SMS, email, or physical displays.

# 🔍 Troubleshooting

- Ensure MERCHANT_ID and MERCHANT_KEY are valid (contact YagoutPay).
- For dynamic payments, verify ngrok URLs for callbacks.
- For static payments, ensure qrcode and pillow are installed.
- Disable SSL verification (verify=False) for testing only; enable in production.
- Check API responses for errors (e.g., "Invalid encrypted payload").
- Refer to the repository for examples: CLICK HERE.

📄 License
MIT License. See LICENSE.```
