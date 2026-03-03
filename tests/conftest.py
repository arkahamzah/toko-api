import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["REDIS_URL"] = "redis://localhost:6379"

from unittest.mock import MagicMock
import app.cache as cache_module

# Mock Redis — tidak perlu koneksi nyata
mock_redis = MagicMock()
mock_redis.get.return_value = None  # cache selalu kosong
cache_module.r = mock_redis

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
