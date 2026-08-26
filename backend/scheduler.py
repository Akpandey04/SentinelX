import schedule
import time
import os
import sys
import datetime

# Add the parent directory to sys.path so python can resolve "backend.app..."
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.reporting import generate_pdf_report
from backend.app.mailer import send_alerts_to_list
from backend.database.sqlite_adapter import SQLiteAdapter

def job():
    print(f"\n--- [{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting Scheduled SOC SIEM Report & Email ---")
    try:
        # Create reports dir
        os.makedirs("reports", exist_ok=True)
        
        # Connect to DB to get stats
        db = SQLiteAdapter("siem_data.db")
        with db._get_connection() as conn:
            # Fetch recent incidents for the report
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, source_ip, event_type, metadata FROM events WHERE state = 'INCIDENT' ORDER BY timestamp DESC LIMIT 10")
            incidents = cursor.fetchall()
            
        if not incidents:
            print("No new incidents to report. Skipping email.")
            return

        summary_rows = []
        import json
        for row in incidents:
            meta = {}
            if row[3]:
                try: meta = json.loads(row[3])
                except: pass
            
            summary_rows.append({
                "timestamp": row[0],
                "source_ip": row[1],
                "incident_type": row[2],
                "severity": meta.get('severity', 'High'),
                "hostname": meta.get('hostname', 'Unknown'),
                "summary": meta.get('description', f"Incident detected for {row[2]}")
            })

        report_filename = f"reports/Scheduled_SOC_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        print(f"Generating PDF Report: {report_filename}")
        
        generate_pdf_report(
            output_path=report_filename,
            title="Scheduled SOC Incident Report",
            summary_rows=summary_rows
        )
        
        print("Dispatching Scheduled Email Alerts...")
        send_alerts_to_list(report_filename)
        
        print(f"--- [{time.strftime('%Y-%m-%d %H:%M:%S')}] Scheduled task completed successfully! ---\n")
    except Exception as e:
        print(f"--- [{time.strftime('%Y-%m-%d %H:%M:%S')}] Scheduled task failed with error: {str(e)} ---\n")

print("SOC SIEM Scheduler Started!")
print("Keep this terminal open. The script will automatically run based on the schedule.")

# ---------------------------------------------------------
# TIMING CONFIGURATION (Aap apni zaroorat ke hisaab se set karein)
# ---------------------------------------------------------

# Option 1: Har X minute baad mail bhejne ke liye (Abhi 10 minute par set hai)
schedule.every(1).minutes.do(job)

# Agar aap chahte hain ki script start hote hi ek baar turant mail bhej de, toh isko uncomment karein:
# job()

while True:
    schedule.run_pending()
    time.sleep(1)
