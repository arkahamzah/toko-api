import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["REDIS_URL"] = "redis://localhost:6379"

from unittest.mock import MagicMock
import app.cache as cache_module

# Mock Redis
mock_redis = MagicMock()
mock_redis.get.return_value = None
cache_module.r = mock_redis

# Mock Celery tasks
import app.tasks as tasks_module
tasks_module.kirim_email = MagicMock(delay=MagicMock())
tasks_module.proses_order = MagicMock(delay=MagicMock())

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.database import Base
from app.main import app

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)
