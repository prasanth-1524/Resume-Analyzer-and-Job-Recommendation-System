# Viva Questions and Answers

**1. What is the project?** A web application for encrypted file storage and controlled file sharing.

**2. What is encryption at rest?** Protecting data while it is stored on disk.

**3. Which encryption tool is used?** Fernet from Python's `cryptography` package, which provides symmetric authenticated encryption.

**4. How are passwords stored?** As password hashes using Werkzeug's scrypt-based password hashing.

**5. Why use SQLite?** It is lightweight and suitable for a local academic project.

**6. How does a share link work?** A random token is generated; only its digest and expiry are stored in the database.

**7. What is a bearer link?** Anyone who possesses the URL can use it, so the URL must be treated as a secret.

**8. What happens when a link expires?** The route compares its expiry timestamp with current UTC time and rejects it.

**9. Is this end-to-end encryption?** No. The server has the key and decrypts files for downloads.

**10. What happens if the key is lost?** Files encrypted with it cannot be recovered without a valid backup of the key.

**11. What are the limitations?** No MFA, CSRF middleware, rate limiting, malware scanning, key rotation, or independent security audit.

**12. What future work is possible?** Cloud storage, key rotation, audit logs, one-time links, recipient verification, and stronger security controls.
