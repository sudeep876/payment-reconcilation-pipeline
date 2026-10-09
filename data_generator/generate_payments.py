
import argparse
import csv
import random
import time
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path


INTERNAL_FIELDS = [
    "payment_id",
    "merchant_id",
    "customer_id",
    "processor",
    "amount",
    "currency",
    "payment_method",
    "payment_timestamp",
    "status",
    "order_id",
    "created_at",
    "updated_at",
]

PROCESSOR_FIELDS = [
    "processor_txn_id",
    "processor",
    "merchant_reference",
    "amount",
    "currency",
    "transaction_timestamp",
    "settlement_date",
    "status",
    "fee",
    "net_amount",
    "received_at",
]


def generate_payments(rows: int, seed: int, output_dir: Path) -> None:
    if rows < 1:
        raise ValueError("rows must be at least 1")

    rng = random.Random(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    internal_path = output_dir / "internal_payments.csv"
    processor_path = (
        output_dir / "bank_a_transactions_20261007_0800.csv"
    )

    start_time = datetime(2026, 10, 7, 8, 0, 0)
    received_time = datetime(2026, 10, 7, 9, 0, 0)

    methods = ["UPI", "CARD", "NETBANKING"]
    statuses = ["SUCCESS", "FAILED"]

    started = time.perf_counter()

    with (
        internal_path.open("w", newline="", encoding="utf-8") as internal_file,
        processor_path.open("w", newline="", encoding="utf-8") as processor_file,
    ):
        internal_writer = csv.DictWriter(
            internal_file, fieldnames=INTERNAL_FIELDS
        )
        processor_writer = csv.DictWriter(
            processor_file, fieldnames=PROCESSOR_FIELDS
        )

        internal_writer.writeheader()
        processor_writer.writeheader()

        for i in range(1, rows + 1):
            payment_id = f"PAY_{i:09d}"
            processor_txn_id = f"BANK_{i:09d}"

            merchant_id = f"MER_{rng.randint(1, 1000):06d}"
            customer_id = f"CUS_{rng.randint(1, 100000):08d}"
            order_id = f"ORD_{i:09d}"

            # Generate monetary values in cents to avoid float errors.
            amount = Decimal(rng.randint(100, 500000)) / Decimal("100")
            fee = (amount * Decimal("0.01")).quantize(
                Decimal("0.01")
            )
            net_amount = amount - fee

            payment_time = start_time + timedelta(seconds=i - 1)
            created_time = payment_time + timedelta(seconds=1)
            status = rng.choices(
                statuses, weights=[95, 5], k=1
            )[0]

            common_amount = f"{amount:.2f}"

            internal_writer.writerow({
                "payment_id": payment_id,
                "merchant_id": merchant_id,
                "customer_id": customer_id,
                "processor": "BANK_A",
                "amount": common_amount,
                "currency": "INR",
                "payment_method": rng.choice(methods),
                "payment_timestamp": payment_time.isoformat(sep=" "),
                "status": status,
                "order_id": order_id,
                "created_at": created_time.isoformat(sep=" "),
                "updated_at": created_time.isoformat(sep=" "),
            })

            processor_writer.writerow({
                "processor_txn_id": processor_txn_id,
                "processor": "BANK_A",
                "merchant_reference": payment_id,
                "amount": common_amount,
                "currency": "INR",
                "transaction_timestamp": (
                    payment_time + timedelta(seconds=3)
                ).isoformat(sep=" "),
                "settlement_date": "2026-10-08",
                "status": status,
                "fee": f"{fee:.2f}",
                "net_amount": f"{net_amount:.2f}",
                "received_at": received_time.isoformat(sep=" "),
            })

    elapsed = time.perf_counter() - started

    print("PAYMENT DATA GENERATION COMPLETE")
    print(f"Internal records:  {rows:,}")
    print(f"Processor records: {rows:,}")
    print(f"Internal file:     {internal_path}")
    print(f"Processor file:    {processor_path}")
    print(f"Internal size:     {internal_path.stat().st_size:,} bytes")
    print(f"Processor size:    {processor_path.stat().st_size:,} bytes")
    print(f"Generation time:   {elapsed:.2f} seconds")
    print(f"Random seed:       {seed}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate synthetic payment reconciliation data."
    )
    parser.add_argument("--rows", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/generated"),
    )
    args = parser.parse_args()

    generate_payments(args.rows, args.seed, args.output_dir)


if __name__ == "__main__":
    main()