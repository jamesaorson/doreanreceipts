__all__ = [
    "gather",
]

import json
from datetime import datetime


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


def fetch_new_receipts(
    bearer_token: str, existing_receipts: set[Receipt]
) -> set[Receipt]:
    # This function should implement the logic to fetch new receipts from an API.
    # For now, we will return an empty set to simulate no new receipts.
    # In a real implementation, you would use the bearer_token to authenticate
    # and fetch data from the API.
    return set(
        Receipt(
            author="example_author",
            content="#doreancon nice!",
            timestamp=datetime.now(),
        )
        for _ in range(3)  # Simulating 3 new receipts
    )


def gather(bearer_token: str) -> list[Receipt]:
    existing_receipts = Receipt.from_file(RECEIPTS_FILE)
    new_receipts = fetch_new_receipts(bearer_token, existing_receipts)
    receipts = new_receipts - existing_receipts
    if new_receipts:
        with open(RECEIPTS_FILE, "w+") as file:
            json.dump(
                [r.to_dict() for r in new_receipts | existing_receipts],
                file,
                indent=4,
                sort_keys=True,
            )
    return receipts
