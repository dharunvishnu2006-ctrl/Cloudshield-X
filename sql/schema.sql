CREATE TABLE IF NOT EXISTS ip_addresses (
    id INTEGER PRIMARY KEY,
    ip TEXT UNIQUE NOT NULL,
    country TEXT,
    first_seen TEXT,
    is_blocklisted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS threat_actors (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT
);

CREATE TABLE IF NOT EXISTS security_events (
    id INTEGER PRIMARY KEY,
    event_time TEXT NOT NULL,
    source_ip INTEGER REFERENCES ip_addresses(id),
    actor_id INTEGER REFERENCES threat_actors(id),
    event_type TEXT,
    request TEXT,
    status INTEGER,
    severity_score REAL
);

CREATE INDEX IF NOT EXISTS idx_events_ip_time ON security_events(source_ip, event_time);

CREATE TABLE IF NOT EXISTS host_links (
    src_host TEXT NOT NULL,
    dst_host TEXT NOT NULL
);