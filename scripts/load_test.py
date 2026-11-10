
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx

API_URL = "http://localhost:8000"
TOTAL_REQUESTS = 150
MAX_WORKERS = 25


def reserve_ticket(event_id, customer_number):
    payload = {
        "event_id": event_id,
        "customer_email": f"loadtest{event_id}_{customer_number}@example.com"
    }

    try:
        response = httpx.post(
            f"{API_URL}/reservations",
            json=payload,
            timeout=30
        )
        return response.status_code
    except httpx.RequestError:
        return "network_error"


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/load_test.py EVENT_ID")
        sys.exit(1)

    event_id = int(sys.argv[1])

    print(f"Testing event ID: {event_id}")
    print(f"Sending {TOTAL_REQUESTS} reservation requests...")

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(reserve_ticket, event_id, i)
            for i in range(TOTAL_REQUESTS)
        ]

        results = [
            future.result()
            for future in as_completed(futures)
        ]

    duration = time.perf_counter() - start
    counts = Counter(results)

    print("\n--- Test Results ---")
    print(f"Successful (201): {counts[201]}")
    print(f"Rejected (409): {counts[409]}")
    print(f"Other results: {dict((k, v) for k, v in counts.items() if k not in (201, 409))}")
    print(f"Duration: {duration:.2f} seconds")

    if counts[201] == 100 and counts[409] == 50:
        print("\nPASS: Expected reservation limits respected.")
    else:
        print("\nCHECK: Unexpected result. Investigate before continuing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
