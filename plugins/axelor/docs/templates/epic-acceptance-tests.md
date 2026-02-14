# EPIC Acceptance Tests Template

This template defines how to structure end-to-end acceptance test scenarios for EPICs. These scenarios validate that the complete EPIC delivers the intended business value.

## Template

```textile
h2. EPIC Acceptance Tests

h3. Scenario 1: [Happy Path - Normal Flow]

# Step 1: [User action]
#* *Expected Result:* [What should happen]
# Step 2: [Next action]
#* *Expected Result:* [What should happen]
# Step 3: [Final action]
#* *Expected Result:* [Final state]

h3. Scenario 2: [Alternative Flow or Error Handling]

# Step 1: [User action with invalid data]
#* *Expected Result:* [Error message displayed]
# Step 2: [Correction]
#* *Expected Result:* [Success]

h3. Scenario 3: [Edge Case]

# [Edge case testing]
```

## Guidelines

### Scenario Types

Each EPIC should have at least 3 scenarios covering:

1. **Happy Path**: Normal user flow with valid data and expected usage
2. **Alternative Flow**: Valid alternative paths or error handling
3. **Edge Cases**: Boundary conditions, unusual data, or rare situations

### Scenario Naming

- **Format**: [Type] - [Brief Description]
- **Examples**:
  - "Happy Path - Create and Send Email"
  - "Error Handling - Invalid Email Address"
  - "Edge Case - Email with Large Attachment"

### Step Structure

Each step should follow this pattern:

```textile
# Step N: [User action in active voice]
#* *Expected Result:* [Observable outcome that can be verified]
```

**Good example**:
```textile
# Step 3: User clicks "Mark as Read" button
#* *Expected Result:* Email subject changes to normal font, envelope icon changes to open, unread count decreases by 1
```

**Bad example**:
```textile
# Step 3: System updates status
#* *Expected Result:* Status changed
```

### Expected Results

Expected results should be:
- **Observable**: Can be seen or measured by the tester
- **Specific**: Exact values, states, or behaviors
- **Verifiable**: Clear pass/fail criteria

**Include**:
- UI changes (text, icons, visibility)
- Data state changes (database values)
- System feedback (messages, notifications)
- Side effects (emails sent, logs created)

## Complete Example

```textile
h2. EPIC Acceptance Tests - Email Status Management

h3. Scenario 1: Happy Path - Mark Single Email as Unread for Follow-up

# Step 1: User opens Inbox grid view
#* *Expected Result:* Grid displays 15 emails, 3 shown in bold (unread), unread badge shows "3"
# Step 2: User sees email from "John Doe <john@example.com>" with subject "Quotation Request" in normal font (read status)
#* *Expected Result:* Email row displays with open envelope icon, normal font weight
# Step 3: User right-clicks on the email row
#* *Expected Result:* Context menu appears with options: "Mark as Unread", "Delete"
# Step 4: User clicks "Mark as Unread"
#* *Expected Result:* Email subject changes to bold, envelope icon changes to closed, unread badge updates to "4", notification displays "Email marked as unread"
# Step 5: User closes and reopens Inbox
#* *Expected Result:* Email still displayed in bold with unread status persisted

h3. Scenario 2: Bulk Mark Multiple Emails as Read

# Step 1: User selects 5 unread emails via checkboxes
#* *Expected Result:* Bulk action toolbar appears with "Mark as Read" button enabled
# Step 2: User clicks "Mark as Read" button
#* *Expected Result:* Progress indicator shown while processing
# Step 3: System processes all 5 emails (4 succeed, 1 fails due to permission)
#* *Expected Result:* Grid refreshes, 4 emails now in normal font with open envelope icons, notification displays "4 emails marked as read, 1 failed", unread badge decreases by 4
# Step 4: User clicks notification to see error details
#* *Expected Result:* Error message displays: "Permission denied for email: [subject]"

h3. Scenario 3: Edge Case - Mark Email as Unread Immediately After Opening

# Step 1: User double-clicks unread email to open detail view
#* *Expected Result:* Form view opens, email automatically marked as read (statusSelect=2), "Mark as Unread" button visible
# Step 2: User immediately clicks "Mark as Unread" without reading content
#* *Expected Result:* Status reverts to unread (statusSelect=1), "Mark as Unread" button disappears, Reply/Forward buttons hidden
# Step 3: User closes form and returns to grid
#* *Expected Result:* Email displayed in bold with closed envelope icon, unread count increased by 1

h3. Scenario 4: Error Handling - Mark Email Without Permission

# Step 1: User (role: Sales Rep) attempts to mark email in manager's mailbox as read
#* *Expected Result:* "Mark as Read" action disabled or grayed out
# Step 2: User tries to use browser console to bypass UI restriction
#* *Expected Result:* Backend validation fails, error returned: "You do not have permission to modify this email"
# Step 3: Grid remains unchanged
#* *Expected Result:* Email status unchanged, error logged in audit trail
```

## End-to-End Test Coverage

Ensure scenarios cover:

### Functional Coverage
- [ ] All major user workflows (happy paths)
- [ ] All alternative flows and decision points
- [ ] All error conditions and validations
- [ ] All edge cases and boundary conditions

### Integration Coverage
- [ ] All entity relationships tested
- [ ] All service integrations verified
- [ ] All external system interactions validated
- [ ] All permission/security rules enforced

### Data Coverage
- [ ] Valid data inputs
- [ ] Invalid data inputs
- [ ] Boundary values (min/max)
- [ ] Empty/null values
- [ ] Large datasets (performance)

### User Role Coverage
- [ ] All user roles with different permissions
- [ ] Role-based access control verified
- [ ] Cross-role scenarios tested

## Definition of Done for EPIC Testing

```textile
h2. Definition of Done (DoD)

For this EPIC to be considered complete:

* [ ] All User Stories in DONE status
* [ ] All acceptance scenarios executed and passing
* [ ] Integration tests written and passing
* [ ] Code reviewed and compliant with Axelor conventions
* [ ] Technical documentation updated (JavaDoc, inline comments)
* [ ] i18n keys defined for all languages
* [ ] Database migration script created (if needed)
* [ ] Deployed to test environment
* [ ] Functional validation by Product Owner completed
* [ ] No critical or blocking bugs remaining
* [ ] Performance benchmarks met (if applicable)
* [ ] Security audit passed (if applicable)
```

## Relationship to User Story Acceptance Criteria

**EPIC Acceptance Tests** vs. **US Acceptance Criteria**:

| Aspect | EPIC Acceptance Tests | US Acceptance Criteria |
|--------|----------------------|------------------------|
| **Scope** | End-to-end business flows | Single feature implementation |
| **Level** | Integration across multiple US | Unit/component level |
| **Focus** | Business value delivery | Technical correctness |
| **Tester** | Product Owner, QA | Developer, QA |
| **When** | After all US completed | After single US completed |

**Example**:
- **US Acceptance Criterion**: "Grid displays columns: From, Subject, Date"
- **EPIC Acceptance Scenario**: "User opens Inbox, searches for customer emails, marks them as read, and verifies they appear in 'Read' folder"

## Related Templates

- [EPIC Template](epic-template.md)
- [User Story Template](user-story-template.md)
