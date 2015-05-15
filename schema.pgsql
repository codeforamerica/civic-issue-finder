DROP TABLE IF EXISTS issue_clicks;

CREATE TABLE IF NOT EXISTS issue_clicks (

    datetime    TIMESTAMP WITHOUT TIME ZONE,
    remote_addr VARCHAR,
    visitor_id  VARCHAR,
    referer     VARCHAR,
    issue_url   VARCHAR

);
