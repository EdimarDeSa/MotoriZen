GRANT CREATE ON DATABASE motorizen TO motorizen;

SET ROLE motorizen;

CREATE SCHEMA IF NOT EXISTS motorizen;

SET search_path TO motorizen;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Função que previne a modificação manual dos campos de timestap críticos
CREATE OR REPLACE FUNCTION set_timestamp()
RETURNS TRIGGER AS $$
BEGIN

    IF TG_OP = 'INSERT' THEN
        IF NEW.created_at IS NOT NULL THEN
            RAISE EXCEPTION 'Cannot set created_at timestamp manually';
        END IF;

        IF NEW.updated_at IS NOT NULL THEN
            RAISE EXCEPTION 'Cannot set updated_at timestamp manually';
        END IF;

        IF NEW.deleted_at IS NOT NULL THEN
            RAISE EXCEPTION 'Cannot set deleted_at timestamp manually';
        END IF;

        NEW.created_at = CURRENT_TIMESTAMP;
        NEW.updated_at = CURRENT_TIMESTAMP;
    END IF;

    IF TG_OP = 'UPDATE' THEN
        IF NEW.created_at != OLD.created_at THEN
            RAISE EXCEPTION 'Cannot set created_at timestamp manually';
        END IF;

        IF NEW.updated_at != OLD.updated_at THEN
            RAISE EXCEPTION 'Cannot set updated_at timestamp manually';
        END IF;

        IF NEW.deleted_at != OLD.deleted_at THEN
            RAISE EXCEPTION 'Cannot set deleted_at timestamp manually';
        END IF;

        NEW.updated_at = CURRENT_TIMESTAMP;
    END IF;

    IF TG_OP = 'DELETE' THEN
        IF OLD.deleted_at IS NOT NULL THEN
            RAISE EXCEPTION 'Record already deleted';
        END IF;

        NEW.updated_at = CURRENT_TIMESTAMP;
        NEW.deleted_at = CURRENT_TIMESTAMP;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


/* How to use:
CREATE TRIGGER {set_brand}_timestamps
BEFORE INSERT OR UPDATE OR DELETE ON "{tb_register}"
FOR EACH ROW
EXECUTE FUNCTION set_timestamp();
*/
 