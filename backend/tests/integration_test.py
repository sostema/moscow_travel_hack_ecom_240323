import uuid

from schemas.prompt import PromptRequest
from shared.containers import Container


class TestIntegration:
    def test_get_ddl_ok(self, combat_container: Container):
        ...
        # print(combat_container.heath_service.db_repository.compile_table(ATM))
        # print(combat_container.heath_service.db_repository.compile_table(Office))

    async def test_check_ok(self, combat_container: Container):
        await combat_container.heath_service.check()

    def test_kandinsky_get_model_ok(self, combat_container: Container):
        print(combat_container.kandinsky_supplier.get_model())

    def test_kandinsky_save_ok(self, combat_container: Container):
        combat_container.kandinsky_supplier.generate_and_safe(
            PromptRequest(
                prompt="Pixilated girl",
                style="ANIME",
                width=1024,
                height=1024,
            ),
            count=5,
        )

    def test_kandinsky_mutate_ok(self, combat_container: Container):
        _, a = combat_container.kandinsky_supplier.populate_prompt(
            PromptRequest(
                prompt="Pixilated girl",
                width=1024,
                height=1024,
            )
        )
        print(a.jsonable_encoder())

        _, b = combat_container.kandinsky_supplier.populate_prompt(
            PromptRequest(
                prompt="Pixilated girl",
                width=1024,
                height=1024,
            )
        )
        print(b.jsonable_encoder())

        res = combat_container.kandinsky_supplier.mutate(
            PromptRequest(
                prompt="Pixilated girl", width=1024, height=1024, attributes=a
            ),
            PromptRequest(
                prompt="Pixilated girl", width=1024, height=1024, attributes=b
            ),
        )
        print(res.attributes.jsonable_encoder())

    def test_gigachat_ok(self, combat_container: Container):
        res = combat_container.gigachat_supplier.single_message(
            "Сделай пропт для кандинского для классного аниме стикера",
        )
        print(res)

    def test_gigachat_translate_ok(self, combat_container: Container):
        res = combat_container.gigachat_supplier.translate_to_english(
            "Привет, как дела?",
        )
        print(res)

    def test_tg_create_stickers_ok(self, combat_container: Container):
        combat_container.tg_supplier.create_stickers(
            418878871,
            sticker_id=uuid.uuid4(),
            ids=[uuid.UUID("19c3a34a-f919-4ae5-8b3c-5f4547c887af")],
        )

    def test_generate_prompt_ok(self, combat_container: Container):
        combat_container.prompt_service.generate_prompt("Белый флаг")

    def test_generate_images_ok(self, combat_container: Container):
        combat_container.prompt_service.generate_for_patterns()

    def test_get_all_images_ok(self, combat_container: Container):
        result = combat_container.prompt_service.get_all()
        print(result.images.keys())

    def test_remove_bg_ok(self, combat_container: Container):
        img = combat_container.prompt_service.get_images(
            img_id=uuid.UUID("f5b454c9-d3f8-483c-b181-56a063a42b1f")
        )
        assert img is not None

        combat_container.prompt_service.photoroom_supplier.remove_bg(img)

    def test_gen_images_ok(self, combat_container: Container):
        combat_container.prompt_service.gen_all_images_md()
