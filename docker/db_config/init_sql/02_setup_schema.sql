GRANT CREATE ON DATABASE motorizen TO motorizen;

SET ROLE motorizen;

CREATE SCHEMA IF NOT EXISTS motorizen;

SET search_path TO motorizen;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

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

