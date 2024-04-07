GRANT ALL PRIVILEGES ON DATABASE db_main TO db_main;

\c db_main;

CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE public.event (
        type TEXT,
        restaurant_type TEXT[],
        name TEXT,
        description TEXT,
        link TEXT,
        img_link TEXT,
        price DECIMAL,
        address TEXT,
        lat FLOAT,
        lng FLOAT,
        id BIGSERIAL NOT NULL,
        internal_id UUID NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (internal_id)
)

-- run after start of server
-- ALTER TABLE langchain_pg_embedding
--   ALTER COLUMN cmetadata
--   SET DATA TYPE jsonb
--   USING cmetadata::jsonb;

update event e
set img_link = 'https://cms.russpass.ru/v1/file/65c1db0652a0ac9c49c176a3'
where e.name = 'ГМИИ им. А.С. Пушкина';
update event e
set img_link = 'https://cms.russpass.ru/v1/file/65f42f7ede1ca4820a8feb6c'
where e.name = 'Выставка картин в технике жикле «Босх и Брейгели. Загадки мистической эпохи»';
update event e
set img_link = 'https://cms.russpass.ru/v1/file/639b2d8b3db12c838e92218a'
where e.name = 'Музей истории ВМФ России';
update event e
set img_link = 'https://cms.russpass.ru/v1/file/653fb54fd2b6381af04061d0'
where e.name = 'Выставочный зал парка «Зарядье»';
update event e
set img_link = 'https://russpass.ru/mesta-i-sobytiya/_next/image?url=https%3A%2F%2Fcms.russpass.ru%2Fv1%2Ffile%2F65420ad0d2b6381af066b9f9%2F924&w=3840&q=75'
where e.name = 'Экскурсия «Флорариум. Как все устроено»';
update event e
set img_link = 'https://russpass.ru/mesta-i-sobytiya/_next/image?url=https%3A%2F%2Fcms.russpass.ru%2Fv1%2Ffile%2F65420ad0d2b6381af066b9f9%2F924&w=3840&q=75'
where e.name = 'Экскурсия «Флорариум. Как все устроено»';
