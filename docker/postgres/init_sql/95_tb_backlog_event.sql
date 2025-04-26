SET
    ROLE motorizen;

SET
    search_path TO motorizen_backlog;

CREATE TABLE
    IF NOT EXISTS "tb_backlog_event" (
        "id_backlog_event" SERIAL PRIMARY KEY NOT NULL,
        "cd_backlog_event_type" INTEGER NOT NULL REFERENCES "tb_backlog_event_type" ("id_backlog_event_type"),
        "cd_user" UUID NOT NULL REFERENCES "motorizen_schema"."tb_user" ("id_user"),
        "comment" TEXT CHECK (
            "comment" IS NULL
            OR TRIM("comment") <> ''
        ),
        "created_at" TIMESTAMP
    );

CREATE INDEX idx_backlog_event_type ON "tb_backlog_event" ("cd_backlog_event_type");

CREATE INDEX idx_backlog_user ON "tb_backlog_event" ("cd_user");

CREATE INDEX idx_backlog_created_at ON "tb_backlog_event" ("created_at");

CREATE TRIGGER set_backlog_event_timestamps BEFORE INSERT ON "tb_backlog_event" FOR EACH ROW EXECUTE FUNCTION set_backlog_timestamp ();