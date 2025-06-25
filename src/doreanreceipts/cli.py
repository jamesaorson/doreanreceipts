import os
import time

import doreanreceipts.receipts as receipts


def main(bearer_token: str):
    client = receipts.Client(bearer_token)
    is_running = True
    while is_running:
        for receipt in client.gather():
            print(receipt)
        time.sleep(5)


if __name__ == "__main__":
    bearer_token = os.getenv("X_BEARER_TOKEN")
    if not bearer_token:
        print("Please set the X_BEARER_TOKEN environment variable.")
        exit(1)
    main(bearer_token)
