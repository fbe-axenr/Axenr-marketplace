# Form Layout Patterns from Axelor Open Suite

Real-world form layout patterns extracted from Axelor Open Suite (AOS) codebase.

## Table of Contents

1. [Master-Detail Layout](#master-detail-layout)
2. [Sidebar Status Layout](#sidebar-status-layout)
3. [Tabbed Layout with Dashlets](#tabbed-layout-with-dashlets)
4. [Modular Panel Layout](#modular-panel-layout)
5. [Dashboard Form Layout](#dashboard-form-layout)
6. [Wizard Form Layout](#wizard-form-layout)
7. [Configuration Form Layout](#configuration-form-layout)

---

## Master-Detail Layout

**Use Case:** Forms with main information in left column and status/actions in right sidebar.

**Pattern from AOS Project:**

```xml
<form name="project-form" model="com.axelor.apps.project.db.Project"
      width="large" onNew="action-group-project-onnew"
      onLoad="action-group-project-onload" onSave="action-group-project-onsave">

  <!-- Toolbar for primary actions -->
  <toolbar>
    <button name="finishBtn" title="Finish" icon="check-circle"
            showIf="id &amp;&amp; !projectStatus.isCompleted"
            onClick="action-group-project-finish-project"/>
    <button name="cancelBtn" title="Cancel" css="btn-danger"
            hideIf="projectStatus.id == $canceledProjectStatusId || !id"
            icon="x-circle"
            onClick="action-group-project-status-canceled"/>
  </toolbar>

  <!-- Menubar for grouped actions -->
  <menubar>
    <menu name="taskMenu" title="Tasks" showTitle="true" icon="fa-tasks">
      <item name="myOpenTasks" title="My open tasks"
            action="save,action-project-method-my-open-tasks"
            showIf="id &amp;&amp; taskStatusManagementSelect != 1"/>
      <item name="allTasks" title="All tasks"
            action="save,action-project-method-all-tasks" showIf="id"/>
      <divider/>
      <item name="allTasksTree" title="All tasks (tree)"
            action="save,action-view-show-project-task-tree" showIf="id"/>
    </menu>

    <menu name="projectToolsMenu" title="Tools" showTitle="true" icon="fa-wrench">
      <item name="ganttItem" title="Gantt" showIf="id &amp;&amp; isShowGantt"
            action="save,action-project-open-gantt"/>
      <item name="calendarItem" title="Calendar"
            action="save,action-project-view-calendar" showIf="id"/>
    </menu>
  </menubar>

  <!-- Main panel (8 columns) -->
  <panel name="mainPanel" colSpan="8">
    <!-- Use panel-include for modular structure -->
    <panel-include view="incl-information-panel-form"/>
    <panel-include view="incl-project-overview-panel-form"/>

    <panel-tabs name="mainPanelTab">
      <panel name="taskPanel" title="Tasks">
        <panel-dashlet name="projectTaskDashletPanel" title="Tasks"
                       x-show-bars="true" canSearch="true"
                       action="action-project-dashlet-project-task"/>
      </panel>

      <panel-include view="incl-wiki-panel-form"/>
      <panel-include view="incl-checklist-panel-form"/>
      <panel-include view="incl-log-times-panel-form"/>

      <panel name="planningPanel" title="Planning"
             if="__config__.app.isApp('employee')"
             onTabSelect="action-project-dashboard-method-load-planned-time-chart">
        <!-- Dashlet content -->
      </panel>
    </panel-tabs>
  </panel>

  <!-- Sidebar (4 columns) -->
  <panel name="sidebarPanel" sidebar="true" colSpan="4">
    <field name="statusSelect" widget="NavSelect" showTitle="false"
           selection="project.project.status.select" colSpan="12"/>
    <field name="projectStatus" showTitle="false" colSpan="12"
           onSelect="action-project-attrs-project-status-domain"/>

    <panel name="actionsPanel" colSpan="12">
      <button name="seeProjectDashBoardBtn" title="Dashboard"
              onClick="save,action-project-method-see-my-project"
              showIf="id" colSpan="12"/>
      <button name="showPlanningBtn" title="Planning"
              onClick="save,action-project-view-planning"
              showIf="id" colSpan="12"/>
    </panel>

    <field name="company" required="true" canEdit="false" colSpan="12"
           form-view="company-form" grid-view="company-grid"/>
    <field name="clientPartner" domain="self.isCustomer = true"
           form-view="partner-form" grid-view="partner-grid"
           onChange="action-project-record-client-partner-onchange"
           colSpan="12"/>
    <field name="assignedTo" colSpan="12"
           onChange="action-project-record-assigned-to-onchange"/>

    <panel name="datesPanel" title="Dates" colSpan="12">
      <field name="fromDate" colSpan="12"/>
      <field name="toDate" colSpan="12"/>
    </panel>
  </panel>

  <!-- Mail panel at the end -->
  <panel-mail name="mailPanel">
    <mail-messages limit="4"/>
    <mail-followers/>
  </panel-mail>

</form>
```

**Key Features:**
- Main content in 8-column left panel
- Sidebar with status widget and quick info in 4-column right panel
- Toolbar for primary actions
- Menubar for grouped actions
- Panel-tabs for organizing related information
- Panel-include for modular, reusable sections
- Mail panel at the very end

---

## Sidebar Status Layout

**Use Case:** Forms where status is prominently displayed in sidebar with navigation-style widget.

**Pattern:**

```xml
<panel name="sidebarPanel" sidebar="true" colSpan="4">
  <!-- Status with NavSelect widget (no title) -->
  <field name="statusSelect" widget="NavSelect" showTitle="false"
         selection="order.status.select" colSpan="12"
         x-order="sequence"/>

  <!-- Related status field (detailed selection) -->
  <field name="orderStatus" showTitle="false" colSpan="12"
         form-view="order-status-form" grid-view="order-status-grid"
         onSelect="action-order-attrs-order-status-domain"/>

  <!-- Key information fields -->
  <field name="company" required="true" colSpan="12"/>
  <field name="orderDate" colSpan="12"/>
  <field name="expectedDate" colSpan="12"/>

  <!-- Collapsible panel for additional info -->
  <panel name="additionalInfoPanel" title="Additional Information"
         canCollapse="true" collapseIf="true" colSpan="12">
    <field name="notes" colSpan="12"/>
  </panel>
</panel>
```

**Guidelines:**
- Always use `widget="NavSelect"` for main status
- Always use `showTitle="false"` on NavSelect
- Always use `colSpan="12"` for all fields in sidebar
- Use `x-order="sequence"` to control status ordering
- Secondary status field can have title

---

## Tabbed Layout with Dashlets

**Use Case:** Forms with multiple sections organized in tabs, some containing embedded dashlets.

**Pattern:**

```xml
<panel-tabs name="mainPanelTab">
  <!-- Overview tab with dashboard -->
  <panel name="overviewPanel" title="Overview"
         onTabSelect="action-project-dashboard-method-on-new">
    <field name="description" colSpan="12" widget="html"/>
    <panel-include view="project-dashboard-form"/>
    <panel-include view="project-activity-dashboard-form"/>
  </panel>

  <!-- Tasks tab with dashlet -->
  <panel name="taskPanel" title="Tasks">
    <panel-dashlet name="projectTaskDashletPanel" title="Tasks"
                   action="action-project-dashlet-project-task"
                   canSearch="true" x-show-bars="true"
                   colSpan="12" height="350"/>
  </panel>

  <!-- Related records tab -->
  <panel name="resourcePanel" title="Resources">
    <panel-related name="resourceBookingListPanel"
                   field="resourceBookingList"
                   form-view="resource-booking-form"
                   grid-view="resource-booking-grid"
                   colSpan="12"/>
  </panel>

  <!-- Timesheets tab (conditional) -->
  <panel name="timesheetPanel" title="Timesheets"
         if="__config__.app.isApp('timesheet')"
         if-module="axelor-human-resource">
    <panel-dashlet name="validatedTimesheetsPanel"
                   title="Validated timesheets"
                   action="action-project-dashlet-validated-timesheet-line"
                   x-show-bars="true" canSearch="true"/>
  </panel>

  <!-- Documents tab -->
  <panel name="documentsPanel" title="Documents"
         onTabSelect="action-load-documents">
    <field name="$documents" showTitle="false" colSpan="12">
      <viewer><![CDATA[
        <>
          <h:DocumentList documents={$documents}/>
        </>
      ]]></viewer>
    </field>
  </panel>
</panel-tabs>
```

**Guidelines:**
- Use `onTabSelect` for lazy loading tab content
- Use `panel-dashlet` with `canSearch="true"` for embedded grids
- Always set `x-show-bars="true"` on dashlets for navigation
- Use `colSpan="12"` for full-width dashlets
- Use `if` and `if-module` for conditional tabs
- Height can be set as percentage or pixels: `height="350"` or `height="200%"`

---

## Modular Panel Layout

**Use Case:** Breaking down complex forms into reusable panel modules.

**Main Form:**

```xml
<form name="project-form" model="com.axelor.apps.project.db.Project">
  <panel name="mainPanel" colSpan="12">
    <!-- Include modular panels -->
    <panel-include view="incl-information-panel-form"/>
    <panel-include view="incl-project-overview-panel-form"/>
    <panel-include view="incl-project-config-panel-form"/>
  </panel>

  <panel-tabs>
    <panel-include view="incl-wiki-panel-form"/>
    <panel-include view="incl-checklist-panel-form"/>
    <panel-include view="incl-log-times-panel-form" if-module="axelor-human-resource"/>
  </panel-tabs>
</form>
```

**Reusable Panel Definition:**

```xml
<!-- incl-information-panel-form.xml -->
<form name="incl-information-panel-form" title="Information"
      model="com.axelor.apps.project.db.Project">
  <panel name="informationPanel">
    <!-- Full name with inline editor -->
    <field name="fullName" showTitle="false" colSpan="12"
           css="label-bold bold large">
      <editor x-show-titles="false">
        <field name="code" showTitle="false" colSpan="3"
               css="label-bold bold large"
               x-bind="{{code|unaccent|uppercase}}"/>
        <field name="name" showTitle="false" colSpan="6"
               css="label-bold bold large"/>
      </editor>
    </field>

    <field name="company" colSpan="4"/>
    <field name="projectTypeSelect" colSpan="4"/>
    <field name="categorySelect" colSpan="4"/>
  </panel>
</form>
```

**Naming Convention:**
```
incl-{section}-panel-form     → Reusable form panel
incl-{section}-panel-grid     → Reusable grid panel (rare)
```

**Guidelines:**
- Prefix reusable panels with `incl-`
- Each panel should be self-contained
- Include model attribute in reusable panel definition
- Use for sections reused across multiple forms
- Use for complex forms to improve maintainability

---

## Dashboard Form Layout

**Use Case:** Forms that display dashboard information with custom viewers and interactive elements.

**Pattern:**

```xml
<form name="project-dashboard-form" title="Project dashboard"
      model="com.axelor.utils.db.Wizard"
      onNew="action-project-dashboard-method-on-new"
      width="large" canNew="false" canEdit="false" canDelete="false">

  <panel name="overviewPanel" title="Dashboard" readonly="true"
         colSpan="12" canCollapse="true">

    <!-- Task tracking with custom viewer -->
    <panel name="issueTrackingPanel" title="Task tracking" icon="fa-sticky-note">
      <field name="$categoryList" showTitle="false" hideIf="$categoryList.length == 0">
        <viewer><![CDATA[
          <>
            <Table striped>
              <TableHead>
                <TableRow>
                  <TableCell as="th"></TableCell>
                  <TableCell as="th">{_t('Open')}</TableCell>
                  <TableCell as="th">{_t('Closed')}</TableCell>
                  <TableCell as="th">{_t('Total')}</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {$categoryList.map((item,index) => (
                  <TableRow key={item.categoryId}>
                    <TableCell>
                      <Button variant="link"
                              onClick={() => $execute("action-view-tasks", {categoryId: item.categoryId})}>
                        {item.categoryName}
                      </Button>
                    </TableCell>
                    <TableCell>{item.open}</TableCell>
                    <TableCell>{item.closed}</TableCell>
                    <TableCell>{item.total}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </>
        ]]></viewer>
      </field>
    </panel>

    <!-- Members list with custom viewer -->
    <panel name="membersPanel" title="Members" icon="fa-users"
           hideIf="$membersList.length == 0">
      <field name="$membersList" showTitle="false">
        <viewer><![CDATA[
          <>
            {$membersList.map((item, index) => (
              <span key={index}>
                <Button variant="link" p={0}
                        onClick={() => $execute("action-view-user", {userId: item.id})}>
                  {item.name}
                </Button>
              </span>
            )).reduce((prev, curr) => prev ? [prev, ', ', curr] : [curr],'')}
          </>
        ]]></viewer>
      </field>
    </panel>

    <!-- Spent time panel -->
    <panel name="spentTimePanel" title="Spent time" icon="fa-clock-o"
           if="__config__.app.isApp('timesheet')"
           if-module="axelor-human-resource"
           hideIf="$spentTime == 0">
      <field name="$spentTime" showTitle="false" colSpan="12">
        <viewer><![CDATA[
          <>
            <p>{$spentTime} <span>{_t('hours')}</span></p>
            <Box/>
            <Button variant="link" p={0}
                    onClick={() => $execute("action-log-time")}>
              {_t('Log time')}
            </Button> |
            <Button variant="link" p={0}
                    onClick={() => $execute("action-view-details")}>
              {_t('Details')}
            </Button>
          </>
        ]]></viewer>
      </field>
    </panel>

    <!-- Hidden fields for context -->
    <field name="$projectId" hidden="true"/>
  </panel>
</form>
```

**Guidelines:**
- Use `model="com.axelor.utils.db.Wizard"` for dashboard forms without persistence
- Set `canNew="false" canEdit="false" canDelete="false"`
- Use dummy fields (prefixed with `$`) for dashboard data
- Use custom viewers for interactive display
- Use `hideIf` based on data availability
- Include hidden fields for passing context to actions
- Use `readonly="true"` on main panel

---

## Wizard Form Layout

**Use Case:** Multi-step processes or configuration wizards.

**Pattern:**

```xml
<form name="import-wizard-form" title="Import Wizard"
      model="com.axelor.apps.base.db.ImportWizard"
      onNew="action-wizard-defaults" width="large">

  <panel name="mainPanel" colSpan="12">
    <!-- Step indicator -->
    <field name="$currentStep" readonly="true" showTitle="false" colSpan="12">
      <viewer><![CDATA[
        <>
          <Box d="flex" justifyContent="center" mb={3}>
            <Badge bg={$currentStep >= 1 ? "primary" : "secondary"}>1. Select File</Badge>
            <Box mx={2}>→</Box>
            <Badge bg={$currentStep >= 2 ? "primary" : "secondary"}>2. Configure</Badge>
            <Box mx={2}>→</Box>
            <Badge bg={$currentStep >= 3 ? "primary" : "secondary"}>3. Import</Badge>
          </Box>
        </>
      ]]></viewer>
    </field>

    <!-- Step 1: File selection -->
    <panel name="step1Panel" title="Step 1: Select File"
           showIf="$currentStep == 1" colSpan="12">
      <field name="dataFile" widget="binary" colSpan="12"
             onChange="action-wizard-method-analyze-file"/>
      <field name="$fileInfo" readonly="true" showTitle="false" colSpan="12"/>
    </panel>

    <!-- Step 2: Configuration -->
    <panel name="step2Panel" title="Step 2: Configuration"
           showIf="$currentStep == 2" colSpan="12">
      <field name="importType" selection="import.type.select" colSpan="6"/>
      <field name="encoding" colSpan="6"/>
      <field name="separator" colSpan="6"/>
      <!-- More configuration fields -->
    </panel>

    <!-- Step 3: Import -->
    <panel name="step3Panel" title="Step 3: Import"
           showIf="$currentStep == 3" colSpan="12">
      <field name="$previewData" showTitle="false" colSpan="12">
        <viewer><![CDATA[
          <><h:PreviewTable data={$previewData}/></>
        ]]></viewer>
      </field>
    </panel>

    <!-- Navigation buttons -->
    <panel name="navigationPanel" colSpan="12">
      <button name="btnPrevious" title="Previous"
              onClick="action-wizard-method-previous"
              showIf="$currentStep > 1" colSpan="4"/>
      <button name="btnNext" title="Next"
              onClick="action-wizard-method-next"
              showIf="$currentStep &lt; 3" colSpan="4"/>
      <button name="btnImport" title="Import" css="btn-success"
              onClick="action-wizard-method-import"
              showIf="$currentStep == 3" colSpan="4"/>
    </panel>
  </panel>
</form>
```

**Guidelines:**
- Use dummy field `$currentStep` to track progress
- Use `showIf` to display only current step
- Provide clear step indicators (visual progress)
- Include navigation buttons (Previous, Next, Finish)
- Validate before allowing next step
- Use `width="large"` for better UX

---

## Configuration Form Layout

**Use Case:** Application or module configuration screens.

**Pattern:**

```xml
<form name="project-config-form" title="Project Configuration"
      model="com.axelor.apps.project.db.ProjectConfig"
      onLoad="action-project-config-load">

  <panel name="mainPanel" colSpan="12">
    <!-- General settings panel -->
    <panel name="generalPanel" title="General Settings" colSpan="12">
      <field name="company" required="true" colSpan="12"
             onChange="action-project-config-company-change"/>

      <field name="isManageMultiCompany" widget="inline-checkbox" colSpan="12"
             onChange="action-project-config-attrs-multi-company"/>

      <field name="enableTaskStatusManagement" widget="boolean-switch" colSpan="6"/>
      <field name="enableAutoTaskNumbering" widget="boolean-switch" colSpan="6"/>
    </panel>

    <!-- Task management panel -->
    <panel name="taskPanel" title="Task Management" colSpan="12"
           showIf="enableTaskStatusManagement">
      <field name="taskStatusManagementSelect" widget="RadioSelect"
             selection="task.status.management.select" colSpan="12"
             onChange="action-project-config-record-status-management"/>

      <panel-related name="projectTaskStatusSetPanel"
                     field="projectTaskStatusSet"
                     showIf="taskStatusManagementSelect == 2"
                     widget="TagSelect" colSpan="12"
                     form-view="task-status-form" grid-view="task-status-grid"/>

      <field name="completedTaskStatus" colSpan="6"
             showIf="taskStatusManagementSelect != 1"/>
      <field name="canceledTaskStatus" colSpan="6"
             showIf="taskStatusManagementSelect != 1"/>
    </panel>

    <!-- Integration panel (conditional) -->
    <panel name="integrationPanel" title="Integrations" colSpan="12"
           if-module="axelor-project-dms">
      <field name="enableDms" widget="boolean-switch" colSpan="12"/>
      <field name="dmsFolder" showIf="enableDms" colSpan="12"/>
    </panel>

    <!-- Default values panel -->
    <panel name="defaultsPanel" title="Default Values" colSpan="12">
      <field name="defaultProjectStatus" colSpan="6"/>
      <field name="defaultTaskStatus" colSpan="6"/>
      <field name="defaultPriority" colSpan="6"/>
    </panel>
  </panel>
</form>
```

**Guidelines:**
- Group settings by category in separate panels
- Use `widget="boolean-switch"` for enable/disable settings
- Use `widget="inline-checkbox"` for compact boolean options
- Use `widget="RadioSelect"` for important choices (2-5 options)
- Use `showIf` to display conditional configuration
- Use `if-module` for module-specific settings
- Always specify `required="true"` for company field

---

## Common Layout Elements

### Full-Width Header Field

Pattern for prominent title/name field at top of form:

```xml
<field name="fullName" showTitle="false" colSpan="12"
       css="label-bold bold large">
  <editor x-show-titles="false">
    <field name="code" showTitle="false" colSpan="3"
           css="label-bold bold large"
           x-bind="{{code|unaccent|uppercase}}"/>
    <field name="name" showTitle="false" colSpan="6"
           css="label-bold bold large"/>
  </editor>
</field>
```

### Collapsible Detail Panel

Pattern for optional details that can be hidden:

```xml
<panel name="detailsPanel" title="Additional Details"
       canCollapse="true" collapseIf="true" colSpan="12">
  <field name="notes" widget="text-area" colSpan="12"/>
  <field name="reference" colSpan="6"/>
  <field name="externalRef" colSpan="6"/>
</panel>
```

### Action Button Panel

Pattern for grouping related action buttons:

```xml
<panel name="actionsPanel" title="Actions" colSpan="12">
  <button name="btnGenerate" title="Generate Report"
          onClick="action-generate-report"
          showIf="id" colSpan="6"/>
  <button name="btnExport" title="Export Data"
          onClick="action-export-data"
          showIf="id" colSpan="6"/>
</panel>
```

---

## Layout Grid System

Axelor uses a 12-column grid system:

```
colSpan="12"  → Full width (100%)
colSpan="6"   → Half width (50%)
colSpan="4"   → One third (33.33%)
colSpan="3"   → One quarter (25%)
colSpan="8"   → Two thirds (66.67%)
colSpan="9"   → Three quarters (75%)
```

**Common Combinations:**
- Main + Sidebar: `colSpan="8"` + `sidebar colSpan="4"`
- Two columns: `colSpan="6"` + `colSpan="6"`
- Three columns: `colSpan="4"` + `colSpan="4"` + `colSpan="4"`

---

## Best Practices Summary

1. **Use modular panels** (panel-include) for complex forms
2. **Main content left, status right** (8-4 column split)
3. **Use NavSelect for status** in sidebar with `showTitle="false"`
4. **Always colSpan="12"** for all fields in sidebar
5. **Group actions in toolbar/menubar** at top of form
6. **Use panel-tabs** for organizing multiple sections
7. **Use panel-dashlet** for embedded grids with `x-show-bars="true"`
8. **Place panel-mail at the very end** of form definition
9. **Use icons** on panels (`icon="fa-users"`)
10. **Use canCollapse for optional panels** with `collapseIf`
11. **Use onTabSelect** for lazy loading expensive tab content
12. **Use dummy fields** (`$fieldName`) for computed/display-only data
13. **Use if-module** for module-specific functionality
14. **Follow AOS naming conventions** for consistency

These patterns are observed in production-level Axelor applications and represent best practices for creating maintainable, user-friendly forms.
