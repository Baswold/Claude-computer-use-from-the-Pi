"""Timer manager for scheduling periodic agent check-ins"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Callable, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger

logger = logging.getLogger(__name__)


class TimerManager:
    """Manages periodic timers and scheduled events for the agent"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.check_in_callback: Optional[Callable] = None

    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Timer manager started")

    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Timer manager stopped")

    def schedule_check_in(self, interval_minutes: int, callback: Callable):
        """
        Schedule periodic check-ins with the agent

        Args:
            interval_minutes: How often to check in (in minutes)
            callback: Async function to call on each check-in
        """
        self.check_in_callback = callback

        # Remove existing check-in job if any
        if self.scheduler.get_job("periodic_checkin"):
            self.scheduler.remove_job("periodic_checkin")

        # Add new check-in job
        self.scheduler.add_job(
            callback,
            trigger=IntervalTrigger(minutes=interval_minutes),
            id="periodic_checkin",
            name="Periodic Agent Check-in",
            replace_existing=True,
        )

        logger.info(f"Scheduled periodic check-in every {interval_minutes} minutes")

    def schedule_one_time(
        self, delay_minutes: int, callback: Callable, job_id: str, prompt: str = ""
    ):
        """
        Schedule a one-time event

        Args:
            delay_minutes: Minutes from now to trigger
            callback: Async function to call
            job_id: Unique identifier for this job
            prompt: Optional prompt to pass to callback
        """
        run_time = datetime.now() + timedelta(minutes=delay_minutes)

        self.scheduler.add_job(
            callback,
            trigger=DateTrigger(run_date=run_time),
            id=job_id,
            name=f"Timer: {prompt[:50]}",
            kwargs={"prompt": prompt},
            replace_existing=True,
        )

        logger.info(
            f"Scheduled one-time timer '{job_id}' for {run_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def cancel_timer(self, job_id: str) -> bool:
        """
        Cancel a scheduled timer

        Args:
            job_id: ID of the job to cancel

        Returns:
            True if cancelled, False if job not found
        """
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Cancelled timer '{job_id}'")
            return True
        except Exception as e:
            logger.warning(f"Failed to cancel timer '{job_id}': {e}")
            return False

    def list_timers(self) -> list:
        """Get list of all scheduled timers"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append(
                {
                    "id": job.id,
                    "name": job.name,
                    "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                }
            )
        return jobs

    async def trigger_check_in_now(self):
        """Manually trigger a check-in immediately"""
        if self.check_in_callback:
            logger.info("Manually triggering check-in")
            await self.check_in_callback()
        else:
            logger.warning("No check-in callback registered")
