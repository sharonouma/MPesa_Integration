import json
from urllib.request import HTTPBasicAuthHandler
from django import db
from django.http import HttpResponse, JsonResponse
import requests
import base64
from flask import Flask, current_app, request, jsonify
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import Transaction

app = Flask(__name__)
from mpesa_api.mpesa_credentials import LipanaMpesaPpassword, MpesaAccessToken

@csrf_exempt
@csrf_exempt
def getAccessToken(request):
    consumer_key = 'YOUR_CONSUMER_KEY'
    consumer_secret = 'YOUR_CONSUMER_SECRET'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials' #YOUR API URL

    try:
        r = requests.get(api_URL, auth=(consumer_key, consumer_secret))

        # Check the HTTP status code
        if r.status_code == 200:
            # Parse the response as JSON
            mpesa_access_token = json.loads(r.text)
            validated_mpesa_access_token = mpesa_access_token.get('access_token', '')
            return HttpResponse(validated_mpesa_access_token)
        else:
            # Handle non-200 status codes
            return JsonResponse({'error': f'Failed to fetch access token. Status code: {r.status_code}'}, status=r.status_code)
    except Exception as e:
        # Handle any other exceptions
        return JsonResponse({'error': f'Failed to fetch access token: {str(e)}'}, status=500)


@csrf_exempt
def lipa_na_mpesa_online(stat):
    json_data = json.loads(stat.body.decode('utf-8'))
    phone_number = json_data.get('phone_number', '')
    amount = json_data.get('amount', '')
    print("Phone number:", phone_number)
    print("amount:", amount)
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": phone_number,  # replace with your phone number to get stk push
        "CallBackURL": "https://mydomain.com/pth",
        "AccountReference": "MamaPesa",
        "TransactionDesc": "Testing",
    }

    response = requests.post(api_url, json=request, headers=headers)
    print(response)
    return HttpResponse('success')

@csrf_exempt
@app.route('/callback', methods=['POST'])
def handle_callback(request):
    try:
        with app.app_context():
            callback_data = request.json

            # Check if callback_data contains required fields
            if 'Body' in callback_data and 'stkCallback' in callback_data['Body']:
                stk_callback = callback_data['Body']['stkCallback']
                
                # Check the result code
                result_code = stk_callback.get('ResultCode', None)
                if result_code is None:
                    return jsonify({'error': 'ResultCode not found in callback data'}), 400

                if result_code != '0':
                    # If the result code is not 0, there was an error
                    error_message = stk_callback.get('ResultDesc', 'Unknown error')
                    response_data = {'ResultCode': result_code, 'ResultDesc': error_message}
                    return jsonify(response_data)

                # If the result code is 0, the transaction was completed
                callback_metadata = stk_callback.get('CallbackMetadata', {})
                amount = None
                phone_number = None
                for item in callback_metadata.get('Item', []):
                    if item['Name'] == 'Amount':
                        amount = item['Value']
                    elif item['Name'] == 'PhoneNumber':
                        phone_number = item['Value']
                
                # Save transaction details to database
                save_transaction(amount, phone_number)
                # Return a success response to the M-Pesa server
                response_data = {'ResultCode': result_code, 'ResultDesc': 'Success'}
                return jsonify(response_data)
            else:
                return jsonify({'error': 'Invalid callback data format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Save the variables to a database or file, etc.
# Example: SaveTransaction(amount, phone_number)
def save_transaction(amount, phone_number):
    # Create a new Transaction object
    transaction = Transaction(amount=amount, phone_number=phone_number)

    # Add the object to the session and commit
    db.session.add(transaction)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
