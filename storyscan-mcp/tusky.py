import os
import json
import requests
from tusclient import client as tus_client  # pip install tuspy
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
from nacl.bindings import crypto_sign_ed25519_pk_to_curve25519

# Tusky API는 고정 주소를 사용합니다.
TUSKY_API_URL = "https://api.tusky.io"

class TuskyClient:
    def __init__(self):
        self.api_url = TUSKY_API_URL.rstrip("/")
        # Api-Key 환경변수
        self.api_key = os.getenv("TUSKY_API_KEY")
        if not self.api_key:
            raise ValueError("TUSKY_API_KEY 환경변수가 필요합니다.")

    def get_file_data(self, file_path: str) -> dict:

        endpoint = f"{self.api_url}/files/{file_path}/data"
        headers = {
            "Api-Key": self.api_key
        }
        response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"

        return response.json()

