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
