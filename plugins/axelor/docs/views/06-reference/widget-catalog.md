# Axelor Widget Catalog

Complete reference of all widgets available in Axelor views with their attributes and usage examples.

## Table of Contents

1. [Text Input Widgets](#text-input-widgets)
2. [Numeric Widgets](#numeric-widgets)
3. [Date/Time Widgets](#datetime-widgets)
4. [Boolean Widgets](#boolean-widgets)
5. [Selection Widgets](#selection-widgets)
6. [Relational Widgets](#relational-widgets)
7. [Binary Widgets](#binary-widgets)
8. [Special Widgets](#special-widgets)
9. [Layout Widgets](#layout-widgets)

---

## Text Input Widgets

### Standard Text Input

**Widget:** `text` (default)

**Usage:**
```xml
<field name="name"/>
<field name="firstName" placeholder="Enter first name"/>
```

**Attributes:**
- `placeholder`: Placeholder text
- `pattern`: Regex validation pattern
- `maxlength`: Maximum character length

---

### Text Area

**Widget:** `text-area`

**Usage:**
```xml
<field name="notes" widget="text-area" height="5"/>
<field name="description" widget="text-area" colSpan="12"/>
```

**Attributes:**
- `height`: Number of rows (default: 3)
- `maxlength`: Maximum character length

---

### HTML Editor

**Widget:** `html`

**Usage:**
```xml
<field name="description" widget="html" colSpan="12"/>
<field name="content" widget="html" height="400"/>
```

**Attributes:**
- `height`: Editor height in pixels
- `colSpan`: Recommended 12 for full width

**Best Practices:**
- Always use colSpan="12" for HTML editors
- Suitable for rich text content (formatting, lists, links)

---

### Email

**Widget:** `email`

**Usage:**
```xml
<field name="email" widget="email"/>
<field name="contactEmail" widget="email" required="true"/>
```

**Features:**
- Automatic email validation
- Clickable mailto: link in readonly mode

---

### URL

**Widget:** `url`

**Usage:**
```xml
<field name="website" widget="url"/>
<field name="linkedinProfile" widget="url" placeholder="https://"/>
```

**Features:**
- URL validation
- Clickable link in readonly mode

---

### Phone

**Widget:** `phone`

**Usage:**
```xml
<field name="phone" widget="phone"/>
<field name="mobile" widget="phone"/>
```

**Features:**
- Phone number formatting
- Clickable tel: link in readonly mode

---

### Password

**Widget:** `password`

**Usage:**
```xml
<field name="password" widget="password"/>
<field name="confirmPassword" widget="password"/>
```

**Features:**
- Masked input
- Never displayed in readonly mode

---

### Code Editor

**Widget:** `code-editor`

**Usage:**
```xml
<field name="script" widget="code-editor" x-code-syntax="javascript"/>
<field name="query" widget="code-editor" x-code-syntax="sql"/>
<field name="template" widget="code-editor" x-code-syntax="html"/>
```

**X-Attributes:**
- `x-code-syntax`: Language for syntax highlighting
  - `javascript`, `java`, `python`, `sql`, `xml`, `html`, `css`, `json`

---

## Numeric Widgets

### Integer

**Widget:** (default for integer fields)

**Usage:**
```xml
<field name="quantity"/>
<field name="stock" min="0" max="999999"/>
```

**Attributes:**
- `min`: Minimum value
- `max`: Maximum value

---

### Decimal

**Widget:** (default for decimal fields)

**Usage:**
```xml
<field name="price" x-scale="2"/>
<field name="amount" precision="20" scale="2"/>
```

**Attributes:**
- `precision`: Total number of digits (default: 18)
- `scale`: Number of decimal places (default: 2)
- `x-scale`: Alias for scale

---

### Duration

**Widget:** `duration`

**Usage:**
```xml
<field name="duration" widget="duration"/>
<field name="timeSpent" widget="duration"/>
```

**Features:**
- Stores value as integer (seconds)
- Displays as HH:MM format
- Input supports: "2h30m", "150m", "2:30", "02:30:00"

---

### Progress

**Widget:** `progress`

**Usage:**
```xml
<field name="completion" widget="progress" min="0" max="100"/>
<field name="taskProgress" widget="progress" readonly="true"/>
```

**Features:**
- Visual progress bar
- Value typically 0-100
- Usually readonly (computed)

---

### Slider

**Widget:** `Slider`

**Usage:**
```xml
<field name="progress" widget="Slider" x-step="1" x-scale="0"
       min="0" max="100"/>
<field name="priority" widget="Slider" min="1" max="5" x-step="1"/>
```

**X-Attributes:**
- `x-step`: Step increment (default: 1)
- `x-scale`: Decimal places (default: 0)

**Attributes:**
- `min`: Minimum value (required)
- `max`: Maximum value (required)

---

### Rating

**Widget:** `rating`

**Usage:**
```xml
<field name="rating" widget="rating" max="5"/>
<field name="satisfaction" widget="rating" max="10"/>
```

**Attributes:**
- `max`: Maximum rating (number of stars)

---

## Date/Time Widgets

### Date

**Widget:** `date` (default for date fields)

**Usage:**
```xml
<field name="orderDate"/>
<field name="startDate" onChange="action-compute-end-date"/>
```

**Features:**
- Date picker calendar
- Format based on user locale

---

### DateTime

**Widget:** `datetime` (default for datetime fields)

**Usage:**
```xml
<field name="createdOn" readonly="true"/>
<field name="scheduledAt" widget="datetime"/>
```

**Features:**
- Date and time picker
- Format based on user locale
- Timezone aware

---

### Time

**Widget:** `time`

**Usage:**
```xml
<field name="startTime" widget="time"/>
<field name="endTime" widget="time"/>
```

**Features:**
- Time picker (hours:minutes)
- 24-hour or 12-hour format based on locale

---

## Boolean Widgets

### Checkbox

**Widget:** (default for boolean fields)

**Usage:**
```xml
<field name="active"/>
<field name="isCustomer" title="Is customer?"/>
```

**Features:**
- Standard checkbox
- True/false values

---

### Boolean Switch

**Widget:** `boolean-switch`

**Usage:**
```xml
<field name="active" widget="boolean-switch"/>
<field name="isPublic" widget="boolean-switch" onChange="action-update-visibility"/>
```

**Features:**
- Toggle switch UI
- More modern appearance than checkbox

---

### Boolean Radio

**Widget:** `boolean-radio`

**Usage:**
```xml
<field name="active" widget="boolean-radio"/>
```

**Features:**
- Radio buttons for Yes/No
- More explicit than checkbox

---

### Inline Checkbox

**Widget:** `inline-checkbox` or `InlineCheckbox`

**Usage:**
```xml
<field name="isActive" widget="InlineCheckbox"/>
<field name="manageTimeSpent" widget="inline-checkbox"
       onChange="action-project-record-manage-timespent"/>
```

**Features:**
- Checkbox displayed inline with label
- Used in AOS for compact layouts

---

### Toggle (for O2M editors)

**Widget:** `toggle`

**Usage:**
```xml
<field name="emails">
  <editor layout="table">
    <field name="email"/>
    <field name="primary" widget="toggle" x-icon="star"
           x-icon-active="star-fill" x-exclusive="true"/>
    <field name="optOut" widget="toggle" x-icon="ban"/>
  </editor>
</field>
```

**X-Attributes:**
- `x-icon`: Icon when false (Bootstrap Icons)
- `x-icon-active`: Icon when true
- `x-exclusive`: Only one can be true in the list

**Best Practice:**
- Only use in O2M editors with `layout="table"`

---

## Selection Widgets

### Standard Selection

**Widget:** `selection` (default for selection fields)

**Usage:**
```xml
<field name="statusSelect" selection="order.status.select"/>
<field name="type" selection="product.type.select" required="true"/>
```

**Features:**
- Dropdown select
- Single selection

---

### Nav Select

**Widget:** `NavSelect` or `nav-select`

**Usage:**
```xml
<field name="statusSelect" widget="NavSelect" showTitle="false"
       selection="project.status.selection" x-order="sequence"/>
<field name="priority" widget="nav-select" selection="priority.selection"/>
```

**X-Attributes:**
- `x-order`: Field name for ordering options (e.g., "sequence")

**Attributes:**
- `showIcons`: Show icons if defined in selection

**Features:**
- Navigation-style pills/badges
- Visual status indicator
- Commonly used for status fields in sidebar

---

### Single Select

**Widget:** `single-select`

**Usage:**
```xml
<field name="category" widget="single-select" selection="category.select"/>
```

**Features:**
- Dropdown with search capability
- Better for long selection lists

---

### Radio Select

**Widget:** `RadioSelect`

**Usage:**
```xml
<field name="taskStatusManagementSelect" widget="RadioSelect"
       selection="task.status.management.select" colSpan="12"/>
<field name="gender" widget="RadioSelect" selection="gender.select"/>
```

**Features:**
- Radio button group
- All options visible at once
- Good for 2-5 options

---

### Multi-Select

**Widget:** `multi-select` or `MultiSelect`

**Usage:**
```xml
<field name="categories" widget="multi-select" selection="category.select"/>
<field name="$statusFilter" widget="MultiSelect"
       selection="task.status.select"/>
```

**Features:**
- Multiple selection dropdown
- Returns list of values

---

### Checkbox Select

**Widget:** `checkbox-select`

**Usage:**
```xml
<field name="features" widget="checkbox-select" selection="feature.select"/>
```

**Features:**
- Checkbox list
- Multiple selections
- All options visible

---

### Tag Select

**Widget:** `TagSelect`

**Usage:**
```xml
<!-- For many-to-many relations -->
<field name="membersUserSet" widget="TagSelect" canNew="false"
       form-view="user-form" grid-view="user-grid" canEdit="false"/>

<!-- With color field -->
<field name="tagSet" widget="TagSelect" x-color-field="color"
       form-view="tag-form" grid-view="tag-grid"
       onSelect="action-set-tag-domain"/>

<!-- For selection list -->
<field name="projectTaskStatusSet" widget="TagSelect"
       selection="task.status.select" canEdit="false"/>
```

**X-Attributes:**
- `x-color-field`: Field name for tag color (e.g., "color")

**Features:**
- Displays selected items as colored tags/chips
- Supports both selections and M2M relations
- Compact multi-select display

---

## Relational Widgets

### Many-to-One

**Widget:** (default for M2O fields)

**Usage:**
```xml
<field name="customer" domain="self.isCustomer = true"
       canNew="false" canEdit="false"
       form-view="partner-form" grid-view="partner-grid"
       onChange="action-customer-change"/>
```

**Attributes:**
- `domain`: Filter available records
- `canNew`: Allow creating new record
- `canEdit`: Allow editing selected record
- `canView`: Allow viewing selected record
- `form-view`: Custom form view
- `grid-view`: Custom grid view for selection
- `onChange`: Action on value change
- `onSelect`: Custom selection action

---

### Ref-Select

**Widget:** `ref-select`

**Usage:**
```xml
<field name="category" widget="ref-select" domain="self.active = true"/>
<field name="relatedTo" widget="ref-select"/>  <!-- polymorphic -->
```

**Features:**
- Dropdown style (instead of autocomplete)
- Better for short lists
- Supports polymorphic references

---

### Ref-Text

**Widget:** `ref-text`

**Usage:**
```xml
<field name="customer" widget="ref-text" readonly="true"/>
<field name="fullName" widget="ref-text"/>
```

**Features:**
- Read-only reference display
- Shows formatted value
- No selection capability

---

### One-to-Many / Many-to-Many

**Widget:** See panel-related and field editors

**Usage:**
```xml
<!-- Panel-related (recommended) -->
<panel-related field="orderLines" colSpan="12"
               form-view="order-line-form"
               grid-view="order-line-grid"
               editable="true"
               canNew="true" canEdit="true" canRemove="true">
  <field name="product"/>
  <field name="quantity"/>
  <field name="price"/>
</panel-related>

<!-- Inline editor -->
<field name="lines" colSpan="12">
  <editor>
    <field name="product" onChange="action-compute-price"/>
    <field name="quantity"/>
    <field name="price"/>
  </editor>
</field>
```

---

### Master-Detail

**Widget:** `master-detail`

**Usage:**
```xml
<field name="parent" widget="master-detail"/>
<panel-related field="items" widget="master-detail"/>
```

**Features:**
- Shows parent-child relationships
- Tree-like expansion

---

## Binary Widgets

### Binary

**Widget:** `binary`

**Usage:**
```xml
<field name="attachment" widget="binary"/>
<field name="document" widget="binary" accept=".pdf,.doc,.docx"/>
```

**Attributes:**
- `accept`: File type filter (MIME types or extensions)

**Features:**
- File upload
- Download button

---

### Binary Link

**Widget:** `binary-link`

**Usage:**
```xml
<field name="document" widget="binary-link"/>
<field name="report" widget="binary-link" readonly="true"/>
```

**Features:**
- Shows filename as download link
- No upload capability (readonly)

---

### Image

**Widget:** `image`

**Usage:**
```xml
<field name="photo" widget="image" height="200"/>
<field name="logo" widget="image" colSpan="12"/>
```

**Attributes:**
- `height`: Image display height in pixels

**Features:**
- Image upload with preview
- Click to enlarge
- Recommended colSpan="12"

---

## Special Widgets

### Color

**Widget:** `color`

**Usage:**
```xml
<field name="color" widget="color"/>
<field name="tagColor" widget="color" colSpan="3"/>
```

**Features:**
- Color picker
- Returns hex color value

---

### JSON Field

**Widget:** `json-field`

**Usage:**
```xml
<field name="metadata" widget="json-field" colSpan="12"/>
<field name="attrs" widget="json-field"/>
```

**Features:**
- JSON editor with validation
- Custom field manager
- Dynamic form fields

---

### Suggest Box

**Widget:** `suggest-box`

**Usage:**
```xml
<field name="search" widget="suggest-box"/>
```

**Features:**
- Autocomplete text input
- Custom suggestions via action

---

## Layout Widgets

### Spacer

**Usage:**
```xml
<spacer colSpan="6"/>
<spacer/>  <!-- Takes remaining space -->
```

**Purpose:**
- Create empty space in layout
- Align fields

---

### Separator

**Usage:**
```xml
<separator title="Address Information" colSpan="12"/>
<separator colSpan="12"/>  <!-- Line only -->
```

**Purpose:**
- Visual section divider
- Optional title text

---

### Label / Static

**Usage:**
```xml
<label title="Important Notice" colSpan="12" css="label-important"/>
<static name="helpText" colSpan="12">
  Please review all information before submitting.
</static>
```

**Purpose:**
- Display static text
- Help text
- Instructions

---

## Widget Selection Guide

### When to use what?

**Status/State Fields:**
- Use `NavSelect` for visual status indicators
- Use `RadioSelect` for 2-4 states
- Use `selection` (dropdown) for 5+ states

**Multi-Selection:**
- Use `TagSelect` for M2M relations (visual tags)
- Use `MultiSelect` for selection lists
- Use `checkbox-select` when all options should be visible

**Boolean Values:**
- Use `boolean-switch` for modern toggle appearance
- Use `inline-checkbox` for compact layouts
- Use `boolean-radio` for explicit Yes/No choice
- Use `toggle` only in O2M table editors

**Text Input:**
- Use `html` for rich formatted text
- Use `text-area` for plain multi-line text
- Use `code-editor` for code/scripts
- Use standard text input for single-line

**Relational Fields:**
- Use default M2O for autocomplete search
- Use `ref-select` for dropdown selection (short lists)
- Use `TagSelect` for M2M with visual tags
- Use `panel-related` for O2M/M2M grids

---

## Common X-Attributes Reference

| Attribute | Used With | Purpose | Example |
|-----------|-----------|---------|---------|
| `x-order` | NavSelect | Order selection options | `x-order="sequence"` |
| `x-color-field` | TagSelect | Field for tag color | `x-color-field="color"` |
| `x-icon` | Toggle | Icon when false | `x-icon="star"` |
| `x-icon-active` | Toggle | Icon when true | `x-icon-active="star-fill"` |
| `x-exclusive` | Toggle | Only one true allowed | `x-exclusive="true"` |
| `x-show-bars` | Panel-dashlet | Show navigation bars | `x-show-bars="true"` |
| `x-selector` | Panel-related, Grid | Selection type | `x-selector="checkbox"` |
| `x-tree-limit` | Panel-related | Tree depth limit | `x-tree-limit="1"` |
| `x-step` | Slider | Step increment | `x-step="5"` |
| `x-scale` | Slider, Decimal | Decimal places | `x-scale="2"` |
| `x-code-syntax` | Code Editor | Language for syntax | `x-code-syntax="javascript"` |
| `x-bind` | Field | Formatting expression | `x-bind="{{code\|uppercase}}"` |
| `x-show-titles` | Editor | Show field titles | `x-show-titles="false"` |
| `x-show-on-new` | Editor | Show on new record | `x-show-on-new="true"` |
| `x-viewer` | Editor | Treat as viewer | `x-viewer="true"` |
| `x-dirty` | Field | Dirty flag control | `x-dirty="false"` |

---

## Best Practices

1. **Always specify widget explicitly for clarity** when not using default
2. **Use colSpan="12"** for HTML editors, images, and wide content
3. **Use NavSelect** for status fields in sidebar with `showTitle="false"`
4. **Use TagSelect** for M2M relations to save space and improve UX
5. **Use RadioSelect** for important choices that should be visible
6. **Use panel-related** instead of inline O2M editors for complex grids
7. **Add x-color-field** to TagSelect for colored tags
8. **Use x-order** with NavSelect to control option ordering
9. **Use InlineCheckbox** for compact boolean fields in forms
10. **Always provide placeholder** for text inputs when meaning not obvious

---

## Widget Compatibility Matrix

| Widget | Form | Grid | Editor | Viewer |
|--------|:----:|:----:|:------:|:------:|
| text | ✓ | ✓ | ✓ | ✓ |
| text-area | ✓ | ✗ | ✓ | ✓ |
| html | ✓ | ✗ | ✗ | ✓ |
| NavSelect | ✓ | ✓ | ✗ | ✓ |
| TagSelect | ✓ | ✗ | ✗ | ✓ |
| InlineCheckbox | ✓ | ✗ | ✗ | ✓ |
| RadioSelect | ✓ | ✗ | ✗ | ✓ |
| Slider | ✓ | ✗ | ✗ | ✓ |
| toggle | ✗ | ✗ | ✓ | ✗ |
| progress | ✓ | ✓ | ✗ | ✓ |
| image | ✓ | ✓ | ✗ | ✓ |
| binary | ✓ | ✗ | ✗ | ✓ |
| binary-link | ✓ | ✓ | ✗ | ✓ |
| code-editor | ✓ | ✗ | ✗ | ✓ |
| json-field | ✓ | ✗ | ✗ | ✓ |
| duration | ✓ | ✓ | ✓ | ✓ |
| rating | ✓ | ✓ | ✗ | ✓ |
| color | ✓ | ✗ | ✗ | ✓ |

---

This comprehensive widget catalog covers all widgets found in Axelor framework and observed in AOS codebase.
