# Axelor Open Suite (AOS) Modules Reference

Quick reference guide for AOS module capabilities to accelerate gap analysis. This catalog helps identify which AOS modules provide functionality matching client requirements.

**AOS Version**: 8.0.x
**Last Updated**: 2025-10
**Purpose**: Gap analysis reference for aos-analyzer agent

---

## Core Modules

### axelor-base

**Purpose**: Foundation module with core business entities

**Key Entities**:
- **Partner**: Business partner (customer, supplier, contact)
  - Fields: code, name, partnerCategory, emailAddress, mobilePhone, website, language
  - Multi-address support
  - Multi-company support
- **Company**: Organization/company entity
  - Fields: code, name, currency, address, logo
  - Multi-company architecture foundation
- **Address**: Postal addresses with geocoding
- **Currency**: Multi-currency support with exchange rates
- **User**: Application users with roles and permissions
- **Team**: User groups for permissions and assignments
- **Sequence**: Auto-number generation (orders, invoices, etc.)
- **Product**: Generic product/article entity
  - Fields: code, name, productType, price, unit
  - Product categories and variants
- **MetaFile**: File attachment management
- **Bank**: Bank information and bank details
- **Period**: Fiscal periods and year management

**Key Features**:
- Partner management (CRM foundation)
- Multi-company architecture
- Address book with geocoding
- File attachment system
- Product catalog management
- User and permission management
- Sequence generation
- Multi-currency support
- Calendar and scheduling
- Document template engine
- Batch job framework

**Reuse Scenarios**:
- Any project needing customer/supplier management
- Multi-company requirements
- Product catalog
- User management and permissions
- File attachments
- Auto-numbering sequences

**Documentation**: https://docs.axelor.com/aos/modules/base/

---

### axelor-crm

**Purpose**: Customer Relationship Management

**Key Entities**:
- **Lead**: Sales leads/prospects
  - Fields: name, company, email, phone, status, source, industry
  - Workflow: NEW → CONTACTED → QUALIFIED → CONVERTED | LOST
  - Lead scoring and assignment
- **Opportunity**: Sales opportunities
  - Fields: name, partner, expectedAmount, probability, stage
  - Sales pipeline management
  - Weighted revenue calculation
- **Event**: Calendar events and meetings
  - Integration with Partner and Lead
  - Reminder notifications
- **Target**: Sales targets and quotas
- **CatalogContact**: Contact person management

**Key Features**:
- Lead capture and qualification
- Lead scoring based on activity
- Automatic lead assignment (by territory, workload)
- Sales pipeline management
- Opportunity tracking with stages
- Email integration (send, track)
- Event/meeting management
- Target vs achievement tracking
- CRM reporting and dashboards
- Kanban views for leads/opportunities

**Reuse Scenarios**:
- Any CRM requirement
- Lead management and qualification
- Sales pipeline tracking
- Opportunity management
- Sales forecasting

**Documentation**: https://docs.axelor.com/aos/modules/crm/

---

### axelor-sale

**Purpose**: Sales order management

**Key Entities**:
- **SaleOrder**: Sales orders and quotes
  - Fields: saleOrderNumber, orderDate, customer, totalAmount, status
  - Workflow: DRAFT → CONFIRMED → VALIDATED → COMPLETED
  - Order lines with products, quantities, prices
- **SaleOrderLine**: Order line items
  - Product, quantity, price, discount, tax
  - Automatic calculations (subtotal, tax, total)
- **Invoice**: Customer invoices (integration with axelor-account)
- **Delivery**: Delivery notes and shipping

**Key Features**:
- Quote generation and management
- Order confirmation workflow
- Automatic pricing and discount calculation
- Tax calculation
- Order to invoice conversion
- Delivery management
- Payment terms
- Multi-currency orders
- PDF generation (orders, quotes)
- Email integration (send quotes/orders)

**Reuse Scenarios**:
- Order management systems
- Quote-to-cash workflows
- E-commerce backend
- Sales transactions

**Documentation**: https://docs.axelor.com/aos/modules/sale/

---

### axelor-purchase

**Purpose**: Purchase order and procurement management

**Key Entities**:
- **PurchaseOrder**: Purchase orders to suppliers
  - Similar structure to SaleOrder
  - Supplier management
  - Purchase workflow
- **PurchaseOrderLine**: Purchase order lines
- **SupplierCatalog**: Supplier product catalog with prices

**Key Features**:
- Purchase requisition
- Purchase order creation and approval
- Supplier selection
- Price comparison
- Goods receipt management
- Purchase to payment workflow

**Reuse Scenarios**:
- Procurement systems
- Supplier management
- Purchase approval workflows

**Documentation**: https://docs.axelor.com/aos/modules/purchase/

---

## Human Resources Modules

### axelor-hr

**Purpose**: Human resource management

**Key Entities**:
- **Employee**: Employee records
  - Fields: name, hireDate, department, manager, position
  - Contract information
  - Salary and benefits
- **Department**: Organizational departments
- **LeaveRequest**: Leave/vacation requests
  - Types: vacation, sick leave, etc.
  - Approval workflow
- **Timesheet**: Time tracking
  - Project and activity tracking
  - Approval workflow
- **Expense**: Expense reports
  - Expense lines with categories
  - Approval and reimbursement workflow

**Key Features**:
- Employee database
- Organization chart
- Leave management with balance tracking
- Timesheet management
- Expense report workflow
- Absence calendar
- Employee self-service portal

**Reuse Scenarios**:
- HR management systems
- Employee directory
- Leave tracking
- Time and expense tracking
- Resource management

**Documentation**: https://docs.axelor.com/aos/modules/hr/

---

## Accounting & Finance Modules

### axelor-account

**Purpose**: Accounting and financial management

**Key Entities**:
- **Account**: Chart of accounts
- **Move**: Accounting entries/journal entries
- **MoveLine**: Journal entry lines (debit/credit)
- **Invoice**: Customer and supplier invoices
- **Payment**: Payments and receipts
- **FiscalYear**: Fiscal year periods
- **Journal**: Accounting journals

**Key Features**:
- Multi-company accounting
- Chart of accounts management
- Journal entry creation and validation
- Invoice management (AR/AP)
- Payment processing
- Bank reconciliation
- Multi-currency accounting
- Tax management (VAT, sales tax)
- Financial reporting
- Period closing

**Reuse Scenarios**:
- Any accounting requirement
- Invoice generation and tracking
- Payment processing
- Financial reporting
- Tax compliance

**Documentation**: https://docs.axelor.com/aos/modules/account/

---

### axelor-budget

**Purpose**: Budget management and control

**Key Entities**:
- **Budget**: Budget definitions
- **BudgetLine**: Budget line items
- **BudgetDistribution**: Budget allocation

**Key Features**:
- Budget creation and approval
- Budget vs actual tracking
- Budget consumption alerts
- Multi-level budget structure

**Reuse Scenarios**:
- Budget planning and control
- Project budgeting
- Departmental budgets

---

## Project & Task Management Modules

### axelor-project

**Purpose**: Project and task management

**Key Entities**:
- **Project**: Projects with tasks and milestones
  - Fields: name, code, customer, startDate, endDate, status
- **ProjectTask**: Tasks with assignments
  - Fields: name, project, assignedTo, priority, status, progress
- **ProjectPlanning**: Gantt chart and planning

**Key Features**:
- Project creation and management
- Task management with dependencies
- Gantt chart planning
- Resource assignment
- Time tracking integration
- Project dashboards
- Milestone tracking

**Reuse Scenarios**:
- Project management
- Task tracking
- Resource planning
- Agile/Scrum workflows

**Documentation**: https://docs.axelor.com/aos/modules/project/

---

## Stock & Inventory Modules

### axelor-stock

**Purpose**: Inventory and warehouse management

**Key Entities**:
- **StockLocation**: Warehouses and storage locations
- **StockMove**: Stock transfers and movements
- **StockMoveLine**: Movement line items
- **Inventory**: Physical inventory counts
- **Product**: Extended for stock management

**Key Features**:
- Multi-warehouse management
- Stock transfers
- Goods receipt and delivery
- Inventory counting
- Stock valuation
- Serial/lot number tracking
- Stock level alerts

**Reuse Scenarios**:
- Inventory management
- Warehouse operations
- Stock tracking
- Logistics

**Documentation**: https://docs.axelor.com/aos/modules/stock/

---

## Manufacturing Modules

### axelor-production

**Purpose**: Manufacturing and production management

**Key Entities**:
- **BillOfMaterial**: Product recipes and BOMs
- **ManufacturingOrder**: Production orders
- **OperationOrder**: Manufacturing operation tracking
- **WorkCenter**: Production resources

**Key Features**:
- Bill of materials management
- Production order planning
- Manufacturing execution
- Work center scheduling
- Production cost tracking

**Reuse Scenarios**:
- Manufacturing operations
- Production planning
- Shop floor management

---

## Communication Modules

### axelor-message

**Purpose**: Messaging and communication

**Key Entities**:
- **Message**: Messages and notifications
- **EmailAccount**: Email account configuration
- **Template**: Email templates

**Key Features**:
- Email integration (send/receive)
- Email templates with variables
- Internal messaging
- Notification system
- Comment threads on entities
- File attachments in messages

**Reuse Scenarios**:
- Any project needing email notifications
- Internal communication
- Comment/discussion features
- Email templates

**Documentation**: https://docs.axelor.com/aos/modules/message/

---

## Mobile & Portal Modules

### axelor-mobile

**Purpose**: Mobile application backend

**Key Features**:
- Mobile API endpoints
- Offline sync support
- Mobile-optimized views

**Reuse Scenarios**:
- Mobile app backend
- Field workforce management

---

## Additional Modules

### axelor-contract

**Purpose**: Contract management

**Key Entities**:
- **Contract**: Contracts with customers/suppliers
- **ContractLine**: Contract line items
- **ContractVersion**: Contract versioning

**Key Features**:
- Contract lifecycle management
- Recurring invoicing from contracts
- Contract templates
- Renewal management

---

### axelor-quality

**Purpose**: Quality management

**Key Entities**:
- **QualityControl**: Quality control records
- **Anomaly**: Defect and non-conformance tracking

**Key Features**:
- Quality control process
- Non-conformance management
- Corrective action tracking

---

### axelor-supplychain

**Purpose**: Supply chain integration

**Purpose**: Links sales, purchase, and stock modules

**Key Features**:
- Order fulfillment automation
- Purchase-to-pay integration
- Dropshipping support
- Inter-company transfers

---

## Common Patterns Across Modules

### Standard Workflows

Most business entities follow similar patterns:
- **Status workflow**: DRAFT → VALIDATED → COMPLETED → CANCELED
- **Approval workflow**: Created → Pending → Approved → Rejected
- **Versioning**: Draft versions, published versions, archives

### Standard Features

Available in most modules:
- **Multi-company**: Entity filtering by company
- **Security**: Role-based permissions (MetaPermission)
- **Audit**: createdOn, createdBy, updatedOn, updatedBy fields
- **Attachments**: MetaFile integration for documents
- **Notes**: Comment/discussion threads
- **Reporting**: Standard and custom reports
- **Export**: PDF, Excel, CSV export
- **Email**: Email integration and templates
- **Print**: Print templates (BIRT)
- **Search**: Full-text search
- **Filters**: Advanced filtering and views

---

## How to Use This Reference

### For Gap Analysis

1. **Identify client requirement category**: CRM? Sales? HR? Accounting?

2. **Check corresponding AOS module**: Look up module capabilities

3. **Search specific entities**: Use Grep to find exact entity definitions

4. **Compare capabilities**: Match client requirements vs AOS features

5. **Make reuse decision**: REUSE / EXTEND / DEVELOP_NEW

### Search Commands

**Find module directory**:
```bash
ls /path/to/axelor-open-suite/axelor-*/
```

**Search for entity**:
```bash
grep -ri "entity.*Partner" /path/to/axelor-open-suite/axelor-base/
```

**Find all entities in module**:
```bash
find /path/to/axelor-open-suite/axelor-crm/ -name "*.xml" -path "*/domains/*"
```

**Read entity definition**:
```bash
cat /path/to/axelor-open-suite/axelor-base/src/main/resources/domains/Partner.xml
```

---

## AOS Version Compatibility

**Current AOS**: 8.0.x (2024)
**Previous versions**: 7.x, 6.x (major architectural differences)

**Important**: Always match AOS version in client projects to ensure compatibility.

---

## Additional Resources

- **AOS Documentation**: https://docs.axelor.com/aos/
- **AOS GitHub**: https://github.com/axelor/axelor-open-suite
- **AOS Community**: https://community.axelor.com/

---

**This reference should be updated as new AOS versions and modules are released.**
