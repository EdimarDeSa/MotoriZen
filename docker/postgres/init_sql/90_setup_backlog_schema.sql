SET
    ROLE motorizen;

CREATE SCHEMA IF NOT EXISTS motorizen_backlog AUTHORIZATION motorizen;

SET
    search_path TO motorizen_backlog;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Função que previne a modificação manual dos campos de timestap críticos
CREATE OR REPLACE FUNCTION set_backlog_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF NEW.created_at IS NOT NULL THEN
            RAISE EXCEPTION 'Cannot set created_at timestamp manually';
        END IF;
        
        NEW.created_at = CURRENT_TIMESTAMP;
    END IF;

    IF TG_OP = 'UPDATE' THEN
        RAISE EXCEPTION 'Cannot update backlog events';
    END IF;

    IF TG_OP = 'DELETE' THEN
        RAISE EXCEPTION 'Cannot delete backlog events';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION set_backlog_timestamp () IS 'Evita alterações manuais nos campos de data dos eventos de backlog';