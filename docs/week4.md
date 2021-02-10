# Weekly report 4

## Tasks

### Administrative:

- [ ] User-stories updated & Time usage reported (see: User Story Assignment for Week 4).
- [x] Group meeting with mentor (see: Mentor weekly meetings).
- [ ] Weekly report of tasks done (see: docs/reporting.md)

### DevOps

- [x] Work on implementing customer requirements.
- [x] Add Localization support (see: docs/adding-localization.md).
- [x] Implement admin interface.
- [x] Write bug and security issue reporting guide (see: GitLab: Description Templates).
- [x] Describe how to report issues in README.md.
- [x] Bughunt! You will be assigned to evaluate two other teams’ implementation, and to identify security and bug issues within their solution (peer review).
- [ ] Bonus: Collect interesting metrics.



## Security

In minimum, addressing the five bolded web application security risks needs to be reported
weekly by each group. Extra points available for further consideration of the other risks.
https://owasp.org/www-project-top-ten/

1. **Injection**
    - restricted user input length
    - hid latitude and longitude fields -> less attack surface
2. Broken authentication
3. **Sensitive data exposure**
4. XML External Entities (XXE)
5. Broken access control
6. **Security misconfiguration**
7. Cross-Site Scripting (XSS)
    - added subsource integrity hashes for stylesheets and scripts supplied by third parties
8. Insecure Deserialization
9. **Using components with known vulnerabilities**
10. **Insufficient logging & monitoring**