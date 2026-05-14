# Repeat Prescription Process Investigation

## Objective

The purpose of this investigation was to understand and validate the repeat prescription workflow within the SystmOnline portal to determine whether the process can be reliably automated using Selenium.

---

# Repeat Prescription Process (Mapped Workflow)

```text
1. Open SystmOnline Portal
    ↓
2. Login
    ↓
3. Open Medication Menu
    ↓
4. Select "Request Medication"
    ↓
5. Wait for Repeat Prescription Page
    ↓
6. Select Medication(s)
    ↓
7. Continue to Confirmation Page
    ↓
8. Submit Medication Request
```

---

# Step 1 — Open SystmOnline Portal

### Description
The automation navigates to the SystmOnline portal URL.

### Page Elements

| Element | Selector |
|----------|-----------|
| Portal URL | `https://systmonline.tpp-uk.com` |

### Potential Risks
- Website unavailable
- Slow loading page
- URL changes

### Mitigations
- Use explicit waits after page load
- Log failures when portal cannot be reached
- Keep base URL configurable

---

# Step 2 — Login

### Description
The user is authenticated using stored portal credentials.

### Page Elements

| Element | Selector Type | Selector |
|----------|---------------|-----------|
| Username Input | `By.NAME` | `Username` |
| Password Input | `By.NAME` | `Password` |

### Potential Risks
- Invalid credentials
- Slow page loading
- Portal introduces MFA or CAPTCHA
- Login page structure changes

### Mitigations
- Store credentials securely in `.env`
- Use explicit waits before interacting
- Log authentication failures
- Monitor for portal changes

---

# Step 3 — Open Medication Menu

### Description
After authentication, the automation navigates to the medication section.

### Page Elements

| Element | Selector |
|----------|-----------|
| Medication Menu Button | `//button[contains(., 'Medication')]` |

### Potential Risks
- Element not loaded yet
- Button text changes
- Portal navigation redesign

### Mitigations
- Use `WebDriverWait`
- Wait for clickable state
- Log navigation failures

---

# Step 4 — Select "Request Medication"

### Description
The automation opens the repeat prescription request page.

### Page Elements

| Element | Selector |
|----------|-----------|
| Request Medication Button | `//form[@action='Medication']//button` |

### Potential Risks
- Selector becomes invalid
- Portal workflow changes
- Delayed page rendering

### Mitigations
- Use explicit waits
- Log failures
- Review selectors periodically

---

# Step 5 — Wait for Repeat Prescription Page

### Description
The automation validates successful navigation before proceeding.

### Page Elements

| Element | Selector |
|----------|-----------|
| Regular Medication Header | `//h4[contains(., 'Regular Medication')]` |

### Potential Risks
- Page loads slowly
- Header text changes
- Partial page rendering

### Mitigations
- Validate page state before continuing
- Use visibility waits
- Add timeout handling

---

# Step 6 — Select Medication(s)

### Description
Medication checkboxes are selected dynamically using medication names.

### Page Elements

| Element | Selector |
|----------|-----------|
| Medication Checkbox | `//h3[contains(.,'{med}')]/ancestor::tr//input` |

### Potential Risks
- Medication name mismatch
- Medication unavailable
- Portal HTML structure changes

### Mitigations
- Log medication selection failures
- Continue processing remaining medications
- Validate medication exists before proceeding

---

# Step 7 — Continue to Confirmation Page

### Description
Selected medications are confirmed and workflow progresses.

### Page Elements

| Element | Selector |
|----------|-----------|
| Continue Button | `//button[contains(., 'Continue')]` |

### Potential Risks
- Button unavailable
- No medication selected
- Portal validation errors

### Mitigations
- Verify at least one medication selected
- Use explicit waits
- Log failures

---

# Step 8 — Submit Medication Request

### Description
The request is submitted to the prescription portal.

### Page Elements

| Element | Selector |
|----------|-----------|
| Request Medication Button | `//button[@type='submit' and normalize-space()='Request Medication']` |

### Potential Risks
- Accidental submission during testing
- Selector changes
- Submission failures

### Mitigations
- Test using dry-run approach during development
- Add confirmation checks
- Log submission status

---

# Outcome / Conclusion

The repeat prescription workflow was successfully mapped and validated for automation.

### Confirmed Outcomes
- Login process can be automated successfully
- Navigation to the medication section is reliable
- Repeat prescription page can be reached consistently
- Medication selection works dynamically using medication names
- Multiple medications can be selected in a single request
- Final submission workflow is technically automatable

### Risks Identified
- XPath selectors are dependent on portal structure
- Medication names require exact matching
- Portal changes may break automation
- MFA/CAPTCHA could prevent future automation

### Conclusion
The SystmOnline repeat prescription process is suitable for Selenium automation. No major technical blockers were identified during investigation, and the workflow can be reliably automated with appropriate logging, waits, and error handling.