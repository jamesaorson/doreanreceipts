__all__ = [
    "gather",
]

from datetime import datetime


class Receipt:
    def __init__(self, author: str, content: str, timestamp: datetime):
        self.author = author
        self.content = content
        self.timestamp = timestamp

    def __str__(self):
        return f'@{self.author}\n{self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}\n{self.content}\n'


def gather() -> list[Receipt]:
    return [
        Receipt(
            author="papa_ursinia",
            content="woohoo, doreancon!",
            timestamp=datetime(2023, 10, 1, 12, 0, 0),
        ),
    ]
