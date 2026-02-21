from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import random
from generator import ContentGenerator
from poster import SocialPoster

class SchedulerManager:
    def __init__(self, api_keys=None):
        self.scheduler = BackgroundScheduler()
        self.generator = ContentGenerator()
        self.poster = SocialPoster()
        self.running = False
        self.log_callback = None
        self.next_run_callback = None

    def set_log_callback(self, callback): self.log_callback = callback
    def set_next_run_callback(self, callback): self.next_run_callback = callback

    def log(self, message):
        if self.log_callback:
            self.log_callback(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        print(f"Log: {message}")

    def generate_and_post(self):
        self.log("Brainstorming session started (Gemini talking to Gemini)...")
        content = self.generator.generate_post()
        self.log(f"Generated Post: {content[:100]}...")
        
        results = self.poster.post_to_all(content)
        for result in results:
            self.log(result)
        
        # Calculate next run (1 hour from now)
        next_run = datetime.now() + timedelta(hours=1)
        if self.next_run_callback:
            self.next_run_callback(next_run.strftime('%H:%M:%S'))

    def start(self):
        if not self.running:
            # We add a job to run every 1 hour (60 minutes)
            # This is a fixed interval as requested, providing constant activity
            self.scheduler.add_job(self.generate_and_post, IntervalTrigger(minutes=60), id="hourly_post")
            self.scheduler.start()
            self.running = True
            self.log("Hourly scheduler started. First post in 60 minutes.")
            
            # Optionally, trigger a post immediately on start?
            # self.generate_and_post()

    def stop(self):
        if self.running:
            self.scheduler.shutdown()
            self.running = False
            self.log("Scheduler stopped.")
