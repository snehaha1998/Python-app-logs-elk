import time
import random
from logger import get_logger

log = get_logger("my-app")

def process_order(order_id):
    log.info(f"Processing order {order_id}")
    time.sleep(random.uniform(0.1, 0.5))  # simulate work

    if random.random() < 0.2:            # 20% chance of failure
        log.error(f"Order {order_id} failed — payment declined")
        return False

    log.info(f"Order {order_id} completed successfully")
    return True

def main():
    log.info("Application started")

    passed = failed = 0
    for i in range(1, 11):               # process 10 orders
        if process_order(f"ORD-{i:03d}"):
            passed += 1
        else:
            failed += 1

    log.info(f"Run complete — passed={passed} failed={failed}")

    if failed > 0:
        log.warning(f"{failed} orders failed in this run")

if __name__ == "__main__":
    main()
