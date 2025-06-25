import time

import doreanreceipts.receipts as receipts


def main():
    is_running = True
    while is_running:
        for r in receipts.gather():
            print(r)
            time.sleep(5)


if __name__ == "__main__":
    main()
