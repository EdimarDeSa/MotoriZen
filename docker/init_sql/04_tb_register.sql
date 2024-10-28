SET search_path TO motorizen;

-- Função que previne a modificação manual do campo creation
CREATE OR REPLACE FUNCTION prevent_manually_creation()
RETURNS TRIGGER AS $$
BEGIN
    -- Preventing manually set creation
    IF NEW.creation IS DISTINCT FROM OLD.creation THEN
        RAISE EXCEPTION 'Cannot modify the creation timestamp manually';
    END IF;
    
    IF OLD.creation IS NULL THEN
    NEW.creation = CURRENT_TIMESTAMP;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Função que previne a modificação manual dos campos creation e last_update
CREATE OR REPLACE FUNCTION check_manually_changes_on_timestamp_fields()
RETURNS TRIGGER AS $$
BEGIN
    -- Preventing manually set creation
    IF NEW.creation IS DISTINCT FROM OLD.creation THEN
        RAISE EXCEPTION 'Cannot modify the creation timestamp.';
    END IF;

    IF OLD.creation IS NULL THEN
        NEW.creation = CURRENT_TIMESTAMP;
    END IF;

    -- Preventing manually set last_update
    IF NEW.last_update IS DISTINCT FROM OLD.last_update THEN
        RAISE EXCEPTION 'Cannot modify the last_update timestamp.';
    END IF;

    NEW.last_update = CURRENT_TIMESTAMP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


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