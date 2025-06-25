__all__ = [
    "Client",
]

import json
from datetime import datetime

import tweepy


RECEIPTS_FILE = "receipts.json"


class Receipt:
    def __init__(self, author: str, content: str, timestamp: datetime):
        self.author = author
        self.content = content
        self.timestamp = timestamp

    def __str__(self):
        return f"@{self.author}\n{self.timestamp.isoformat()}\n{self.content}\n"

    def __hash__(self):
        return hash((self.author, self.content, self.timestamp))

    def __eq__(self, other):
        if not isinstance(other, Receipt):
            return NotImplemented
        return (
            self.author == other.author
            and self.content == other.content
            and self.timestamp == other.timestamp
        )

    def to_dict(self):
        return {
            "author": self.author,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Receipt":
        return cls(
            author=data["author"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )

    @classmethod
    def from_file(cls, file_path: str) -> set["Receipt"]:
        try:
            with open(file_path, "r") as file:
                receipts = json.load(file)
                return set(Receipt.from_dict(r) for r in receipts)
        except Exception as e:
            return set()

    @classmethod
    def from_tweet(cls, tweet: tweepy.Tweet) -> "Receipt":
        return cls(
            author=tweet.author_id,
            content=tweet.text,
            timestamp=tweet.created_at,
        )


class Client:
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.client = tweepy.Client(bearer_token=bearer_token)
        self.existing_receipts: set[Receipt] = set()

    def _fetch_new_receipts(self) -> set[Receipt]:
        response = self.client.search_recent_tweets(
            query="doreancon",
            tweet_fields=["created_at", "author_id"],
            max_results=10,
        )
        receipts = set(Receipt.from_tweet(r) for r in response.data)
        return receipts - self.existing_receipts

    def gather(self) -> set[Receipt]:
        self.existing_receipts = Receipt.from_file(RECEIPTS_FILE)
        new_receipts = self._fetch_new_receipts()
        if new_receipts:
            with open(RECEIPTS_FILE, "w+") as file:
                json.dump(
                    [r.to_dict() for r in new_receipts | self.existing_receipts],
                    file,
                    indent=4,
                    sort_keys=True,
                )
        return new_receipts
