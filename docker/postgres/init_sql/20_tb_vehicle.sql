SET
    ROLE motorizen;

SET
    search_path TO motorizen_schema;

CREATE TABLE
    IF NOT EXISTS "tb_vehicle" (
        "id_vehicle" UUID PRIMARY KEY DEFAULT gen_random_uuid (),
        "cd_user" UUID NOT NULL REFERENCES "tb_user" ("id_user") ON DELETE CASCADE,
        "cd_brand" INTEGER NOT NULL REFERENCES "tb_brand" ("id_brand"),
        "renavam" VARCHAR(11) UNIQUE DEFAULT NULL,
        "model" VARCHAR(100) NOT NULL,
        "year" SMALLINT NOT NULL,
        "color" VARCHAR(25) NOT NULL,
        "license_plate" VARCHAR(10) UNIQUE DEFAULT NULL,
        "cd_fuel_type" INTEGER NOT NULL REFERENCES "tb_fuel_type" ("id_fuel_type"),
        "fuel_capacity" INTEGER NOT NULL DEFAULT 0,
        "odometer" FLOAT NOT NULL DEFAULT 0.0,
        "is_active" BOOLEAN NOT NULL DEFAULT TRUE,
        "updated_at" TIMESTAMP,
        "created_at" TIMESTAMP,
        "deleted_at" TIMESTAMP
    );

CREATE TRIGGER set_brand_timestamps BEFORE INSERT
OR
UPDATE
OR DELETE ON "tb_vehicle" FOR EACH ROW EXECUTE FUNCTION set_timestamp ();

CREATE INDEX idx_vehicle_user ON "tb_vehicle" ("cd_user");

CREATE INDEX idx_vehicle_brand ON "tb_vehicle" ("cd_brand");

COMMENT ON TABLE "tb_vehicle" IS 'Tabela de carros de um usuário do sistema Motorizen.';