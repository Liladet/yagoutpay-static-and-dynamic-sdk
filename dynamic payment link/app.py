from flask import Flask, render_template, request, jsonify
import os
import sys

sys.path.append(os.path.dirname(__file__))

from dynamic_link_sdk import YagoutPaySDK

app = Flask(__name__)

# Initialize SDK
sdk = YagoutPaySDK(
    merchant_id="me id",
    encryption_key="aes key"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create-payment-link', methods=['POST'])
def create_payment_link():
    try:
        # Get data from frontend form
        data = request.json
        
        # Build complete payload
        payload = {
            "req_user_id": "yagou381",
            "me_id": sdk.merchant_id,
            "amount": data['amount'],
            "customer_email": data.get('customer_email', ''),
            "mobile_no": data['mobile_no'],
            "expiry_date": data.get('expiry_date', '2025-10-23'),
            "media_type": ["API"],
            "order_id": data['order_id'],
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "product": data['product'],
            "dial_code": data.get('dial_code', '+251'),
            "failure_url": data.get('failure_url', 'http://localhost:5000/failure'),
            "success_url": data.get('success_url', 'http://localhost:5000/success'),
            "country": data.get('country', 'ETH'),
            "currency": data.get('currency', 'ETB')
        }
        
        # Create dynamic link
        result = sdk.create_dynamic_link(payload)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        })

@app.route('/success')
def success():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Successful</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .success { color: green; font-size: 24px; }
            .button { background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="success">✅ Payment Successful!</div>
        <p>Thank you for your payment.</p>
        <a href="/" class="button">Create Another Payment</a>
    </body>
    </html>
    """

@app.route('/failure')
def failure():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Failed</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .error { color: red; font-size: 24px; }
            .button { background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="error">❌ Payment Failed</div>
        <p>Please try again.</p>
        <a href="/" class="button">Try Again</a>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5000)
