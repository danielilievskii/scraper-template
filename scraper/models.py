from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Record:
    """Represents a scraped record."""

    id: str
    title: str
    site_url: str
    page_url: str
    content: Optional[str] = None
    published_at: Optional[str] = None
    categories: List[str] = None

    def to_dict(self) -> dict:
        """Serialize the Record into a dictionary."""

        return {
            "id": self.id,
            "title": self.title,
            "site_url": self.site_url,
            "page_url": self.page_url,
            "content": self.content,
            "published_at": self.published_at,
            "categories": self.categories,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Record":
        """Deserialize a dictionary into a Record instance."""

        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            site_url=data.get("site_url", ""),
            page_url=data.get("page_url", ""),
            content=data.get("content"),
            published_at=data.get("published_at"),
            categories=data.get("categories"),
        )