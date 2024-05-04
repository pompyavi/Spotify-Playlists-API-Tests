from utils.request import APIRequest
from config import ACCOUNT_BASE_URI, REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET
from datetime import datetime, timedelta


class TokenManager:
    request = APIRequest()
    access_token = None
    expiry_time = None

    @classmethod
    def __renew_token(cls):
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': REFRESH_TOKEN,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = cls.request.get_access_token(url=ACCOUNT_BASE_URI + 'api/token', data=payload)
        if response.status_code != 200:
            raise RuntimeError('Not able to refresh token...')
        return response.as_dict

    @classmethod
    def get_token(cls):
        try:
            if cls.access_token is None or datetime.now() > cls.expiry_time:
                print("Renewing token ...")
                response = cls.__renew_token()
                print('Token renewed...')
                cls.access_token = response["access_token"]
                expiry_duration_in_seconds = response["expires_in"]
                cls.expiry_time = datetime.now() + timedelta(seconds=expiry_duration_in_seconds - 300)
            else:
                print("Token is good to use")
        except Exception as e:
            print("Failed to get token:", e)
            raise RuntimeError("ABORT!!! Failed to get token")

        return cls.access_token


