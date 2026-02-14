# Complete Java Examples for Axelor

## Overview

This document contains complete, working examples of real-world Axelor Java code covering services, repositories, controllers, and full end-to-end features.

## Complete Service Example: SaleOrderService

### SaleOrderService Interface

```java
package com.axelor.apps.sale.service;

import com.axelor.apps.base.db.Company;
import com.axelor.apps.base.db.Partner;
import com.axelor.apps.sale.db.SaleOrder;
import com.axelor.apps.sale.db.SaleOrderLine;
import com.axelor.exception.AxelorException;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

public interface SaleOrderService {

    // Creation
    SaleOrder createOrder(Partner customer, Company company) throws AxelorException;
    SaleOrder createFromTemplate(SaleOrder template, Partner customer) throws AxelorException;

    // Computation
    SaleOrder computeLines(SaleOrder saleOrder) throws AxelorException;
    SaleOrder computeTaxes(SaleOrder saleOrder) throws AxelorException;
    SaleOrder computeTotals(SaleOrder saleOrder) throws AxelorException;
    SaleOrder computeAll(SaleOrder saleOrder) throws AxelorException;

    // Validation
    void validate(SaleOrder saleOrder) throws AxelorException;
    void validateLines(SaleOrder saleOrder) throws AxelorException;
    boolean canConfirm(SaleOrder saleOrder);
    boolean canCancel(SaleOrder saleOrder);

    // Workflow
    SaleOrder finalize(SaleOrder saleOrder) throws AxelorException;
    SaleOrder confirm(SaleOrder saleOrder) throws AxelorException;
    SaleOrder complete(SaleOrder saleOrder) throws AxelorException;
    SaleOrder cancel(SaleOrder saleOrder) throws AxelorException;

    // Document generation
    Invoice generateInvoice(SaleOrder saleOrder) throws AxelorException;
    StockMove generateDelivery(SaleOrder saleOrder) throws AxelorException;

    // Queries
    List<SaleOrder> findPendingOrders(Company company);
    List<SaleOrder> findOverdueOrders(Company company, LocalDate asOfDate);
    BigDecimal getTotalRevenue(Company company, LocalDate startDate, LocalDate endDate);

    // Utilities
    String getSequence(Company company) throws AxelorException;
    Map<String, Object> getOrderSummary(SaleOrder saleOrder);
}
```

### SaleOrderServiceImpl Implementation

```java
package com.axelor.apps.sale.service;

import com.axelor.apps.base.db.Company;
import com.axelor.apps.base.db.Partner;
import com.axelor.apps.base.db.Sequence;
import com.axelor.apps.base.service.administration.SequenceService;
import com.axelor.apps.base.service.app.AppBaseService;
import com.axelor.apps.sale.db.Invoice;
import com.axelor.apps.sale.db.SaleOrder;
import com.axelor.apps.sale.db.SaleOrderLine;
import com.axelor.apps.sale.db.SaleOrderTaxLine;
import com.axelor.apps.sale.db.StockMove;
import com.axelor.apps.sale.db.repo.SaleOrderRepository;
import com.axelor.apps.sale.exception.SaleExceptionMessage;
import com.axelor.auth.AuthUtils;
import com.axelor.auth.db.User;
import com.axelor.exception.AxelorException;
import com.axelor.exception.db.repo.TraceBackRepository;
import com.axelor.i18n.I18n;
import com.axelor.inject.Beans;
import com.google.inject.Inject;
import com.google.inject.persist.Transactional;
import java.lang.invoke.MethodHandles;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SaleOrderServiceImpl implements SaleOrderService {

    private static final Logger LOG = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());

    protected SaleOrderRepository saleOrderRepository;
    protected SaleOrderLineService saleOrderLineService;
    protected SequenceService sequenceService;
    protected AppBaseService appBaseService;
    protected InvoiceService invoiceService;
    protected StockMoveService stockMoveService;

    @Inject
    public SaleOrderServiceImpl(
            SaleOrderRepository saleOrderRepository,
            SaleOrderLineService saleOrderLineService,
            SequenceService sequenceService,
            AppBaseService appBaseService,
            InvoiceService invoiceService,
            StockMoveService stockMoveService) {
        this.saleOrderRepository = saleOrderRepository;
        this.saleOrderLineService = saleOrderLineService;
        this.sequenceService = sequenceService;
        this.appBaseService = appBaseService;
        this.invoiceService = invoiceService;
        this.stockMoveService = stockMoveService;
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder createOrder(Partner customer, Company company) throws AxelorException {
        LOG.debug("Creating sale order for customer: {} and company: {}",
            customer.getName(), company.getName());

        // Validate inputs
        if (customer == null) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_MISSING_FIELD,
                I18n.get(SaleExceptionMessage.SALE_ORDER_CUSTOMER_REQUIRED)
            );
        }

        if (company == null) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_MISSING_FIELD,
                I18n.get(SaleExceptionMessage.SALE_ORDER_COMPANY_REQUIRED)
            );
        }

        // Create new order
        SaleOrder saleOrder = new SaleOrder();
        saleOrder.setCustomer(customer);
        saleOrder.setCompany(company);

        // Set dates
        LocalDate today = appBaseService.getTodayDate(company);
        saleOrder.setCreationDate(today);
        saleOrder.setOrderDate(today);

        // Set status
        saleOrder.setStatusSelect(SaleOrderRepository.STATUS_DRAFT_QUOTATION);

        // Initialize from customer
        initializeFromCustomer(saleOrder, customer);

        // Initialize collections
        saleOrder.setSaleOrderLineList(new ArrayList<>());
        saleOrder.setSaleOrderTaxLineList(new ArrayList<>());

        // Save
        saleOrder = saleOrderRepository.save(saleOrder);
        LOG.info("Sale order created with ID: {}", saleOrder.getId());

        return saleOrder;
    }

    protected void initializeFromCustomer(SaleOrder saleOrder, Partner customer) {
        saleOrder.setCurrency(customer.getCurrency());
        saleOrder.setPriceList(customer.getSalePriceList());
        saleOrder.setPaymentMode(customer.getPaymentMode());
        saleOrder.setPaymentCondition(customer.getPaymentCondition());
        saleOrder.setDeliveryAddress(customer.getMainAddress());
        saleOrder.setInvoiceAddress(customer.getInvoicingAddress());
        saleOrder.setFiscalPosition(customer.getFiscalPosition());
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder createFromTemplate(SaleOrder template, Partner customer)
            throws AxelorException {
        LOG.debug("Creating sale order from template: {}", template.getId());

        SaleOrder saleOrder = createOrder(customer, template.getCompany());

        // Copy template fields
        saleOrder.setPriceList(template.getPriceList());
        saleOrder.setPaymentMode(template.getPaymentMode());
        saleOrder.setPaymentCondition(template.getPaymentCondition());
        saleOrder.setNotes(template.getNotes());

        // Copy lines
        if (template.getSaleOrderLineList() != null) {
            for (SaleOrderLine templateLine : template.getSaleOrderLineList()) {
                SaleOrderLine newLine = saleOrderLineService.copyLine(templateLine);
                newLine.setSaleOrder(saleOrder);
                saleOrder.addSaleOrderLineListItem(newLine);
            }
        }

        // Compute
        saleOrder = computeAll(saleOrder);

        saleOrder = saleOrderRepository.save(saleOrder);
        LOG.info("Sale order created from template with ID: {}", saleOrder.getId());

        return saleOrder;
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder computeLines(SaleOrder saleOrder) throws AxelorException {
        LOG.debug("Computing lines for sale order: {}", saleOrder.getId());

        if (saleOrder.getSaleOrderLineList() != null) {
            for (SaleOrderLine line : saleOrder.getSaleOrderLineList()) {
                saleOrderLineService.compute(line, saleOrder);
            }
        }

        return saleOrder;
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder computeTaxes(SaleOrder saleOrder) throws AxelorException {
        LOG.debug("Computing taxes for sale order: {}", saleOrder.getId());

        Map<TaxLine, BigDecimal> taxMap = new HashMap<>();

        // Aggregate taxes from lines
        if (saleOrder.getSaleOrderLineList() != null) {
            for (SaleOrderLine line : saleOrder.getSaleOrderLineList()) {
                TaxLine taxLine = line.getTaxLine();
                if (taxLine != null) {
                    BigDecimal taxAmount = computeLineTaxAmount(line);
                    taxMap.merge(taxLine, taxAmount, BigDecimal::add);
                }
            }
        }

        // Clear existing tax lines
        if (saleOrder.getSaleOrderTaxLineList() != null) {
            saleOrder.getSaleOrderTaxLineList().clear();
        } else {
            saleOrder.setSaleOrderTaxLineList(new ArrayList<>());
        }

        // Create new tax lines
        for (Map.Entry<TaxLine, BigDecimal> entry : taxMap.entrySet()) {
            SaleOrderTaxLine taxLine = new SaleOrderTaxLine();
            taxLine.setSaleOrder(saleOrder);
            taxLine.setTaxLine(entry.getKey());
            taxLine.setTaxAmount(entry.getValue());
            saleOrder.addSaleOrderTaxLineListItem(taxLine);
        }

        return saleOrder;
    }

    protected BigDecimal computeLineTaxAmount(SaleOrderLine line) {
        if (line.getTaxLine() == null || line.getExTaxTotal() == null) {
            return BigDecimal.ZERO;
        }

        return line.getExTaxTotal()
            .multiply(line.getTaxLine().getValue())
            .divide(BigDecimal.valueOf(100), 2, RoundingMode.HALF_UP);
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder computeTotals(SaleOrder saleOrder) throws AxelorException {
        LOG.debug("Computing totals for sale order: {}", saleOrder.getId());

        BigDecimal exTaxTotal = BigDecimal.ZERO;
        BigDecimal taxTotal = BigDecimal.ZERO;

        // Sum line totals
        if (saleOrder.getSaleOrderLineList() != null) {
            for (SaleOrderLine line : saleOrder.getSaleOrderLineList()) {
                if (line.getExTaxTotal() != null) {
                    exTaxTotal = exTaxTotal.add(line.getExTaxTotal());
                }
            }
        }

        // Sum tax amounts
        if (saleOrder.getSaleOrderTaxLineList() != null) {
            for (SaleOrderTaxLine taxLine : saleOrder.getSaleOrderTaxLineList()) {
                if (taxLine.getTaxAmount() != null) {
                    taxTotal = taxTotal.add(taxLine.getTaxAmount());
                }
            }
        }

        // Set totals
        saleOrder.setExTaxTotal(exTaxTotal);
        saleOrder.setTaxTotal(taxTotal);
        saleOrder.setInTaxTotal(exTaxTotal.add(taxTotal));

        LOG.debug("Computed totals - ExTax: {}, Tax: {}, InTax: {}",
            exTaxTotal, taxTotal, saleOrder.getInTaxTotal());

        return saleOrder;
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder computeAll(SaleOrder saleOrder) throws AxelorException {
        LOG.debug("Computing all for sale order: {}", saleOrder.getId());

        saleOrder = computeLines(saleOrder);
        saleOrder = computeTaxes(saleOrder);
        saleOrder = computeTotals(saleOrder);

        return saleOrder;
    }

    @Override
    public void validate(SaleOrder saleOrder) throws AxelorException {
        LOG.debug("Validating sale order: {}", saleOrder.getId());

        // Required fields
        if (saleOrder.getCustomer() == null) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_MISSING_FIELD,
                I18n.get(SaleExceptionMessage.SALE_ORDER_CUSTOMER_REQUIRED)
            );
        }

        if (saleOrder.getCompany() == null) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_MISSING_FIELD,
                I18n.get(SaleExceptionMessage.SALE_ORDER_COMPANY_REQUIRED)
            );
        }

        // Business rules
        if (saleOrder.getCustomer().getBlocked()) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(SaleExceptionMessage.SALE_ORDER_CUSTOMER_BLOCKED),
                saleOrder.getCustomer().getName()
            );
        }

        // Lines validation
        validateLines(saleOrder);

        // Total validation
        if (saleOrder.getExTaxTotal() == null ||
            saleOrder.getExTaxTotal().compareTo(BigDecimal.ZERO) <= 0) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(SaleExceptionMessage.SALE_ORDER_INVALID_TOTAL)
            );
        }

        LOG.debug("Sale order validation successful");
    }

    @Override
    public void validateLines(SaleOrder saleOrder) throws AxelorException {
        if (saleOrder.getSaleOrderLineList() == null ||
            saleOrder.getSaleOrderLineList().isEmpty()) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(SaleExceptionMessage.SALE_ORDER_NO_LINES)
            );
        }

        for (SaleOrderLine line : saleOrder.getSaleOrderLineList()) {
            saleOrderLineService.validate(line);
        }
    }

    @Override
    public boolean canConfirm(SaleOrder saleOrder) {
        if (saleOrder == null || saleOrder.getStatusSelect() == null) {
            return false;
        }

        Integer status = saleOrder.getStatusSelect();
        return status.equals(SaleOrderRepository.STATUS_DRAFT_QUOTATION) ||
               status.equals(SaleOrderRepository.STATUS_FINALIZED_QUOTATION);
    }

    @Override
    public boolean canCancel(SaleOrder saleOrder) {
        if (saleOrder == null || saleOrder.getStatusSelect() == null) {
            return false;
        }

        Integer status = saleOrder.getStatusSelect();
        if (status.equals(SaleOrderRepository.STATUS_CANCELED) ||
            status.equals(SaleOrderRepository.STATUS_ORDER_COMPLETED)) {
            return false;
        }

        // Check if has generated documents
        if (saleOrder.getInvoiceList() != null && !saleOrder.getInvoiceList().isEmpty()) {
            return false;
        }

        return true;
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder finalize(SaleOrder saleOrder) throws AxelorException {
        LOG.info("Finalizing sale order: {}", saleOrder.getId());

        validate(saleOrder);

        if (saleOrder.getStatusSelect() != SaleOrderRepository.STATUS_DRAFT_QUOTATION) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(SaleExceptionMessage.SALE_ORDER_CANNOT_FINALIZE)
            );
        }

        saleOrder.setStatusSelect(SaleOrderRepository.STATUS_FINALIZED_QUOTATION);

        saleOrder = saleOrderRepository.save(saleOrder);
        LOG.info("Sale order finalized: {}", saleOrder.getId());

        return saleOrder;
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder confirm(SaleOrder saleOrder) throws AxelorException {
        LOG.info("Confirming sale order: {}", saleOrder.getId());

        validate(saleOrder);

        if (!canConfirm(saleOrder)) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(SaleExceptionMessage.SALE_ORDER_CANNOT_CONFIRM)
            );
        }

        // Generate sequence number
        if (saleOrder.getOrderNumber() == null) {
            String sequence = getSequence(saleOrder.getCompany());
            saleOrder.setOrderNumber(sequence);
        }

        // Update status
        saleOrder.setStatusSelect(SaleOrderRepository.STATUS_ORDER_CONFIRMED);
        saleOrder.setConfirmationDateTime(
            appBaseService.getTodayDateTime(saleOrder.getCompany()).toLocalDateTime()
        );
        saleOrder.setConfirmedByUser(AuthUtils.getUser());

        saleOrder = saleOrderRepository.save(saleOrder);
        LOG.info("Sale order confirmed with number: {}", saleOrder.getOrderNumber());

        return saleOrder;
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder complete(SaleOrder saleOrder) throws AxelorException {
        LOG.info("Completing sale order: {}", saleOrder.getId());

        if (saleOrder.getStatusSelect() != SaleOrderRepository.STATUS_ORDER_CONFIRMED) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(SaleExceptionMessage.SALE_ORDER_CANNOT_COMPLETE)
            );
        }

        saleOrder.setStatusSelect(SaleOrderRepository.STATUS_ORDER_COMPLETED);
        saleOrder.setCompletionDate(appBaseService.getTodayDate(saleOrder.getCompany()));

        saleOrder = saleOrderRepository.save(saleOrder);
        LOG.info("Sale order completed: {}", saleOrder.getId());

        return saleOrder;
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder cancel(SaleOrder saleOrder) throws AxelorException {
        LOG.info("Canceling sale order: {}", saleOrder.getId());

        if (!canCancel(saleOrder)) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(SaleExceptionMessage.SALE_ORDER_CANNOT_CANCEL)
            );
        }

        saleOrder.setStatusSelect(SaleOrderRepository.STATUS_CANCELED);
        saleOrder.setCancelDate(appBaseService.getTodayDate(saleOrder.getCompany()));
        saleOrder.setCanceledByUser(AuthUtils.getUser());

        saleOrder = saleOrderRepository.save(saleOrder);
        LOG.info("Sale order canceled: {}", saleOrder.getId());

        return saleOrder;
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public Invoice generateInvoice(SaleOrder saleOrder) throws AxelorException {
        LOG.info("Generating invoice for sale order: {}", saleOrder.getId());

        if (saleOrder.getStatusSelect() < SaleOrderRepository.STATUS_ORDER_CONFIRMED) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(SaleExceptionMessage.SALE_ORDER_NOT_CONFIRMED)
            );
        }

        Invoice invoice = invoiceService.createFromSaleOrder(saleOrder);

        // Link invoice to order
        if (saleOrder.getInvoiceList() == null) {
            saleOrder.setInvoiceList(new ArrayList<>());
        }
        saleOrder.addInvoiceListItem(invoice);

        saleOrderRepository.save(saleOrder);
        LOG.info("Invoice generated: {}", invoice.getInvoiceNumber());

        return invoice;
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public StockMove generateDelivery(SaleOrder saleOrder) throws AxelorException {
        LOG.info("Generating delivery for sale order: {}", saleOrder.getId());

        if (saleOrder.getStatusSelect() < SaleOrderRepository.STATUS_ORDER_CONFIRMED) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(SaleExceptionMessage.SALE_ORDER_NOT_CONFIRMED)
            );
        }

        StockMove stockMove = stockMoveService.createFromSaleOrder(saleOrder);

        // Link stock move to order
        if (saleOrder.getStockMoveList() == null) {
            saleOrder.setStockMoveList(new ArrayList<>());
        }
        saleOrder.addStockMoveListItem(stockMove);

        saleOrderRepository.save(saleOrder);
        LOG.info("Delivery generated: {}", stockMove.getStockMoveSeq());

        return stockMove;
    }

    @Override
    public List<SaleOrder> findPendingOrders(Company company) {
        return saleOrderRepository.findPendingOrders(company);
    }

    @Override
    public List<SaleOrder> findOverdueOrders(Company company, LocalDate asOfDate) {
        return Query.of(SaleOrder.class)
            .filter("self.company = :company " +
                    "AND self.statusSelect = :status " +
                    "AND self.expectedDeliveryDate < :asOfDate")
            .bind("company", company)
            .bind("status", SaleOrderRepository.STATUS_ORDER_CONFIRMED)
            .bind("asOfDate", asOfDate)
            .fetch();
    }

    @Override
    public BigDecimal getTotalRevenue(Company company, LocalDate startDate, LocalDate endDate) {
        BigDecimal total = saleOrderRepository.sumTotalByCompanyAndPeriod(
            company, startDate, endDate);
        return total != null ? total : BigDecimal.ZERO;
    }

    @Override
    public String getSequence(Company company) throws AxelorException {
        Sequence sequence = company.getSaleOrderSequence();

        if (sequence == null) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_CONFIGURATION_ERROR,
                I18n.get(SaleExceptionMessage.SALE_ORDER_SEQUENCE_NOT_CONFIGURED),
                company.getName()
            );
        }

        return sequenceService.getSequenceNumber(sequence);
    }

    @Override
    public Map<String, Object> getOrderSummary(SaleOrder saleOrder) {
        Map<String, Object> summary = new HashMap<>();

        summary.put("orderNumber", saleOrder.getOrderNumber());
        summary.put("customerName", saleOrder.getCustomer().getName());
        summary.put("orderDate", saleOrder.getOrderDate());
        summary.put("exTaxTotal", saleOrder.getExTaxTotal());
        summary.put("inTaxTotal", saleOrder.getInTaxTotal());
        summary.put("lineCount", saleOrder.getSaleOrderLineList() != null ?
            saleOrder.getSaleOrderLineList().size() : 0);
        summary.put("status", saleOrder.getStatusSelect());

        return summary;
    }
}
```

## Complete Custom Repository Example: SaleOrderRepo

**IMPORTANT:** Axelor auto-generates `SaleOrderRepository extends JpaRepository<SaleOrder>` in `build/src-gen/`.
Only create a custom repository when you need additional query methods or computed fields.
Custom repositories extend the GENERATED repository, NOT JpaRepository directly.

```java
package com.axelor.apps.sale.db.repo;

import com.axelor.apps.base.db.Company;
import com.axelor.apps.base.db.Partner;
import com.axelor.apps.base.db.Product;
import com.axelor.apps.sale.db.SaleOrder;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

// Custom repository extending the AUTO-GENERATED SaleOrderRepository
public class SaleOrderRepo extends SaleOrderRepository {

    // Status constants (can also be defined in domain XML and auto-generated)
    public static final int STATUS_DRAFT_QUOTATION = 1;
    public static final int STATUS_FINALIZED_QUOTATION = 2;
    public static final int STATUS_ORDER_CONFIRMED = 3;
    public static final int STATUS_ORDER_COMPLETED = 4;
    public static final int STATUS_CANCELED = 5;

    // Invoice state
    public static final int INVOICE_STATE_NOT_INVOICED = 1;
    public static final int INVOICE_STATE_PARTIALLY_INVOICED = 2;
    public static final int INVOICE_STATE_FULLY_INVOICED = 3;

    // Find by order number
    public SaleOrder findByOrderNumber(String orderNumber) {
        return Query.of(SaleOrder.class)
            .filter("self.orderNumber = :orderNumber")
            .bind("orderNumber", orderNumber)
            .fetchOne();
    }

    // Find by customer
    public List<SaleOrder> findByCustomer(Partner customer) {
        return Query.of(SaleOrder.class)
            .filter("self.customer = :customer")
            .bind("customer", customer)
            .order("-orderDate")
            .fetch();
    }

    // Find by customer and status
    public List<SaleOrder> findByCustomerAndStatus(Partner customer, Integer status) {
        return Query.of(SaleOrder.class)
            .filter("self.customer = :customer AND self.statusSelect = :status")
            .bind("customer", customer)
            .bind("status", status)
            .order("-orderDate")
            .fetch();
    }

    // Find pending orders
    public List<SaleOrder> findPendingOrders(Company company) {
        return Query.of(SaleOrder.class)
            .filter("self.company = :company AND self.statusSelect IN :statuses")
            .bind("company", company)
            .bind("statuses", List.of(STATUS_DRAFT_QUOTATION, STATUS_FINALIZED_QUOTATION))
            .order("-orderDate")
            .fetch();
    }

    // Find confirmed orders in date range
    public List<SaleOrder> findConfirmedOrdersByDateRange(
            Company company, LocalDate startDate, LocalDate endDate) {
        return Query.of(SaleOrder.class)
            .filter("self.company = :company " +
                    "AND self.statusSelect >= :minStatus " +
                    "AND self.orderDate >= :startDate " +
                    "AND self.orderDate <= :endDate")
            .bind("company", company)
            .bind("minStatus", STATUS_ORDER_CONFIRMED)
            .bind("startDate", startDate)
            .bind("endDate", endDate)
            .order("-orderDate")
            .fetch();
    }

    // Find high value orders
    public List<SaleOrder> findHighValueOrders(Company company, BigDecimal minAmount) {
        return Query.of(SaleOrder.class)
            .filter("self.company = :company " +
                    "AND self.exTaxTotal >= :minAmount " +
                    "AND self.statusSelect != :canceledStatus")
            .bind("company", company)
            .bind("minAmount", minAmount)
            .bind("canceledStatus", STATUS_CANCELED)
            .order("-exTaxTotal")
            .fetch();
    }

    // Find orders containing product
    public List<SaleOrder> findOrdersContainingProduct(Product product) {
        return Query.of(SaleOrder.class)
            .filter("EXISTS (SELECT 1 FROM SaleOrderLine line " +
                    "WHERE line.saleOrder = self AND line.product = :product)")
            .bind("product", product)
            .order("-orderDate")
            .fetch();
    }

    // Find orders with custom query
    public List<SaleOrder> findOrdersToInvoice(Company company) {
        return Query.of(SaleOrder.class)
            .filter("self.company = :company " +
                    "AND self.statusSelect = :status " +
                    "AND self.invoiceState != :fullyInvoiced")
            .bind("company", company)
            .bind("status", STATUS_ORDER_CONFIRMED)
            .bind("fullyInvoiced", INVOICE_STATE_FULLY_INVOICED)
            .order("-orderDate")
            .fetch();
    }

    // Count orders by customer
    public Long countByCustomer(Partner customer) {
        return Query.of(SaleOrder.class)
            .filter("self.customer = :customer")
            .bind("customer", customer)
            .count();
    }

    // Count confirmed orders
    public Long countConfirmedOrders(Company company, LocalDate startDate, LocalDate endDate) {
        return Query.of(SaleOrder.class)
            .filter("self.company = :company " +
                    "AND self.statusSelect >= :minStatus " +
                    "AND self.orderDate >= :startDate " +
                    "AND self.orderDate <= :endDate")
            .bind("company", company)
            .bind("minStatus", STATUS_ORDER_CONFIRMED)
            .bind("startDate", startDate)
            .bind("endDate", endDate)
            .count();
    }

    // Sum total by company and period
    public BigDecimal sumTotalByCompanyAndPeriod(
            Company company, LocalDate startDate, LocalDate endDate) {
        String jpql = "SELECT SUM(self.exTaxTotal) FROM SaleOrder self " +
                      "WHERE self.company = :company " +
                      "AND self.statusSelect >= :minStatus " +
                      "AND self.orderDate >= :startDate " +
                      "AND self.orderDate <= :endDate";

        BigDecimal result = (BigDecimal) Query.of(BigDecimal.class)
            .filter(jpql)
            .bind("company", company)
            .bind("minStatus", STATUS_ORDER_CONFIRMED)
            .bind("startDate", startDate)
            .bind("endDate", endDate)
            .fetchOne();

        return result != null ? result : BigDecimal.ZERO;
    }

    // Get order statistics by status
    public List<Object[]> getOrderStatsByStatus(Company company) {
        String jpql = "SELECT self.statusSelect, COUNT(self), SUM(self.exTaxTotal) " +
                      "FROM SaleOrder self " +
                      "WHERE self.company = :company " +
                      "GROUP BY self.statusSelect " +
                      "ORDER BY self.statusSelect";

        return (List<Object[]>) Query.of(Object[].class)
            .filter(jpql)
            .bind("company", company)
            .fetch();
    }

    // Check if order number exists
    public boolean existsByOrderNumber(String orderNumber) {
        return Query.of(SaleOrder.class)
            .filter("self.orderNumber = :orderNumber")
            .bind("orderNumber", orderNumber)
            .count() > 0;
    }

    // Find with pagination
    public List<SaleOrder> findByCustomerPaginated(
            Partner customer, int pageNumber, int pageSize) {
        int offset = (pageNumber - 1) * pageSize;
        return Query.of(SaleOrder.class)
            .filter("self.customer = :customer")
            .bind("customer", customer)
            .order("-orderDate")
            .fetch(pageSize, offset);
    }
}
```

## Complete Controller Example: SaleOrderController

```java
package com.axelor.apps.sale.web;

import com.axelor.apps.base.db.Company;
import com.axelor.apps.base.db.Partner;
import com.axelor.apps.base.db.repo.CompanyRepository;
import com.axelor.apps.base.db.repo.PartnerRepository;
import com.axelor.apps.base.service.app.AppBaseService;
import com.axelor.apps.base.service.user.UserService;
import com.axelor.apps.sale.db.Invoice;
import com.axelor.apps.sale.db.SaleOrder;
import com.axelor.apps.sale.db.StockMove;
import com.axelor.apps.sale.db.repo.SaleOrderRepository;
import com.axelor.apps.sale.service.SaleOrderService;
import com.axelor.apps.sale.service.SaleOrderWorkflowService;
import com.axelor.exception.service.TraceBackService;
import com.axelor.inject.Beans;
import com.axelor.meta.schema.actions.ActionView;
import com.axelor.rpc.ActionRequest;
import com.axelor.rpc.ActionResponse;
import com.axelor.rpc.Context;
import java.time.LocalDate;
import java.util.Map;

// IMPORTANT: Controllers are NOT singletons and do NOT use @Inject
// Controllers use Beans.get() to access services
public class SaleOrderController {

    // NO @Inject in controllers - use Beans.get() directly in methods

    // ==================== Form Actions ====================

    public void onNew(ActionRequest request, ActionResponse response) {
        try {
            Company company = Beans.get(UserService.class).getActiveCompany();

            if (company != null) {
                response.setValue("company", company);
                response.setValue("currency", company.getCurrency());
                response.setValue("priceList", company.getDefaultSalePriceList());
                response.setValue("stockLocation", company.getDefaultStockLocation());
            }

            LocalDate today = Beans.get(AppBaseService.class).getTodayDate(company);
            response.setValue("orderDate", today);
            response.setValue("creationDate", today);
            response.setValue("statusSelect", SaleOrderRepository.STATUS_DRAFT_QUOTATION);

            response.setAttr("customer", "domain", "self.isCustomer = true");

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    public void onLoad(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            if (saleOrder.getId() == null) {
                return;
            }

            Integer status = saleOrder.getStatusSelect();
            boolean isConfirmed = status != null &&
                status >= SaleOrderRepository.STATUS_ORDER_CONFIRMED;

            // Set readonly fields
            if (isConfirmed) {
                response.setAttr("customer", "readonly", true);
                response.setAttr("company", "readonly", true);
                response.setAttr("orderDate", "readonly", true);
                response.setAttr("saleOrderLineList", "readonly", true);
            }

            // Show/hide panels
            if (status != null && status == SaleOrderRepository.STATUS_ORDER_CONFIRMED) {
                response.setAttr("invoicePanel", "hidden", false);
                response.setAttr("deliveryPanel", "hidden", false);
            }

            // Button visibility
            response.setAttr("finalizeBtn", "hidden",
                status == null || status != SaleOrderRepository.STATUS_DRAFT_QUOTATION);
            response.setAttr("confirmBtn", "hidden", isConfirmed);
            response.setAttr("completeBtn", "hidden",
                status == null || status != SaleOrderRepository.STATUS_ORDER_CONFIRMED);
            response.setAttr("cancelBtn", "hidden",
                status != null && status == SaleOrderRepository.STATUS_CANCELED);

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // ==================== onChange Actions ====================

    public void onChangeCustomer(ActionRequest request, ActionResponse response) {
        try {
            Context context = request.getContext();
            Partner customer = (Partner) context.get("customer");

            if (customer == null) {
                return;
            }

            customer = Beans.get(PartnerRepository.class).find(customer.getId());

            // Set customer-related fields
            response.setValue("priceList", customer.getSalePriceList());
            response.setValue("paymentMode", customer.getPaymentMode());
            response.setValue("paymentCondition", customer.getPaymentCondition());
            response.setValue("deliveryAddress", customer.getMainAddress());
            response.setValue("invoiceAddress", customer.getInvoicingAddress());
            response.setValue("currency", customer.getCurrency());
            response.setValue("fiscalPosition", customer.getFiscalPosition());

            // Set domains
            response.setAttr("contactPartner", "domain",
                "self.mainPartner.id = " + customer.getId());

            // Warnings
            if (customer.getBlocked()) {
                response.setNotify("Warning: Customer is blocked", "warning");
            }

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    public void onChangeCompany(ActionRequest request, ActionResponse response) {
        try {
            Company company = (Company) request.getContext().get("company");

            if (company == null) {
                return;
            }

            company = Beans.get(CompanyRepository.class).find(company.getId());

            response.setValue("currency", company.getCurrency());
            response.setValue("priceList", company.getDefaultSalePriceList());
            response.setValue("stockLocation", company.getDefaultStockLocation());

            // Update customer domain
            response.setAttr("customer", "domain",
                "self.isCustomer = true AND :company MEMBER OF self.companySet");

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    public void onChangeOrderDate(ActionRequest request, ActionResponse response) {
        try {
            LocalDate orderDate = (LocalDate) request.getContext().get("orderDate");

            if (orderDate != null) {
                LocalDate expectedDeliveryDate = orderDate.plusDays(7);
                response.setValue("expectedDeliveryDate", expectedDeliveryDate);
            }
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // ==================== Button Actions ====================

    public void finalizeQuotation(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            saleOrder = Beans.get(SaleOrderWorkflowService.class).finalize(saleOrder);

            response.setReload(true);
            response.setFlash("Quotation finalized");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    public void confirmOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            if (!Beans.get(SaleOrderWorkflowService.class).canConfirm(saleOrder)) {
                response.setError("Cannot confirm this order");
                return;
            }

            saleOrder = Beans.get(SaleOrderWorkflowService.class).confirm(saleOrder);

            response.setReload(true);
            response.setFlash("Order " + saleOrder.getOrderNumber() + " confirmed successfully");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    public void completeOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            saleOrder = Beans.get(SaleOrderWorkflowService.class).complete(saleOrder);

            response.setReload(true);
            response.setFlash("Order completed");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    public void cancelOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            if (!Beans.get(SaleOrderWorkflowService.class).canCancel(saleOrder)) {
                response.setError("Cannot cancel this order");
                return;
            }

            saleOrder = Beans.get(SaleOrderWorkflowService.class).cancel(saleOrder);

            response.setReload(true);
            response.setNotify("Order canceled");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    public void computeTotals(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            saleOrder = Beans.get(SaleOrderService.class).computeAll(saleOrder);

            response.setReload(true);
            response.setNotify("Totals computed");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    public void generateInvoice(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            Invoice invoice = Beans.get(SaleOrderService.class).generateInvoice(saleOrder);

            response.setReload(true);
            response.setFlash("Invoice generated: " + invoice.getInvoiceNumber());

            // Open generated invoice
            response.setView(ActionView
                .define("Generated Invoice")
                .model(Invoice.class.getName())
                .add("form", "invoice-form")
                .param("forceEdit", "true")
                .context("_showRecord", invoice.getId())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    public void generateDelivery(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            StockMove stockMove = Beans.get(SaleOrderService.class).generateDelivery(saleOrder);

            response.setReload(true);
            response.setFlash("Delivery generated: " + stockMove.getStockMoveSeq());

            // Open generated delivery
            response.setView(ActionView
                .define("Generated Delivery")
                .model(StockMove.class.getName())
                .add("form", "stock-move-form")
                .param("forceEdit", "true")
                .context("_showRecord", stockMove.getId())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // ==================== View Actions ====================

    public void showInvoices(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            response.setView(ActionView
                .define("Invoices")
                .model(Invoice.class.getName())
                .add("grid", "invoice-grid")
                .add("form", "invoice-form")
                .domain("self.saleOrder.id = :saleOrderId")
                .context("saleOrderId", saleOrder.getId())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    public void showDeliveries(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            response.setView(ActionView
                .define("Deliveries")
                .model(StockMove.class.getName())
                .add("grid", "stock-move-grid")
                .add("form", "stock-move-form")
                .domain("self.saleOrder.id = :saleOrderId")
                .context("saleOrderId", saleOrder.getId())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    public void showCustomerOrders(ActionRequest request, ActionResponse response) {
        try {
            Partner customer = (Partner) request.getContext().get("customer");

            if (customer == null) {
                response.setError("Please select a customer");
                return;
            }

            response.setView(ActionView
                .define("Customer Orders")
                .model(SaleOrder.class.getName())
                .add("grid", "sale-order-grid")
                .add("form", "sale-order-form")
                .domain("self.customer.id = :customerId")
                .context("customerId", customer.getId())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // ==================== Utility Actions ====================

    public void printOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            String fileLink = ReportFactory.createReport(
                    IReport.SALE_ORDER, saleOrder.getOrderNumber() + "-${date}")
                .addParam("SaleOrderId", saleOrder.getId())
                .addParam("Locale", ReportSettings.getPrintingLocale(saleOrder.getCustomer()))
                .generate()
                .getFileLink();

            response.setView(ActionView
                .define("Sale Order")
                .add("html", fileLink)
                .map());

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

## Workflow Service Example

```java
package com.axelor.apps.sale.service;

import com.axelor.apps.sale.db.SaleOrder;
import com.axelor.apps.sale.db.repo.SaleOrderRepository;
import com.axelor.apps.sale.exception.SaleExceptionMessage;
import com.axelor.exception.AxelorException;
import com.axelor.exception.db.repo.TraceBackRepository;
import com.axelor.i18n.I18n;
import com.google.inject.Inject;
import com.google.inject.persist.Transactional;
import java.lang.invoke.MethodHandles;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SaleOrderWorkflowServiceImpl implements SaleOrderWorkflowService {

    private static final Logger LOG = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());

    @Inject
    protected SaleOrderRepository saleOrderRepository;

    @Inject
    protected SaleOrderService saleOrderService;

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder draft(SaleOrder saleOrder) throws AxelorException {
        LOG.info("Setting sale order to draft: {}", saleOrder.getId());

        saleOrder.setStatusSelect(SaleOrderRepository.STATUS_DRAFT_QUOTATION);

        return saleOrderRepository.save(saleOrder);
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder finalize(SaleOrder saleOrder) throws AxelorException {
        LOG.info("Finalizing sale order: {}", saleOrder.getId());

        validateTransition(saleOrder,
            saleOrder.getStatusSelect(),
            SaleOrderRepository.STATUS_FINALIZED_QUOTATION);

        Beans.get(SaleOrderService.class).validate(saleOrder);

        saleOrder.setStatusSelect(SaleOrderRepository.STATUS_FINALIZED_QUOTATION);

        return saleOrderRepository.save(saleOrder);
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder confirm(SaleOrder saleOrder) throws AxelorException {
        LOG.info("Confirming sale order: {}", saleOrder.getId());

        validateTransition(saleOrder,
            saleOrder.getStatusSelect(),
            SaleOrderRepository.STATUS_ORDER_CONFIRMED);

        return Beans.get(SaleOrderService.class).confirm(saleOrder);
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder complete(SaleOrder saleOrder) throws AxelorException {
        LOG.info("Completing sale order: {}", saleOrder.getId());

        validateTransition(saleOrder,
            saleOrder.getStatusSelect(),
            SaleOrderRepository.STATUS_ORDER_COMPLETED);

        return Beans.get(SaleOrderService.class).complete(saleOrder);
    }

    @Override
    @Transactional(rollbackOn = {Exception.class})
    public SaleOrder cancel(SaleOrder saleOrder) throws AxelorException {
        LOG.info("Canceling sale order: {}", saleOrder.getId());

        if (!canCancel(saleOrder)) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(SaleExceptionMessage.SALE_ORDER_CANNOT_CANCEL)
            );
        }

        return Beans.get(SaleOrderService.class).cancel(saleOrder);
    }

    @Override
    public boolean canFinalize(SaleOrder saleOrder) {
        return saleOrder != null &&
               saleOrder.getStatusSelect() != null &&
               saleOrder.getStatusSelect().equals(SaleOrderRepository.STATUS_DRAFT_QUOTATION);
    }

    @Override
    public boolean canConfirm(SaleOrder saleOrder) {
        return Beans.get(SaleOrderService.class).canConfirm(saleOrder);
    }

    @Override
    public boolean canComplete(SaleOrder saleOrder) {
        return saleOrder != null &&
               saleOrder.getStatusSelect() != null &&
               saleOrder.getStatusSelect().equals(SaleOrderRepository.STATUS_ORDER_CONFIRMED);
    }

    @Override
    public boolean canCancel(SaleOrder saleOrder) {
        return Beans.get(SaleOrderService.class).canCancel(saleOrder);
    }

    @Override
    public Map<String, Object> getWorkflowState(SaleOrder saleOrder) {
        Map<String, Object> state = new HashMap<>();

        state.put("canFinalize", canFinalize(saleOrder));
        state.put("canConfirm", canConfirm(saleOrder));
        state.put("canComplete", canComplete(saleOrder));
        state.put("canCancel", canCancel(saleOrder));
        state.put("currentStatus", saleOrder.getStatusSelect());

        return state;
    }

    @Override
    public List<String> getAvailableActions(SaleOrder saleOrder) {
        List<String> actions = new ArrayList<>();

        if (canFinalize(saleOrder)) {
            actions.add("finalize");
        }
        if (canConfirm(saleOrder)) {
            actions.add("confirm");
        }
        if (canComplete(saleOrder)) {
            actions.add("complete");
        }
        if (canCancel(saleOrder)) {
            actions.add("cancel");
        }

        return actions;
    }

    @Override
    public void validateTransition(SaleOrder saleOrder, Integer fromStatus, Integer toStatus)
            throws AxelorException {

        // Define valid transitions
        Map<Integer, List<Integer>> validTransitions = new HashMap<>();
        validTransitions.put(SaleOrderRepository.STATUS_DRAFT_QUOTATION,
            List.of(SaleOrderRepository.STATUS_FINALIZED_QUOTATION, SaleOrderRepository.STATUS_CANCELED));
        validTransitions.put(SaleOrderRepository.STATUS_FINALIZED_QUOTATION,
            List.of(SaleOrderRepository.STATUS_ORDER_CONFIRMED, SaleOrderRepository.STATUS_CANCELED));
        validTransitions.put(SaleOrderRepository.STATUS_ORDER_CONFIRMED,
            List.of(SaleOrderRepository.STATUS_ORDER_COMPLETED, SaleOrderRepository.STATUS_CANCELED));

        List<Integer> allowed = validTransitions.get(fromStatus);
        if (allowed == null || !allowed.contains(toStatus)) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(SaleExceptionMessage.SALE_ORDER_INVALID_TRANSITION),
                fromStatus, toStatus
            );
        }
    }
}
```

## Computation Service Example

```java
package com.axelor.apps.sale.service;

import com.axelor.apps.base.db.PriceList;
import com.axelor.apps.base.db.PriceListLine;
import com.axelor.apps.base.db.Product;
import com.axelor.apps.base.db.TaxLine;
import com.axelor.apps.sale.db.SaleOrder;
import com.axelor.apps.sale.db.SaleOrderLine;
import com.axelor.exception.AxelorException;
import com.google.inject.Inject;
import java.lang.invoke.MethodHandles;
import java.math.BigDecimal;
import java.math.RoundingMode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SaleOrderLineServiceImpl implements SaleOrderLineService {

    private static final Logger LOG = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());
    private static final int PRICE_SCALE = 6;
    private static final int AMOUNT_SCALE = 2;

    @Inject
    protected PriceListService priceListService;

    @Override
    public SaleOrderLine compute(SaleOrderLine line, SaleOrder saleOrder) throws AxelorException {
        LOG.debug("Computing sale order line: {}", line.getId());

        line = computePrice(line, saleOrder);
        line = computeDiscount(line, saleOrder);
        line = computeTax(line, saleOrder);
        line = computeTotals(line, saleOrder);

        return line;
    }

    @Override
    public SaleOrderLine computePrice(SaleOrderLine line, SaleOrder saleOrder)
            throws AxelorException {

        Product product = line.getProduct();
        if (product == null) {
            return line;
        }

        BigDecimal price = BigDecimal.ZERO;

        // Get price from price list
        if (saleOrder != null && saleOrder.getPriceList() != null) {
            price = priceListService.getPrice(
                saleOrder.getPriceList(),
                product,
                line.getQty()
            );
        }

        // Fallback to product sale price
        if (price.compareTo(BigDecimal.ZERO) == 0) {
            price = product.getSalePrice();
        }

        line.setPrice(price.setScale(PRICE_SCALE, RoundingMode.HALF_UP));

        return line;
    }

    @Override
    public SaleOrderLine computeDiscount(SaleOrderLine line, SaleOrder saleOrder)
            throws AxelorException {

        BigDecimal price = line.getPrice();
        BigDecimal discountPercent = line.getDiscountPercent();

        if (price == null || discountPercent == null) {
            line.setDiscountAmount(BigDecimal.ZERO);
            return line;
        }

        BigDecimal discountAmount = price
            .multiply(discountPercent)
            .divide(BigDecimal.valueOf(100), PRICE_SCALE, RoundingMode.HALF_UP);

        line.setDiscountAmount(discountAmount);

        return line;
    }

    @Override
    public SaleOrderLine computeTax(SaleOrderLine line, SaleOrder saleOrder)
            throws AxelorException {

        Product product = line.getProduct();
        if (product == null) {
            return line;
        }

        // Get tax from fiscal position or product
        TaxLine taxLine = null;
        if (saleOrder != null && saleOrder.getFiscalPosition() != null) {
            taxLine = fiscalPositionService.getTaxLine(
                saleOrder.getFiscalPosition(),
                product.getSaleTaxLine()
            );
        } else {
            taxLine = product.getSaleTaxLine();
        }

        line.setTaxLine(taxLine);

        return line;
    }

    @Override
    public SaleOrderLine computeTotals(SaleOrderLine line, SaleOrder saleOrder)
            throws AxelorException {

        BigDecimal qty = line.getQty();
        BigDecimal price = line.getPrice();
        BigDecimal discountAmount = line.getDiscountAmount();

        if (qty == null || price == null) {
            line.setExTaxTotal(BigDecimal.ZERO);
            line.setInTaxTotal(BigDecimal.ZERO);
            return line;
        }

        // Calculate net price
        BigDecimal netPrice = price.subtract(
            discountAmount != null ? discountAmount : BigDecimal.ZERO
        );

        // Calculate ex-tax total
        BigDecimal exTaxTotal = netPrice
            .multiply(qty)
            .setScale(AMOUNT_SCALE, RoundingMode.HALF_UP);

        line.setExTaxTotal(exTaxTotal);

        // Calculate tax amount
        BigDecimal taxAmount = BigDecimal.ZERO;
        if (line.getTaxLine() != null) {
            taxAmount = exTaxTotal
                .multiply(line.getTaxLine().getValue())
                .divide(BigDecimal.valueOf(100), AMOUNT_SCALE, RoundingMode.HALF_UP);
        }

        // Calculate in-tax total
        BigDecimal inTaxTotal = exTaxTotal.add(taxAmount);
        line.setInTaxTotal(inTaxTotal);

        return line;
    }

    @Override
    public BigDecimal getPrice(Product product, PriceList priceList) throws AxelorException {
        if (priceList == null) {
            return product.getSalePrice();
        }

        return priceListService.getPrice(priceList, product, BigDecimal.ONE);
    }

    @Override
    public void validate(SaleOrderLine line) throws AxelorException {
        if (line.getProduct() == null) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_MISSING_FIELD,
                I18n.get("Product is required")
            );
        }

        if (line.getQty() == null || line.getQty().compareTo(BigDecimal.ZERO) <= 0) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get("Quantity must be greater than zero")
            );
        }

        if (line.getPrice() == null || line.getPrice().compareTo(BigDecimal.ZERO) < 0) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get("Price cannot be negative")
            );
        }
    }

    @Override
    public SaleOrderLine copyLine(SaleOrderLine line) {
        SaleOrderLine newLine = new SaleOrderLine();
        newLine.setProduct(line.getProduct());
        newLine.setProductName(line.getProductName());
        newLine.setQty(line.getQty());
        newLine.setUnit(line.getUnit());
        newLine.setPrice(line.getPrice());
        newLine.setDiscountPercent(line.getDiscountPercent());
        newLine.setTaxLine(line.getTaxLine());
        newLine.setDescription(line.getDescription());

        return newLine;
    }
}
```

## End-to-End Feature Example: Order Confirmation

This example shows a complete flow from controller → service → repository for confirming a sale order.

### 1. User clicks "Confirm" button in UI

### 2. Controller receives request

```java
// SaleOrderController.java
public void confirmOrder(ActionRequest request, ActionResponse response) {
    try {
        // Extract order from request
        SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
        saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

        // Check if can confirm
        if (!Beans.get(SaleOrderWorkflowService.class).canConfirm(saleOrder)) {
            response.setError("Cannot confirm this order");
            return;
        }

        // Call service
        saleOrder = Beans.get(SaleOrderWorkflowService.class).confirm(saleOrder);

        // Update UI
        response.setReload(true);
        response.setFlash("Order " + saleOrder.getOrderNumber() + " confirmed");
    } catch (Exception e) {
        TraceBackService.trace(response, e);
    }
}
```

### 3. Workflow service validates transition

```java
// SaleOrderWorkflowServiceImpl.java
@Transactional(rollbackOn = {Exception.class})
public SaleOrder confirm(SaleOrder saleOrder) throws AxelorException {
    log.info("Confirming sale order: {}", saleOrder.getId());

    // Validate state transition
    validateTransition(saleOrder,
        saleOrder.getStatusSelect(),
        SaleOrderRepository.STATUS_ORDER_CONFIRMED);

    // Delegate to main service
    return Beans.get(SaleOrderService.class).confirm(saleOrder);
}
```

### 4. Main service performs business logic

```java
// SaleOrderServiceImpl.java
@Transactional(rollbackOn = {Exception.class})
public SaleOrder confirm(SaleOrder saleOrder) throws AxelorException {
    log.info("Confirming sale order: {}", saleOrder.getId());

    // Validate order
    validate(saleOrder);

    // Check if can confirm
    if (!canConfirm(saleOrder)) {
        throw new AxelorException(
            TraceBackRepository.CATEGORY_INCONSISTENCY,
            I18n.get(SaleExceptionMessage.SALE_ORDER_CANNOT_CONFIRM)
        );
    }

    // Generate sequence number
    if (saleOrder.getOrderNumber() == null) {
        String sequence = getSequence(saleOrder.getCompany());
        saleOrder.setOrderNumber(sequence);
    }

    // Update status
    saleOrder.setStatusSelect(SaleOrderRepository.STATUS_ORDER_CONFIRMED);
    saleOrder.setConfirmationDateTime(LocalDateTime.now());
    saleOrder.setConfirmedByUser(AuthUtils.getUser());

    // Save
    saleOrder = saleOrderRepository.save(saleOrder);
    log.info("Sale order confirmed with number: {}", saleOrder.getOrderNumber());

    return saleOrder;
}
```

### 5. Repository saves entity

```java
// JpaRepository base class handles save
saleOrder = saleOrderRepository.save(saleOrder);
```

### 6. Response sent back to UI

```java
// Controller updates UI
response.setReload(true);
response.setFlash("Order SO-2024-001 confirmed");
```

This complete end-to-end example demonstrates proper separation of concerns:
- **Controller**: Handles HTTP request/response, extracts data, updates UI
- **Service**: Contains business logic, validation, orchestration
- **Repository**: Manages data access and persistence

---

## Complete Example: Background Job with Batch Processing

This example shows proper batch processing in a scheduled job.

### 1. Job Implementation

```java
package com.axelor.apps.license.job;

import com.axelor.apps.license.db.License;
import com.axelor.apps.license.db.repo.LicenseRepository;
import com.axelor.apps.license.service.LicenseService;
import com.axelor.db.JPA;
import com.google.inject.Inject;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.lang.invoke.MethodHandles;
import java.time.LocalDate;
import java.util.List;

public class LicenseExpirationWarningJob implements Job {

    private static final Logger LOG = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());
    private static final int BATCH_SIZE = 20;

    @Inject
    private LicenseService licenseService;

    @Inject
    private LicenseRepository licenseRepository;

    @Inject
    private AppGuardianService appGuardianService;

    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        LOG.info("Starting license expiration warning job");

        try {
            int daysBeforeExpiration = appGuardianService.getAppGuardian().getDaysBeforeExpiration();
            Template template = appGuardianService.getAppGuardian().getExpirationWarningTemplate();

            LocalDate now = LocalDate.now();
            LocalDate endDate = now.plusDays(daysBeforeExpiration);

            // Count total licenses using repository
            long count = licenseRepository.countExpiringLicenses(now, endDate);

            log.debug("Found {} licenses expiring within the next {} days", count, daysBeforeExpiration);

            // Process in batches
            processExpiringLicenses(now, endDate, template);

            log.info("License expiration warning job completed");
        } catch (Exception e) {
            log.error("Error in license expiration warning job", e);
            throw new JobExecutionException(e);
        }
    }

    private void processExpiringLicenses(LocalDate now, LocalDate endDate, Template template) {
        int offset = 0;
        List<License> licenses;

        do {
            licenses = licenseRepository.findExpiringLicenses(now, endDate, BATCH_SIZE, offset);

            // Process batch
            for (License license : licenses) {
                try {
                    licenseService.sendExpirationWarning(license, template);
                } catch (Exception e) {
                    log.error("Error sending expiration warning for license: {}",
                        license.getId(), e);
                }
            }

            // CRITICAL: Clear JPA context to free memory
            JPA.clear();

            offset += BATCH_SIZE;
        } while (!licenses.isEmpty());
    }
}
```

### 2. Job Configuration (XML)

```xml
<job name="license-expiration-warning-job"
     class="com.axelor.apps.license.job.LicenseExpirationWarningJob">
  <description>Send expiration warnings for licenses expiring soon</description>
  <trigger>
    <!-- Run every day at 8 AM -->
    <cron>0 0 8 * * ?</cron>
  </trigger>
</job>
```

**Key Points:**
- Repository methods encapsulate queries
- Batch processing with JPA.clear() prevents memory leaks
- Loggers helper for clean logging
- Error handling per-item doesn't stop batch
- Clean separation of concerns

---

## Complete Example: Repository with save() Override

This example shows computed field pattern in repositories.

### 1. Repository Implementation

```java
package com.axelor.apps.license.db.repo;

import com.axelor.apps.license.db.License;
import com.axelor.db.JPA;
import java.util.StringJoiner;

// Custom repository extending the AUTO-GENERATED LicenseRepository
public class LicenseRepo extends LicenseRepository {

    @Override
    public License save(License entity) {
        // First save to get ID and relationships
        License license = super.save(entity);

        // Compute derived name field
        StringJoiner stringJoiner = new StringJoiner(" - ");
        stringJoiner.add(license.getApplication().getName())
                    .add(license.getLicenseUsage().getName());

        if (license.getLicenseScope() != null) {
            stringJoiner.add(license.getLicenseScope().getName());
        }

        // Set computed field
        license.setName(stringJoiner.toString());

        // Second save with computed values
        return JPA.save(license);
    }
}
```

### 2. Domain Model

```xml
<entity name="License">
  <many-to-one name="application" ref="LicenseApplication" required="true"/>
  <many-to-one name="licenseUsage" ref="LicenseUsage" required="true"/>
  <many-to-one name="licenseScope" ref="LicenseScope"/>

  <!-- Computed field -->
  <string name="name" max="512" readonly="true"/>
</entity>
```

### 3. Service Using Repository

```java
package com.axelor.apps.license.service;

import com.axelor.apps.license.db.License;
import com.axelor.apps.license.db.repo.LicenseRepository;
import com.google.inject.Inject;
import com.google.inject.persist.Transactional;

public class LicenseServiceImpl implements LicenseService {

    @Inject
    protected LicenseRepository licenseRepository;

    @Override
    @Transactional(rollbackOn = Exception.class)
    public License create(LicenseApplication application, LicenseUsage usage, LicenseScope scope) {
        License license = new License();
        license.setApplication(application);
        license.setLicenseUsage(usage);
        license.setLicenseScope(scope);

        // Repository automatically computes name on save
        return licenseRepository.save(license);
    }
}
```

**Key Points:**
- Double-save pattern: super.save() then JPA.save()
- Computed field automatically updated
- Service code stays clean
- Name field marked readonly in XML

---

This comprehensive examples document provides real, working code that demonstrates all the key patterns in Axelor development.
