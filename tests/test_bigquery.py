import pytest
from src.bigquery_ops import run_query


def test_run_query():
    result = run_query("SELECT 1 as test_value")
    rows = list(result)
    assert rows[0].test_value == 1
