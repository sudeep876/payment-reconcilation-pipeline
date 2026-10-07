# Source System Design

## 1. Overview

PayFlow receives transaction data from multiple external
payment processors.

Different processors may use different integration mechanisms
and delivery frequencies.

The initial implementation focuses on BANK_A.

---

## 2. BANK_A

### Integration Type

Batch file delivery.

### File Format

CSV.

### Frequency

Hourly.

### Expected Delivery

One transaction file per hour.

### Example File

bank_a_transactions_20261007_0800.csv