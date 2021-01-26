# Weekly report 2

## Tasks

### Administrative:

- [x] User-stories written (see: User Story Assignment for Week 2).
- [x] Group meeting with mentor (see: Mentor weekly meetings).
- [x] Weekly report of tasks done (see: docs/reporting.md)
- [ ] Bonus from week 1: Register as student in GitHub: https://education.github.com/. Existing github accounts can add university email to get education benefits on their main account.

### Operative:
- [x] Database set up
  - google cloud datastore set up

### Development:

- [x] User can add locations.
  - ui implemented
- [X] Added locations are shown and saved to the backend.
  - added locations are loaded and saved asynchronously
- [X] Begin: Admin interface / CRUD
- [x] Begin: Testing.
  - basic input validation pure function tests

## Security

In minimum, addressing the five bolded web application security risks needs to be reported
weekly by each group. Extra points available for further consideration of the other risks.
https://owasp.org/www-project-top-ten/

1. **Injection**
    - TODO: input handling service
      - Input validation => Sanization approach (Reference: https://dev.to/mrkanthaliya/validating-and-sanitizing-user-inputs-on-python-projects-rest-api-5a4)
        - Special characters escape
        - maybe using prepared statements

    - Saving to datastore is only done when two valid floating point numbers (latitude, longitude) are send to be saved. 
    - Input json schema is not validated yet so it's possible to manually build a json list post request instead of object which leads to program crashing (probably, not tested). 

2. Broken authentication
    - Done: flask-login package implemented
      - implemented token authentication => prevent partially impersonation attacks
      - implemented session based authentication => further research needed...
    - TODO:
      - timeout function: brute-force login
      - DO not use verbose failure messages (i.e. "username is wrong" => means it is not in the database)
      - admin session-key is heavily "randomized" to prevent impersonation attacks
      - avoid predictable admin IDs & passwords
3. **Sensitive data exposure**
    - Only locations are saved, so there is no sensitive data yet.
4. XML External Entities (XXE)
5. Broken access control
    - TODO:
      - only admin has access to the list of recommended bee-hives
      - admin gets unique & heavily randomized session-key
      - "centralized component": Admin-Session-Checker for all /routes regarding CRUD operations
6. **Security misconfiguration**
    - Google application credentials are shared through gitlab. Credentials are only transmitted to the host engine, when the CI/CD pipeline through Gitlab is triggered. Meaning, all security is handled by Gitlab in this regard.
7. Cross-Site Scripting (XSS)
    - At the time of writing, only locations are saved and they can only be numbers and pplication crashes on invalid input, so it's safe.
    - TODO:
      - Input handling service 
        - escape special characters
8. Insecure Deserialization
    - Done: flask-login package implemented
      - implemented password hashing => makes eavesdrop harder
9. **Using components with known vulnerabilities**
    - using components from official and trusted sources

10. **Insufficient logging & monitoring**
    - Done: flask-login package implemented
    - TODO:
      - build UI for login tracking (low priority)
    