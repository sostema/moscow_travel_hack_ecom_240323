import uuid

from persistence.database import Event
from shared.containers import Container, init_combat_container

container = init_combat_container()


class TestIntegration:
    def test_compile_table_ok(self):
        print(container.heath_service.pg_repository.compile_table(Event))
