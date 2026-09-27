"""Tests for the branch report.

Run them with:  pytest -v

These tests never touch the database. They pass small lists straight into the
function, which is why they run in milliseconds and give the same answer every time.
"""
from branch_report import flag_large_withdrawals, format_kwd


def test_flags_a_withdrawal_above_the_threshold():
    withdrawals = [{"amount_kwd": 15000.0}]
    assert len(flag_large_withdrawals(withdrawals, threshold=10000)) == 1


def test_ignores_a_small_withdrawal():
    withdrawals = [{"amount_kwd": 250.0}]
    assert flag_large_withdrawals(withdrawals, threshold=10000) == []


def test_flags_a_withdrawal_exactly_on_the_threshold():
    """A withdrawal of exactly 10,000 KWD must be reviewed.

    The rule says "at or above". A transaction sitting exactly on the line is the
    one a reviewer most needs to see, so it counts.
    """
    withdrawals = [{"amount_kwd": 10000.0}]
    assert len(flag_large_withdrawals(withdrawals, threshold=10000)) == 1


def test_keeps_only_the_large_ones():
    withdrawals = [
        {"amount_kwd": 120.5},
        {"amount_kwd": 18400.0},
        {"amount_kwd": 9999.999},
        {"amount_kwd": 10000.0},
    ]
    flagged = flag_large_withdrawals(withdrawals, threshold=10000)
    assert len(flagged) == 2


def test_format_kwd_uses_three_decimals():
    assert format_kwd(1234.5) == "1,234.500 KWD"