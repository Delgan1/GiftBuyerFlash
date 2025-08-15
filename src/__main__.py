from data import Config, set_logger
from models import Sessions, GiftsCache
from core import GiftFlashBuyer, TaskManager

from toml import load 
from asyncio import run

async def main():
    config = Config(load("config.toml"))
    logger = set_logger("GiftFlashBuyer", log_path=config.logs_file_path, debug_disabled=True)  # Если хотите выключить необъязательные логи, удалите строку debug_disabled

    sessions = Sessions(config, logger)
    gift_cache = GiftsCache(config)
    tasks = TaskManager()

    buyer = GiftFlashBuyer(config, logger, tasks, gift_cache, sessions)

    await buyer.account_starter()
    
    while True:
        try:
            await buyer.main()
        except Exception as e:
            logger.error(f"Started was ended with error: {e}")
            break

if __name__ == "__main__":
    try:
        run((main()))
    except KeyboardInterrupt:
        pass
