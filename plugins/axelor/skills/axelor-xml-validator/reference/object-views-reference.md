# XSD Elements Reference

This document provides a comprehensive reference of all XML elements and their available attributes.

---

## `<action>`

**Type:** `ActAction`

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`name`** (**required**)
  - Type: `string`

---

## `<action-attrs>`

**Type:** `ActionAttrs`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

- **`name`** (**required**)
  - Type: `string`
  - Action name.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only execute the action if the given module is installed.

- **`model`** (*optional*)
  - Type: `string`
  - Fully qualified name of the model object.

---

## `<action-condition>`

**Type:** `ActionCondition`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

- **`name`** (**required**)
  - Type: `string`
  - Action name.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only execute the action if the given module is installed.

- **`model`** (*optional*)
  - Type: `string`
  - Fully qualified name of the model object.

---

## `<action-export>`

**Type:** `ActionExport`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

- **`name`** (**required**)
  - Type: `string`
  - Action name.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only execute the action if the given module is installed.

- **`model`** (*optional*)
  - Type: `string`
  - Fully qualified name of the model object.

- **`attachment`** (*optional*)
  - Type: `boolean`
  - Whether to attach the exported file to current record

---

## `<action-group>`

**Type:** `ActionGroup`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

- **`name`** (**required**)
  - Type: `string`
  - Action name.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only execute the action if the given module is installed.

- **`model`** (*optional*)
  - Type: `string`
  - Fully qualified name of the model object.

---

## `<action-import>`

**Type:** `ActionImport`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

- **`name`** (**required**)
  - Type: `string`
  - Action name.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only execute the action if the given module is installed.

- **`model`** (*optional*)
  - Type: `string`
  - Fully qualified name of the model object.

- **`config`** (**required**)
  - Type: `string`
  - XML data import config file.

---

## `<action-menu>`

**Type:** `ActionMenuItem`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`name`** (**required**)
  - Type: `string`
  - The name of the menu item. It serves as an identifier.

- **`title`** (**required**)
  - Type: `string`
  - The display text of this menu item.

- **`parent`** (*optional*)
  - Type: `string`
  - The name of the parent menu item.

- **`icon`** (*optional*)
  - Type: `string`
  - The image for this menu item.

- **`icon-background`** (*optional*)
  - Type: `ColorStyle`
  - Specify icon background color (predefined or html hex color)

- **`action`** (*optional*)
  - Type: `string`
  - The name of the action to perform when this menu is clicked.

- **`order`** (*optional*)
  - Type: `string`
  - Specify menu sequence order.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`left`** (*optional*)
  - Type: `boolean`
  - Whether to show the menu item in the left navigation menu.

- **`mobile`** (*optional*)
  - Type: `boolean`
  - Whether to show the menu item in the mobile menu.

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the menu with given name.

- **`tag`** (*optional*)
  - Type: `string`
  - Specify a tag to show on menu item as a fixed label. This attribute gets preference over 'tag-count' and 'tag-get' attributes.

- **`tag-count`** (*optional*)
  - Type: `boolean`
  - Specify whether to use count of menu action records as tag.

- **`tag-get`** (*optional*)
  - Type: `string`
  - Specify a method call to get tag value. This attribute gets preference over 'tag-count' attribute. The signature of the controller method should be:<br><br> <code> void someMethod(ActionRequest request, ActionResponse response) </code>

- **`tag-style`** (*optional*)
  - Type: `LabelStyle`
  - Specify the tag display style.

- **`icon`** (*optional*)

- **`groups`** (*optional*)

- **`category`** (*optional*)
  - Type: `string`
  - Category name to group the action menus. Can be used to filter the toplevel action menus.

---

## `<action-method>`

**Type:** `ActionMethod`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

- **`name`** (**required**)
  - Type: `string`
  - Action name.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only execute the action if the given module is installed.

- **`model`** (*optional*)
  - Type: `string`
  - Fully qualified name of the model object.

---

## `<action-record>`

**Type:** `ActionRecord`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

- **`name`** (**required**)
  - Type: `string`
  - Action name.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only execute the action if the given module is installed.

- **`model`** (**required**)
  - Type: `string`
  - Fully qualified name of the model object.

- **`search`** (*optional*)
  - Type: `string`
  - Search for a record before creating new one.

- **`ref`** (*optional*)
  - Type: `string`
  - Reference to the existing record from context. This attribute gets preference over 'search' attribute if used along with 'search'.

- **`copy`** (*optional*)
  - Type: `boolean`
  - Whether to create a copy of the searched/referenced record instead of referencing it.

- **`saveIf`** (*optional*)
  - Type: `string`
  - Save the record if the given boolean expression is true and "id" is null or "version" field is provided.

---

## `<action-report>`

**Type:** `ActionReport`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

- **`name`** (**required**)
  - Type: `string`
  - Action name.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only execute the action if the given module is installed.

- **`model`** (*optional*)
  - Type: `string`
  - Fully qualified name of the model object.

- **`design`** (**required**)
  - Type: `string`
  - Specify the report design name (rptdesign)

- **`output`** (**required**)
  - Type: `string`
  - Specify the report output name

- **`format`** (*optional*)
  - Specify the output format.
  - Possible values: pdf, html, doc, xls, docx, xlsx, odt, ods

- **`attachment`** (*optional*)
  - Type: `boolean`
  - Specify whether to attach the generated report to current object

---

## `<action-script>`

**Type:** `ActionScript`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

- **`name`** (**required**)
  - Type: `string`
  - Action name.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only execute the action if the given module is installed.

- **`model`** (*optional*)
  - Type: `string`
  - Fully qualified name of the model object.

---

## `<action-validate>`

**Type:** `ActionValidate`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

- **`name`** (**required**)
  - Type: `string`
  - Action name.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only execute the action if the given module is installed.

- **`model`** (*optional*)
  - Type: `string`
  - Fully qualified name of the model object.

---

## `<action-view>`

**Type:** `ActionView`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

- **`name`** (**required**)
  - Type: `string`
  - Action name.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only execute the action if the given module is installed.

- **`model`** (*optional*)
  - Type: `string`
  - Fully qualified name of the model object.

- **`title`** (**required**)
  - Type: `string`

- **`icon`** (*optional*)
  - Type: `string`
  - Path of the image.

- **`home`** (*optional*)
  - Type: `boolean`
  - Specify whether this action can be used as home action.

---

## `<action-ws>`

**Type:** `ActionWS`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

- **`name`** (**required**)
  - Type: `string`
  - Action name.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only execute the action if the given module is installed.

- **`model`** (*optional*)
  - Type: `string`
  - Fully qualified name of the model object.

- **`service`** (**required**)
  - Type: `string`
  - Service URL or reference to another action-ws with service is set to some url. In that case, the referenced action is called prior to this one. This allows to perform some intial actions like `login`.

- **`connect-timeout`** (*optional*)
  - Type: `int`
  - Default: `30`
  - Connection timeout in seconds (default 60 seconds).

- **`read-timeout`** (*optional*)
  - Type: `int`
  - Default: `120`
  - Read timeout in seconds (default 300 seconds).

---

## `<actions>`

Define actions added on chart dashlet menu.

*No attributes*

---

## `<alert>`

**Type:** `ActMessage`

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`message`** (**required**)
  - Type: `string`
  - The message to show.

- **`action`** (*optional*)
  - Type: `string`
  - An action to be executed on error or alert message to make corrective measures, when error dialog is closed or alert dialog is canceled.

- **`title`** (*optional*)
  - Type: `string`
  - Title of the modal/notification

- **`confirm-btn-title`** (*optional*)
  - Type: `string`
  - Title of the confirm button.

- **`cancel-btn-title`** (*optional*)
  - Type: `string`
  - Title of the cancel button.

---

## `<attribute>`

**Type:** `ActAttribute`

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`for`** (**required**)
  - Type: `string`
  - Comma-separated list of field names.

- **`name`** (**required**)
  - Type: `string`
  - Name of the attribute.<br><br> Example : hidden, readonly, ...

- **`expr`** (**required**)
  - Type: `string`
  - A Groovy boolean expression against the current form values.

---

## `<button>`

**Type:** `GridButton`

### Attributes

- **`name`** (**required**)
  - Type: `string`
  - Button name.

- **`icon`** (*optional*)
  - Type: `string`
  - Specify the button icon (an image or an icon).

- **`iconHover`** (*optional*)
  - Type: `string`

- **`link`** (*optional*)
  - Type: `string`
  - If specified then the button is rendered as a link. Use empty value if you only need a link effect and perform actual action with `onClick`.

- **`prompt`** (*optional*)
  - Type: `string`
  - Show a confirmation message before performing client action.

- **`onClick`** (**required**)
  - Type: `string`
  - An action to execute on click event. The current node record is passed as context the context handler.

- **`widget`** (*optional*)
  - Type: `string`

- **`x-field`** (*optional*)

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`colSpan`** (*optional*)

- **`colOffset`** (*optional*)

- **`rowSpan`** (*optional*)

- **`rowOffset`** (*optional*)

- **`height`** (*optional*)

- **`link`** (*optional*)

---

## `<button-group>`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`
  - Container name.

---

## `<calendar>`

**Type:** `CalendarView`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing view, provide an unique id to identify current view.

- **`title`** (**required**)
  - Type: `string`
  - The display text.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`css`** (*optional*)
  - Type: `string`
  - Specify additional css class names

- **`width`** (*optional*)
  - The preferred width style of the view.<br><br> For example: <br><pre> width="mini" width="mid" width="large"</pre>
  - Pattern: `((\*|mini|mid|large)|(\d+)(%|px|em)?)((:(\d+)(px|em)?){1,2})?`

- **`helpLink`** (*optional*)
  - Type: `string`
  - Link to a web page.

- **`eventStart`** (**required**)
  - Type: `string`
  - Name of the field of type date/datetime to be used as event start time.

- **`eventStop`** (*optional*)
  - Type: `string`
  - Name of the field of type date/datetime to be used as event stop time.

- **`eventLength`** (*optional*)
  - Default: `1`
  - If eventStop is not given, the length of an event in hour (default is 1).

- **`onChange`** (*optional*)
  - Type: `string`
  - The onchange action is called when event is moved or resized in the calendar view.

- **`onDelete`** (*optional*)
  - Type: `string`
  - Comma-separated list of actions to execute on delete event.

- **`colorBy`** (*optional*)
  - Type: `string`
  - Name of the field to be used to colorize the events.

- **`mode`** (*optional*)
  - Default: `month`
  - Possible values: month, week, day

- **`canNew`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the 'New' button.

- **`canDelete`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the 'Delete' button.

---

## `<call>`

**Type:** `ActCall`

Controller method call.<br><br> The signature of the controller method should be:<br><br> <code> void someMethod(ActionRequest request, ActionResponse response) </code>

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`class`** (**required**)
  - Type: `string`
  - Target class name.

- **`method`** (**required**)
  - Type: `string`
  - Method name.

- **`if`** (*optional*)

---

## `<cards>`

**Type:** `CardsView`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing view, provide an unique id to identify current view.

- **`title`** (**required**)
  - Type: `string`
  - The display text.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`css`** (*optional*)
  - Type: `string`
  - Specify additional css class names

- **`width`** (*optional*)
  - The preferred width style of the view.<br><br> For example: <br><pre> width="mini" width="mid" width="large"</pre>
  - Pattern: `((\*|mini|mid|large)|(\d+)(%|px|em)?)((:(\d+)(px|em)?){1,2})?`

- **`helpLink`** (*optional*)
  - Type: `string`
  - Link to a web page.

- **`name`** (**required**)
  - Type: `string`
  - The name of the view.

- **`model`** (**required**)
  - Type: `string`
  - Specify the model object name.

- **`orderBy`** (*optional*)
  - Type: `string`
  - List of comma-separated field names optionally prefix with `-` to order by DESC. For example: orderBy="name,-age"

- **`canNew`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the 'New' button.

- **`canEdit`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the 'Edit' button.

- **`canDelete`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the 'Delete' button.

- **`edit-window`** (*optional*)
  - Type: `CardEditWindow`
  - Specify how to show editor window.

- **`onDelete`** (*optional*)
  - Type: `string`
  - Comma-separated list of actions to execute on delete event.

---

## `<category>`

### Attributes

- **`key`** (**required**)
  - Type: `string`

- **`title`** (*optional*)
  - Type: `string`

- **`type`** (*optional*)
  - Possible values: number, decimal, date, time, month, year, text

---

## `<chart>`

**Type:** `ChartView`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing view, provide an unique id to identify current view.

- **`title`** (**required**)
  - Type: `string`
  - The display text.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`css`** (*optional*)
  - Type: `string`
  - Specify additional css class names

- **`width`** (*optional*)
  - The preferred width style of the view.<br><br> For example: <br><pre> width="mini" width="mid" width="large"</pre>
  - Pattern: `((\*|mini|mid|large)|(\d+)(%|px|em)?)((:(\d+)(px|em)?){1,2})?`

- **`helpLink`** (*optional*)
  - Type: `string`
  - Link to a web page.

- **`name`** (**required**)
  - Type: `string`
  - The name of the view.

- **`stacked`** (*optional*)
  - Type: `boolean`

- **`onInit`** (*optional*)
  - Type: `string`
  - Call an action when chart is initialized.

---

## `<check>`

Define a check condition. The condition expression can be specified as a string value or required field condition can be defined with `field` attribute.

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`field`** (*optional*)
  - Type: `string`
  - Check whether the field value exists. If not the field is marked as required.

- **`error`** (*optional*)
  - Type: `string`
  - Specify the error message.

---

## `<column>`

Define a tree column.

### Attributes

- **`name`** (**required**)
  - Type: `string`

- **`title`** (*optional*)
  - Type: `string`

- **`type`** (*optional*)
  - Possible values: string, integer, boolean, decimal, datetime, date, enum, reference, button

- **`target`** (*optional*)
  - Type: `string`

- **`target-name`** (*optional*)
  - Type: `string`

- **`domain`** (*optional*)
  - Type: `string`

- **`selection`** (*optional*)
  - Type: `string`

- **`widget`** (*optional*)
  - Type: `string`

- **`colSpan`** (*optional*)
  - Type: `ResponsiveNumber`
  - Specify the number of columns taken by the widget.

- **`multiple`** (*optional*)
  - Type: `boolean`

- **`required`** (*optional*)
  - Type: `boolean`

- **`multiple`** (*optional*)

- **`colSpan`** (*optional*)

- **`required`** (*optional*)

---

## `<config>`

### Attributes

- **`name`** (**required**)
  - Type: `string`

- **`value`** (**required**)
  - Type: `string`

---

## `<context>`

**Type:** `ActContext`

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`name`** (**required**)
  - Type: `string`
  - Comma-separated list of field names

- **`expr`** (**required**)
  - Type: `string`
  - A Groovy boolean expression against the current form values.

- **`copy`** (*optional*)
  - Type: `boolean`
  - Use the result of `expr` by copy.

---

## `<custom>`

**Type:** `CustomView`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing view, provide an unique id to identify current view.

- **`title`** (**required**)
  - Type: `string`
  - The display text.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`css`** (*optional*)
  - Type: `string`
  - Specify additional css class names

- **`width`** (*optional*)
  - The preferred width style of the view.<br><br> For example: <br><pre> width="mini" width="mid" width="large"</pre>
  - Pattern: `((\*|mini|mid|large)|(\d+)(%|px|em)?)((:(\d+)(px|em)?){1,2})?`

- **`helpLink`** (*optional*)
  - Type: `string`
  - Link to a web page.

- **`name`** (**required**)
  - Type: `string`
  - The name of the view.

---

## `<dashboard>`

**Type:** `Dashboard`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing view, provide an unique id to identify current view.

- **`title`** (**required**)
  - Type: `string`
  - The display text.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`css`** (*optional*)
  - Type: `string`
  - Specify additional css class names

- **`width`** (*optional*)
  - The preferred width style of the view.<br><br> For example: <br><pre> width="mini" width="mid" width="large"</pre>
  - Pattern: `((\*|mini|mid|large)|(\d+)(%|px|em)?)((:(\d+)(px|em)?){1,2})?`

- **`helpLink`** (*optional*)
  - Type: `string`
  - Link to a web page.

- **`name`** (**required**)
  - Type: `string`
  - The name of the view.

- **`onInit`** (*optional*)
  - Type: `string`
  - Call an action when dashboard is initialized.

---

## `<dashlet>`

**Type:** `Dashlet`

Specify an action view as a dashlet.

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`
  - Container name.

- **`action`** (**required**)
  - Type: `string`

- **`canSearch`** (*optional*)
  - Type: `boolean`
  - Whether to enable search header (for grid views) or search box (for card views).

- **`x-show-bars`** (*optional*)
  - Type: `boolean`
  - Specify whether to show toolbar and menubar.

- **`canNew`** (*optional*)
  - Type: `string`
  - Specify whether to allow to create new record.

- **`canEdit`** (*optional*)
  - Type: `string`
  - Specify whether to allow to edit the records.

- **`canDelete`** (*optional*)
  - Type: `string`
  - Default: `false`
  - Specify whether to allow to remove the record.

---

## `<dataset>`

**Type:** `DataSet`

### Attributes

- **`type`** (**required**)
  - Possible values: jpql, sql, rpc

- **`limit`** (*optional*)
  - Type: `int`
  - Specify query result limit

---

## `<divider>`

**Type:** `MenubarMenuDivider`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`name`** (*optional*)
  - Type: `string`

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

---

## `<domain>`

**Type:** `string`

Domain for the filter.

*No attributes*

---

## `<editor>`

**Type:** `PanelEditor`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`
  - Container name.

- **`showFrame`** (*optional*)
  - Type: `boolean`
  - Default: `true`
  - Specify whether to show frame around the panel.

- **`sidebar`** (*optional*)
  - Type: `boolean`
  - Specify whether to show this panel in sidebar.

- **`stacked`** (*optional*)
  - Type: `boolean`
  - Specify whether to stack panel items.

- **`attached`** (*optional*)
  - Type: `boolean`
  - Specify whether to attach the panel with previous one.

- **`onTabSelect`** (*optional*)
  - Type: `string`
  - Specify an action to execute when the panel tab is selected (if it's top-level in panel-tabs).

- **`width`** (*optional*)

- **`layout`** (*optional*)
  - Type: `string`
  - Specify alternative layout (e.g. table)

- **`onNew`** (*optional*)
  - Type: `string`
  - Specify an onNew action

- **`x-viewer`** (*optional*)
  - Type: `boolean`
  - Specify whether to use editor as viewer

- **`x-show-titles`** (*optional*)
  - Type: `boolean`
  - Specify whether to show item titles by default

- **`x-show-on-new`** (*optional*)
  - Type: `boolean`
  - Specify whether to show editor on new record (o2m/m2m fields)

- **`depends`** (*optional*)

- **`onTabSelect`** (*optional*)

- **`sidebar`** (*optional*)

---

## `<error>`

**Type:** `ActError`

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`message`** (**required**)
  - Type: `string`
  - The message to show.

- **`action`** (*optional*)
  - Type: `string`
  - An action to be executed on error or alert message to make corrective measures, when error dialog is closed or alert dialog is canceled.

- **`title`** (*optional*)
  - Type: `string`
  - Title of the modal/notification

- **`confirm-btn-title`** (*optional*)
  - Type: `string`
  - Title of the confirm button.

- **`cancel-btn-title`** (*optional*)
  - Type: `string`
  - Title of the cancel button.

- **`cancel-btn-title`** (*optional*)
  - Type: `string`

---

## `<export>`

An export task.

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`name`** (**required**)
  - Type: `string`
  - Output file name.

- **`template`** (**required**)
  - Type: `string`
  - The template to be used to generate output file.

- **`engine`** (*optional*)
  - Possible values: ST, groovy

---

## `<extend>`

**Type:** `ExtendForm`

### Attributes

- **`target`** (**required**)
  - Type: `string`

- **`if-feature`** (*optional*)
  - Type: `string`

- **`if-module`** (*optional*)
  - Type: `string`

---

## `<field>`

**Type:** `ActField`

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`name`** (**required**)
  - Type: `string`
  - Comma-separated list of field names

- **`expr`** (**required**)
  - Type: `string`
  - A Groovy boolean expression against the current form values.

- **`copy`** (*optional*)
  - Type: `boolean`
  - Use the result of `expr` by copy.

---

## `<filter>`

**Type:** `SearchFilter`

Define a search filter.

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`name`** (*optional*)
  - Type: `string`
  - The name of the filter.

- **`title`** (**required**)
  - Type: `string`
  - The display text of the filter.

---

## `<form>`

**Type:** `NestedFormView`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing view, provide an unique id to identify current view.

- **`title`** (**required**)
  - Type: `string`
  - The display text.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`css`** (*optional*)
  - Type: `string`
  - Specify additional css class names

- **`width`** (*optional*)
  - The preferred width style of the view.<br><br> For example: <br><pre> width="mini" width="mid" width="large"</pre>
  - Pattern: `((\*|mini|mid|large)|(\d+)(%|px|em)?)((:(\d+)(px|em)?){1,2})?`

- **`helpLink`** (*optional*)
  - Type: `string`
  - Link to a web page.

- **`onLoad`** (*optional*)
  - Type: `string`
  - Comma-separated list of actions to execute on load event.

- **`onSave`** (*optional*)
  - Type: `string`
  - Comma-separated list of actions to execute on save event.

- **`onNew`** (*optional*)
  - Type: `string`
  - Comma-separated list of actions to execute on new event.

- **`onDelete`** (*optional*)
  - Type: `string`
  - Comma-separated list of actions to execute on delete event.

- **`onCopy`** (*optional*)
  - Type: `string`
  - Comma-separated list of actions to execute on copy event.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`canNew`** (*optional*)
  - Type: `string`
  - Show the 'New' button if the given JavaScript expression is true.

- **`canEdit`** (*optional*)
  - Type: `string`
  - Show the 'Edit' button if the given JavaScript expression is true.

- **`canSave`** (*optional*)
  - Type: `string`
  - Show the 'Save' button if the given JavaScript expression is true.

- **`canDelete`** (*optional*)
  - Type: `string`
  - Show the 'Delete' button if the given JavaScript expression is true.

- **`canArchive`** (*optional*)
  - Type: `string`
  - Show the 'Archive' button if the given JavaScript expression is true.

- **`canCopy`** (*optional*)
  - Type: `string`
  - Show the 'Copy' button if the given JavaScript expression is true.

- **`canAttach`** (*optional*)
  - Type: `string`
  - Show the 'Attachment' button if the given JavaScript expression is true.

- **`editable`** (*optional*)
  - Type: `boolean`

---

## `<gantt>`

**Type:** `GanttView`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing view, provide an unique id to identify current view.

- **`title`** (**required**)
  - Type: `string`
  - The display text.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`css`** (*optional*)
  - Type: `string`
  - Specify additional css class names

- **`width`** (*optional*)
  - The preferred width style of the view.<br><br> For example: <br><pre> width="mini" width="mid" width="large"</pre>
  - Pattern: `((\*|mini|mid|large)|(\d+)(%|px|em)?)((:(\d+)(px|em)?){1,2})?`

- **`helpLink`** (*optional*)
  - Type: `string`
  - Link to a web page.

- **`taskStart`** (**required**)
  - Type: `string`
  - Name of the field of type date/datetime to be used as start time.

- **`taskDuration`** (*optional*)
  - Type: `string`
  - Name of the duration field.

- **`taskEnd`** (*optional*)
  - Type: `string`
  - Name of the field of type date/datetime to be used as end time.

- **`taskParent`** (*optional*)
  - Type: `string`
  - Name of the parent field.

- **`taskProgress`** (*optional*)
  - Type: `string`
  - Name of the progress field.

- **`taskSequence`** (*optional*)
  - Type: `string`
  - Name of a field to order tasks in sequence.

- **`taskUser`** (*optional*)
  - Type: `string`
  - Name of the user field related to task.

- **`mode`** (*optional*)
  - Default: `month`
  - Possible values: year, month, week, day

- **`x-finish-to-start`** (*optional*)
  - Type: `string`
  - Name of the M2M field containing tasks to finish before starting current task.

- **`x-start-to-start`** (*optional*)
  - Type: `string`
  - Name of the M2M field containing tasks to start before starting current task.

- **`x-finish-to-finish`** (*optional*)
  - Type: `string`
  - Name of the M2M field containing tasks to finish before finishing current task.

- **`x-start-to-finish`** (*optional*)
  - Type: `string`
  - Name of the M2M field containing tasks to start before finishing current task.

---

## `<grid>`

**Type:** `NestedGridView`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing view, provide an unique id to identify current view.

- **`title`** (**required**)
  - Type: `string`
  - The display text.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`css`** (*optional*)
  - Type: `string`
  - Specify additional css class names

- **`width`** (*optional*)
  - The preferred width style of the view.<br><br> For example: <br><pre> width="mini" width="mid" width="large"</pre>
  - Pattern: `((\*|mini|mid|large)|(\d+)(%|px|em)?)((:(\d+)(px|em)?){1,2})?`

- **`helpLink`** (*optional*)
  - Type: `string`
  - Link to a web page.

- **`widget`** (*optional*)
  - Pattern: `[Ee]xpandable|[Tt]ree-?[Gg]rid`

- **`sortable`** (*optional*)
  - Type: `boolean`

- **`orderBy`** (*optional*)
  - Type: `string`
  - List of comma-separated field names optionally prefix with `-` to order by DESC. For example: orderBy="name,-age"

- **`groupBy`** (*optional*)
  - Type: `string`
  - List of comma-separated field names to group the data items.

- **`summary-view`** (*optional*)
  - Type: `string`
  - Specify custom form view to be used for summary view

- **`x-row-height`** (*optional*)
  - Type: `int`
  - Specify custom row height.

- **`x-col-width`** (*optional*)
  - Type: `int`
  - Specify minimum column width.

- **`x-no-fetch`** (*optional*)
  - Type: `boolean`
  - Whether to fetch initial records.

- **`x-selector`** (*optional*)
  - Type: `SelectorType`
  - Specify the row selection control

- **`edit-icon`** (*optional*)
  - Type: `boolean`
  - Default: `true`
  - Whether to show edit icon.

- **`onNew`** (*optional*)
  - Type: `string`
  - Comma-separated list of actions to execute on new event.

- **`onSave`** (*optional*)
  - Type: `string`
  - Comma-separated list of actions to execute on save event.

- **`onDelete`** (*optional*)
  - Type: `string`
  - Comma-separated list of actions to execute on delete event.

- **`canNew`** (*optional*)
  - Type: `string`
  - Specify whether to show the 'New' button.

- **`canEdit`** (*optional*)
  - Type: `string`
  - Specify whether to show the 'Edit' button.

- **`canSave`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the 'Save' button.

- **`canDelete`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the 'Delete' button.

- **`canArchive`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the 'Archive' button.

- **`canMove`** (*optional*)
  - Type: `boolean`
  - Specify whether the rows can be moved to re-orders by sequence.

- **`editable`** (*optional*)
  - Type: `boolean`
  - Specify whether the grid is editable.

---

## `<help>`

**Type:** `Help`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`

- **`title`** (*optional*)

- **`showTitle`** (*optional*)

- **`readonly`** (*optional*)

- **`readonlyIf`** (*optional*)

- **`help`** (*optional*)

- **`variant`** (*optional*)
  - Variant to use. Accepted values are: `info`, `success`, `warning` and `danger`. Default to `info`.
  - Possible values: info, success, warning, danger

---

## `<hilite>`

**Type:** `Hilite`

Hilite the field with given color/background-color/strong combination.

### Attributes

- **`color`** (*optional*)
  - Type: `HiliteStyle`
  - Highlight text color style

- **`background`** (*optional*)
  - Type: `HiliteStyle`
  - Highlight background color style

- **`strong`** (*optional*)
  - Type: `boolean`
  - Highlight text with strong font style

- **`if`** (**required**)
  - Type: `string`
  - Highlight condition

---

## `<import>`

### Attributes

- **`file`** (**required**)
  - Type: `string`
  - XML input file name as configured in config file.

- **`provider`** (**required**)
  - Type: `string`
  - The data stream provider. The value should be a reference to another action that returns the stream. Generally, an `action-ws` reference.

- **`name`** (*optional*)
  - Type: `string`
  - Put the data as the given name in the result map.

---

## `<info>`

**Type:** `ActInfo`

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`message`** (**required**)
  - Type: `string`
  - The message to show.

- **`action`** (*optional*)
  - Type: `string`
  - An action to be executed on error or alert message to make corrective measures, when error dialog is closed or alert dialog is canceled.

- **`title`** (*optional*)
  - Type: `string`
  - Title of the modal/notification

- **`confirm-btn-title`** (*optional*)
  - Type: `string`
  - Title of the confirm button.

- **`cancel-btn-title`** (*optional*)
  - Type: `string`
  - Title of the cancel button.

- **`action`** (*optional*)
  - Type: `string`

- **`cancel-btn-title`** (*optional*)
  - Type: `string`

---

## `<input>`

### Attributes

- **`name`** (**required**)
  - Type: `string`
  - Link to search field in order to provide the value used in where condition. Can be anything else if `expr` is used.

- **`field`** (**required**)
  - Type: `string`
  - Match against any field from the object graph.

- **`matchStyle`** (*optional*)
  - Default: `equals`
  - How to match the input. Possible value can be: - contains : if the field value contains the given input value - startsWith : if field value starts with the given input value - endsWith : if the field value ends with the given input value - equals : if the field value equals the input value (default matchStyle) - notEquals : if the field value is not equal to the input value - lessThan : if field value is less than the input value - greaterThan : if field value is greater than the input value - lessOrEqual : if field value is less then or equal to the input value - greaterOrEqual : if field value is greater than or equal to the input value
  - Possible values: startsWith, endsWith, contains, equals, notEquals, lessThan, greaterThan, lessOrEqual, greaterOrEqual

- **`if`** (*optional*)
  - Type: `string`
  - If the result of the expression is false, evaluates against the input values, then these elements are skipped.

- **`expr`** (*optional*)
  - Type: `string`
  - The result of the expression, evaluates against the input values, is used as the search input (instead using the provided input).

---

## `<insert>`

### Attributes

- **`position`** (**required**)
  - Type: `Position`

---

## `<item>`

**Type:** `MenubarMenuItem`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (**required**)
  - Type: `string`
  - The display text

- **`action`** (**required**)
  - Type: `string`
  - Comma-separated list of actions to execute on click event.

- **`name`** (*optional*)
  - Type: `string`
  - The name of this menu item.

- **`prompt`** (*optional*)
  - Type: `string`
  - Show a confirmation message before performing client action.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

---

## `<kanban>`

**Type:** `KanbanView`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing view, provide an unique id to identify current view.

- **`title`** (**required**)
  - Type: `string`
  - The display text.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`css`** (*optional*)
  - Type: `string`
  - Specify additional css class names

- **`width`** (*optional*)
  - The preferred width style of the view.<br><br> For example: <br><pre> width="mini" width="mid" width="large"</pre>
  - Pattern: `((\*|mini|mid|large)|(\d+)(%|px|em)?)((:(\d+)(px|em)?){1,2})?`

- **`helpLink`** (*optional*)
  - Type: `string`
  - Link to a web page.

- **`name`** (**required**)
  - Type: `string`
  - The name of the view.

- **`model`** (**required**)
  - Type: `string`
  - Specify the model object name.

- **`orderBy`** (*optional*)
  - Type: `string`
  - List of comma-separated field names optionally prefix with `-` to order by DESC. For example: orderBy="name,-age"

- **`canNew`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the 'New' button.

- **`canEdit`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the 'Edit' button.

- **`canDelete`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the 'Delete' button.

- **`edit-window`** (*optional*)
  - Type: `CardEditWindow`
  - Specify how to show editor window.

- **`onDelete`** (*optional*)
  - Type: `string`
  - Comma-separated list of actions to execute on delete event.

- **`columnBy`** (**required**)
  - Type: `string`
  - Specify a field to create columns. Can be an enum, selection or a reference field.

- **`cardWidth`** (*optional*)

- **`orderBy`** (*optional*)

- **`draggable`** (*optional*)
  - Type: `boolean`
  - Default: `true`
  - Whether to enable drag && drop feature.

- **`sequenceBy`** (**required**)
  - Type: `string`
  - Specify a numeric field to re-order cards.

- **`onNew`** (*optional*)
  - Type: `string`
  - Specify an action (action-record or action-method) that returns required values to create a new record.

- **`onMove`** (*optional*)
  - Type: `string`
  - Specify an action (action-record or action-method) that returns values to update kanban record being moved.

- **`limit`** (*optional*)
  - Type: `integer`
  - Specify pagination limit per column.

- **`x-limit-columns`** (*optional*)
  - Type: `integer`
  - Specify maximum number of columns when columnBy is a reference field.

- **`x-collapse-columns`** (*optional*)
  - Type: `string`
  - Comma-separated list of columns that are collapsed by default (reference fields not supported).

---

## `<label>`

**Type:** `Label`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`

- **`showTitle`** (*optional*)

- **`readonly`** (*optional*)

- **`readonlyIf`** (*optional*)

---

## `<mail-followers>`

*No attributes*

---

## `<mail-messages>`

### Attributes

- **`filter`** (*optional*)
  - Specify the messages type to show: `all` (default), `comment`, `notification`.
  - Possible values: comment, notification, all

- **`limit`** (*optional*)
  - Type: `int`
  - Specify the maximum number of messages to display.

---

## `<menu>`

**Type:** `MenubarMenu`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`name`** (*optional*)
  - Type: `string`

- **`title`** (**required**)
  - Type: `string`
  - The display text

- **`icon`** (*optional*)
  - Type: `string`
  - Path of the image.

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

---

## `<menubar>`

**Type:** `Menubar`

*No attributes*

---

## `<menuitem>`

**Type:** `MenuItem`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`name`** (**required**)
  - Type: `string`
  - The name of the menu item. It serves as an identifier.

- **`title`** (**required**)
  - Type: `string`
  - The display text of this menu item.

- **`parent`** (*optional*)
  - Type: `string`
  - The name of the parent menu item.

- **`icon`** (*optional*)
  - Type: `string`
  - The image for this menu item.

- **`icon-background`** (*optional*)
  - Type: `ColorStyle`
  - Specify icon background color (predefined or html hex color)

- **`action`** (*optional*)
  - Type: `string`
  - The name of the action to perform when this menu is clicked.

- **`order`** (*optional*)
  - Type: `string`
  - Specify menu sequence order.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`left`** (*optional*)
  - Type: `boolean`
  - Whether to show the menu item in the left navigation menu.

- **`mobile`** (*optional*)
  - Type: `boolean`
  - Whether to show the menu item in the mobile menu.

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the menu with given name.

- **`tag`** (*optional*)
  - Type: `string`
  - Specify a tag to show on menu item as a fixed label. This attribute gets preference over 'tag-count' and 'tag-get' attributes.

- **`tag-count`** (*optional*)
  - Type: `boolean`
  - Specify whether to use count of menu action records as tag.

- **`tag-get`** (*optional*)
  - Type: `string`
  - Specify a method call to get tag value. This attribute gets preference over 'tag-count' attribute. The signature of the controller method should be:<br><br> <code> void someMethod(ActionRequest request, ActionResponse response) </code>

- **`tag-style`** (*optional*)
  - Type: `LabelStyle`
  - Specify the tag display style.

---

## `<move>`

### Attributes

- **`source`** (**required**)
  - Type: `string`

- **`position`** (**required**)
  - Type: `Position`

---

## `<node>`

### Attributes

- **`model`** (**required**)
  - Type: `string`
  - The model name.

- **`parent`** (*optional*)
  - Type: `string`
  - The name of the parent field.

- **`onClick`** (*optional*)
  - Type: `string`
  - An action to execute on click event. The current node record is passed as context the context handler.

- **`onMove`** (*optional*)
  - Type: `string`
  - Comma-separated list of actions to execute on move event.

- **`draggable`** (*optional*)
  - Type: `boolean`
  - Whether the node can be draggable. <br><br> If draggable and parent field is given then node's parent can be changed with drag and drop feature.

- **`domain`** (*optional*)
  - Type: `string`
  - The domain for the node records.

- **`orderBy`** (*optional*)
  - Type: `string`
  - Sort the node results by the given field.

---

## `<notify>`

**Type:** `ActNotify`

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`message`** (**required**)
  - Type: `string`
  - The message to show.

- **`action`** (*optional*)
  - Type: `string`
  - An action to be executed on error or alert message to make corrective measures, when error dialog is closed or alert dialog is canceled.

- **`title`** (*optional*)
  - Type: `string`
  - Title of the modal/notification

- **`confirm-btn-title`** (*optional*)
  - Type: `string`
  - Title of the confirm button.

- **`cancel-btn-title`** (*optional*)
  - Type: `string`
  - Title of the cancel button.

- **`action`** (*optional*)
  - Type: `string`

- **`confirm-btn-title`** (*optional*)
  - Type: `string`

- **`cancel-btn-title`** (*optional*)
  - Type: `string`

---

## `<object-views>`

*No attributes*

---

## `<option>`

### Attributes

- **`value`** (**required**)
  - Type: `string`
  - Option value stored in database.

- **`icon`** (*optional*)
  - Type: `string`
  - Image icon to show for this item.

- **`color`** (*optional*)
  - Type: `string`
  - Tag color for this item.

- **`order`** (*optional*)
  - Type: `int`
  - Specify the sequence number to order the option.

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide this option from selection.

- **`data-description`** (*optional*)
  - Type: `string`
  - Specify description of the step under the label for Stepper widget.

- **`data-domain`** (*optional*)
  - Type: `string`
  - Specify the domain for the corresponding m2o input. Only apply on RefSelect widget.

- **`data-grid`** (*optional*)
  - Type: `string`
  - Specify the grid view for the corresponding m2o input. Only apply on RefSelect widget.

- **`data-form`** (*optional*)
  - Type: `string`
  - Specify the form view for the corresponding m2o input. Only apply on RefSelect widget.

---

## `<panel>`

**Type:** `Panel`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`
  - Container name.

- **`showFrame`** (*optional*)
  - Type: `boolean`
  - Default: `true`
  - Specify whether to show frame around the panel.

- **`sidebar`** (*optional*)
  - Type: `boolean`
  - Specify whether to show this panel in sidebar.

- **`stacked`** (*optional*)
  - Type: `boolean`
  - Specify whether to stack panel items.

- **`attached`** (*optional*)
  - Type: `boolean`
  - Specify whether to attach the panel with previous one.

- **`onTabSelect`** (*optional*)
  - Type: `string`
  - Specify an action to execute when the panel tab is selected (if it's top-level in panel-tabs).

- **`width`** (*optional*)

- **`canCollapse`** (*optional*)
  - Type: `boolean`
  - Specify whether the panel is collapsible.

- **`collapseIf`** (*optional*)
  - Type: `string`
  - Specify a boolean expression to collapse/expend this panel.

- **`icon`** (*optional*)
  - Type: `string`
  - Specify an icon to show in panel title.

- **`icon-background`** (*optional*)
  - Type: `ColorStyle`
  - Specify icon background color (predefined or html hex color)

---

## `<panel-dashlet>`

**Type:** `PanelDashlet`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`
  - Container name.

- **`action`** (**required**)
  - Type: `string`

- **`canSearch`** (*optional*)
  - Type: `boolean`
  - Whether to enable search header (for grid views) or search box (for card views).

- **`x-show-bars`** (*optional*)
  - Type: `boolean`
  - Specify whether to show toolbar and menubar.

- **`canNew`** (*optional*)
  - Type: `string`
  - Specify whether to allow to create new record.

- **`canEdit`** (*optional*)
  - Type: `string`
  - Specify whether to allow to edit the records.

- **`canDelete`** (*optional*)
  - Type: `string`
  - Default: `false`
  - Specify whether to allow to remove the record.

---

## `<panel-include>`

**Type:** `FormInclude`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`view`** (**required**)
  - Type: `string`
  - Name of an existing view.

- **`from`** (*optional*)
  - Type: `string`
  - Name of the module from which the view should be included.

---

## `<panel-mail>`

**Type:** `PanelMail`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`
  - Container name.

- **`showFrame`** (*optional*)
  - Type: `boolean`
  - Default: `true`
  - Specify whether to show frame around the panel.

- **`sidebar`** (*optional*)
  - Type: `boolean`
  - Specify whether to show this panel in sidebar.

- **`stacked`** (*optional*)
  - Type: `boolean`
  - Specify whether to stack panel items.

- **`attached`** (*optional*)
  - Type: `boolean`
  - Specify whether to attach the panel with previous one.

- **`onTabSelect`** (*optional*)
  - Type: `string`
  - Specify an action to execute when the panel tab is selected (if it's top-level in panel-tabs).

- **`width`** (*optional*)

---

## `<panel-related>`

**Type:** `PanelRelated`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`
  - Container name.

- **`showFrame`** (*optional*)
  - Type: `boolean`
  - Default: `true`
  - Specify whether to show frame around the panel.

- **`sidebar`** (*optional*)
  - Type: `boolean`
  - Specify whether to show this panel in sidebar.

- **`stacked`** (*optional*)
  - Type: `boolean`
  - Specify whether to stack panel items.

- **`attached`** (*optional*)
  - Type: `boolean`
  - Specify whether to attach the panel with previous one.

- **`onTabSelect`** (*optional*)
  - Type: `string`
  - Specify an action to execute when the panel tab is selected (if it's top-level in panel-tabs).

- **`width`** (*optional*)

- **`cols`** (*optional*)

- **`colWidths`** (*optional*)

- **`itemSpan`** (*optional*)

- **`stacked`** (*optional*)

- **`field`** (**required**)
  - Type: `string`

- **`editable`** (*optional*)
  - Type: `boolean`

- **`required`** (*optional*)
  - Type: `boolean`

- **`requiredIf`** (*optional*)
  - Type: `string`

- **`validIf`** (*optional*)
  - Type: `string`

- **`orderBy`** (*optional*)
  - Type: `string`

- **`groupBy`** (*optional*)
  - Type: `string`

- **`onNew`** (*optional*)
  - Type: `string`

- **`onChange`** (*optional*)
  - Type: `string`

- **`onCopy`** (*optional*)
  - Type: `string`
  - action to call after duplicating record in o2m/m2m grid

- **`onDelete`** (*optional*)
  - Type: `string`
  - action to call when removing record in o2m/m2m grid

- **`canMove`** (*optional*)
  - Type: `boolean`
  - Specify whether the rows can be moved to re-orders by sequence.

- **`x-selector`** (*optional*)
  - Type: `SelectorType`
  - Specify the row selection control

- **`widget`** (*optional*)
  - Type: `string`

- **`showTitle`** (*optional*)

---

## `<panel-stack>`

**Type:** `PanelTabs`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`
  - Container name.

- **`showFrame`** (*optional*)
  - Type: `boolean`
  - Default: `true`
  - Specify whether to show frame around the panel.

- **`sidebar`** (*optional*)
  - Type: `boolean`
  - Specify whether to show this panel in sidebar.

- **`stacked`** (*optional*)
  - Type: `boolean`
  - Specify whether to stack panel items.

- **`attached`** (*optional*)
  - Type: `boolean`
  - Specify whether to attach the panel with previous one.

- **`onTabSelect`** (*optional*)
  - Type: `string`
  - Specify an action to execute when the panel tab is selected (if it's top-level in panel-tabs).

- **`width`** (*optional*)

- **`stacked`** (*optional*)

- **`cols`** (*optional*)

- **`colWidths`** (*optional*)

- **`itemSpan`** (*optional*)

- **`showFrame`** (*optional*)

- **`showTitle`** (*optional*)

- **`title`** (*optional*)

- **`help`** (*optional*)

- **`onTabSelect`** (*optional*)

- **`x-row-height`** (*optional*)
  - Type: `int`

---

## `<panel-tabs>`

**Type:** `PanelTabs`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`
  - Container name.

- **`showFrame`** (*optional*)
  - Type: `boolean`
  - Default: `true`
  - Specify whether to show frame around the panel.

- **`sidebar`** (*optional*)
  - Type: `boolean`
  - Specify whether to show this panel in sidebar.

- **`stacked`** (*optional*)
  - Type: `boolean`
  - Specify whether to stack panel items.

- **`attached`** (*optional*)
  - Type: `boolean`
  - Specify whether to attach the panel with previous one.

- **`onTabSelect`** (*optional*)
  - Type: `string`
  - Specify an action to execute when the panel tab is selected (if it's top-level in panel-tabs).

- **`width`** (*optional*)

- **`stacked`** (*optional*)

- **`cols`** (*optional*)

- **`colWidths`** (*optional*)

- **`itemSpan`** (*optional*)

- **`showFrame`** (*optional*)

- **`showTitle`** (*optional*)

- **`title`** (*optional*)

- **`help`** (*optional*)

- **`onTabSelect`** (*optional*)

- **`x-row-height`** (*optional*)
  - Type: `int`

---

## `<param>`

**Type:** `ActContext`

Define a report parameter.

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`name`** (**required**)
  - Type: `string`
  - Comma-separated list of field names

- **`expr`** (**required**)
  - Type: `string`
  - A Groovy boolean expression against the current form values.

- **`copy`** (*optional*)
  - Type: `boolean`
  - Use the result of `expr` by copy.

---

## `<replace>`

*No attributes*

---

## `<result-fields>`

Defines the fields displayed in the grid view. They will be mapped with the fields define in each <search>.

*No attributes*

---

## `<script>`

### Attributes

- **`language`** (**required**)
  - Specify the scripting language.
  - Possible values: js, groovy

- **`transactional`** (*optional*)
  - Type: `boolean`
  - Specify whether the action is transactional. In that case, EntityManager will be available as $em variable.

---

## `<search>`

**Type:** `Search`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing view, provide an unique id to identify current view.

- **`title`** (**required**)
  - Type: `string`
  - The display text.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`css`** (*optional*)
  - Type: `string`
  - Specify additional css class names

- **`width`** (*optional*)
  - The preferred width style of the view.<br><br> For example: <br><pre> width="mini" width="mid" width="large"</pre>
  - Pattern: `((\*|mini|mid|large)|(\d+)(%|px|em)?)((:(\d+)(px|em)?){1,2})?`

- **`helpLink`** (*optional*)
  - Type: `string`
  - Link to a web page.

- **`name`** (**required**)
  - Type: `string`
  - The name of the view.

- **`limit`** (**required**)
  - Type: `int`
  - Specify query result limit for each select.

- **`search-form`** (*optional*)
  - Type: `string`
  - The form view to be used as search form using the given search fields.

---

## `<search-fields>`

Defines the fields to be used as context.

*No attributes*

---

## `<search-filters>`

**Type:** `SearchFilters`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing view, provide an unique id to identify current view.

- **`title`** (**required**)
  - Type: `string`
  - The display text.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`css`** (*optional*)
  - Type: `string`
  - Specify additional css class names

- **`width`** (*optional*)
  - The preferred width style of the view.<br><br> For example: <br><pre> width="mini" width="mid" width="large"</pre>
  - Pattern: `((\*|mini|mid|large)|(\d+)(%|px|em)?)((:(\d+)(px|em)?){1,2})?`

- **`helpLink`** (*optional*)
  - Type: `string`
  - Link to a web page.

- **`name`** (**required**)
  - Type: `string`
  - The name of the view.

- **`model`** (**required**)
  - Type: `string`
  - The model name.

---

## `<select>`

**Type:** `SearchSelect`

### Attributes

- **`model`** (**required**)
  - Type: `string`
  - Name of the model class for the search.

- **`title`** (*optional*)
  - Type: `string`
  - The text displayed in the first column of the result grid view.

- **`view-title`** (*optional*)
  - Type: `string`
  - Specify an expression used to customize the opened tab title.

- **`selected`** (*optional*)
  - Type: `boolean`
  - Specify if the select object is selected by default.

- **`orderBy`** (*optional*)
  - Type: `string`
  - List of comma-separated field names (from the object graph) optionally prefix with `-` to order by DESC. For example: orderBy="name,-age"

- **`if`** (*optional*)
  - Type: `string`
  - If the result of the expression is false, evaluates against the input values, then these elements are skipped.

- **`form-view`** (*optional*)
  - Type: `string`
  - The form view to be used to edit the selected record.

- **`grid-view`** (*optional*)
  - Type: `string`
  - The grid view to be used to list the selected records.

- **`limit`** (*optional*)
  - Type: `int`
  - Specify query result limit for the select. This attribute gets preference over 'limit' attribute of 'search'.

- **`distinct`** (*optional*)
  - Type: `boolean`
  - Default: `false`
  - Whether to return only distinct records (based on `id`). Useful when searching on relational fields (O2M/M2M).

---

## `<selection>`

**Type:** `Selection`

### Attributes

- **`name`** (**required**)
  - Type: `string`
  - Selection name.

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing one, provide an unique id to identify this one.

---

## `<separator>`

**Type:** `Separator`

### Attributes

- **`name`** (*optional*)
  - Type: `string`

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

---

## `<series>`

A chart data series. You must provide either `key` or `expr` or both.

### Attributes

- **`key`** (**required**)
  - Type: `string`

- **`groupBy`** (*optional*)
  - Type: `string`

- **`title`** (*optional*)
  - Type: `string`

- **`type`** (*optional*)
  - Possible values: pie, bar, hbar, line, area, text, donut, radar, gauge, scatter, funnel

- **`side`** (*optional*)
  - Possible values: left, right

- **`aggregate`** (*optional*)
  - Possible values: sum, count, average, maximum, minimum, variance, deviation

- **`scale`** (*optional*)
  - Type: `int`
  - Scale of the values (number of digits in decimal part)

---

## `<spacer>`

**Type:** `Spacer`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`

- **`title`** (*optional*)

- **`showTitle`** (*optional*)

- **`hidden`** (*optional*)

- **`help`** (*optional*)

- **`readonly`** (*optional*)

- **`readonlyIf`** (*optional*)

---

## `<static>`

**Type:** `Static`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - Unique id to identify the current widget.

- **`if`** (*optional*)
  - Type: `string`
  - Only use this widget if the given expression is true.

- **`if-module`** (*optional*)
  - Type: `string`
  - Only use the widget if the given module is installed.

- **`title`** (*optional*)
  - Type: `string`
  - The display text

- **`showTitle`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the title.

- **`help`** (*optional*)
  - Type: `string`
  - The help text

- **`hidden`** (*optional*)
  - Type: `boolean`
  - Specify whether to hide the widget.

- **`readonly`** (*optional*)
  - Type: `boolean`
  - Specify whether the widget should be considered readonly.

- **`css`** (*optional*)
  - Type: `string`
  - Custom css class to apply.

- **`height`** (*optional*)
  - Specify the widget height.<br><br> The height can be specified as a percentage or fixed value.<br><br> The fixed height can be either in 'px' or 'em'; 'px' is assumed if not specified. For 'text' and 'panel-related' widgets, it defines the number of rows taken by the widget.
  - Pattern: `\d+(%|px|pt|em)?`

- **`width`** (*optional*)
  - Specify the widget width.<br><br> The width can be specified as percentage or fixed value.<br><br> The fix width can be either in 'px' or 'em', 'px' is assumed if not specified.
  - Pattern: `(\*)|(\d+(%|px|em)?)`

- **`showIf`** (*optional*)
  - Type: `string`
  - Show if the given JavaScript expression is true.

- **`hideIf`** (*optional*)
  - Type: `string`
  - Hide if the given JavaScript expression is true.

- **`readonlyIf`** (*optional*)
  - Type: `string`
  - Readonly if the given JavaScript expression is true.

- **`depends`** (*optional*)
  - Type: `string`
  - Specify comma-separated list of field names on which this widget depends.

- **`name`** (*optional*)
  - Type: `string`

- **`title`** (*optional*)

- **`showTitle`** (*optional*)

- **`readonly`** (*optional*)

- **`readonlyIf`** (*optional*)

- **`help`** (*optional*)

---

## `<template>`

**Type:** `string`

Define the event popover content template.

*No attributes*

---

## `<toolbar>`

**Type:** `Toolbar`

*No attributes*

---

## `<tooltip>`

**Type:** `ToolTip`

### Attributes

- **`call`** (*optional*)
  - Type: `string`
  - Specify a controller method to fetch tooltip data.

---

## `<tree>`

**Type:** `TreeView`

### Attributes

- **`id`** (*optional*)
  - Type: `string`
  - If overriding some existing view, provide an unique id to identify current view.

- **`title`** (**required**)
  - Type: `string`
  - The display text.

- **`groups`** (*optional*)
  - Type: `string`
  - Comma-separated list of authorized groups.

- **`css`** (*optional*)
  - Type: `string`
  - Specify additional css class names

- **`width`** (*optional*)
  - The preferred width style of the view.<br><br> For example: <br><pre> width="mini" width="mid" width="large"</pre>
  - Pattern: `((\*|mini|mid|large)|(\d+)(%|px|em)?)((:(\d+)(px|em)?){1,2})?`

- **`helpLink`** (*optional*)
  - Type: `string`
  - Link to a web page.

- **`name`** (**required**)
  - Type: `string`
  - The name of the view.

- **`showHeader`** (*optional*)
  - Type: `boolean`
  - Specify whether to show the column header.

---

## `<view>`

**Type:** `ActView`

### Attributes

- **`if`** (*optional*)
  - Type: `string`
  - A boolean expression against the current form values.

- **`type`** (**required**)
  - Type: `ViewType`
  - View type. For exemple: form, grid, calendar, ...

- **`name`** (*optional*)
  - Type: `string`
  - View name.

---

## `<view-param>`

Additional view parameters (anything). The client view implementation utilizes these params.

### Attributes

- **`name`** (**required**)
  - Type: `string`
  - Param name.

- **`value`** (**required**)
  - Type: `string`
  - Param value.

---

## `<viewer>`

**Type:** `PanelViewer`

### Attributes

- **`depends`** (*optional*)
  - Type: `string`

---

## `<where>`

Define a sub filter.

### Attributes

- **`match`** (*optional*)
  - Default: `all`
  - The SQL operator used between each sub filters or inputs. - "all" is for an `AND` operator, - "any" is for an `OR` operator.
  - Possible values: all, any

- **`showArchived`** (*optional*)
  - Type: `boolean`
  - Default: `false`
  - Whether to search on archived records.

- **`if`** (*optional*)
  - Type: `string`
  - If the result of the expression is false, evaluates against the input values, then these elements are skipped.

- **`showArchived`** (*optional*)

---

