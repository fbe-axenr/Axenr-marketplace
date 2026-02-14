# Axelor View Semantic Validation Rules

## 1. Field Existence Validation

### Rule
Every `<field name="X">` must exist in the domain model.

### Process
1. Extract `model` attribute from view
2. Locate domain XML
3. Build field index
4. Verify each field name

### Examples

**Valid:**
```xml
<form model="com.axelor.apps.project.db.Project">
  <field name="name"/>  <!-- OK -->
</form>
```

**Invalid:**
```xml
<form model="com.axelor.apps.project.db.Project">
  <field name="nonExistent"/>  <!-- ERROR -->
</form>
```

## 2. Action Existence Validation

### Rule
Actions in onClick/onChange must be defined.

### Process
1. Scan all view XMLs to build action index
2. Verify each action reference exists
3. Handle comma-separated lists

### Special Cases
- `save`: Built-in, always valid
- Comma-separated: Each validated separately

## 3. Widget Compatibility

### Widget-Type Matrix

| Widget | Compatible Types | Use Case |
|--------|------------------|----------|
| progress | decimal, integer | Progress bars |
| slider | decimal, integer | Numeric sliders |
| html | string | Rich text editor |
| nav-select | integer, string | Status navigation |
| tag-select | many-to-many, one-to-many | Tag chips |
| toggle | boolean | Toggle switch |

### Example

**Valid:**
```xml
<field name="progress" widget="progress"/>  <!-- decimal -->
```

**Invalid:**
```xml
<field name="description" widget="progress"/>  <!-- string -->
```

## 4. Best Practices

### Grid orderBy
```xml
<!-- Warning -->
<grid name="project-grid">
</grid>

<!-- Recommended -->
<grid name="project-grid" orderBy="code,name">
</grid>
```

### One-to-Many panel-related
```xml
<!-- Suboptimal -->
<field name="orderLines"/>

<!-- Recommended -->
<panel-related field="orderLines" colSpan="12" orderBy="sequence">
</panel-related>
```

## 5. Dummy Fields

Dummy fields (prefix `$`) excluded from validation:
```xml
<field name="$searchText"/>  <!-- OK: dummy field -->
```

## 6. Cross-File Scope

### Entity Index
- Scans: `domains/*.xml`
- Extracts: entity + fields
- O(1) lookups

### Action Index
- Scans: `views/*.xml`
- Extracts: all `<action-*>` elements
- Maps: action name → file path

## Summary

**Complementary with XSD**:
- XSD: Element/attribute validity
- Semantic: Cross-file coherence, widget compatibility, best practices

**0% redundancy** between validators.
