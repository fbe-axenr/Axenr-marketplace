# Axelor Development Commands Comparison

Comparison of development workflow commands available in the axelor plugin.

## Feature Comparison

| Feature | `/develop` | `/develop-complete-feature` | `/analyze-requirements` |
|---------|------------|----------------------------|------------------------|
| **Requirements analysis** | No | Yes | Yes |
| **Architecture design** | Yes | Yes | No |
| **Code generation** | Yes | Yes | No |
| **Test generation** | Yes (optional) | Yes | No |
| **Checkpoint commits** | Yes (5) | Yes (4) | No |
| **Validation gates** | **6** (one per phase) | 4 | 4 |
| **Resume capability** | Yes | Yes | Limited |
| **Extend mode** | Yes | No | No |
| **Auto-commit option** | Yes | Yes | No |

---

## When to Use Each Command

### `/develop`

**Best for:**
- Implementation from ready specifications
- Bug fixes requiring code generation
- Extending existing architecture
- Quick iteration with manual commits
- Workflows needing fine-grained control

**Phases:** 7 (Architecture → Domain → Views → Java → Tests → Review → Commit)

### `/develop-complete-feature`

**Best for:**
- End-to-end feature development
- Starting from scratch with requirements
- Automated workflows
- Full documentation needs

**Phases:** 19 (Analysis → Refinement → EPIC/US → Architecture → Implementation)

### `/analyze-requirements`

**Best for:**
- Requirements gathering only
- Gap analysis against existing system
- Specification documentation
- Preparing input for `/develop`

**Phases:** 4 (Analysis → Refinement → Gap Analysis → EPIC/US Generation)

---

## Decision Tree

```
Need to generate code?
├── No → /analyze-requirements
└── Yes
    ├── Have specifications ready?
    │   ├── Yes → /develop
    │   └── No → /develop-complete-feature
    │
    └── Need full automated workflow?
        ├── Yes → /develop-complete-feature
        └── No → /develop
```

---

## See Also

- [/develop Command](../../commands/develop.md)
- [/develop-complete-feature Command](../../commands/develop-complete-feature.md)
- [/analyze-requirements Command](../../commands/analyze-requirements.md)
