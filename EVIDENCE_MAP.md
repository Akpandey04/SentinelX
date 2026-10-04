# Evidence Map

| Paper Item | Metric / Claim | Evidence File in Repo | Reproduction Script | Input / Scenario File |
|---|---|---|---|---|
| Fig. 1 / 2 | End-to-end Architecture Flow | ARCHITECTURE.md | Source code inspect | src/core/pipeline_manager.py |
| Table IV | Deterministic Detection Rules | src/engines/detection.py | pytest tests/test_detection_rules.py | In-memory SentinelEvent |
| Table V | Predefined Risk & Severity | src/engines/risk.py | pytest tests/test_risk_mapping.py | In-memory SentinelEvent |
| Table IX / Fig. 6 | 500-Event Throughput (261.16 vs 122.27 EPS) | evidence/summaries/table_ix_throughput.csv | experiments/benchmarks/run_ablation.py | configs/simulations/ssh_bruteforce.yaml |
| Table X / Fig. 7 | P99 Latency (5.35 ms vs 12.06 ms) | evidence/summaries/table_x_latency.csv | experiments/benchmarks/run_ablation.py | configs/simulations/ssh_bruteforce.yaml |
| Table XI / Figs. 8, 9 | Resource Scaling (CPU peak 34.2%, RSS peak 81.4MB) | evidence/summaries/table_xi_resources.csv | experiments/resource_profiling/profile_resources.py | Pre-buffered synthetic events |
| Table XII (Case 1) | 4 Alerts -> 3 Incidents (AAR = 25.0%) | evidence/summaries/table_xii_aar.csv | experiments/incident_grouping/test_grouping.py | experiments/incident_grouping/incident_grouping_tests.csv |
| Table XII (Case 2) | 206 Alerts -> 1 Incident (AAR = 99.51%) | evidence/summaries/table_xii_aar.csv | experiments/incident_grouping/run_aar_validation.py | Continuous SSH_LOGIN_FAILED stream |