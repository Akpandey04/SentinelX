# Reproducibility Guide

## Experiment 1: Stateless vs. Stateful Architectural Ablation (500 events)
**Paper Target:**
- Stateless: 261.16 ± 6.06 EPS, P99: 5.35 ± 0.20 ms.
- Stateful: 122.27 ± 1.34 EPS, P99: 12.06 ± 1.15 ms.
- Throughput reduction: 53.18%; P99 increase: +6.71 ms (+125.42%).

**Command:** python experiments/benchmarks/run_ablation.py --workload 500 --runs 5

## Experiment 2: Resource Scaling (500, 1,000, 5,000, 10,000 events)
**Paper Target:**
- 500 events: 12.4% avg / 18.1% peak CPU; 45.2 MB avg / 46.8 MB peak RSS.
- 10,000 events: 22.1% avg / 34.2% peak CPU; 68.9 MB avg / 81.4 MB peak RSS.

**Command:** python experiments/resource_profiling/profile_resources.py --tiers 500,1000,5000,10000

## Experiment 3: Deterministic Grouping & Boundary Separation
**Paper Target:** 4 alerts with mixed attributes -> 3 distinct incidents (AAR = 25.0%).
**Command:** pytest experiments/incident_grouping/test_grouping.py -v

## Experiment 4: Continuous Repetitive Workload Consolidation
**Paper Target:** 206 SSH_LOGIN_FAILED alerts sharing attacker/target -> 1 active incident (AAR = 99.51%).
**Command:** python experiments/incident_grouping/run_aar_validation.py --alerts 206