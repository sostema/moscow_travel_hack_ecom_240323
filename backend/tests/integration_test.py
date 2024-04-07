import uuid

from persistence.database import Event
from shared.containers import Container, init_combat_container

container = init_combat_container()


class TestIntegration:
    def test_compile_table_ok(self):
        print(container.heath_service.pg_repository.compile_table(Event))

    def test_user_requires_new_ok(self):
        assert container.chat_service.user_requires_new(
            "Давай сначала. Какая есть грузинская кухня?"
        )

    def test_user_requires_new_not_found(self):
        assert container.chat_service.user_requires_new("А какая есть еда там?")
