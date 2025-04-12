import os
import tempfile
import unittest
import json
from tusky import TuskyClient
from dotenv import load_dotenv
load_dotenv()  # .env 파일의 환경변수 로드
from server import upload_file_and_create_ip

class TestTuskyFileUploadIPCreation(unittest.TestCase):
    def setUp(self):
        # 환경변수로부터 필수 값을 읽어옵니다.
        self.vault_id = os.getenv("TUSKY_VAULT_ID")
        self.api_key = os.getenv("TUSKY_API_KEY")
        if not (self.vault_id and self.api_key):
            self.skipTest("TUSKY_VAULT_ID, TUSKY_API_KEY 환경변수가 필요합니다.")
        
        # 업로드할 파일 용도로 임시 파일을 생성합니다.
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b"Test content for Tusky upload and IP creation")
        self.temp_file.close()

    def tearDown(self):
        # 테스트 종료 후 임시 파일 삭제
        os.remove(self.temp_file.name)

    def test_upload_file_and_create_ip(self):
        # 테스트용 IP 태그
        ip_tag = "test-ip-tag"

        # server.py의 함수를 사용하여 파일 업로드 및 IP 생성을 진행합니다.
        result = upload_file_and_create_ip(self.temp_file.name, ip_tag)

        # 에러 문자열이면 테스트 실패
        if result.startswith("Error:") or "환경변수가 없습니다" in result:
            self.fail(f"IP 생성 실패: {result}")

        # 결과 JSON 문자열을 파싱합니다.
        try:
            result_data = json.loads(result)
        except Exception as e:
            self.fail(f"결과 파싱 실패: {str(e)}")

        # 업로드 결과 검증
        upload_result = result_data.get("upload_result")
        self.assertIsNotNone(upload_result, "upload_result는 None이면 안됩니다.")
        self.assertIn("fileId", upload_result, "업로드 결과에 fileId가 존재해야 합니다.")
        self.assertEqual(upload_result["vaultId"], self.vault_id, "vaultId가 일치해야 합니다.")
        self.assertEqual(upload_result["ipTag"], ip_tag, "ipTag 값이 일치해야 합니다.")

        # IP 생성 결과 검증
        ip_creation_result = result_data.get("ip_creation_result")
        self.assertIsNotNone(ip_creation_result, "ip_creation_result는 None이면 안됩니다.")
        self.assertIn(
            "Successfully minted and registered IP asset", 
            ip_creation_result,
            "IP 생성 결과 메시지가 예상과 다릅니다."
        )

        print("업로드 및 IP 생성 결과:", json.dumps(result_data, indent=2))

if __name__ == "__main__":
    unittest.main()