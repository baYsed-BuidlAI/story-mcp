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

    def upload_file(self, file_path: str, vault_id: str, ip_tag: str) -> dict:
        """
        파일을 Tusky의 Vault에 업로드합니다.
        업로드 엔드포인트는 /uploads를 사용하며, 헤더에는 Api-Key가 포함됩니다.
        
        Args:
            file_path: 업로드할 파일 경로.
            vault_id: 업로드 대상 Vault ID.
            ip_tag: 사용자가 입력한 IP 태그.
        
        Returns:
            dict: 업로드 결과 ({ "vaultId": vault_id, "fileId": file_id, "ipTag": ip_tag }).
        """
        endpoint = f"{self.api_url}/uploads"
        headers = {
            "Api-Key": self.api_key
        }
        metadata = {
            "vaultId": vault_id,
        }
        tus_client_instance = tus_client.TusClient(endpoint, headers=headers)
        uploader = tus_client_instance.uploader(file_path=file_path, metadata=metadata)
        uploader.upload()  # 파일 업로드 실행
        file_id = uploader.url.split("/")[-1]  # URL의 마지막 부분을 fileId로 사용
        return {
            "vaultId": vault_id,
            "fileId": file_id,
            "ipTag": ip_tag
        }

