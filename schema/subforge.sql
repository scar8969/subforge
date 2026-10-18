-- 🛰 v2scar schema
CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, vmess_uuid TEXT, ss_port INTEGER UNIQUE, level INTEGER DEFAULT 0, upload_traffic INTEGER DEFAULT 0, download_traffic INTEGER DEFAULT 0, total_traffic INTEGER DEFAULT 21474836480, enable INTEGER DEFAULT 1, is_admin INTEGER DEFAULT 0, created_at DATETIME);
CREATE TABLE nodes(id INTEGER PRIMARY KEY, name TEXT, server TEXT, port INTEGER DEFAULT 443, country TEXT, used_traffic INTEGER DEFAULT 0, total_traffic INTEGER DEFAULT 1073741824, enable INTEGER DEFAULT 1, last_seen DATETIME);
CREATE TABLE traffic_logs(id INTEGER PRIMARY KEY, user_id INTEGER, node_id INTEGER, upload INTEGER DEFAULT 0, download INTEGER DEFAULT 0, created_at DATETIME);
