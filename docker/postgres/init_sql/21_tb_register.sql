SET
    ROLE motorizen;

SET
    search_path TO motorizen;

CREATE TABLE
    IF NOT EXISTS "tb_register" (
        "id_register" UUID PRIMARY KEY DEFAULT gen_random_uuid (),
        "cd_user" UUID NOT NULL REFERENCES "tb_user" ("id_user") ON DELETE CASCADE,
        "cd_vehicle" UUID NOT NULL REFERENCES "tb_vehicle" ("id_vehicle"),
        "distance" FLOAT NOT NULL DEFAULT 0.0,
        "working_time" TIME NOT NULL DEFAULT '00:00:00',
        "mean_consuption" FLOAT DEFAULT 0.0,
        "number_of_trips" INTEGER NOT NULL DEFAULT 1,
        "total_value" FLOAT NOT NULL DEFAULT 0.0,
        "register_date" DATE NOT NULL DEFAULT CURRENT_DATE,
        "updated_at" TIMESTAMP,
        "created_at" TIMESTAMP,
        "deleted_at" TIMESTAMP
    );

CREATE TRIGGER set_brand_timestamps BEFORE INSERT
OR
UPDATE
OR DELETE ON "tb_register" FOR EACH ROW EXECUTE FUNCTION set_timestamp ();

COMMENT ON TABLE "tb_register" IS 'Tabela de registros de eventos de ganho de um usuário do sistema Motorizen.';