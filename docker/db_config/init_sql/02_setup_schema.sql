GRANT CREATE ON DATABASE motorizen TO motorizen;

SET ROLE motorizen;

CREATE SCHEMA IF NOT EXISTS motorizen;

SET search_path TO motorizen;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Função que previne a modificação manual dos campos de timestap críticos
CREATE OR REPLACE FUNCTION set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.created_at IS NOT NULL THEN
        RAISE EXCEPTION 'Cannot set created_at timestamp manually';
    END IF;

    IF NEW.updated_at IS NOT NULL THEN
        RAISE EXCEPTION 'Cannot set updated_at timestamp manually';
    END IF;

    IF NEW.deleted_at IS NOT NULL THEN
        RAISE EXCEPTION 'Cannot set deleted_at timestamp manually';
    END IF;

    IF TG_OP = 'INSERT' THEN
        NEW.created_at = CURRENT_TIMESTAMP;
        NEW.updated_at = CURRENT_TIMESTAMP;

    ELSEIF TG_OP = 'UPDATE' THEN
        NEW.updated_at = CURRENT_TIMESTAMP;

    ELSEIF TG_OP = 'DELETE' THEN
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
 