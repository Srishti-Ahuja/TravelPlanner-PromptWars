import os
from google.cloud import secretmanager
from google.api_core import exceptions

class SecretService:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id: str, version_id: str = "latest") -> str:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        try:
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8").strip()
        except exceptions.NotFound:
            print(f"Secret {secret_id} not found.")
            return os.getenv(secret_id, "") # Fallback to env var for local dev
        except Exception as e:
            print(f"Error retrieving secret {secret_id}: {e}")
            return os.getenv(secret_id, "")
