"""Failing test (TDD red) for the weather ingestion upsert.

Contract being specified: ingesting weather for a given date is IDEMPOTENT.
Running it twice for the same date must leave EXACTLY ONE row in
`daily_automated_data`, holding the LATEST value. That's the same
on-conflict-do-update behaviour you already wrote in create_mood, now
pointed at the new table.

This test FAILS until you implement the upsert. The first failure you'll see
is an ImportError, because `upsert_weather` doesn't exist yet -- that's the
point of a red test. You own the implementation; if you choose a different
name/signature/module, just update the import and the two calls below.

NOTE: this test queries `daily_automated_data`, so the table must exist --
run the migration first, or you'll get "relation does not exist" instead of
the meaningful red.
"""

from datetime import date

import pytest

from database import SessionLocal
from models import DailyAutomatedData

# YOU implement this. Suggested home: weather.py. Suggested signature:
#     upsert_weather(db, day: date, weather_code: str) -> None
# It should INSERT a daily_automated_data row for `day`, or UPDATE the
# existing one on conflict -- never create a duplicate for the same date.
from weather import upsert_weather

TEST_DATE = date(2999, 12, 31)


@pytest.fixture
def db():
    """A DB session with a clean slate for TEST_DATE before and after."""
    session = SessionLocal()

    def _clear():
        session.query(DailyAutomatedData).filter(
            DailyAutomatedData.date == TEST_DATE
        ).delete()
        session.commit()

    _clear()
    try:
        yield session
    finally:
        _clear()
        session.close()


def test_ingest_is_idempotent(db):
    # Run the ingestion twice for the SAME date, with different values.
    upsert_weather(db, TEST_DATE, "clear")
    upsert_weather(db, TEST_DATE, "overcast")

    rows = (
        db.query(DailyAutomatedData)
        .filter(DailyAutomatedData.date == TEST_DATE)
        .all()
    )

    # Idempotency: the second run must NOT create a duplicate row...
    assert len(rows) == 1
    # ...and the row must hold the LATEST value written.
    assert rows[0].weather_code == "overcast"
