# Software Requirements Specification

## Purpose
Define requirements for CipherVault, a local encrypted file vault with temporary sharing.

## Users
- Registered user: upload, list, download, share, and delete owned files.
- Recipient: download a file through a valid unexpired share link.
- Developer/operator: configure and run the application.

## Functional Requirements
- FR-01: Register a unique username and password of at least 10 characters.
- FR-02: Store password hashes, never plain-text passwords.
- FR-03: Authenticate users and support logout.
- FR-04: Accept uploads within the configured maximum size.
- FR-05: Encrypt file bytes before writing them to disk.
- FR-06: Show only the current user's files.
- FR-07: Permit owners to download and decrypt their files.
- FR-08: Create random share tokens with expiry timestamps.
- FR-09: Reject unknown and expired share tokens.
- FR-10: Delete an owned file and associated share links.
- FR-11: Display validation feedback.

## Non-Functional Requirements
- Security: authenticated encryption and password hashing.
- Privacy: ownership checks for private file operations.
- Usability: browser-based interface.
- Maintainability: separate templates, styles, configuration, and routes.
- Portability: Python-supported operating systems.

## Constraints
The encryption key is configured by the operator. Local disk and SQLite are used. HTTPS is required for deployment. This prototype should not be exposed publicly without hardening.
