---
name: axelor-controller-method-extractor
description: Extracts controller method signatures from Axelor view XML files. Identifies all action-method elements and generates a structured list of methods to implement in each controller class.
---

# Axelor Controller Method Extractor

## Mission

Scan generated Axelor view XML files to identify all controller methods that need to be implemented. Extract action-method elements and provide a structured report of methods grouped by controller class.

## Purpose

When views are generated, they often reference controller methods via `<action-method>` elements. This skill automatically:
1. Scans all view XML files in the project
2. Identifies all `<action-method>` elements
3. Extracts the controller class and method name
4. Groups methods by controller
5. Provides a structured report for the Java generator

## Action-Method Format

According to Axelor conventions, action-method elements follow this pattern:

```xml
<action-method name="action-[modulename]-method-[purpose]">
  <call class="[package].web.[Domain]Controller"
        method="[methodName]"/>
</action-method>
```

**Example:**
```xml
<action-method name="action-project-method-check-permissions">
  <call class="com.axelor.apps.project.web.ProjectController"
        method="checkUserPermissions"/>
</action-method>
```

## Extraction Process

### Step 1: Locate View Files

Search for all view XML files in the project:

```bash
# Find all XML files in typical view locations
find . -path "*/resources/views/*.xml" -type f
# OR
find . -path "*/axelor-*/src/main/resources/views/*.xml" -type f
```

### Step 2: Extract Action-Method Elements

For each XML file, identify all `<action-method>` elements:

1. Read the XML file
2. Search for `<action-method>` tags
3. Extract the `name` attribute
4. Find the nested `<call>` element
5. Extract `class` and `method` attributes

### Step 3: Parse Controller Information

From each action-method:

**Extract:**
- **Action name**: Full action-method name (e.g., `action-project-method-check-permissions`)
- **Module name**: Extracted from action name (e.g., `project`)
- **Purpose**: Extracted from action name (e.g., `check-permissions`)
- **Controller class**: Full qualified class name (e.g., `com.axelor.apps.project.web.ProjectController`)
- **Package**: Extracted from class (e.g., `com.axelor.apps.project`)
- **Simple class name**: Controller name only (e.g., `ProjectController`)
- **Domain**: Extracted from controller name (e.g., `Project`)
- **Method name**: Method to implement (e.g., `checkUserPermissions`)

### Step 4: Group by Controller

Group all methods by their controller class:

```
ProjectController (com.axelor.apps.project.web.ProjectController)
  - checkUserPermissions
  - validateProjectDates
  - computeTotalCost

OrderController (com.axelor.apps.sale.web.OrderController)
  - confirmOrder
  - cancelOrder
```

## Output Format

Provide a structured report in this format:

```markdown
# Controller Methods Extraction Report

## Summary
- Total action-method elements found: [count]
- Total controllers identified: [count]
- Total methods to implement: [count]

## Controllers and Methods

### 1. [Domain]Controller

**Full class name:** `[package].web.[Domain]Controller`
**Package:** `[package]`
**Domain:** `[Domain]`

**Methods to implement:**

#### Method: [methodName]
- **Action name:** `action-[module]-method-[purpose]`
- **Purpose:** [purpose description]
- **Source view:** `[view-file-path]`

---

### 2. [NextDomain]Controller
...
```

## Detailed Example

Given these action-methods in `project-view.xml`:

```xml
<action-method name="action-project-method-validate">
  <call class="com.axelor.apps.project.web.ProjectController"
        method="validateProject"/>
</action-method>

<action-method name="action-project-method-compute-cost">
  <call class="com.axelor.apps.project.web.ProjectController"
        method="computeTotalCost"/>
</action-method>

<action-method name="action-task-method-assign">
  <call class="com.axelor.apps.project.web.TaskController"
        method="assignToUser"/>
</action-method>
```

**Output:**

```markdown
# Controller Methods Extraction Report

## Summary
- Total action-method elements found: 3
- Total controllers identified: 2
- Total methods to implement: 3

## Controllers and Methods

### 1. ProjectController

**Full class name:** `com.axelor.apps.project.web.ProjectController`
**Package:** `com.axelor.apps.project`
**Domain:** `Project`

**Methods to implement:**

#### Method: validateProject
- **Action name:** `action-project-method-validate`
- **Purpose:** validate
- **Source view:** `src/main/resources/views/project-view.xml`

#### Method: computeTotalCost
- **Action name:** `action-project-method-compute-cost`
- **Purpose:** compute-cost
- **Source view:** `src/main/resources/views/project-view.xml`

---

### 2. TaskController

**Full class name:** `com.axelor.apps.project.web.TaskController`
**Package:** `com.axelor.apps.project`
**Domain:** `Task`

**Methods to implement:**

#### Method: assignToUser
- **Action name:** `action-task-method-assign`
- **Purpose:** assign
- **Source view:** `src/main/resources/views/project-view.xml`
```

## Implementation Notes

### Method Signature Template

For each extracted method, the controller should implement:

```java
public void [methodName](ActionRequest request, ActionResponse response) {
    // Implementation here
}
```

### Using Grep for Extraction

You can use grep to find action-method patterns:

```bash
# Find all action-method elements
grep -r "<action-method" --include="*.xml" src/main/resources/views/

# Extract class and method attributes
grep -A 2 "<action-method" src/main/resources/views/*.xml | grep "<call"
```

### Parsing Strategy

1. Use `Glob` to find all view XML files
2. Use `Read` to read each XML file
3. Use regex or string parsing to extract action-method elements
4. Parse the class and method attributes
5. Group results by controller class

**Regex patterns:**

```regex
# Match action-method element
<action-method\s+name="([^"]+)"[^>]*>

# Match call element with class and method
<call\s+class="([^"]+)"\s+method="([^"]+)"

# Extract module from action name
action-([^-]+)-method-(.+)
```

## Edge Cases

### 1. Multiple Modules

If views reference controllers from different modules:
- Group by full package path
- Indicate which module each controller belongs to

### 2. Missing Controllers

If a controller class doesn't exist yet:
- Note that it needs to be created
- Suggest the package and class name

### 3. Duplicate Methods

If the same method is referenced multiple times:
- List it once
- Note all action names that reference it

### 4. Complex Method Names

If method names contain special characters or are unclear:
- Flag for manual review
- Suggest conventional naming

## Validation Checks

Before reporting, verify:

- [ ] All controller class names follow `[Domain]Controller` pattern
- [ ] All packages follow `com.axelor.apps.[module].web` pattern
- [ ] All method names follow camelCase convention
- [ ] No duplicate controller/method combinations
- [ ] All referenced view files exist

## Integration with Java Generator

This skill output should be used by the `java-agent` agent:

1. **Input:** Architecture specification + View files
2. **Run this skill:** Extract controller methods
3. **Generate controllers:** Use extracted methods to create controller classes
4. **Implement methods:** Follow controller patterns from `@docs/java/controller-patterns.md`

## Common Controller Method Patterns

Based on extracted method purposes:

| Purpose Pattern | Method Signature Example | Common Use Case |
|----------------|-------------------------|-----------------|
| `validate-*` | `validateOrder(ActionRequest, ActionResponse)` | Validation logic |
| `compute-*` | `computeTotalAmount(ActionRequest, ActionResponse)` | Calculation logic |
| `check-*` | `checkPermissions(ActionRequest, ActionResponse)` | Authorization checks |
| `generate-*` | `generateReport(ActionRequest, ActionResponse)` | Document generation |
| `send-*` | `sendNotification(ActionRequest, ActionResponse)` | Communication actions |
| `confirm-*` | `confirmOrder(ActionRequest, ActionResponse)` | Status transitions |
| `cancel-*` | `cancelOrder(ActionRequest, ActionResponse)` | Cancellation logic |
| `import-*` | `importData(ActionRequest, ActionResponse)` | Data import |
| `export-*` | `exportData(ActionRequest, ActionResponse)` | Data export |

## Output for Automation

For programmatic consumption, also provide JSON format:

```json
{
  "summary": {
    "totalActionMethods": 3,
    "totalControllers": 2,
    "totalMethods": 3
  },
  "controllers": [
    {
      "className": "ProjectController",
      "fullClassName": "com.axelor.apps.project.web.ProjectController",
      "package": "com.axelor.apps.project",
      "domain": "Project",
      "module": "project",
      "methods": [
        {
          "methodName": "validateProject",
          "actionName": "action-project-method-validate",
          "purpose": "validate",
          "sourceView": "src/main/resources/views/project-view.xml"
        }
      ]
    }
  ]
}
```

## Usage

```bash
# Invoke this skill in Claude Code
# It will automatically scan views and generate the report
```

The agent will:
1. Find all view XML files
2. Extract action-method elements
3. Parse controller and method information
4. Generate structured report
5. Provide recommendations for Java generator
