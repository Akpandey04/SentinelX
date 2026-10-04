# SentinelX Incident Detection Rules

This document outlines the rule logic currently implemented in the SentinelX pipeline that determines how raw events are flagged, scored, and escalated into incidents.

## 1. Detection Phase (`backend/engines/detection.py`)

The Detection Engine evaluates every normalized event against baseline security rules.

**Current Active Rule:**
* **Trigger:** Any event with `event_type == "SSH_LOGIN_FAILED"`
* **Action:** The event's state is upgraded to `DETECTED`.
* **Tags Added:** `AuthFailure`

*Note: In the future, this engine is designed to parse external YAML files in this directory to allow dynamic rule creation (e.g., Sigma or YARA style rules).*

## 2. Risk & Severity Phase (`backend/engines/risk.py`)

Once an event passes the Detection Engine, the Risk Engine assigns a severity and a numeric risk score to quantify the threat level.

**Current Active Rule:**
* **Trigger:** Any event where the state is `DETECTED` or `CORRELATED`.
* **Action:** 
  * The event is assigned a **Risk Score of 50**.
  * The event is assigned a **Severity of HIGH**.

## 3. Incident Escalation Phase (`backend/engines/incident.py`)

The Incident Engine maintains state. Instead of treating every single log as an isolated alert, it groups related attacks together.

**Current Active Rule:**
* **Trigger:** Any event that is `DETECTED` and has an assigned severity, containing both a `source_ip` (Attacker) and `destination_ip` (Target).
* **Action (New Attack):** If no active incident exists for this Attacker-Target pair, a new Incident is created with the title `"Suspicious Activity from [Attacker IP]"`. The event state is upgraded to `INCIDENT`.
* **Action (Ongoing Attack):** If an active incident already exists for this IP pair, the new event is grouped under the existing incident. The incident's overall risk score is dynamically updated to match the highest risk score of its grouped events.
