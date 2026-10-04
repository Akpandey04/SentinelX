import pandas as pd

def brute_force_detector(df: pd.DataFrame, threshold: int = 5):
    failed = df[df["event_type"].str.contains("Failed Login", case=False, na=False)]
    grouped = failed.groupby(["source_ip", "destination_ip"]).size().reset_index(name="failed_count")
    alerts = grouped[grouped["failed_count"] >= threshold].copy()
    alerts["alert_type"] = "Brute Force"
    return alerts

def password_spray_detector(df: pd.DataFrame, threshold_users: int = 5):
    failed = df[df["event_type"].str.contains("Failed Login", case=False, na=False)]
    grouped = failed.groupby("source_ip")["user_name"].nunique().reset_index(name="unique_users")
    alerts = grouped[grouped["unique_users"] >= threshold_users].copy()
    alerts["alert_type"] = "Password Spray"
    return alerts

def port_scan_detector(df: pd.DataFrame, threshold_ports: int = 5):
    scans = df[df["event_type"].str.contains("Port Scan Detected", case=False, na=False)]
    grouped = scans.groupby("source_ip")["destination_port"].nunique().reset_index(name="unique_ports")
    alerts = grouped[grouped["unique_ports"] >= threshold_ports].copy()
    alerts["alert_type"] = "Port Scan"
    return alerts

def off_hours_detector(df: pd.DataFrame, start_hour: int = 9, end_hour: int = 18):
    tmp = df.copy()
    tmp["timestamp"] = pd.to_datetime(tmp["timestamp"])
    tmp["hour"] = tmp["timestamp"].dt.hour
    suspicious = tmp[(tmp["auth_result"] == "success") & ((tmp["hour"] < start_hour) | (tmp["hour"] >= end_hour))]
    return suspicious