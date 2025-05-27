from typing import List, Optional
from pydantic import BaseModel


class ListingItem(BaseModel):
    id: str
    name: str
    icon: str
    url: str
    guild: str
    trader_name: str
    trader_zone: str
    trader_location: str
    trader_url: str
    quality: int
    level: int
    champion: Optional[str] = None
    seller_name: str
    price: str
    amount: str
    ppu: str
    last_seen: str
    expires_at: str
    description: Optional[str] = None


class PaginationData(BaseModel):
    current_page: int
    has_next_page: bool
    has_previous_page: bool
    next_page_url: Optional[str] = None
    previous_page_url: Optional[str] = None
    total_items: str


class ListingsResponse(BaseModel):
    data: List[ListingItem]
    current_page: int
    has_next_page: bool
    has_previous_page: bool
    next_page_url: Optional[str] = None
    previous_page_url: Optional[str] = None
    total_items: str
