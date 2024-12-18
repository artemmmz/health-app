import asyncio
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest

from fastapi.testclient import TestClient

from app.core.settings import Settings
from app.main import app


@pytest.fixture(scope='class', autouse=True)
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
def settings():
    base_dir = Path(__file__).resolve().parent.parent
    settings = Settings(_env_file=base_dir / '.env.test')  # type: ignore
    return settings


@pytest.fixture(scope='session', autouse=True)
def mock_settings(settings):
    with patch('app.core.settings.Settings', new_callable=lambda: settings):
        yield


@pytest.fixture(scope='class')
async def client(mock_settings):
    with TestClient(app=app) as test_client:
        yield test_client
