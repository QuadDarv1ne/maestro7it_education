from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import atexit
from app.utils.notifications import notification_service
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        
        # Schedule tasks
        self.schedule_reminders()
        self.schedule_daily_updates()
        
        # Graceful shutdown
        atexit.register(lambda: self.shutdown())
    
    def schedule_reminders(self):
        """Schedule reminder sending every hour"""
        self.scheduler.add_job(
            func=self.send_tournament_reminders,
            trigger=IntervalTrigger(minutes=30),  # Check every 30 minutes
            id='tournament_reminders',
            name='Send tournament reminders',
            replace_existing=True
        )
        logger.info("Scheduled tournament reminders job")
    
    def schedule_daily_updates(self):
        """Schedule daily updates"""
        self.scheduler.add_job(
            func=self.daily_tournament_check,
            trigger='cron',
            hour=9,  # Daily at 9 AM
            id='daily_tournament_check',
            name='Daily tournament check',
            replace_existing=True
        )
        logger.info("Scheduled daily tournament check job")
    
    def send_tournament_reminders(self):
        """Send tournament reminders"""
        try:
            logger.info("Running scheduled tournament reminders check")
            sent_count = notification_service.send_reminders()
            logger.info(f"Sent {sent_count} tournament reminders")
        except Exception as e:
            logger.error(f"Error in scheduled tournament reminders: {e}")
    
    def daily_tournament_check(self):
        """Daily check for tournament updates"""
        try:
            logger.info("Running daily tournament check")
            
            # Here you could add checks for:
            # - New tournaments
            # - Status changes
            # - Other updates
            
            logger.info("Daily tournament check completed")
        except Exception as e:
            logger.error(f"Error in daily tournament check: {e}")
    
    def add_job(self, func, trigger, id, name, **kwargs):
        """Add a custom job to the scheduler"""
        self.scheduler.add_job(
            func=func,
            trigger=trigger,
            id=id,
            name=name,
            replace_existing=True,
            **kwargs
        )
    
    def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler shut down")

# Global scheduler instance
scheduler_service = SchedulerService()