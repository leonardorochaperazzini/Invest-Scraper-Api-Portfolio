import os
import pytest
from fastapi.testclient import TestClient

from app.api import app

from app.model.ScraperRun import ScraperRun as ScraperRunModel
from app.repository.ScraperRun import ScraperRun as ScraperRunRepository

from app.service.Auth.model.User import User as UserModelService
from app.service.Auth import get_current_active_user

client = TestClient(app)

async def mock_get_current_active_user():
    return UserModelService(
        username='mock', 
        email="mock@example.com", 
        full_name="mock", 
        disabled=False
    )

@pytest.fixture
def override_dependency():
    # Override da dependência antes dos testes
    app.dependency_overrides[get_current_active_user] = mock_get_current_active_user
    yield
    # Limpar o override após os testes
    app.dependency_overrides = {}

def test_scraper_run(override_dependency):
    form_data = {
        'limit': 2,
        'max_workers': 1
    }

    response = client.post("/scraper/run", json=form_data)

    response_json = response.json()

    assert response.status_code == 200
    assert 'scraper_run' in response_json
    assert response_json['scraper_run']['started_at'] is not None
    assert response_json['scraper_run']['ended_at'] is not None

def test_scraper_run_driver_fail_remote_connect(override_dependency):
    original_selenium_hub_url = os.environ.get('SELENIUM_HUB_URL')
    os.environ['SELENIUM_HUB_URL'] = 'localhost:1111'

    form_data = {
        'limit': 1,
        'max_workers': 1
    }

    response = client.post("/scraper/run", json=form_data)

    response_json = response.json()

    os.environ['SELENIUM_HUB_URL'] = original_selenium_hub_url

    assert response.status_code == 500
    assert response_json == {"detail": "Scraper remote driver failed to connect"}


def test_scraper_run_already_running(override_dependency):
    scraper_run_repository = ScraperRunRepository(ScraperRunModel)

    scraper_run = scraper_run_repository.create({
        'started_at': scraper_run_repository.get_current_date(),
        'ended_at': None
    })

    form_data = {
        'limit': 1,
        'max_workers': 1
    }

    response = client.post("/scraper/run", json=form_data)

    response_json = response.json()

    scraper_run_repository.delete(scraper_run.id)

    assert response.status_code == 429
    assert response_json == {"detail": "Scraper is already running"}