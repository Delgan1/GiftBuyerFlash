from pyrogram.types import Gift
from pyrogram.errors import StargiftUsageLimited, FormSubmitDuplicate, FloodWait

from models import GiftsCache, Session,  Sessions
from data import Config, Logger
from .task_manager import TaskManager

from asyncio import sleep
class GiftFlashBuyer:
    def __init__(
        self,
        config: Config,
        logger: Logger,
        tasks: TaskManager,
        gift_cache: GiftsCache,
        sessions: Sessions
    ):
        self.config = config
        self.logger = logger
        self.new_gifts = None
        self.tasks = tasks
        self.gift_cache = gift_cache
        self.sessions = sessions

        self.new_gifts = None

    async def check_gifts_from_session(self, session: Session):
        self.logger.info("Started checking")

        while True:
            available_gifts = await session.cli.get_available_gifts()    # чекаем новые подарки
            self.gift_cache.init_cache(available_gifts)

            new_gifts_available = self.gift_cache.get_new_gifts_available(available_gifts)
            if new_gifts_available:
                log_message = "Available new gifts:\n"
                for gift in new_gifts_available:
                    log_message += GiftsCache.log_gift_string(gift)
                self.logger.info(log_message.strip())
                self.logger.info("Stopping checker")
                raise StopAsyncIteration

            self.logger.debug("Checked. No new gifts availbale")
            await sleep(self.config.sleep_checking_seconds)

    async def buy_gift(self, session: Session, gift: Gift):

        self.logger.debug(f"Trying to buy gift {GiftsCache.log_gift_string(gift)}")

        send_to = None
        for config in self.config.send_config:
            if session.name == config.session_name_send_from:
                send_to = config.username_send_to

        attempts = 0
        max_attempts = 30
        while attempts < max_attempts:
            try:
                await session.cli.send_gift(send_to, gift.id, is_private=True, text="gift from @kod4dusha")
                self.logger.info(f"Gift {GiftsCache.log_gift_string(gift)} was buyed sucessfully")
                break
            except StargiftUsageLimited:
                self.logger.error(f"Oops, [{session.name} --> {send_to}] {GiftsCache.log_gift_string(gift)}: StargiftUsageLimited'")
                break
            except FloodWait as e:
                self.logger.error(f"FloodWait Error, waiting for {e.value} sec")
                await sleep(e.value)
            except FormSubmitDuplicate:
                wait_time = 0.3
                self.logger.error(f"FormSubmitDuplicate Error, waiting for {wait_time} sec")
                await sleep(wait_time)
            except Exception as e:
                self.logger.error(f"Buying a gift was ended with error: {e}")
                await sleep(0.3)

        self.logger.info(f"[{session.name} --> {send_to}] done")

    async def main(self):

        self.logger.debug("Checking gifts")
        await self.tasks.run([self.check_gifts_from_session(session) for session in self.sessions.checker_sessions])
        self.logger.debug("Stoped checking gifts")

        if not self.gift_cache.new_gifts_available:
            self.logger.debug("No new gifts availbale, stopping main")
            return

        self.logger.debug("Сreating buying tasks")
        tasks_buy = []
        for session in self.sessions.buyer_sessions:
            while session.balance_available:
                start_balance = session.balance_available

                for gift in self.gift_cache.new_gifts_available:
                    if session.balance_available >= gift.price:
                        tasks_buy.append(self.buy_gift(session, gift))
                        self.logger.info(f"Account: {session.name}, buy {GiftsCache.log_gift_string(gift)}")
                        session.balance_available -= gift.price
                    else:
                        self.logger.warn(f"Not enough stars balance {session.balance_available} to buy {GiftsCache.log_gift_string(gift)}")
                        continue

                if session.balance_available == start_balance:
                    break

        self.logger.debug("Starting tasks...")
        await self.task_manager_checker.run(tasks_buy)
        self.logger.debug("Done tasks")

    async def account_starter(self):
        self.logger.info("Starting checker sessions...")
        for session in self.config.sessions_for_checking:
            is_sucessesfully_started = await self.sessions.add_session(
                session_name_file=session,
                is_checker=True,
            )
            if is_sucessesfully_started:
                self.logger.debug("Checker sessions started succesfully.")

        self.logger.info("Starting buyer sessions...")
        for config in self.config.send_config:
            is_sucessesfully_started = await self.sessions.add_session(
                session_name_file=config.session_name_send_from,
                is_buying=True,
            )
            if is_sucessesfully_started:
                self.logger.debug("Buyer sessions started succesfully.")