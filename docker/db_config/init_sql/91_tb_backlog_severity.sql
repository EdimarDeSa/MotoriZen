SET
    ROLE motorizen;

SET
    search_path TO backlog;

CREATE TABLE
    IF NOT EXISTS "tb_backlog_severity" (
        "id_backlog_severity" SERIAL PRIMARY KEY NOT NULL,
        "description" VARCHAR(10) NOT NULL UNIQUE
    );

INSERT INTO
    "tb_backlog_severity" ("id_backlog_severity", "description")
VALUES
    (1, "INFO"),
    (2, "ERROR"),
    (3, "WARNING"),
    (4, "CRITICAL");