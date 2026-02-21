# AcreetionOS AutoPoster

A modern Windows application that uses Gemini AI to generate and schedule social media posts about AcreetionOS three times a day at random intervals.

## Features
- **Modern GUI**: Built with CustomTkinter for a sleek Windows experience.
- **AI-Powered**: Uses Gemini 1.5 Flash for unique content generation.
- **Random Scheduling**: Posts 3 times daily between 9 AM and 9 PM at randomized times.
- **Persistent Logging**: Track success/failure of posts in real-time.
- **Setting & Forget**: Once started, it handles everything automatically.

## Getting Started

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))
- X (Twitter) Developer Keys (Optional - if you want to post to X)

### 2. Installation
1. Clone this repository or download the files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Usage
1. Run the application:
   ```bash
   python main.py
   ```
2. Navigate to **Settings**.
3. Paste your **Gemini API Key**.
4. Paste your social media API keys (X/Twitter, etc.).
5. Click **Save Settings**.
6. Go to **Dashboard** and click **Start Scheduler**.

## Notes on Platform APIs
- **X/Twitter**: Requires a Developer account. You need the API Key, API Secret, Access Token, and Access Token Secret.
- **Other Platforms**: The current version includes a plugin architecture. I've added mocks for LinkedIn and Instagram. You can expand `poster.py` as you get API access for those platforms.

## Developer Note
This app is designed to be "set and forget." It will automatically recalculate its 3 random daily posts every day it remains running.
