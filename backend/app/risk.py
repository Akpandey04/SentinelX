def score_event(row) -> int:
    score = 0
    et = str(row.get("event_type", "")).lower()
    auth = str(row.get("auth_result", "")).lower()
    country = str(row.get("country", "")).lower()
    bytes_received = int(row.get("bytes_received", 0) or 0)

    if "failed login" in et:
        score += 20
    if "brute force" in et:
        score += 35
    if "password spray" in et:
        score += 30
    if "port scan" in et:
        score += 35
    if auth == "success" and country not in {"india", ""}:
        score += 20
    if bytes_received > 1000000:
        score += 30
    return min(score, 100)

def severity_from_score(score: int) -> str:
    if score >= 80:
        return "Critical"
    if score >= 60:
        return "High"
    if score >= 30:
        return "Medium"
    return "Low"