import pytest
import dotenv
import os


@pytest.fixture(scope='class', autouse=True)
def load_env_vars():
    dotenv.load_dotenv(verbose=True)


@pytest.fixture
def api_url() -> str:
    return f'{os.environ.get("API_DEV_HOST")}/api/v1'


@pytest.fixture
def mock_pull_request() -> dict:
    return {'title': 'My awesome commit!',
            'description': 'Great feature getting merge',
            'source_branch': 'dev',
            'destiny_branch': 'master'}
