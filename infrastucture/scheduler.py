import logging
from typing import List, Callable
from fastapi import FastAPI
import asyncio
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import async_timeout
from dataclasses import dataclass


@dataclass
class DataGenerationJob:
    ticker: str
    data_generator: Callable
    data_interface: Callable


class JobRunner:
    async def execute(self, callback: DataGenerationJob, timeout: int):
        async with async_timeout.timeout(timeout):
            return await callback.data_interface(callback.data_generator())


class SchedulerApp(FastAPI):
    scheduler: AsyncIOScheduler
    tasks: set[asyncio.Task] = set()
    execute_lock = asyncio.Lock()
    runner: JobRunner = JobRunner()
    job_store: List[DataGenerationJob] = []

    def initialize_scheduler(self):
        self.scheduler = AsyncIOScheduler(
            executors={
                'default': AsyncIOExecutor(),
            },
            job_defaults={
                'coalesce': True,
                'max_instances': 1,
            },
        )

    def start_scheduler(self):
        self.scheduler.start()

    async def stop_scheduler(self, timeout=30):
        self.scheduler.shutdown()
        try:
            async with async_timeout.timeout(timeout):
                while self.tasks:
                    await asyncio.sleep(.1)
        except asyncio.TimeoutError:
            for task in self.tasks:
                task.cancel()

    async def execute(self, callback, timeout: int):
        task = asyncio.create_task(self.runner.execute(callback, timeout))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        try:
            while not task.done():
                await asyncio.sleep(.1)
        except asyncio.CancelledError as e:
            exception = e
            result = None
            logging.error(f"[JobExecutionError] Timeout on job {type(exception).__name__}")
        else:
            result, exception = (task.result(), task.exception())

        if exception and not isinstance(exception, asyncio.CancelledError):
            raise exception
        return result



