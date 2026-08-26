# SentinelX: Mini SOC SIEM - Detailed System Documentation

Welcome to the comprehensive documentation for the **SentinelX Mini SOC SIEM**. This document breaks down every component of the project, explaining how data is generated, processed, stored, and visualized in the dashboard.

---

## 1. System Workflow & Architecture

SentinelX is a centralized Security Information and Event Management (SIEM) system. The core workflow operates as follows:

1. **Data Collection (The Inputs):** Background Python scripts (Collectors) constantly run to fetch or generate raw logs.
2. **Event Pipeline (The Brain):** The `PipelineManager` receives logs via an `EventBus`, analyzes them against Threat Intelligence (IoCs), and categorizes them.
3. **Storage (The Vault):** All processed events are stored in a lightning-fast relational database (`siem_data.db` using SQLite).
4. **API Layer (The Bridge):** A FastAPI server (`server.py`) provides REST API endpoints to access the database securely.
5. **Frontend Dashboard (The Eyes):** A React.js UI polls the API to fetch live data and renders interactive graphs, maps, and tables for the Security Analyst.
6. **Automated Scheduler (The Reporter):** An independent script runs on a timer to generate PDF reports of recent incidents and emails them to stakeholders.

---

## 2. Data Generation & Collection

How is data actually entering the system? The backend utilizes several **Collectors** (`backend/collectors/`).

### The Simulator (`simulator_collector.py`)
Currently, the system is actively generating **automatic raw data**. The simulator reads attack profiles (like Brute Force or Password Spray) from `config/simulations/*.yaml` and injects fake logs into the system every few seconds. This ensures the dashboard always has "live" data to demonstrate the system's capabilities.

### Elastic & Wazuh Connectors (`elastic_adapter.py`, `wazuh_collector.py`)
* **What are they?** Wazuh is an open-source endpoint security platform, and Elasticsearch is a massive big-data search engine.
* **Their Role Here:** SentinelX does not replace them; it integrates with them. If your organization uses Wazuh to monitor servers, the `wazuh_collector.py` script authenticates with the Wazuh API, pulls the highest-priority alerts, and normalizes them into SentinelX's SQLite database. The same applies to Elastic. They act as heavy-lifting raw data sources, while SentinelX acts as the unified presentation and correlation layer.

---

## 3. Backend Connectivity (`main.py` & `server.py`)

* **`main.py`:** This is the entry point. When you run `python -m backend.main`, it uses `asyncio` to simultaneously launch the FastAPI web server AND all the background collector scripts (Simulator, Windows, Linux, Wazuh).
* **`server.py` (The API):** This script contains endpoints like `/api/stats`, `/api/logs`, and `/api/alert_history`. When the frontend asks for data, these endpoints execute SQL queries directly against `siem_data.db` and return the results as JSON.

---

## 4. Frontend: How the Dashboard Pages Work

The React frontend (`frontend/src/App.jsx`) is broken down into three main tabs. It uses `setInterval` to fetch new data from the backend every 5 seconds (Live Refresh).

### A. The Dashboard Tab
This is the visual command center. Every widget is powered by real database queries.

1. **Top KPI Cards (Numbers):**
   * *How it works:* The backend runs SQL `COUNT(*)` queries on the `events` table (e.g., Total Events, Unique IPs) and sends the exact numbers to the UI.
2. **Global Threat Map:**
   * *How it works:* The backend queries the top 5 most frequent `source_ip` addresses. Because the SQLite database lacks a massive GeoIP library, the backend uses a deterministic hash (`hashlib.md5`) on the IP address to assign it a mock latitude, longitude, and Country Name. The UI then plots a red blinking dot on those coordinates.
3. **Attacks by Country (Histogram/Bar Chart):**
   * *How it works:* Using the same hashed GeoIP data, the backend groups the attack counts by Country. The UI uses the `Recharts` library to draw a yellow Bar Chart. Hovering over a bar dynamically calculates the percentage: `(Country Count / Total Attacks) * 100`.
4. **Incidents by Severity (Pie Chart):**
   * *How it works:* The backend runs `SELECT severity, COUNT(*) FROM incidents GROUP BY severity`. To ensure the pie chart always looks colorful and professional even if only one type of attack is happening, a small baseline number (padding) is added to Critical, High, Medium, and Low.
5. **Events Over Time (Bar Chart):**
   * *How it works:* The backend uses the SQLite `strftime('%Y-%m-%d', timestamp)` function to group raw events by their calendar date for the last 7 days, plotting a timeline of attack volume.
6. **MITRE ATT&CK Mapping:**
   * *How it works:* The UI looks at the live logs feed and maps the raw `event_type` string (e.g., `PASSWORD_SPRAY`) to a hardcoded dictionary of MITRE techniques (e.g., `T1110.003 Password Spraying`).

### B. The Log Activity Tab
* **What it shows:** A raw, unfiltered, scrollable table of every single event in the database. 
* **How it works:** It fetches up to 50 logs at a time. It features a Search Bar that uses React state (`useState`) to instantly filter the rows by IP address, Event Type, or Status without needing to query the database again. This is the primary tool for SOC Analysts during deep investigations.

### C. The Mail History Tab
* **What it shows:** A historical ledger of every PDF report that was successfully generated and emailed.
* **How it works:** It queries the `/api/alert_history` endpoint, which reads directly from the `mini_soc_siem_alert_history.csv` file. It displays who received the email, the timestamp, and provides a "View" button. The View button works because FastAPI serves the `reports/` folder as a static directory, allowing the browser to download/open the PDF.

---

## 5. Automated PDF Reporting (`scheduler.py`)

The reporting engine operates completely independently of the website. 

1. **Trigger:** `python backend\scheduler.py` runs a loop (e.g., every 10 minutes).
2. **Fetch:** It executes a query to grab the latest severe logs (`WHERE state = 'INCIDENT'`).
3. **Generate:** It passes those logs into an HTML template (`Jinja2`). A tool called `pdfkit` converts that HTML into a polished, branded PDF file and saves it in the `reports/` directory.
4. **Deliver:** The `mailer.py` script opens `emails.csv`, reads the list of authorized recipients, connects to the SMTP Email Server, attaches the PDF, and sends it out automatically. It then records the success in the `alert_history` CSV.
