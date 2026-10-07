# Payment Reconciliation Pipeline — Data Contract

## 1. Purpose

This document defines the structure, meaning, data types, and
validation rules for the datasets used by the Payment
Reconciliation Pipeline.

The pipeline initially uses three logical datasets:

1. Internal Payments
2. Processor Transactions
3. Reconciliation Results

---

# 2. Internal Payments

The Internal Payments dataset represents the transaction record
maintained by PayFlow's internal payment system.

## Schema

| Column | Type | Required | Description |
|---|---|---|---|
| payment_id | STRING | Yes | Unique internal payment identifier |
| merchant_id | STRING | Yes | Merchant associated with the payment |
| customer_id | STRING | Yes | Customer who initiated the payment |
| processor | STRING | Yes | Processor selected for the transaction |
| amount | DECIMAL(18,2) | Yes | Payment amount |
| currency | STRING | Yes | ISO currency code |
| payment_method | STRING | Yes | Payment method such as UPI, CARD, NETBANKING |
| payment_timestamp | TIMESTAMP | Yes | Time when payment was initiated |
| status | STRING | Yes | Internal payment status |
| order_id | STRING | Yes | Merchant order identifier |
| created_at | TIMESTAMP | Yes | Record creation timestamp |
| updated_at | TIMESTAMP | Yes | Last record update timestamp |

## Example

textpayment_id: PAY_000001
merchant_id: MER_00123
customer_id: CUS_98473
processor: BANK_A
amount: 1499.00
currency: INR
payment_method: UPI
payment_timestamp: 2026-10-07 08:12:31
status: SUCCESS
order_id: ORD_827361
created_at: 2026-10-07 08:12:32
updated_at: 2026-10-07 08:12:32