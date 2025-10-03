from datetime import datetime
from io import TextIOWrapper
import os
import json
import sys
import time

SLEEP_SECONDS = int(os.getenv("SLEEP_SECONDS", 5))

WATCH_DIR = os.path.expanduser("~/Downloads")
HISTORY_FILE = "./history.json"
PREFIX = "doreanreceipts"

printed_files = set()


class Tweet:
    def __init__(self, handle: str, datetime: str, content: str):
        self.handle = handle
        self.datetime = datetime
        self.content = content

    def __hash__(self):
        return hash((self.handle, self.datetime, self.content))

    def __eq__(self, value: "Tweet"):
        if not isinstance(value, Tweet):
            return False
        return (
            self.handle,
            self.datetime,
            self.content,
        ) == (
            value.handle,
            value.datetime,
            value.content,
        )

    def __str__(self) -> str:
        return f"{self.handle}\n{self.datetime}\n{self.content}\n\n"

    def __repr__(self) -> str:
        return str(self)

    def as_dict(self) -> dict[str, str]:
        return {
            "handle": self.handle,
            "datetime": self.datetime,
            "content": self.content,
        }

    @staticmethod
    def from_dict(value: dict[str, str]) -> "Tweet":
        return Tweet(
            value.get("handle", ""),
            value.get("datetime", ""),
            value.get("content", ""),
        )


def get_matching_filenames() -> list[str]:
    return [
        os.path.join(WATCH_DIR, f)
        for f in os.listdir(WATCH_DIR)
        if f.startswith(PREFIX)
    ]


def main():
    history: set[Tweet] = set()
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = set(Tweet.from_dict(t) for t in json.load(f))
            except:
                ...

    lp_file: TextIOWrapper | None = None
    lp_device = None
    while True:
        try:
            if not lp_file:
                for dev in os.listdir("/dev"):
                    if dev.startswith("lp"):
                        lp_device = os.path.join("/dev", dev)
                        lp_file = open(lp_device)
                        break
                if lp_device is not None:
                    print(f"Opened printer device: {lp_device}", file=sys.stderr)
            tweets: set[Tweet] = set()
            filenames = get_matching_filenames()
            for filename in filenames:
                with open(filename, "r") as f:
                    tweets.update(set(Tweet.from_dict(t) for t in json.load(f)))
            new_tweets = tweets.difference(history)
            if new_tweets:
                print("Found new tweets:", len(new_tweets), file=sys.stderr)
            else:
                print("No new tweets...", file=sys.stderr)

            for t in sorted(
                new_tweets, key=lambda t: datetime.fromisoformat(t.datetime)
            ):
                print(t)
                if lp_file:
                    print(t, file=lp_file)
            history.update(new_tweets)
            with open(HISTORY_FILE, mode="w+") as f:
                json.dump([t.as_dict() for t in history], f)
            for filename in filenames:
                os.remove(filename)
            time.sleep(SLEEP_SECONDS)
        finally:
            if lp_file:
                lp_file.close()


if __name__ == "__main__":
    main()
