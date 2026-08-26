# Real-Time Mini SIEM / Elastic-Style System Documentation

## 1. Objective

This document explains how to upgrade the current CSV-based mini SOC project into a **real-time log monitoring system** that continuously fetches logs, indexes them, detects suspicious activity, and displays results in a dashboard.

The goal is to make the system behave like a lightweight version of **Elastic Security / Kibana / Wazuh**:

- Logs arrive continuously from servers and endpoints.
- The system ingests them automatically.
- The logs are normalized and stored in a searchable backend.
- Detection rules run on new events.
- Alerts and incidents are created automatically.
- The dashboard updates with near real-time data.
- Critical alerts can trigger PDF reports and email notifications.

---

## 2. Recommended Architecture

```text
Linux Server / Windows Server / Firewall / VPN
            ↓
        Wazuh Agent
            ↓
       Wazuh Manager
            ↓
      Elasticsearch
            ↓
  Python Correlation Engine
            ↓
     Streamlit Dashboard
            ↓
    PDF Report + Email Alert
```

### Why this architecture

This is the best balance between realism and practicality:

- **Wazuh** collects logs from endpoints.
- **Elasticsearch** stores and indexes them.
- **Python** applies custom security logic.
- **Streamlit** gives a live dashboard.
- **ReportLab + SMTP** handles reporting and mail.

---

## 3. What Changes from the Current Setup

Your current project uses CSV files. That is good for development and testing, but it is not real-time.

### Current flow

```text
CSV file → parser → detection → dashboard → PDF/email
```

### Real-time flow

```text
Live logs → agent/collector → Elasticsearch → detection engine → dashboard → PDF/email
```

### Key difference

In the real-time version:

- logs are not manually loaded from CSV
- the system polls or listens for new records
- the dashboard refreshes automatically
- the detection engine works on new events as they arrive

---

## 4. Recommended Components

### 4.1 Wazuh Agent

Install the Wazuh agent on the machine whose logs you want to monitor.

Typical sources:
- Linux auth logs
- syslog
- Windows Event Logs
- firewall logs
- VPN logs

The agent forwards data to the Wazuh manager.

### 4.2 Wazuh Manager

The manager receives logs, decodes them, and creates security alerts.

It is the central processing component for endpoint security and log monitoring.

### 4.3 Elasticsearch

Elasticsearch stores alerts and events in indexed form.

This makes it possible to:
- search by IP
- search by user
- filter by alert severity
- aggregate attacks
- display trends over time

### 4.4 Python Correlation Engine

Your custom Python layer reads from Elasticsearch and performs:
- brute-force detection
- password spray detection
- off-hours login detection
- suspicious country detection
- data-transfer anomaly detection
- incident scoring

### 4.5 Streamlit Dashboard

The dashboard should show:
- total alerts
- critical alerts
- top source IPs
- top targets
- open incidents
- event timeline
- alert table

### 4.6 PDF Report Generator

Use ReportLab or a similar PDF library to generate incident summaries.

### 4.7 Email Notification Service

Use SMTP to send the PDF report to a security mailbox when the system detects a critical event.

---

## 5. Real-Time Ingestion Options

There are three practical ways to implement real-time ingestion.

### Option A — Watch a local log file

Best for a small lab.

Example:
- monitor `/var/log/auth.log`
- monitor a local `firewall.log`
- process new lines as they are appended

Tools:
- Python `watchdog`
- tailing logic

Use this if you want a simple first step.

### Option B — Read from Elasticsearch periodically

Best for your current project.

Flow:
- Wazuh sends events to Elasticsearch
- Python queries Elasticsearch every few seconds
- dashboard refreshes on the same interval

This is the easiest way to add real-time feel without building a heavy message broker.

### Option C — Full event streaming

More advanced.

Use:
- Kafka
- Logstash
- Beats
- custom consumers

This is excellent for production-scale systems but not necessary for your internship project.

---

## 6. Best Choice for Your Project

The best practical choice is:

```text
Wazuh Agent → Wazuh Manager → Elasticsearch → Python Engine → Streamlit Dashboard
```

This gives you:
- real-time ingestion
- real SOC architecture
- searchable logs
- good resume value
- manageable complexity

---

## 7. Data Flow in the Real-Time System

### Step 1: Log creation

A server produces a log entry such as:

```text
Failed password for root from 198.51.100.44 port 55211 ssh2
```

### Step 2: Collection

Wazuh agent reads the log and forwards it.

### Step 3: Processing

Wazuh manager decodes the event and generates an alert if it matches a rule.

### Step 4: Storage

The alert is indexed in Elasticsearch.

### Step 5: Detection

Your Python engine queries the latest alerts and applies custom correlation logic.

### Step 6: Dashboard

Streamlit refreshes the visualizations.

### Step 7: Reporting

If the event severity is high enough, the system generates a PDF report.

### Step 8: Notification

The report is emailed to the security team.

---

## 8. Suggested Project Modules

### 8.1 Log Collector

Purpose:
- collect new logs in real time
- detect file changes or new Elasticsearch events

Inputs:
- auth logs
- VPN logs
- firewall logs
- Windows logs

### 8.2 Log Normalizer

Purpose:
- convert raw logs into structured records
- standardize column names
- parse IPs, usernames, ports, timestamps

### 8.3 Detection Rules

Purpose:
- identify suspicious behavior
- produce alerts

Rules:
- brute force
- password spray
- account lockout
- unusual login time
- foreign IP login
- port scan
- large transfer after login

### 8.4 Risk Engine

Purpose:
- calculate incident severity
- assign priority

Example scoring:
- failed login burst: +20
- foreign IP: +20
- account lockout: +40
- off-hours login: +15
- port scan: +35
- large data transfer: +30

### 8.5 Incident Builder

Purpose:
- group related alerts into incidents
- avoid sending multiple duplicate alerts for the same attack window

### 8.6 PDF Generator

Purpose:
- create a daily or on-demand incident report

### 8.7 Email Sender

Purpose:
- send the PDF to the mailbox
- optionally CC the SOC team

### 8.8 Dashboard

Purpose:
- show live security posture
- let the user filter and search events

---

## 9. Elasticsearch Integration Plan

### 9.1 What to store

Store the following fields in Elasticsearch:

- timestamp
- hostname
- process
- event_type
- auth_result
- action
- user_name
- source_ip
- destination_ip
- destination_port
- protocol
- bytes_sent
- bytes_received
- country
- city
- raw_message
- severity
- incident_id
- risk_score

### 9.2 Index naming

Use an index name such as:

```text
soc-alerts-YYYY.MM.DD
```

or

```text
mini-siem-logs
```

### 9.3 Query strategy

Your Python app can query:
- the last 5 minutes of data
- only high/critical alerts
- only events for a selected host
- only events for a selected user

### 9.4 Refresh strategy

Use a polling loop:
- every 3 to 10 seconds
- fetch the latest events
- update the dashboard

This is simpler than implementing true streaming and still feels real-time.

---

## 10. Wazuh Integration Plan

### 10.1 Install agent

Install the Wazuh agent on:
- Ubuntu server
- Windows VM
- any test Linux machine

### 10.2 What logs to monitor

Recommended logs:
- `/var/log/auth.log`
- `/var/log/syslog`
- Windows Security Logs
- application logs
- firewall logs

### 10.3 Alert flow

Wazuh rules can detect:
- failed SSH attempts
- root login attempts
- suspicious privilege escalation
- file integrity changes
- malware-like behavior

These alerts can then be consumed by your Python project.

---

## 11. Python Correlation Engine

Your Python layer should act like a mini SOC analyst.

### Input

Records from Elasticsearch.

### Output

A list of detected incidents such as:
- Brute Force Attack
- Password Spray
- Off-Hours Access
- Compromised Account
- Port Scan
- Suspicious Data Exfiltration

### Example logic

```python
if failed_login_count >= 5 and time_window <= 2 minutes:
    create_incident("Brute Force")
```

```python
if same_ip_targets_many_users:
    create_incident("Password Spray")
```

```python
if login_time outside normal_work_hours:
    increase_risk_score()
```

---

## 12. Dashboard Design

The Streamlit dashboard should include:

### Top metrics
- total logs
- total alerts
- critical alerts
- open incidents

### Visualizations
- events over time
- top source IPs
- top target hosts
- alerts by severity
- alerts by event type

### Tables
- recent events
- open incidents
- suspicious users
- high-risk IPs

### Filters
- date range
- source IP
- host
- user
- severity
- event type

---

## 13. PDF Report Structure

The PDF report should contain:

### Title
- SOC Incident Report

### Summary section
- report period
- total events processed
- total alerts
- critical incidents

### Incident details
- incident type
- source IP
- affected host
- affected user
- severity
- timeline
- short analyst note

### Recommendations
- block IP
- reset password
- enable MFA
- review logs
- isolate host

---

## 14. Email Notification Logic

Send email when:
- severity is High or Critical
- multiple incidents are detected
- account compromise is suspected
- brute-force attack exceeds a threshold

Email content:
- subject line
- short summary
- PDF attachment
- timestamp

Suggested subject:

```text
[ALERT] SOC Incident Report - High Severity Activity Detected
```

---

## 15. Suggested Development Phases

### Phase 1: Connect to Elasticsearch
- install Elasticsearch
- push events into an index
- verify search queries

### Phase 2: Add live polling
- query new logs every few seconds
- update a live table

### Phase 3: Add detection rules
- brute force
- password spray
- off-hours login
- port scan

### Phase 4: Add dashboard
- metrics
- graphs
- filters

### Phase 5: Add incident generation
- group related logs
- create severity

### Phase 6: Add reporting
- generate PDF
- email it automatically

---

## 16. Recommended Local Setup

### Minimum
- Python 3.10+
- 8 GB RAM
- Docker Desktop or Docker Engine
- Ubuntu VM or WSL2

### Helpful
- one Linux test machine
- one Windows VM
- Docker Compose
- Git

---

## 17. What to Keep from the Current CSV Project

You should keep the current project as a **testing harness**.

Use the CSV version for:
- logic testing
- dashboard prototyping
- PDF formatting
- incident rule validation

Then replace the CSV input with live Elasticsearch queries.

This way, you do not need to rebuild the whole system.

---

## 18. Suggested Implementation Order

1. Make Elasticsearch reachable from your local machine
2. Create an ingestion script that inserts logs into Elasticsearch
3. Create a Python script that polls Elasticsearch for new records
4. Run the existing detection rules on these records
5. Update the dashboard to read from the live backend
6. Generate PDFs for critical incidents
7. Send email notifications
8. Optionally add Wazuh later

---

## 19. Best Practical Recommendation

For a real-time internship project, the best path is:

**Elasticsearch first, Wazuh second.**

That means:
- first make your project read and display live logs from Elasticsearch
- then connect Wazuh for real endpoint and security alert ingestion

This avoids getting stuck too early in complex agent installation and backend setup.

---

## 20. Final Goal

The final project should behave like this:

```text
Logs arrive continuously
→ system indexes them
→ detection rules run
→ suspicious events become incidents
→ dashboard updates instantly
→ high severity incidents become PDF reports
→ report gets emailed automatically
```

That is the real-time SOC system you want to build.

---

## 21. Next Step

The next practical task is to implement:

1. Elasticsearch connection
2. live event ingestion
3. polling-based dashboard refresh
4. automatic incident generation

After that, Wazuh can be added to make the setup closer to a production SOC.

