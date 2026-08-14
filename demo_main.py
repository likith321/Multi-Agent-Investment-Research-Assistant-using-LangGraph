"""
Review-1 minimal demo.

Run:
    python demo_main.py [TICKER]

Runs only the Data Gatherer -> Fundamental Analyst slice of the
pipeline through LangGraph, using the shared Pydantic ResearchState
and the SQLite audit trail -- both real, production pieces of the
project. No API key needed.
"""

import sys

from orchestration.demo_graph import demo_app

ticker = sys.argv[1] if len(sys.argv) > 1 else "NVDA"

initial_state = {
    "ticker": ticker
}

config = {
    "configurable": {
        "thread_id": f"{ticker.lower()}_demo_run"
    }
}

result = demo_app.invoke(initial_state, config=config)

print("\n=== SHARED RESEARCH STATE (after 2 agents) ===\n")
print(f"Ticker:         {result['ticker']}")
print(f"Company:        {result.get('company_name')}")
print(f"Stock price:    {result.get('stock_price')}")
print(f"Fundamentals:   {result.get('fundamentals')}")

print("\n=== AUDIT LOG (in-memory) ===\n")
for entry in result["audit_log"]:
    print("-", entry)

print("\n=== AUDIT LOG (SQLite, persisted to audit.db) ===\n")
import sqlite3
conn = sqlite3.connect("audit.db")
for row in conn.execute("SELECT agent, message FROM audit_logs ORDER BY id DESC LIMIT 5"):
    print("-", row[0], ":", row[1])
conn.close()
