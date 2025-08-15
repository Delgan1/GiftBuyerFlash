from pyrogram.client import Client

from data import Logger, Config

from dataclasses import dataclass
from typing import List

class SessionType:
    checking = 0
    buying = 1

@dataclass
class Session:
    name: str
    is_checker: bool = False
    is_buying: bool = False
    cli: Client = None
    balance_available: int = None

    async def start(self):
        self.cli = Client(self.name)
        await self.cli.start()

class Sessions:
    def __init__(
        self, 
        config: Config,
        logger: Logger
    ):
        self.available: List[Session] = []
        self.config: Config = config
        self.logger: Logger = logger

    @property
    def checker_sessions(self):
        return [session for session in self.available if session.is_checker]

    @property
    def buyer_sessions(self):
        return [session for session in self.available if session.is_buying]

    async def add_session(self, session_name_file: str, is_checker: bool = False, is_buying: bool = False) -> bool:
        for s in self.available:
            if s.name == session_name_file:
                if is_buying:
                    s.is_buying = is_buying
                if is_checker:
                    s.is_checker = is_checker
                self.logger.info(f"Session {session_name_file} already started, continuing")
                return True
            
        session = Session(
            name=session_name_file,
            is_checker=is_checker,
            is_buying=is_buying,
        )
        try:
            await session.start()
            session.balance_available = await session.cli.get_stars_balance()
            if self.config.is_test_mode:
                session.balance_available = min(self.config.test_mode_max_balance, session.balance_available)

            me = await session.cli.get_me()
            self.logger.info(f"Started session: {session.name}, balance: {session.balance_available}, name: {me.first_name} {me.last_name}, username: {me.username}")
            self.available.append(session)
            return True
        except Exception as e:
            self.logger.error(f"Session was failed with error: {e}")

        return False

    async def stop_all(self):
        for session in self.available:
            await session.cli.stop()
