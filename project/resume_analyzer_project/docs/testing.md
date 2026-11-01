# Testing Plan

## Automated tests
Run:
```bash
pytest -q
```
The included tests verify basic vocabulary detection and that missing skills are identified with a bounded score.

## Manual test cases
| ID | Test | Steps | Expected result |
|---|---|---|---|
| TC01 | Register | Submit name, unique email, password ≥ 8 chars | Account created and login page shown |
| TC02 | Duplicate registration | Register same email again | Friendly error; no duplicate account |
| TC03 | Login success | Enter correct credentials | Dashboard opens |
| TC04 | Login failure | Enter wrong password | Error message shown |
| TC05 | Upload PDF | Upload readable PDF under 5 MB | Text extracted; skills shown |
| TC06 | Upload DOCX | Upload DOCX under 5 MB | Text extracted; skills shown |
| TC07 | Invalid file | Upload TXT or image | Upload rejected |
| TC08 | Oversized file | Upload file over 5 MB | Size error shown |
| TC09 | Job search | Search for Python | Relevant sample listings displayed |
| TC10 | Job match | Upload resume with Python and SQL; open role | Score and matched/missing skills displayed |
| TC11 | Save job | Click Save job while logged in | Job appears in dashboard |
| TC12 | Save analysis | Click Save analysis | Analysis appears in history |
| TC13 | Access isolation | Try another user's resume URL while logged in | Resume detail returns 404 |
| TC14 | Empty match | Use resume with no known skills | Score remains within 0–100; gaps shown |

## Test report template
Fill this out after running the project on your own machine.

| Test ID | Actual result | Pass/Fail | Notes |
|---|---|---|---|
| TC01 | [Enter result] | [Pass/Fail] | |
| TC02 | [Enter result] | [Pass/Fail] | |
| TC03 | [Enter result] | [Pass/Fail] | |
| TC05 | [Enter result] | [Pass/Fail] | |
| TC09 | [Enter result] | [Pass/Fail] | |
| TC10 | [Enter result] | [Pass/Fail] | |
| TC11 | [Enter result] | [Pass/Fail] | |

Do not mark a test as passed until you have run it and observed the result.
