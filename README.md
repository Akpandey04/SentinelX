# SentinelX
### Research artifact for 'Design and Functional Evaluation of a Lightweight Security Monitoring System'

## Overview
SentinelX is a lightweight, asynchronous, deterministic SIEM prototype tailored for empirical validation of stateful alert aggregation and resource-constrained security monitoring.

## Architecture Flow
Synthetic Telemetry -> EventBus -> PipelineManager -> Normalizer -> DetectionEngine -> RiskEngine -> IncidentEngine -> SQLitePersistence -> Reporting/Delivery

## Prerequisites
- Python 3.10+
- SQLite3
- wkhtmltopdf (required by pdfkit)

## Quickstart Guide
1. Clone repository
2. Create virtual environment: python -m venv venv && source venv/bin/activate
3. Install dependencies: pip install -r requirements.txt
4. Initialize database: python -m src.database.sqlite_adapter --init
5. Run unit tests: pytest tests/
6. Launch local pipeline: python -m src.core.pipeline_manager

## How to Run Synthetic Scenarios
The simulator will automatically load all YAML profiles placed in configs/simulations/.

## Reproducing Paper Results
Please refer to REPRODUCIBILITY.md for step-by-step instructions matching the manuscript.

## Repository Structure
- src/ : Core SIEM implementation
- configs/ : Runtime configurations and YAML rules
- experiments/ : Benchmark and profiling scripts
- evidence/ : Raw traces and summarized results
- tests/ : Pytest suites
- paper/ : Journal artifacts