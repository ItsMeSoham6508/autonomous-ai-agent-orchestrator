from sqlalchemy import select

from app.database.session import SessionLocal
from app.models import Application


class DatabaseRepository:
    def create_application(self, app_name: str, api_key: str) -> None:
        with SessionLocal.begin() as session:
            session.add(Application(app_name=app_name, api_key=api_key))

    def get_applications(self) -> list[Application]:
        with SessionLocal() as session:
            return session.scalars(select(Application)).all()

    def get_application_by_id(self, application_id: int) -> Application | None:
        with SessionLocal() as session:
            return session.get(Application, application_id)

    def update_application(
        self, application_id: int, app_name: str
    ) -> Application | None:
        with SessionLocal.begin() as session:
            application = session.get(Application, application_id)
            if application is None:
                return None
            application.app_name = app_name
            return application

    def delete_application(self, application_id: int) -> bool:
        with SessionLocal.begin() as session:
            application = session.get(Application, application_id)
            if application is None:
                return False
            session.delete(application)
        return True