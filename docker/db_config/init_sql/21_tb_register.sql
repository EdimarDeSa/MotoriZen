SET ROLE motorizen;
SET search_path TO motorizen;

CREATE TABLE IF NOT EXISTS "tb_register"
(
    "id_register" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "cd_user" UUID NOT NULL REFERENCES "tb_user"("id_user") ON DELETE CASCADE,
    "cd_car" UUID NOT NULL REFERENCES "tb_car"("id_car") ON DELETE SET NULL,
    "distance" FLOAT NOT NULL DEFAULT 0.0,
    "working_time" TIME NOT NULL DEFAULT '00:00:00',
    "mean_consuption" FLOAT DEFAULT 0.0,
    "number_of_trips" INTEGER NOT NULL DEFAULT 1,
    "total_value" FLOAT NOT NULL DEFAULT 0.0,
    "register_date" DATE NOT NULL DEFAULT CURRENT_DATE,
    "last_update" TIMESTAMP,
    "creation" TIMESTAMP
);

CREATE TRIGGER prevent_set_user_creation_and_last_update_field_on_insert
BEFORE INSERT ON "tb_register"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

CREATE TRIGGER prevent_set_user_creation_and_last_update_field_on_update
BEFORE UPDATE ON "tb_register"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();