
class Config:

    def __init__(
        self,
        config
    ):  
        from models import GiftFilterDontBuy, SendFromTo

        self.config = config
        
        self.logs_file_path = self.config["logs_file_path"]
        self.sessions_for_checking = self.config["sessions_for_checking"]
        self.send_config = [SendFromTo(**item) for item in self.config["send_config"]]
        self.sleep_checking_seconds = self.config["sleep_checking_seconds"]
        self.is_test_mode = self.config["is_test_mode"]
        self.test_mode_max_balance = self.config["test_mode_max_balance"]
        self.is_infinite_buying = self.config["is_infinite_buying"]

        self.gift_filters = [
            GiftFilterDontBuy(
                supply_range=(
                    int(item["supply_range"][0]),
                    float('inf') if item["supply_range"][1] == "inf" else int(item["supply_range"][1])
                ),
                price_range=(
                    int(item["price_range"][0]),
                    float('inf') if item["price_range"][1] == "inf" else int(item["price_range"][1])
                )
            )
            for item in self.config["gift_filters"]
        ]