# Weekly report 3

## Tasks

### Administrative:

- [ ] User-stories updated & Time usage reported (see: User Story Assignment for Week 3).
- [ ] Group meeting with mentor (see: Mentor weekly meetings).
- [ ] Weekly report of tasks done (see: docs/reporting.md)

### DevOps

- [ ] Work on implementing customer requirements.
- [ ] Setup logging and monitoring (see: docs/logging/logging.md)
- [x] Add deployment address into week report and/or into README.md.
- [ ] Begin: Localization support (see: flask-babel).
- [ ] Add staging stage into pipeline (see: Adding Staging Stage).
- [ ] Keep coverage high by adding tests.
- [ ] Bonus: Add badges into README.md. (see: Gitlab: Badges)



## Security

In minimum, addressing the five bolded web application security risks needs to be reported
weekly by each group. Extra points available for further consideration of the other risks.
https://owasp.org/www-project-top-ten/

1. **Injection**
2. Broken authentication
        - usage of flask-login 
            - It stores the active user’s ID in the session (easy log in and out)
3. **Sensitive data exposure**
4. XML External Entities (XXE)
5. Broken access control
        - usage of flask-login
            - restriction of views for log-in or log-out user’s
6. **Security misconfiguration**
        - login_manager session protection is set to strong (see flask-login documentation: https://flask-login.readthedocs.io/en/latest/#session-protection)
7. Cross-Site Scripting (XSS)
8. Insecure Deserialization
9. **Using components with known vulnerabilities**
        - used newest version of flask-wtf (0.14.3)
        - used newest version of flask-login (0.5.0)
10. **Insufficient logging & monitoring**