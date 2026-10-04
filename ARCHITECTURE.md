# SentinelX Architecture

## Overview
SentinelX is a lightweight, asynchronous, deterministic SIEM prototype designed to validate stateful log aggregation efficiency.

## Core Pipeline Flow
1. **SimulatorCollector**: Ingests synthetic telemetry via parameterized YAML definitions.
2. **EventBus**: Acts as an asyncio.Queue decoupled transport layer, decoupling ingestion from processing.
3. **PipelineManager**: The asynchronous orchestrator managing the pipeline stages.
4. **Normalizer**: Transforms raw nested dictionaries into the explicitly typed SentinelEvent dataclass schema.
5. **DetectionEngine**: Executes deterministic rule-based conditional evaluation on the five active event types. (Note: _load_rules() is currently a stub).
6. **RiskEngine**: Precondition validation (requires DETECTED/CORRELATED state) and applies a discrete scoring matrix.
7. **IncidentEngine**: Stateful attribute-based grouping via exact SQL lookup on (attacker_ip, target_asset).
8. **SQLitePersistence**: A local relational store backing siem_data.db utilizing sqlite_adapter.py.
9. **Reporting & Mailer**: Decoupled scheduled polling, Jinja2 HTML compilation, pdfkit PDF generation, and SMTP transport.