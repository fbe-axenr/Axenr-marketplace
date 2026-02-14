# Gap Analysis Clarifying Questions

This guide provides structured questions to ask users when they are uncertain about which option to choose (REUSE, EXTEND, DEVELOP_NEW, or HYBRID).

Use these questions to understand user priorities and guide them to the right decision.

---

## When to Use Clarifying Questions

Ask clarifying questions when:
- User responds "I'm not sure" or "I don't know"
- User asks "Which option do you recommend?"
- Match percentage is in borderline range (45-55% or 80-90%)
- Multiple options seem equally viable
- User's priorities are unclear

**Do NOT ask all questions every time**. Select 2-4 most relevant questions based on context.

---

## Question Framework

### Question 1: Strategic Integration

**Ask**: "Do you plan to use other AOS modules (CRM, Sale, Purchase, HR, etc.) that integrate with [EntityName]?"

**Follow-up context**:
- If entity is Partner/Customer: "Will you use Sale, CRM, or Project modules?"
- If entity is Product: "Will you use Sale, Purchase, or Stock modules?"
- If entity is Employee: "Will you use HR, Leave Management, or Timesheet modules?"

**Decision Logic**:

| User Answer | Recommendation | Rationale |
|-------------|----------------|-----------|
| **Yes, many modules** | REUSE or EXTEND | Integration with AOS ecosystem is critical |
| **Yes, 1-2 modules** | EXTEND | Some integration benefit, but can customize |
| **No, standalone** | DEVELOP_NEW viable | No integration dependency |
| **Unsure / Maybe later** | EXTEND | Keeps options open for future integration |

---

### Question 2: Licensing & Dependency Comfort

**Ask**: "Are you comfortable depending on Axelor Open Suite licensing (AGPL-3.0) and maintaining compatibility with AOS releases?"

**Explain context**:
- "AGPL-3.0 requires source code disclosure if you distribute modifications"
- "AOS updates may require migration work if you extend AOS entities"
- "Commercial Axelor license available if AGPL is problematic"

**Decision Logic**:

| User Answer | Recommendation | Rationale |
|-------------|----------------|-----------|
| **Yes, fine with AGPL** | REUSE or EXTEND acceptable | No licensing concerns |
| **Yes, have commercial license** | REUSE or EXTEND acceptable | Commercial license covers usage |
| **No, AGPL is problematic** | DEVELOP_NEW required | Avoid AOS dependency |
| **Unsure about AGPL** | Explain implications, may lean DEVELOP_NEW | Risk mitigation |

---

### Question 3: Team Expertise

**Ask**: "Does your development team have experience with Axelor AOS internals, entity extension, and the Axelor framework?"

**Clarify what "AOS internals" means**:
- Understanding AOS entity inheritance patterns
- Familiarity with AOS services (e.g., PartnerService, AddressService)
- Experience with AOS view customization
- Knowledge of AOS data migration for upgrades

**Decision Logic**:

| User Answer | Recommendation | Rationale |
|-------------|----------------|-----------|
| **Yes, experienced with AOS** | EXTEND is manageable | Team can handle complexity |
| **Some experience** | EXTEND with caution OR REUSE | Can learn as they go |
| **No AOS experience** | REUSE (simple) or DEVELOP_NEW (cleaner) | Avoid extension complexity |
| **Java expertise but no AOS** | DEVELOP_NEW preferred | Leverage Java skills, avoid AOS learning curve |

---

### Question 4: Timeline & Speed to Market

**Ask**: "Is speed critical for this entity? Do you need it deployed quickly, or is development time flexible?"

**Clarify timeline impact**:
- REUSE: ~0.5 days (fastest)
- EXTEND: ~1-2 days (moderate)
- DEVELOP_NEW: ~3-5 days (slowest)
- HYBRID: ~2-3 days (moderate-slow)

**Decision Logic**:

| User Answer | Recommendation | Rationale |
|-------------|----------------|-----------|
| **Very urgent, ASAP** | REUSE (fastest) | Sacrifice customization for speed |
| **Need it soon** | REUSE or EXTEND | Balance speed and customization |
| **Flexible timeline** | Any option viable | Time not a constraint |
| **Long-term project** | DEVELOP_NEW acceptable | Can invest time for better fit |

---

### Question 5: Future Customization Expectations

**Ask**: "Do you anticipate needing more than 5-10 additional custom fields or significant business logic changes in the future?"

**Clarify "significant business logic"**:
- Custom validation rules beyond AOS defaults
- Complex computed fields
- Non-standard workflows
- Integration with external systems specific to your business

**Decision Logic**:

| User Answer | Recommendation | Rationale |
|-------------|----------------|-----------|
| **Yes, heavy customization expected** | DEVELOP_NEW cleaner | Avoid fighting AOS constraints |
| **Yes, but gradual evolution** | EXTEND acceptable | Can add fields incrementally |
| **No, mostly standard** | REUSE or EXTEND sufficient | AOS provides what's needed |
| **Unsure, maybe** | EXTEND (middle ground) | Flexibility for future |

---

### Question 6: Maintenance & Long-term Ownership

**Ask**: "Who will maintain this entity long-term? Your team or Axelor's AOS updates?"

**Clarify maintenance implications**:
- REUSE: AOS team maintains, you get updates automatically
- EXTEND: Shared maintenance (AOS base + your extensions)
- DEVELOP_NEW: Your team owns everything
- HYBRID: Mixed (AOS entity + your custom entity)

**Decision Logic**:

| User Answer | Recommendation | Rationale |
|-------------|----------------|-----------|
| **Prefer AOS to maintain** | REUSE | Minimal maintenance burden |
| **Willing to co-maintain** | EXTEND | Acceptable shared responsibility |
| **Want full control** | DEVELOP_NEW | Own maintenance, own destiny |
| **Limited maintenance capacity** | REUSE preferred | Reduce ongoing work |

---

### Question 7: Data Migration Concerns

**Ask**: "Do you have existing data that needs to be migrated? Is data structure flexibility important?"

**Clarify migration complexity**:
- REUSE: Must map existing data to AOS entity structure
- EXTEND: Map to AOS fields + add custom fields
- DEVELOP_NEW: Full control over data model, easier custom migration
- HYBRID: More complex migration (two entities)

**Decision Logic**:

| User Answer | Recommendation | Rationale |
|-------------|----------------|-----------|
| **Yes, complex existing data** | DEVELOP_NEW may be easier | Custom structure fits existing data |
| **Yes, but simple data** | Any option viable | Migration manageable |
| **No, greenfield project** | Any option viable | No migration constraint |
| **Data structure must match legacy** | DEVELOP_NEW | Exact structure control |

---

## Question Selection Guide

**Based on match percentage:**

| Match % | Typical Decision | Questions to Prioritize |
|---------|------------------|-------------------------|
| **85-95%** | REUSE vs EXTEND | Q1 (Integration), Q4 (Timeline) |
| **50-84%** | EXTEND vs DEVELOP_NEW | Q5 (Future customization), Q3 (Team expertise) |
| **30-49%** | DEVELOP_NEW vs HYBRID | Q1 (Integration), Q6 (Maintenance) |
| **<30%** | DEVELOP_NEW (clear) | No questions needed, obvious choice |

**Based on user profile:**

| User Type | Questions to Prioritize |
|-----------|------------------------|
| **Technical decision maker** | Q3 (Team expertise), Q5 (Customization), Q6 (Maintenance) |
| **Business stakeholder** | Q1 (Integration), Q4 (Timeline), Q2 (Licensing) |
| **Project manager** | Q4 (Timeline), Q6 (Maintenance), Q3 (Team capacity) |
| **Architect** | Q5 (Customization), Q1 (Integration), Q7 (Data migration) |

---

## Conversational Flow Example

**Scenario**: Customer entity, 60% match with AOS Partner

```markdown
Agent: Based on 60% match, I recommend Option 2 (EXTEND).
      However, let me ask a few questions to confirm this is right for you.

Agent: Question 1: Do you plan to use other AOS modules like CRM, Sale, or Purchase
      that integrate with customer/partner management?

User: Yes, we'll use Sale and CRM modules.

Agent: Great, that strongly suggests EXTEND or REUSE for ecosystem integration.

Agent: Question 2: Is speed critical, or do you have time for proper development?

User: We need this functional in 2 weeks.

Agent: With that timeline, let me refine the recommendation:
      - EXTEND will take 1.5-2 days (fits your timeline)
      - DEVELOP_NEW would take 4-5 days (too slow)

Agent: Final recommendation: Option 2 (EXTEND)
      Rationale:
      - You need Sale/CRM integration (EXTEND maintains compatibility)
      - 2-week timeline is achievable with EXTEND
      - 60% match means extension is viable (not starting from scratch)

Agent: Does Option 2 (EXTEND) work for you?

User: Yes, let's go with EXTEND.

Agent: Understood. Recording decision: EXTEND Partner entity with custom fields
      [industry, companySize]. Estimated effort: 1.5 days.
```

---

## After Questions: Refine Recommendation

After collecting answers, synthesize a refined recommendation:

```markdown
### Refined Recommendation

Based on your answers:
- [Priority 1 from user]: [Answer] → Suggests [option]
- [Priority 2 from user]: [Answer] → Suggests [option]
- [Priority 3 from user]: [Answer] → Suggests [option]

**Updated Recommendation**: Option [N] ([REUSE/EXTEND/DEVELOP_NEW/HYBRID])

**Rationale**: [2-3 sentences explaining how user's priorities led to this recommendation]

**Trade-offs accepted**: [What user is giving up with this choice]

**Does this align with your priorities?**
```

---

## Handling Conflicting Priorities

If user's answers point to different options:

```markdown
Agent: I notice your priorities point in different directions:
      - Strategic integration suggests EXTEND
      - But heavy customization needs suggest DEVELOP_NEW

Agent: Which is higher priority for you:
      (A) AOS ecosystem integration, or
      (B) Full customization freedom?

[Let user clarify priority hierarchy]
```

---

## Recording Decision with Context

Once decision is made, record with full context:

```markdown
## Entity: [EntityName]

**Decision**: [OPTION] (User selected Option [N])

**User's Priorities** (from clarifying questions):
1. [Priority 1]: [Answer/Context]
2. [Priority 2]: [Answer/Context]
3. [Priority 3]: [Answer/Context]

**Agent Recommendation**: Option [N] - [OPTION]
**Alignment**: ✓ Aligned | ⚠ User override

**Rationale**: User prioritizes [key factor] over [other factor], leading to [OPTION] choice despite [match %].
```

---

## Tips for Effective Clarification

1. **Don't ask all questions**: Select 2-4 most relevant
2. **Listen for implicit priorities**: User may reveal priorities without direct questions
3. **Provide context**: Explain why question matters for decision
4. **Accept user overrides**: If user has strong preference, document it and move on
5. **Time-box discussion**: Don't spend >5 minutes per entity on questions
6. **Document reasoning**: Capture why user chose what they chose
