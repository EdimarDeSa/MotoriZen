SET search_path TO motorizen;


CREATE TABLE IF NOT EXISTS "tb_car"
(
    "id_car" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "cd_user" UUID NOT NULL REFERENCES "tb_user"("id_user") ON DELETE CASCADE,
    "cd_brand" INTEGER NOT NULL REFERENCES "tb_brand"("id_brand") ON DELETE CASCADE,
    "renavam" VARCHAR(11) UNIQUE DEFAULT '00000000000',
    "model" VARCHAR(100) NOT NULL,
    "year" SMALLINT NOT NULL,
    "color" VARCHAR(25) NOT NULL,
    "license_plate" VARCHAR(10) UNIQUE DEFAULT '0000000000',
    "odometer" FLOAT NOT NULL,
    "is_active" BOOLEAN DEFAULT TRUE NOT NULL,
    "last_update" TIMESTAMP,
    "creation" TIMESTAMP
);

CREATE TRIGGER prevent_set_user_creation_and_last_update_field_on_insert
BEFORE INSERT ON "tb_car"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

CREATE TRIGGER prevent_set_user_creation_and_last_update_field_on_update
BEFORE UPDATE ON "tb_car"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();