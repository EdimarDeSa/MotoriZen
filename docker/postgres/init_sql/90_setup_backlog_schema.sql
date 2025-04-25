SET
    ROLE motorizen;

CREATE SCHEMA IF NOT EXISTS backlog;

SET
    search_path TO backlog;

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
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;