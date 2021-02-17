# Weekly report 5

## Tasks

### Administrative

- [X] User-stories updated & Time usage reported. Marks completed ones as done. (see: User Story Assignment for Week 5).
- [X] Group meeting with mentor (see: Mentor weekly meetings).
- [X] Weekly report of tasks done (see: docs/reporting.md)
- [X] Report bug fixes in weekly report → What were the issues; What was the cause of the issue; What was the solution?

### DevOps

- [X] Triage and prioritize fixing issues.
- [X] Finalize application.
- [X] Client requirements validation.

### Marketing

- [X] Prepare final presentation. Presentation should be about 5 min in length - including time for questions. (More details under Final Event (17.2.2021)


## Security

In minimum, addressing the five bolded web application security risks needs to be reported
weekly by each group. Extra points available for further consideration of the other risks.
https://owasp.org/www-project-top-ten/

1. **Injection**
    - user input is manipulated as little as possible before it goes to datastore. 
2. Broken authentication
    - Admin password was changed to a bit stronger one
3. **Sensitive data exposure**
    - checked whether all error messages were correct
    - outsider should not get too much information out of the messages
    - apis return as little as possible information to user and sensitive endpoints were moved to admin side (behind password)
4. XML External Entities (XXE)
5. Broken access control
6. **Security misconfiguration**
    - disabled CSRF token in suggestion form because of unnecessary token generation
7. Cross-Site Scripting (XSS)
    - XXS: tested strings like `<button>hei</button>` as input and browser didn't interpret them as html elements.
8. Insecure Deserialization
9. **Using components with known vulnerabilities**
    - double checked all used libraries regarding known vulnerabilities
    - Note: WTForms versions &lt;2.1 are vulnerable against XSS, but the used version is 2.3.3
10. **Insufficient logging & monitoring**
    - 
## Bug fixes 

Report bug fixes in weekly report → What were the issues; What was the cause of the issue; What was the solution?

### Input length
  - there was no validation for how long the inputted fields can be. Validation of it was added.

### Email validation
  - Email was not validated. Simple regex validation was added.

### Subresource integrity
  - Loaded javascript libraries didn't have integrity hashes. They were added. 

### Version limit
  - Google app engine had version limit of 210 which was exceeded and as a result ci/cd pipeline failed. 209 version were deleted. Apparently google cloud doesn't do this automatically at least with default settings. 

### Update Suggestion
  - was buggy due to localization -> fixed now