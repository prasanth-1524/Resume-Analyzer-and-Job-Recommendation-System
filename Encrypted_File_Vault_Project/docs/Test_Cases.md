# Test Cases

| ID | Scenario | Steps | Expected result |
|---|---|---|---|
| TC-01 | Valid registration | Submit unique username and 10+ character password | Account created |
| TC-02 | Invalid password | Submit password shorter than 10 characters | Validation error |
| TC-03 | Duplicate username | Register an existing username | Registration rejected |
| TC-04 | Valid login | Enter correct credentials | Vault opens |
| TC-05 | Invalid login | Enter incorrect credentials | Generic login error |
| TC-06 | Upload | Upload a small non-empty file | File appears in vault |
| TC-07 | Encryption at rest | Inspect the `.enc` blob | Stored bytes are ciphertext, not original plaintext |
| TC-08 | Download | Download a stored file | Content matches original |
| TC-09 | Owner isolation | Create two users and upload separate files | Each sees only their own files |
| TC-10 | Valid share | Create link and open it before expiry | File downloads |
| TC-11 | Invalid token | Alter a character in a share URL | Not found response |
| TC-12 | Expired token | Set expiry in the past in test database | Expired response |
| TC-13 | Delete | Delete a stored file | Blob and associated links are removed |
| TC-14 | Large upload | Upload beyond configured limit | HTTP 413 response |

Run tests locally and record actual outcomes. Do not claim a test passed until you execute it.
