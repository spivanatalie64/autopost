import os
import tweepy
import requests
import facebook
from mastodon import Mastodon
from atproto import Client
from dotenv import load_dotenv
from flask import Flask, request
import threading
import webbrowser

load_dotenv()

class SocialPoster:
    def __init__(self):
        # Platform Storage (using .env for persistence)
        self.twitter_keys = {
            'consumer_key': os.getenv('TWITTER_CONSUMER_KEY'),
            'consumer_secret': os.getenv('TWITTER_CONSUMER_SECRET'),
            'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
            'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        }
        self.meta_data = {
            'page_access_token': os.getenv('META_PAGE_ACCESS_TOKEN'),
            'page_id': os.getenv('META_PAGE_ID'),
            'instagram_business_account_id': os.getenv('META_IG_ID')
        }
        self.mastodon_data = {
            'instance': os.getenv('MASTODON_INSTANCE'),
            'access_token': os.getenv('MASTODON_ACCESS_TOKEN')
        }
        self.bluesky_data = {
            'handle': os.getenv('BLUESKY_HANDLE'),
            'app_password': os.getenv('BLUESKY_APP_PASSWORD')
        }
        self.linkedin_data = {
            'access_token': os.getenv('LINKEDIN_ACCESS_TOKEN'),
            'urn': os.getenv('LINKEDIN_URN')
        }

    # --- Generic OAuth 2.0 Local Server ---
    def start_local_auth_server(self, callback_func):
        app = Flask(__name__)
        
        @app.route('/callback')
        def oauth_callback():
            code = request.args.get('code')
            if code:
                callback_func(code)
                return "<h1>Authentication Successful!</h1><p>You can close this tab and return to the app.</p>"
            return "<h1>Authentication Failed!</h1>"

        def run_server():
            app.run(port=8080)
        
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()

    # --- Meta (Facebook/Instagram) Auth ---
    def get_meta_auth_url(self, client_id):
        redirect_uri = "http://localhost:8080/callback"
        # Scopes for Page & Instagram posting
        scopes = "pages_show_list,pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish"
        return f"https://www.facebook.com/v19.0/dialog/oauth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}", None

    # --- LinkedIn Auth ---
    def get_linkedin_auth_url(self, client_id):
        redirect_uri = "http://localhost:8080/callback"
        scopes = "w_member_social,openid,profile"
        return f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}", None

    # --- Twitter Auth ---
    def get_twitter_auth_url(self):
        if not self.twitter_keys['consumer_key']: return None, "Error: Consumer Key missing."
        self.twitter_auth = tweepy.OAuth1UserHandler(self.twitter_keys['consumer_key'], self.twitter_keys['consumer_secret'], callback='oob')
        try: return self.twitter_auth.get_authorization_url(), None
        except Exception as e: return None, str(e)

    def finalize_twitter_auth(self, pin):
        try:
            at, ats = self.twitter_auth.get_access_token(pin)
            return {'access_token': at, 'access_token_secret': ats}, None
        except Exception as e: return None, str(e)

    # --- Posting Logic ---
    def post_to_twitter(self, content):
        if not all(self.twitter_keys.values()): return "Twitter: Skip."
        try:
            client = tweepy.Client(consumer_key=self.twitter_keys['consumer_key'], consumer_secret=self.twitter_keys['consumer_secret'], access_token=self.twitter_keys['access_token'], access_token_auth_secret=self.twitter_keys['access_token_secret'])
            client.create_tweet(text=content)
            return "Twitter: Success!"
        except Exception as e: return f"Twitter Error: {str(e)}"

    def post_to_facebook(self, content):
        if not self.meta_data['page_access_token']: return "Facebook: Skip."
        try:
            graph = facebook.GraphAPI(access_token=self.meta_data['page_access_token'])
            graph.put_object(parent_object=self.meta_data['page_id'], connection_name='feed', message=content)
            return "Facebook: Success!"
        except Exception as e: return f"Facebook Error: {str(e)}"

    def post_to_instagram(self, content):
        # Note: Instagram posting via API requires a media container (usually an image).
        # We will need a placeholder image or a generated image for this to work.
        return "Instagram: Skipping (requires media container logic)."

    def post_to_mastodon(self, content):
        if not self.mastodon_data['access_token']: return "Mastodon: Skip."
        try:
            m = Mastodon(access_token=self.mastodon_data['access_token'], api_base_url=self.mastodon_data['instance'])
            m.toot(content)
            return "Mastodon: Success!"
        except Exception as e: return f"Mastodon Error: {str(e)}"

    def post_to_bluesky(self, content):
        if not self.bluesky_data['app_password']: return "BlueSky: Skip."
        try:
            client = Client()
            client.login(self.bluesky_data['handle'], self.bluesky_data['app_password'])
            client.send_post(text=content)
            return "BlueSky: Success!"
        except Exception as e: return f"BlueSky Error: {str(e)}"

    def post_to_all(self, content):
        results = []
        results.append(self.post_to_twitter(content))
        results.append(self.post_to_facebook(content))
        results.append(self.post_to_mastodon(content))
        results.append(self.post_to_bluesky(content))
        return results
