# Mini SOC SIEM Platform Documentation

## 1. Project Overview

This project is a lightweight, local, ELK-inspired Security Information and Event Management (SIEM) platform designed to help you simulate a real Security Operations Center (SOC) workflow on your own system.

The system is intentionally designed to behave like a mini Elastic stack:
- **Log collection**
- **Parsing and normalization**
- **Indexing into a queryable store**
- **Search and filtering**
- **Detection rules**
- **Risk scoring**
- **Incident generation**
- **PDF report creation**
- **Email notification**
- **Streamlit dashboard**

The project is suitable for a cybersecurity internship because it demonstrates how raw logs can be transformed into actionable security intelligence.

---

## 2. What the Project Solves

A real SOC receives huge amounts of raw logs from:
- Linux servers
- SSH authentication
- VPN gateways
- firewalls
- web servers
- administrative jump hosts
- internal systems

Analysts need to:
1. Ingest logs
2. Parse them
3. Search them
4. Detect suspicious activity
5. Generate incidents
6. Send reports
7. Track trends over time

This project simulates that workflow end-to-end.

---

## 3. Core Idea

The project is **not** just an ML model.

It is a **mini SIEM platform** where the detection engine can:
- find brute-force attempts
- detect password spraying
- identify suspicious off-hours login
- identify port scans
- identify unusual data transfer
- raise incidents
- compute risk score
- generate a PDF report
- email the report

Think of it as a simplified version of what Elastic Security or Splunk would do.

---

## 4. Data Files Included

### Main Log Dataset
- `mini_soc_siem_logs.csv`

This is the master dataset. It contains mixed security events from multiple sources.

### Source-Specific Log Files
- `mini_soc_siem_auth_logs.csv`
- `mini_soc_siem_vpn_logs.csv`
- `mini_soc_siem_firewall_logs.csv`
- `mini_soc_siem_web_logs.csv`

These are useful for source-wise analysis and dashboard filtering.

### Reference Data
- `mini_soc_siem_users.csv`
- `mini_soc_siem_assets.csv`
- `mini_soc_siem_ioc_feed.csv`

### Incident Register
- `mini_soc_siem_incidents.csv`

This file is useful for testing report generation and incident summary views.

---

## 5. Master CSV Schema

The master log file uses the following columns:

- `timestamp`
- `log_source`
- `hostname`
- `process`
- `event_type`
- `auth_result`
- `action`
- `user_name`
- `user_role`
- `source_ip`
- `destination_ip`
- `destination_port`
- `protocol`
- `bytes_sent`
- `bytes_received`
- `country`
- `city`
- `raw_message`

### Notes
- The dataset contains raw-ish logs rather than precomputed fields like severity and anomaly_score.
- That is intentional, because in a real SOC those values are computed by the SIEM/detection engine, not stored in the raw log itself.
- The platform should compute:
  - severity
  - risk score
  - anomaly score
  - incident type
  - alert summary

---

## 6. Why This Data Is Realistic

The generated dataset includes:
- successful internal SSH sessions
- VPN access
- firewall allow/deny events
- repeated failed logins
- brute-force bursts from the same external IP
- password spray behavior against multiple users
- off-hours logins
- compromised account behavior
- large outbound data transfer
- port scans across multiple ports

These are exactly the kinds of events a SOC analyst would investigate.

---

## 7. Detection Logic

The project should implement the following rules:

### 7.1 Brute Force Detection
Trigger when:
- multiple failed logins occur from the same IP
- within a short time window
- against the same target host or account

### 7.2 Password Spray Detection
Trigger when:
- the same source IP tries multiple usernames
- with repeated failures
- within a short period

### 7.3 Off-Hours Login Detection
Trigger when:
- a user logs in outside their normal login window
- especially if the source IP is external or unusual

### 7.4 Port Scan Detection
Trigger when:
- one source IP touches many destination ports
- on the same target host
- within a short period

### 7.5 Suspicious Data Transfer Detection
Trigger when:
- bytes_received or bytes_sent suddenly spikes
- especially after a new login
- or from a foreign source IP

---

## 8. Risk Scoring Model

The risk engine can assign points based on conditions such as:

- failed login burst: +25
- password spray: +30
- foreign IP: +20
- off-hours login: +20
- port scan: +35
- large data transfer: +30
- account lockout: +40
- privilege escalation: +50

Then classify risk as:
- Low
- Medium
- High
- Critical

Example:
- brute force + account lockout + foreign IP = Critical
- off-hours internal login = Medium or High depending on context

---

## 9. Suggested Architecture

```text
Raw Logs
   ↓
Ingestion / Normalization
   ↓
Indexing into SQLite or Elasticsearch-like store
   ↓
Search and filtering
   ↓
Detection rules
   ↓
Risk engine
   ↓
Incident creation
   ↓
PDF report generation
   ↓
Email notification
   ↓
Streamlit dashboard
```

---

## 10. Recommended Folder Structure

```text
mini_soc_siem_project/
│
├── data/
│   ├── mini_soc_siem_logs.csv
│   ├── mini_soc_siem_auth_logs.csv
│   ├── mini_soc_siem_vpn_logs.csv
│   ├── mini_soc_siem_firewall_logs.csv
│   ├── mini_soc_siem_web_logs.csv
│   ├── mini_soc_siem_users.csv
│   ├── mini_soc_siem_assets.csv
│   ├── mini_soc_siem_ioc_feed.csv
│   └── mini_soc_siem_incidents.csv
│
├── app/
│   ├── ingestion.py
│   ├── parser.py
│   ├── detections.py
│   ├── risk.py
│   ├── reporting.py
│   ├── mailer.py
│   └── dashboard.py
│
├── main.py
├── requirements.txt
└── PROJECT_DOCUMENTATION.md
```

---

## 11. Component Responsibilities

### Ingestion
Reads CSV logs and stores them into a searchable backend such as SQLite.

### Parser
Normalizes raw log text into structured fields.

### Detection Engine
Applies rule-based security logic.

### Risk Engine
Calculates incident severity and prioritization.

### Reporting
Builds a PDF summary of detected events.

### Mailer
Sends the PDF report through email.

### Dashboard
Displays:
- total logs
- event breakdown
- top source IPs
- top targets
- incidents by severity
- suspicious event timeline

---

## 12. Suggested Search / Query Features

Your platform can support searches like:
- source_ip = 198.51.100.44
- event_type contains "Failed Login"
- hostname = auth-server
- user_name = alice
- destination_port = 22
- country = Germany
- bytes_received > 1000000

This makes the project feel much closer to Elastic or Splunk.

---

## 13. PDF Report Contents

The PDF report should contain:
- report date
- total events analyzed
- number of alerts
- number of critical incidents
- top attacker IPs
- top affected hosts
- notable suspicious usernames
- incident summaries
- analyst recommendations

Example recommendation:
- reset credentials
- block attacker IP
- review VPN logs
- enable MFA
- investigate unusual off-hours access

---

## 14. Email Notification Flow

When the system detects a high-severity or critical incident:
1. Generate PDF
2. Attach the PDF
3. Send an email to SOC/security mailbox
4. Log the notification status

---

## 15. Suggested Technology Stack

### Core
- Python
- pandas
- SQLite or PostgreSQL
- Streamlit

### Optional / Advanced
- Elasticsearch
- Kibana-style dashboard
- ReportLab
- smtplib
- Plotly
- scikit-learn
- watchdog for live log monitoring

---

## 16. How To Run The Project Locally

### Step 1
Install dependencies:
```bash
pip install pandas streamlit plotly scikit-learn reportlab
```

### Step 2
Run the detection pipeline:
```bash
python main.py
```

### Step 3
Launch dashboard:
```bash
streamlit run app/dashboard.py
```

### Step 4
Generate report:
- run the report generator module
- export the PDF
- email the PDF

---

## 17. Test Scenarios

Your system should correctly identify:
1. Repeated failed SSH logins from the same IP
2. Password spray attempts across multiple usernames
3. Login from an unusual country
4. Off-hours login for a normal user
5. Port scan across multiple ports
6. Large suspicious data transfer
7. Account lockout after repeated failures
8. Compromised account with unusual post-login activity

---

## 18. What Makes This Project Strong For Internship Use

This project shows that you understand:
- raw logs
- SOC workflow
- rule-based detections
- incident prioritization
- reporting
- alerting
- dashboarding
- data engineering for security

That combination is much stronger than a normal ML-only project.

---

## 19. Future Improvements

You can later extend this project by adding:
- live tailing of Linux `/var/log/auth.log`
- Windows Event Log ingestion
- Elasticsearch backend
- full-text search
- saved searches
- alert rules management
- user authentication for the dashboard
- SIEM correlation rules
- threat intel enrichment
- ML-based anomaly detection on top of rule-based detections
- Docker deployment

---

## 20. Final Recommendation

Use the generated data as your lab dataset, then build the system so that:
- the raw logs are ingested
- parsed into structured form
- indexed for search
- analyzed by detection rules
- summarized into incidents
- reported as PDF
- emailed to a security mailbox
- visualized in Streamlit

That is the correct mini-SIEM / mini-Elastic workflow.
