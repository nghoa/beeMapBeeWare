# Weekly report 1
## Tasks

### Administrative:
- [x] Group introductions and communication method selected
- [x] GitLab project group created. Members and mentors (@jtuunas @mtovaska @tearautt) added.
- [x] BeeMapTemplate forked and renamed (see: Local environment and repository setup).
- [x] Group meeting with mentor (see: Mentor weekly meetings) .
- [x] User-stories written (see: User Story Assignment for Week 1).
- [ ] Weekly report of tasks done (see: docs/reporting.md)
- [ ] Bonus: Register as student in GitHub: https://education.github.com/. Existing github accounts can add university email to get education benefits on their main account.
### Operative:

- [x] Continuous Integration environment selected and set up (see: Creating Google Kubernetes Cluster and Creating Azure Kubernetes Cluster).
- [x] Integration runner set up (see: Installing GitLab runner to Kubernetes).
- [x] Deployment target set up (see: Deploy to App Engine).
- [x] Pipeline tested → forked BeeMapTemplate deployment is accessible.
### Development:

- [x] Local development environment set up and git repository from group fork cloned (see: Local environment and repository setup).


## Security

In minimum, addressing the five bolded web application security risks needs to be reported
weekly by each group. Extra points available for further consideration of the other risks.
https://owasp.org/www-project-top-ten/

1. **Injection**
    - no user input yet to the web application
    - user supplied data is not used in any way 
    - handling the '/' route with static response 
    - other requested resources return a default 404 page.

2. Broken authentication
3. **Sensitive data exposure**
    - app uses http but doesn't currently use sensitive data
    - app user can't access files directly from the server
    - app doesn't store passwords, app keys, secrets etc.

4. XML External Entities (XXE)
5. Broken access control
6. **Security misconfiguration**
    - using default static error pages that shouldn't contain stack traces etc.
    - using recent versions of the tools used
      - python 3.8 used in app engine
      - flask 1.1.x
    - access control as specified in the lectures


7. Cross-Site Scripting (XSS)
8. Insecure Deserialization
9. **Using components with known vulnerabilities**
    - no unnecessary dependencies
    - used popular components from trusted sources or managed by google cloud with no known vulnerabilities related to our app

10. **Insufficient logging & monitoring**
    - using google cloud platform logging and monitoring utilities


