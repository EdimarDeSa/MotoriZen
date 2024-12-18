SET search_path TO motorizen;

CREATE TABLE IF NOT EXISTS "tb_fuel_type"
(
    "id_fuel_type" SERIAL PRIMARY KEY NOT NULL,
    "name" VARCHAR(20) NOT NULL UNIQUE
);


INSERT INTO "tb_fuel_type" ("name")
VALUES
    ('Alcohol'),
    ('Eletric'),
    ('Gasoline'),
    ('Hybrid - Alc/Gas'),
    ('Hybrid - Gas/Elec');
