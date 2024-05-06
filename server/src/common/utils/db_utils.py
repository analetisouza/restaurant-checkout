import json
from typing import Tuple

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.sql import select, Select

from database.models.models import Base
from src.common.constants import constants


def connect_to_db() -> Tuple[Engine, Session]:
    """
    Returns an engine and a session object to connect to the database
    """
    engine = create_engine(constants.DATABASE_URL)
    session = scoped_session(sessionmaker(bind=engine))
    return engine, session()


def fetch_all_from_db(engine: Engine, stmt: Select) -> str:
    """
    Given an engine and a statement, fetches all correspondent rows from the database.
    """
    with engine.connect() as conn:
        result = conn.execute(stmt).fetchall()
        return json.dumps([print(row) for row in result])


def fetch_one_by_id(engine: Engine, entity: Base, entity_id: int) -> str:
    """
    Given an engine, an entity class and an entity id, fetches the compatible record from the database.
    """

    with engine.connect() as conn:
        stmt = select(entity).filter(entity.id == entity_id)
        result = conn.execute(stmt).fetchone()
        return json.dumps(dict(result))
