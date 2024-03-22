import pytest
import uvloop

from containers.main import MainContainer


@pytest.fixture(scope="session")
def event_loop_policy():
    return uvloop.EventLoopPolicy()


@pytest.fixture(scope="session")
def event_loop(event_loop_policy):
    loop = event_loop_policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_container():
    container = MainContainer()
    yield container
