# Database Design

## Entity relationships
`users 1 ── many files 1 ── many shares`

## users
- `id`: integer primary key
- `username`: unique text, not null
- `password_hash`: text, not null
- `created_at`: timestamp

## files
- `id`: UUID-derived text primary key
- `owner_id`: foreign key to users
- `original_name`: sanitized download filename
- `stored_name`: unique encrypted blob filename
- `size_bytes`: original file size
- `created_at`: timestamp

## shares
- `id`: integer primary key
- `file_id`: foreign key to files
- `token_hash`: unique SHA-256 digest of share token
- `expires_at`: UTC expiry timestamp
- `created_at`: timestamp

Raw share tokens are placed in URLs but are not stored in the database. Foreign keys are enabled for SQLite connections.
