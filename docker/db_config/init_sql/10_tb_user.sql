SET ROLE motorizen;
SET search_path TO motorizen;

CREATE TABLE IF NOT EXISTS "tb_user"
(
    "id_user" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "first_name" VARCHAR(50) NOT NULL,
    "last_name" VARCHAR(100) NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "birthdate" DATE NOT NULL,
    "cd_auth" UUID NOT NULL UNIQUE,
    "is_active" BOOLEAN DEFAULT TRUE NOT NULL,
    "last_update" TIMESTAMP,
    "creation" TIMESTAMP
);

CREATE TRIGGER prevent_set_user_creation_and_last_update_field_on_insert
BEFORE INSERT ON "tb_user"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

CREATE TRIGGER prevent_set_user_creation_and_last_update_field_on_update
BEFORE UPDATE ON "tb_user"
FOR EACH ROW
EXECUTE FUNCTION check_manually_changes_on_timestamp_fields();

ALTER TABLE "tb_user" ADD CONSTRAINT email_check
CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

CREATE INDEX idx_user_cd_auth ON "tb_user" USING btree ("cd_auth");