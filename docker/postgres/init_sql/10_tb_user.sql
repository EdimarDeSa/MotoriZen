SET
    ROLE motorizen;

SET
    search_path TO motorizen;

CREATE TABLE
    IF NOT EXISTS "tb_user" (
        "id_user" UUID PRIMARY KEY DEFAULT gen_random_uuid (),
        "first_name" VARCHAR(50) NOT NULL CHECK (trim("first_name") <> ''),
        "last_name" VARCHAR(100) NOT NULL CHECK (trim("first_name") <> ''),
        "email" VARCHAR(255) NOT NULL UNIQUE CHECK (
            email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        ),
        "birthdate" DATE NOT NULL CHECK (
            "birthdate" BETWEEN '1900-01-01' AND CURRENT_DATE  - INTERVAL '13 years'
        ),
        "cd_auth" UUID NOT NULL UNIQUE,
        "is_active" BOOLEAN DEFAULT TRUE NOT NULL,
        "updated_at" TIMESTAMP,
        "created_at" TIMESTAMP,
        "deleted_at" TIMESTAMP
    );

CREATE TRIGGER set_user_timestamps BEFORE INSERT
OR
UPDATE
OR DELETE ON "tb_user" FOR EACH ROW EXECUTE FUNCTION set_timestamp ();

CREATE INDEX idx_user_cd_auth ON "tb_user" USING btree ("cd_auth");

CREATE INDEX idx_user_is_active ON "tb_user" USING btree ("is_active");

INSERT ON TABLE "tb_user"
VALUES
    (
        NULL,
        'Motorizen',
        'System',
        'motorizen@efscode.com.br',
        CURRENT_DATE,
        gen_random_uuid (),
        TRUE,
        NULL,
        NULL,
        NULL
    );

COMMENT ON TABLE "tb_user" IS 'Tabela de usuários do sistema Motorizen';

COMMENT ON COLUMN "tb_user"."cd_auth" IS 'Código de autenticação externo (ex: Keycloak)';