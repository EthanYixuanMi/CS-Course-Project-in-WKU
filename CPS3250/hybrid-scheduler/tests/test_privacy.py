from __future__ import annotations

import logging
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from hybrid_scheduler.config import get_settings
from hybrid_scheduler.dispatcher.dispatcher import (
    RoundRobinDispatcher,
    create_mock_nodes,
)
from hybrid_scheduler.main import TaskPayload, app
from hybrid_scheduler.utils.models import Task


@pytest.fixture(autouse=True)
def clear_settings_cache() -> None:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_submit_generates_opaque_identifier() -> None:
    response = TestClient(app).post(
        "/submit",
        json={"category": "CPU", "duration": 0.001},
    )

    assert response.status_code == 200
    UUID(response.json()["id"])
    assert response.json()["status"] == "queued"


def test_submit_rejects_caller_provided_identifier() -> None:
    with pytest.raises(ValidationError):
        TaskPayload.model_validate(
            {"id": "person@example.com", "category": "CPU", "duration": 1}
        )


def test_api_key_protects_submit_when_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("API_KEY", "test-secret-value")
    get_settings.cache_clear()
    client = TestClient(app)

    assert (
        client.post("/submit", json={"category": "IO", "duration": 0.001}).status_code
        == 401
    )
    assert (
        client.post(
            "/submit",
            headers={"X-API-Key": "wrong"},
            json={"category": "IO", "duration": 0.001},
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/submit",
            headers={"X-API-Key": "test-secret-value"},
            json={"category": "IO", "duration": 0.001},
        ).status_code
        == 200
    )


def test_secret_configuration_is_redacted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("RABBITMQ_URL", "amqp://user:private@localhost/")
    get_settings.cache_clear()

    assert "private" not in repr(get_settings())


def test_dispatch_log_omits_task_identifier(caplog: pytest.LogCaptureFixture) -> None:
    task = Task(id="private-task-reference", category="CPU", duration=1)
    dispatcher = RoundRobinDispatcher(create_mock_nodes(1))

    with caplog.at_level(logging.INFO):
        dispatcher.dispatch([task])

    assert "private-task-reference" not in caplog.text
    assert "node-0" in caplog.text
