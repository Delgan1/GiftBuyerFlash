from asyncio import gather, wait, create_task, CancelledError

from typing import List, Any


class TaskManager:
    def __init__(self):
        self._stop_flag = False
        self._tasks = []

    async def run(self, coroutines: List[Any]):
        """
        Запускает задачи в формате:
        await runner.run([
            worker(arg1, arg2),
            another_worker(arg3),
            ...
        ])
        """
        self._stop_flag = False
        self._tasks = [create_task(self._wrap_task(coro)) for coro in coroutines]

        try:
            await gather(*self._tasks, return_exceptions=True)
        except CancelledError:
            await self._cancel_all()

    async def _wrap_task(self, coro):
        if self._stop_flag:
            return
        try:
            return await coro
        except StopAsyncIteration:
            await self.stop()
        except Exception as e:
            print(f"Ошибка в задаче: {e}")

    async def stop(self):
        self._stop_flag = True
        await self._cancel_all()

    async def _cancel_all(self):
        for task in self._tasks:
            if not task.done():
                task.cancel()
        # Убрали return_exceptions, так как wait() его не поддерживает
        await wait(self._tasks)