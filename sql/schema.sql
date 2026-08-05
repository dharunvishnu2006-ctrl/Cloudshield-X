CREATE TABLE ip_addresses (
    id INTEGER PRIMARY KEY,
    ip TEXT UNIQUE NOT NULL,
    country TEXT,
    first_seen TEXT,
    is_blocklisted INTEGER DEFAULT 0
);

CREATE TABLE threat_actors (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT
);

CREATE TABLE security_events (
    id INTEGER PRIMARY KEY,
    event_time TEXT NOT NULL,
    source_ip INTEGER REFERENCES ip_addresses(id),
    actor_id INTEGER REFERENCES threat_actors(id),
    event_type TEXT,
    request TEXT,
    status INTEGER,
    severity_score REAL
);

CREATE INDEX idx_events_ip_time ON security_events(source_ip, event_time);