from infrastructure.config import db_settings

EXCLUDE_DB_TABLES: list[str] = ["alembic_version"]
ALLOWED_DB_SCHEMA = [db_settings.DB_SCHEMA]
