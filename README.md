# Personal Command Center

A modular, production-grade automated lifestyle data pipeline and orchestration engine designed to track personal data streams, monitor target environments, and deliver intelligent alerts.

## Architecture & Data Flow

```text
[ Web Target ] 
      │ (Network HTTP Request)
      ▼
[ Playwright Browser Instance ] 
      │ (Headless Chromium DOM Rendering)
      ▼
[ BeautifulSoup4 Parsing Engine ] 
      │ (Target Node Text Extraction)
      ▼
[ JSON State Logger & Memory Engine ] ──(No Change Detected)──► [ Quiet / Standby ]
      │
      │ (Data Divergence or New Date Detected)
      ▼
[ Secure Credential Middleware (python-dotenv) ]
      │ (Loads Decoupled Tokens)
      ▼
[ Discord Webhook API ] ──► [ Direct Mobile Notification Push ]
```

## Features

- **Headless Browser Automation:** Leverages Playwright to programmatically drive background browser instances, executing realistic page navigations and handling asynchronous JavaScript network payloads.
- **Robust DOM Extraction:** Utilizes BeautifulSoup4 for highly targeted, resilient parsing of HTML structural nodes.
- **Stateful Memory Tracking:** Implements a localized JSON-based logging ledger to store past states and target variables, preventing message spam by evaluating data divergence before triggering alerts.
- **Secure Configuration Management:** Built on zero-trust principles, decoupling sensitive operational credentials (like API webhook endpoints) from code files using environment variables.

## Getting Started

### Prerequisites
- Python 3.10+
- A Discord account and access to a personal server

### Installation & Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd personal-command-center
   ```

2. **Initialize and activate the isolated virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install application dependencies and native browser engines:**
   ```bash
   pip install playwright beautifulsoup4 requests python-dotenv
   playwright install
   ```

4. **Configure Secure Tokens:**
   Create a `.env` file in the root directory:
   ```bash
   touch .env
   ```
   Open the file and add your secret webhook credential:
   ```text
   DISCORD_WEBHOOK_URL=https://discord.com
   ```

5. **Execute the pipeline:**
   ```bash
   python scraper.py
   ```