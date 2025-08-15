from pyrogram.types import Gift

from data import Config

from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class GiftFilterDontBuy:
    supply_range: Tuple[float, float]
    price_range: Tuple[float, float]

@dataclass
class SendFromTo:
    session_name_send_from: str
    username_send_to: str

class GiftsCache:
    def __init__(
        self,
        config: Config
    ):
        self.current_gifts: List[Gift] = []
        self.new_gifts_available: List[Gift] = []
        self.config = config

    def filter_gifts(self, gifts: List[Gift]) -> List[Gift]:
        if self.config.is_test_mode:
            return gifts

        filtered_by_limited = [gift for gift in gifts if gift.is_limited]

        filtered_by_supply_price_config = [
            gift for gift in filtered_by_limited
            if any(
                f.supply_range[0] <= gift.total_amount <= f.supply_range[1] and
                f.price_range[0] <= gift.price <= f.price_range[1]
                for f in self.config.gift_filters
            )
        ]

        return filtered_by_supply_price_config

    def init_cache(self, available_gifts):
        filtered_gifts = self.filter_gifts(available_gifts)

        if not self.current_gifts:
            self.current_gifts = list(filtered_gifts)

        if self.config.is_test_mode:
            self.current_gifts = self.current_gifts[2:]

    def get_new_gifts_available(self, available_gifts_new: List[Gift]) -> List[Gift]:
        filtered_gifts_new = self.filter_gifts(available_gifts_new)

        current_ids = {gift.id for gift in self.current_gifts}
        new_gifts = [
            gift for gift in filtered_gifts_new
            if gift.id not in current_ids
        ]

        self.new_gifts_available = new_gifts
        self.current_gifts = list(filtered_gifts_new)

        return new_gifts

    @staticmethod
    def log_gift_string(gift: Gift):
        return (
            f"ID: {gift.id} | "
            f"Title: {gift.title} | "
            f"Amount: {gift.total_amount} | "
            f"Price: {gift.price}"
        )