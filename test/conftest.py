
import pytest
import app as projeto


@pytest.fixture
def app():
    projeto.app.config.update({
        "TESTING": True,
        "SECRET_KEY": "chave-de-teste"
    })

    yield projeto.app


@pytest.fixture
def client(app):
    return app.test_client()
