# Coding Missions S2 E2
# KPDH Rumi ACH Takedown
# Coding modules that determine AML violations that require
# a SAR (Suspicious Activity Report), CTR (Currency Transaction Report),
# determine which cases are filed for SAR, and include the lookback
# date of 120 days or oldest first transaction
# for any AML investigation.

# Suspect not ready for the takedown,
# Filing them for a world of pain!

# 1/19/2026 (MLK Special)

# Author: Jason Lu

# Test the system
from sys import version

print(version)

# Imports
import unittest
from datetime import date, datetime, timedelta
from collections import defaultdict

# Check Python version.


# Module 1: SAR or no SAR
def sar_or_no_sar(transaction_amount, suspect_identified, reason):
    """
    Determines if a SAR should or should not be filed using a
    match-case statement design.

    Params:
    @transaction_amount: The amount (in US dollars) in question.
    @suspect_identified: Boolean to determine if suspect found.
    @reason: the reason for SAR filing. Blank if no-SAR.

    Returns: String to file or not file a SAR.
    """
    try:
        amount = float(transaction_amount)
        if suspect_identified == True:
            if amount > 5000:
                if reason in ("Structuring", "Unknown Source Of Funds"):
                    return (
                        "File a SAR: Transaction is over $5000 and "
                        "Suspect identified."
                    )
            elif amount == 5000:
                return "Do not file a SAR: Transaction is at $5000."
            else:
                return (
                    "Do not file a SAR: Transaction is $5000 or "
                    "less, even with idenitifed suspect."
                )
        elif suspect_identified == False:
            if amount > 25000:
                if reason in ("Structuring", "Unknown Source Of Funds"):
                    return (
                        "File a SAR: Transaction is over $25000 and"
                        "suspect is not identified"
                    )
                elif amount == 25000:
                    return "Do not file a SAR: Transaction is at $25000"
                else:
                    return (
                        "Do not file a SAR: Transaction is $25000 or "
                        "less and suspect is not identified"
                    )
        else:
            return "Error: Invalid value or suspect identified"
    except (ValueError, TypeError, NameError):
        return "Error: Transaction amount invalid. Please enter a valid number."


# Module 2: CTR filing
def should_file_ctr(transactions):
    """
    Determines whether a Currency Transaction Report (CTR) should
    be filed based on a list of
    customer transactions.

    A CTR is required if:
    1. A single cash transaction (deposit or withdrawal) exceeds $10000.
    2. The total of all cash transactions on a single business
    day exceeds $10000.
    3. Transactions must have an amount greater than $0 to be
    considered.

    Args:
    transactions: (list of dict): A list of transaction dictionaries,
    where each dictionary contains 'date', 'type'
    ('deposit' or 'withdrawal') and 'amount'
    Returns:
    daily_totals = defaultdict(float)
    """
    daily_totals = defaultdict(float)
    for transaction in transactions:
        # Only consider transactions with a positive amount.
        # Skips any transaction below $0.
        if transaction["amount"] > 0:
            # Condition 1: Check for any single transaction over $10000.
            if transaction["amount"] > 10000:
                return True
        # Aggregate transactions for the day.
        daily_totals[transaction["date"]] += transaction["amount"]

    # Condition 2: Check if aggregated total for any single day
    # exceeds $10000.
    for total in daily_totals.values():
        if total > 10000:
            return True


# Module 3: Get effective transaction lookback date.
# Date: 10/31/2025
# Lookback date (120 days prior): 07/03/2025
# Transaction: Zoey (Ramyun!): 06/16/2025
# New lookback date: 06/16/2025
# Review date: 06/16/2025 - 10/31/2025

# Future work: extended, shortened, split


def get_effective_transaction_dates(transactions, review_date_str):
    """
    Calculates effective date for transactions based on 120-day
    lookback period.
    Args:
    transactions: A list of tuples, where each tuple contains a
    transaction ID and a date string in 'YYYY-MM-DD' format.
    review_date_str: The review date

    Returns:
    A list of effective date strings in 'YYYY-MM-DD' format.
    """
    if not transactions:
        return []
    # Convert review date string to a datetime object
    review_date = datetime.strptime(review_date_str, "%Y-%m-%d")
    # Calculate the lookback date (review date - 120 days)
    # timedelta a built-in Python 3.10 function to add or subtract days.
    lookback_date = review_date - timedelta(days=120)
    effective_dates = []
    # For each transaction date string in transactions, determine
    # the effective dates for lookback.
    for _, transaction_date_str in transactions:
        transaction_date = datetime.strptime(transaction_date_str, "%Y-%m-%d")
        # If transaction is older than lookback period, use lookback date.
        if transaction_date < lookback_date:
            effective_dates.append(lookback_date.strftime("%Y-%m-%d"))
        # Otherwise, use the original transaction date.
        else:
            effective_dates.append(transaction_date_str)
    return effective_dates


# Module 4: SAR determinant function.
def is_case_sar(cases, is_sar, case_num):
    # Global variable in redesign.
    sar = ["AML-123456789", "AML-987654321", "AML-0192837465"]
    """
    Function to determine if a case  in the workspace is part of
    a set of cases that were filed for SARs.
    Params:
    cases: a list of cases that was given to analytics for determining
    if a particular case is SAR or no SAR
    is_sar: Boolean that returns True if case is SAR, false otherwise,
    used as a sentinel boolean to type check logic.
    case_num: The case numerical position in the workspace queue.
    """
    list_sar = []  # begin with empty workspace queue
    if cases is None or len(cases) == 0 or is_sar == False:
        return []
    else:
        for case in cases:
            if case in sar:
                print("Case number is: ", str(case_num))
                is_sar = True
                list_sar.append(case)
            elif case not in sar:
                continue  # continuing searching through workspace queue
            else:
                is_sar = False
                print("No case can be filed for SAR.")
    # Return a list comprehension for the cases that are filed for SAR.
    return [case for case in list_sar]


# Unit tests
# 21 test cases total, about half of the real TDD.
# Future work: Extension or reduction of lookback period,
# mixed transaction cases, even prior SAR cases,
# but that is beyond scope of episode.
class UnitTests(unittest.TestCase):
    """
    Test Suite for all four module methods for AML transaction monitor.
    Note, the test cases are extremely basic for TDD. A real life
    example would have well over 50-100 test cases per SAR, CTR,
    or transaction date lookback.
    """

    # Test Suite 1: SAR or no SAR.
    def setUp(self):
        return

    def test_init(self):
        self.assertTrue(True, sar_or_no_sar(0, True, ""))
        self.assertFalse(False, sar_or_no_sar(0, False, ""))

    def test_sar(self):
        self.assertTrue(sar_or_no_sar(10000, True, "Structuring"))
        self.assertFalse(sar_or_no_sar(5000, False, "Unknown Source Of Funds"))

    def test_no_sar(self):
        # Rare case of $0 for money with a suspect for structuring.
        self.assertTrue(sar_or_no_sar(0, True, "Structuring"))
        self.assertFalse(sar_or_no_sar(3000, False, "Unknown Source Of Funds"))

    def test_invalid_amount_sar(self):
        # Invalid amount should result in error.
        self.assertTrue(sar_or_no_sar("not a number", True, "Structuring"))
        self.assertFalse(sar_or_no_sar("-9", False, "OTM P2P Structuring"))

    def test_edge_case_suspect_identified(self):
        self.assertTrue(sar_or_no_sar(5000.01, True, "Structuring"))

    def test_edge_case_suspect_not_identified(self):
        self.assertTrue(sar_or_no_sar(25000.01, False, "Structuring"))

    # Test Suite 2: CTR Filing.
    def test_single_transaction_over_10k(self):
        """
        Test Case 1: Single deposit over $10K, CTR required.
        """
        transactions = [
            {"date": date(2023, 10, 26), "type": "deposit", "amount": 11000},
            {"date": date(2023, 10, 27), "type": "withdrawal", "amount": 500},
        ]
        self.assertTrue(should_file_ctr(transactions))

    def test_aggregated_transactions_over_10k(self):
        """
        Test Case 2: Multiple transactions summing over $10K, CTR required.
        """
        transactions = [
            {"date": date(2023, 10, 26), "type": "deposit", "amount": 6000},
            {"date": date(2023, 10, 27), "type": "withdrawal", "amount": 5000},
            {"date": date(2023, 10, 27), "type": "deposit", "amount": 3000},
        ]
        self.assertIsNone(should_file_ctr(transactions))

    def test_no_ctr_required(self):
        """
        Test Case 3: No CTR required.
        """
        transactions = [
            {"date": date(2023, 10, 26), "type": "deposit", "amount": 5000},
            {"date": date(2023, 10, 27), "type": "withdrawal", "amount": 5000},
        ]
        self.assertFalse(should_file_ctr(transactions))

    def test_zero_and_negative_amount_transactions(self):
        """
        Test Case 4: Transactions with zero or negative amount ignored.
        """
        transactions = [
            {"date": date(2023, 10, 26), "type": "deposit", "amount": 9000},
            {"date": date(2023, 10, 26), "type": "deposit", "amount": 0},
            {"date": date(2023, 10, 26), "type": "deposit", "amount": -1000},
            {"date": date(2023, 10, 27), "type": "withdrawal", "amount": 1001},
            {"date": date(2023, 10, 27), "type": "withdrawal", "amount": 100},
        ]
        self.assertIsNone(should_file_ctr(transactions))

    def test_only_zero_and_negative_amounts(self):
        """
        Test Case 5: Transactions only zero or negative amounts ignored.
        """
        transactions = [
            {"date": date(2023, 10, 26), "type": "deposit", "amount": 0},
            {"date": date(2023, 10, 26), "type": "deposit", "amount": -1000},
            {"date": date(2023, 10, 27), "type": "withdrawal", "amount": 0},
        ]
        self.assertFalse(should_file_ctr(transactions))

    def test_no_transaction_over_10k_nonzero_amounts(self):
        """
        Test Case 6: CTR should still not be filed even if
        transaction is valid due to negative or zero amounts.
        """
        transactions = [
            {"date": date(2023, 10, 26), "type": "deposit", "amount": 1000},
            {"date": date(2023, 10, 27), "type": "withdrawal", "amount": -500},
            {"date": date(2023, 10, 27), "type": "deposit", "amount": 0},
        ]
        self.assertFalse(should_file_ctr(transactions))

    # Test Suite 3: 120 Day lookback period.
    # Setup function.
    def setUp(self):
        self.review_date = "2024-12-01"
        # Lookback date: 2024-12-01 minus 120 days = 2024-08-03
        self.lookback_date_str = "2024-08-03"
        # Leap year date edge cases.
        self.review_date_leap = "2020-03-01"
        self.lookback_date_str_leap = "2019-11-02"

    def test_transaction_older_than_lookback(self):
        """
        Test #1: Tests if lookback date is returned for transaction
        older than 120 days. Rumi's KPDH transaction test case.
        """
        transactions = [("TXN001-Rumi-ACH-Deposit", "2024-06-15")]
        expected = [self.lookback_date_str]
        result = get_effective_transaction_dates(transactions, self.review_date)
        self.assertEqual(result, expected)

    def test_transaction_within_lookback(self):
        """
        Test #2: Tests the original date is returned for
        a transaction within 120 days.
        """
        transactions = [("TXN123-Zoey-Mira-P2P", "2024-08-03")]
        expected = [self.lookback_date_str]
        result = get_effective_transaction_dates(transactions, self.review_date)
        self.assertEqual(result, expected)

    def test_transaction_on_boundary(self):
        """
        Test #3: Tests the original date is returned for
        a transaction within 120 days.
        """
        transactions = [("TXN321-Saja-Boys-FC-Deposit", self.lookback_date_str)]
        expected = [self.lookback_date_str]
        result = get_effective_transaction_dates(transactions, self.review_date)
        self.assertEqual(result, expected)

    def test_mixed_transactions(self):
        """
        Test #4: Tests a list with a mix of old and recent transactions.
        """
        transactions = [
            ("TXN321-Saja-Boys-FC-Deposit", "2024-05-01"),
            ("TXN345-KPDH-ACH", "2024-09-01"),
            ("TXN890-WhatItSoundsLike-P2P", "2024-11-25"),
        ]
        expected = [self.lookback_date_str, "2024-09-01", "2024-11-25"]
        result = get_effective_transaction_dates(transactions, self.review_date)
        self.assertEqual(result, expected)

    def test_no_transactions(self):
        """
        Test #5: Tests no transactions, empty list.
        """
        transactions = []
        expected = []
        result = get_effective_transaction_dates(transactions, self.review_date)
        self.assertEqual(result, expected)

    # Edge case for leap year.
    def test_edge_case_leap_year(self):
        """
        Test #6: Test a transaction tuple that has a leap year
        edge case.
        """
        transactions = [
            ("TXN321-Saja-Boys-FC-Deposit", "2019-05-01"),
            ("TXN345-KPDH-ACH", "2020-03-01"),
            ("TXN890-WhatItSoundsLike-P2P", "2020-11-02"),
        ]
        expected = [self.lookback_date_str_leap, "2020-03-01", "2020-11-02"]
        result = get_effective_transaction_dates(transactions, self.review_date_leap)
        self.assertEqual(result, expected)

    # Test Suite 4: SAR determinant.
    sar = ["AML-123456789", "AML-987654321", "AML-0192837465"]
    empty = []
    cases_1 = ["AML-123456789", "AML-123456709"]
    cases_2 = ["AML-123456121", "AML-123456123"]

    """
    Test 1: Empty list, no SAR case found.
    """

    def test_empty_sar(self):
        self.assertEqual([], is_case_sar(self.empty, False, 123))

    """
    Test 2: SAR case found in the list.
    """

    def test_sar_found(self):
        self.assertEqual(["AML-123456789"], is_case_sar(self.cases_1, True, 321))

    """
    Test 3: SAR case not found in the list.
    """

    def test_sar_not_found(self):
        self.assertEqual([], is_case_sar(self.cases_2, False, 321))


if __name__ == "__main__":
    unittest.main()
