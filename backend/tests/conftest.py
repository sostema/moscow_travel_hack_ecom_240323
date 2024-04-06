import pytest
from shared.containers import Container, init_combat_container


@pytest.fixture(scope="function")
def combat_container() -> Container:
    container = init_combat_container()
    return container
