import customtkinter as ctk
import os
import webbrowser
from scheduler_manager import SchedulerManager
from dotenv import load_dotenv, set_key

load_dotenv()

class AutoPostApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AcreetionOS AutoPoster")
        self.geometry("1000x800")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        
        self.label = ctk.CTkLabel(self.sidebar_frame, text="AcreetionOS", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=20)
        
        self.dashboard_button = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard)
        self.dashboard_button.pack(pady=10, padx=20)
        
        self.settings_button = ctk.CTkButton(self.sidebar_frame, text="Settings", command=self.show_settings)
        self.settings_button.pack(pady=10, padx=20)
        
        self.status_label = ctk.CTkLabel(self.sidebar_frame, text="Status: Stopped", text_color="red")
        self.status_label.pack(side="bottom", pady=20)
        
        # Main
        self.main_content = ctk.CTkFrame(self)
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.scheduler = SchedulerManager()
        self.scheduler.set_log_callback(self.add_log)
        self.scheduler.set_next_run_callback(self.update_next_run)
        
        self.show_dashboard()

    def show_dashboard(self):
        for widget in self.main_content.winfo_children(): widget.destroy()
        self.title_label = ctk.CTkLabel(self.main_content, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=10)
        self.next_run_label = ctk.CTkLabel(self.main_content, text="Next Post: N/A", font=ctk.CTkFont(size=16))
        self.next_run_label.pack(pady=5)
        self.control_frame = ctk.CTkFrame(self.main_content)
        self.control_frame.pack(pady=20)
        self.start_btn = ctk.CTkButton(self.control_frame, text="Start Hourly Scheduler", command=self.start_scheduler, fg_color="green")
        self.start_btn.pack(side="left", padx=10)
        self.instant_btn = ctk.CTkButton(self.control_frame, text="Instant Brainstorm & Post", command=self.scheduler.generate_and_post, fg_color="purple")
        self.instant_btn.pack(side="left", padx=10)
        self.stop_btn = ctk.CTkButton(self.control_frame, text="Stop Scheduler", command=self.stop_scheduler, fg_color="red")
        self.stop_btn.pack(side="left", padx=10)
        self.log_text = ctk.CTkTextbox(self.main_content, height=400)
        self.log_text.pack(fill="both", expand=True, pady=10)

    def show_settings(self):
        for widget in self.main_content.winfo_children(): widget.destroy()
        self.settings_title = ctk.CTkLabel(self.main_content, text="Settings", font=ctk.CTkFont(size=24, weight="bold"))
        self.settings_title.pack(pady=10)
        
        self.api_scroll = ctk.CTkScrollableFrame(self.main_content)
        self.api_scroll.pack(fill="both", expand=True, pady=10)
        
        # Gemini
        self.add_section_header(self.api_scroll, "General Settings")
        self.topic_entry = self.add_setting_field(self.api_scroll, "Post Topic:", os.getenv("POST_TOPIC", "AcreetionOS"))
        self.gemini_entry = self.add_setting_field(self.api_scroll, "Gemini API Key:", os.getenv("GEMINI_API_KEY", ""))
        
        # Twitter
        self.add_section_header(self.api_scroll, "Twitter (X) OAuth")
        self.tw_key = self.add_setting_field(self.api_scroll, "Consumer Key:", os.getenv("TWITTER_CONSUMER_KEY", ""))
        self.tw_secret = self.add_setting_field(self.api_scroll, "Consumer Secret:", os.getenv("TWITTER_CONSUMER_SECRET", ""))
        self.tw_btn = ctk.CTkButton(self.api_scroll, text="Get Twitter PIN", command=self.start_twitter_auth)
        self.tw_btn.pack(pady=5)
        self.tw_pin = self.add_setting_field(self.api_scroll, "Enter PIN:", "")
        self.tw_finish = ctk.CTkButton(self.api_scroll, text="Finish Twitter Auth", command=self.finish_twitter_auth)
        self.tw_finish.pack(pady=5)

        # Meta (FB/IG)
        self.add_section_header(self.api_scroll, "Meta (Facebook / Instagram)")
        self.meta_id = self.add_setting_field(self.api_scroll, "App Client ID:", os.getenv("META_CLIENT_ID", ""))
        self.meta_page_id = self.add_setting_field(self.api_scroll, "Facebook Page ID:", os.getenv("META_PAGE_ID", ""))
        self.meta_token = self.add_setting_field(self.api_scroll, "Page Access Token:", os.getenv("META_PAGE_ACCESS_TOKEN", ""))
        self.meta_auth_btn = ctk.CTkButton(self.api_scroll, text="Launch Meta Auth", command=lambda: webbrowser.open(f"https://developers.facebook.com/apps/"))
        self.meta_auth_btn.pack(pady=5)

        # Mastodon
        self.add_section_header(self.api_scroll, "Mastodon")
        self.mast_inst = self.add_setting_field(self.api_scroll, "Instance URL:", os.getenv("MASTODON_INSTANCE", "mastodon.social"))
        self.mast_token = self.add_setting_field(self.api_scroll, "Access Token:", os.getenv("MASTODON_ACCESS_TOKEN", ""))

        # BlueSky
        self.add_section_header(self.api_scroll, "BlueSky")
        self.bsky_h = self.add_setting_field(self.api_scroll, "Handle:", os.getenv("BLUESKY_HANDLE", ""))
        self.bsky_p = self.add_setting_field(self.api_scroll, "App Password:", os.getenv("BLUESKY_APP_PASSWORD", ""))

        self.save_btn = ctk.CTkButton(self.main_content, text="Save All Settings", command=self.save_settings, fg_color="blue")
        self.save_btn.pack(pady=10)

    def add_setting_field(self, parent, label, value):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)
        ctk.CTkLabel(frame, text=label, width=150, anchor="w").pack(side="left", padx=10)
        entry = ctk.CTkEntry(frame)
        entry.insert(0, value)
        entry.pack(side="right", fill="x", expand=True, padx=10)
        return entry

    def add_section_header(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=14, weight="bold"), anchor="w", text_color="cyan").pack(fill="x", pady=(15, 5), padx=10)

    def start_twitter_auth(self):
        self.scheduler.poster.twitter_keys['consumer_key'] = self.tw_key.get()
        self.scheduler.poster.twitter_keys['consumer_secret'] = self.tw_secret.get()
        url, err = self.scheduler.poster.get_twitter_auth_url()
        if err: self.add_log(f"Twitter Error: {err}")
        else: webbrowser.open(url)

    def finish_twitter_auth(self):
        tokens, err = self.scheduler.poster.finalize_twitter_auth(self.tw_pin.get())
        if err: self.add_log(f"Twitter Error: {err}")
        else:
            set_key(".env", "TWITTER_ACCESS_TOKEN", tokens['access_token'])
            set_key(".env", "TWITTER_ACCESS_TOKEN_SECRET", tokens['access_token_secret'])
            set_key(".env", "TWITTER_CONSUMER_KEY", self.tw_key.get())
            set_key(".env", "TWITTER_CONSUMER_SECRET", self.tw_secret.get())
            self.add_log("Twitter Auth Successful.")

    def save_settings(self):
        env = ".env"
        set_key(env, "POST_TOPIC", self.topic_entry.get())
        set_key(env, "GEMINI_API_KEY", self.gemini_entry.get())
        set_key(env, "META_CLIENT_ID", self.meta_id.get())
        set_key(env, "META_PAGE_ID", self.meta_page_id.get())
        set_key(env, "META_PAGE_ACCESS_TOKEN", self.meta_token.get())
        set_key(env, "MASTODON_INSTANCE", self.mast_inst.get())
        set_key(env, "MASTODON_ACCESS_TOKEN", self.mast_token.get())
        set_key(env, "BLUESKY_HANDLE", self.bsky_h.get())
        set_key(env, "BLUESKY_APP_PASSWORD", self.bsky_p.get())
        self.add_log("Settings Saved.")

    def start_scheduler(self):
        self.scheduler.start()
        self.status_label.configure(text="Status: Running", text_color="green")

    def stop_scheduler(self):
        self.scheduler.stop()
        self.status_label.configure(text="Status: Stopped", text_color="red")

    def add_log(self, msg):
        if hasattr(self, 'log_text'): self.log_text.insert("end", f"{msg}\n"); self.log_text.see("end")

    def update_next_run(self, time_str):
        if hasattr(self, 'next_run_label'): self.next_run_label.configure(text=f"Next Post: {time_str}")

if __name__ == "__main__":
    app = AutoPostApp()
    app.mainloop()
