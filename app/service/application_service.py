from app.models import Application
from app.repository.database_manager import DatabaseRepository
import secrets
import string


class DatabaseService:
    def __init__(self):
        self.repository = DatabaseRepository()

    def generate_api_key(self) -> str:
        alphabet = string.ascii_letters + string.digits + "-_"
        return "".join(secrets.choice(alphabet) for _ in range(32))

    def get_applications(self) -> list[Application]:
        return self.repository.get_applications()

    def register_application(self, app_name: str) -> str:
        api_key = self.generate_api_key()
        self.repository.create_application(app_name, api_key)
        return api_key

    def get_application_by_id(self, application_id: int) -> Application | None:
        return self.repository.get_application_by_id(application_id)

    def update_application(
        self, application_id: int, app_name: str
    ) -> Application | None:
        return self.repository.update_application(application_id, app_name)

    def delete_application(self, application_id: int) -> bool:
        return self.repository.delete_application(application_id)