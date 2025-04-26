SET
    ROLE motorizen;

SET
    search_path TO motorizen_schema;

CREATE TABLE
    IF NOT EXISTS "tb_fuel_type" (
        "id_fuel_type" SERIAL PRIMARY KEY NOT NULL,
        "name" VARCHAR(20) NOT NULL UNIQUE,
        "updated_at" TIMESTAMP,
        "created_at" TIMESTAMP,
        "deleted_at" TIMESTAMP
    );

CREATE TRIGGER set_brand_timestamps BEFORE INSERT
OR
UPDATE
OR DELETE ON "tb_fuel_type" FOR EACH ROW EXECUTE FUNCTION set_timestamp ();

INSERT INTO
    "tb_fuel_type" ("name")
VALUES
    ('Alcohol'),
    ('Electric'),
    ('Gasoline'),
    ('Hybrid - Alc/Gas'),
    ('Hybrid - Gas/Elec');

COMMENT ON TABLE "tb_fuel_type" IS 'Tabela de típos de combustível mapeados.';