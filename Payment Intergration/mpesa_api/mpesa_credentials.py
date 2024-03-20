import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class MpesaC2bCredential:
    """
    This class is used to store the Mpesa C2B credentials required to access the API.
    """
    consumer_key = 'YOUR_CONSUMER_KEY'
    consumer_secret = 'YOUR_CONSUMER_SECRET'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials' # YOUR API URL


class MpesaAccessToken:
    """
   This class is used to retrieve the access token from Mpesa API.
   """
    r = requests.get(MpesaC2bCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    # print(r.text)
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']


class LipanaMpesaPpassword:
    """
   This class is used to generate the Lipa Na Mpesa Online Password.
   """
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "SHORT CODE"
    # Test_c2b_shortcode = "600344"
    passkey = 'PASSKEY'

    data_to_encode = Business_short_code + passkey + lipa_time

    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')

