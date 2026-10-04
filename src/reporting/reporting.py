import pdfkit
from jinja2 import Template
import datetime
import os
from collections import Counter
import matplotlib.pyplot as plt
import io
import base64

def generate_pdf_report(output_path: str, title: str, summary_rows: list[dict]):
    # Analytical Calculations
    severity_counts = Counter(row.get("severity", "Unknown") for row in summary_rows)
    ip_counts = Counter(row.get("source_ip", "Unknown") for row in summary_rows if row.get("source_ip") and row.get("source_ip") != "N/A" and row.get("source_ip") != "nan")
    top_ips = ip_counts.most_common(3)
    
    # Generate Pie Chart
    pie_b64 = ""
    if severity_counts:
        labels = list(severity_counts.keys())
        sizes = list(severity_counts.values())
        colors_map = {'Critical': '#e74c3c', 'High': '#e67e22', 'Medium': '#f1c40f', 'Low': '#2ecc71'}
        colors = [colors_map.get(l, '#95a5a6') for l in labels]
        
        plt.figure(figsize=(5, 3))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 10, 'color': '#2c3e50', 'weight': 'bold'})
        plt.axis('equal')
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        pie_b64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            body { 
                font-family: 'Inter', sans-serif; 
                margin: 0; 
                padding: 40px; 
                background-color: #f4f7f6; 
                color: #2c3e50; 
            }
            .container {
                background: #ffffff;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                border-bottom: 3px solid #34495e;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }
            .header h1 { margin: 0; font-size: 28px; color: #1a252f; text-transform: uppercase; letter-spacing: 1px; }
            .header p { margin: 5px 0 0 0; color: #7f8c8d; font-size: 14px; }
            
            .dashboard {
                display: table;
                width: 100%;
                margin-bottom: 30px;
                border-spacing: 15px;
            }
            .dash-card {
                display: table-cell;
                background: #ecf0f1;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                border-top: 4px solid #3498db;
            }
            .dash-card.critical { border-top-color: #e74c3c; background: #fdf0ed; }
            .dash-card.high { border-top-color: #e67e22; background: #fdf5eb; }
            .dash-card.total { border-top-color: #2c3e50; background: #eef1f2; }
            
            .dash-value { font-size: 32px; font-weight: 700; margin-bottom: 5px; color: #2c3e50; }
            .dash-label { font-size: 12px; text-transform: uppercase; color: #7f8c8d; font-weight: 600; letter-spacing: 0.5px; }

            .section-title {
                font-size: 18px;
                color: #2c3e50;
                margin-bottom: 15px;
                font-weight: 700;
                border-left: 4px solid #3498db;
                padding-left: 10px;
            }

            .top-ips {
                margin-bottom: 30px;
                background: #fdfdfd;
                border: 1px solid #ecf0f1;
                border-radius: 6px;
                padding: 15px;
            }
            .top-ips ul { margin: 0; padding-left: 20px; color: #e74c3c; font-family: monospace; font-size: 14px; }
            
            table { width: 100%; border-collapse: collapse; font-size: 13px; }
            th, td { border-bottom: 1px solid #ecf0f1; padding: 12px 10px; text-align: left; }
            th { 
                background-color: #f8f9fa; 
                color: #34495e; 
                text-transform: uppercase; 
                letter-spacing: 0.5px; 
                font-size: 11px; 
                font-weight: 700;
            }
            tr:hover { background-color: #fcfcfc; }
            
            .badge { 
                padding: 4px 8px; 
                border-radius: 4px; 
                font-weight: 700; 
                color: white; 
                font-size: 11px;
                text-transform: uppercase;
                display: inline-block; 
                text-align: center; 
            }
            .Critical { background-color: #e74c3c; }
            .High { background-color: #e67e22; }
            .Medium { background-color: #f1c40f; color: #000; }
            .Low { background-color: #2ecc71; }
            
            .footer {
                margin-top: 40px;
                text-align: center;
                font-size: 11px;
                color: #bdc3c7;
                border-top: 1px solid #ecf0f1;
                padding-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <table style="width: 100%; margin-bottom: 20px; border: none;">
                <tr style="background: transparent;">
                    <td style="border: none; padding: 0;">
                        <h1 style="margin: 0; font-size: 28px; color: #1a252f; text-transform: uppercase; letter-spacing: 1px;">{{ title }}</h1>
                        <p style="margin: 5px 0 0 0; color: #7f8c8d; font-size: 14px;">Automated Security Intelligence Report</p>
                    </td>
                    <td style="text-align: right; border: none; padding: 0;">
                        <p style="margin: 0; color: #7f8c8d; font-size: 14px;"><strong>Date:</strong> {{ date }}</p>
                        <p style="margin: 5px 0 0 0; color: #e74c3c; font-size: 14px; font-weight: bold;">Confidentiality: Strictly Internal</p>
                    </td>
                </tr>
            </table>
            <hr style="border: 1px solid #34495e; margin-bottom: 30px;">

            <h2 class="section-title">Threat Overview</h2>
            <div class="dashboard">
                <div class="dash-card total">
                    <div class="dash-value">{{ total }}</div>
                    <div class="dash-label">Total Events</div>
                </div>
                <div class="dash-card critical">
                    <div class="dash-value" style="color: #e74c3c;">{{ critical_count }}</div>
                    <div class="dash-label">Critical Alerts</div>
                </div>
                <div class="dash-card high">
                    <div class="dash-value" style="color: #e67e22;">{{ high_count }}</div>
                    <div class="dash-label">High Alerts</div>
                </div>
            </div>

            <table style="width: 100%; border: none; margin-bottom: 30px;">
                <tr style="background: transparent;">
                    <td style="border: none; vertical-align: top; width: 50%;">
                        {% if pie_chart %}
                        <div style="text-align: center;">
                            <h3 style="margin-top: 0; font-size: 14px; color: #34495e;">Alerts by Severity</h3>
                            <img src="data:image/png;base64,{{ pie_chart }}" style="max-width: 300px; height: auto;">
                        </div>
                        {% endif %}
                    </td>
                    <td style="border: none; vertical-align: top; width: 50%;">
                        {% if top_ips %}
                        <div class="top-ips">
                            <h3 style="margin-top: 0; font-size: 14px; color: #34495e;">Top Attacker IPs Identified:</h3>
                            <ul>
                                {% for ip, count in top_ips %}
                                <li>{{ ip }} ({{ count }} events)</li>
                                {% endfor %}
                            </ul>
                        </div>
                        {% endif %}
                    </td>
                </tr>
            </table>

            <h2 class="section-title">Incident Details Log</h2>
            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Incident Type</th>
                        <th>Source IP</th>
                        <th>Host</th>
                        <th>Severity</th>
                        <th>Summary</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in rows %}
                    <tr>
                        <td style="color: #7f8c8d; font-size: 11px;">{{ row.timestamp }}</td>
                        <td><strong>{{ row.incident_type }}</strong></td>
                        <td style="font-family: monospace; color: #c0392b;">{{ row.source_ip }}</td>
                        <td style="color: #34495e;">{{ row.hostname }}</td>
                        <td><span class="badge {{ row.severity }}">{{ row.severity }}</span></td>
                        <td style="color: #7f8c8d;">{{ row.summary }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <div class="footer">
                Report automatically generated by Mini SOC SIEM System. Do not distribute outside of the security team.
            </div>
        </div>
    </body>
    </html>
    """
    
    template = Template(html_template)
    html_out = template.render(
        title=title, 
        date=datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S"),
        total=len(summary_rows),
        critical_count=severity_counts.get("Critical", 0),
        high_count=severity_counts.get("High", 0),
        top_ips=top_ips,
        pie_chart=pie_b64,
        rows=summary_rows
    )
    
    path_wkhtmltopdf = r"D:\Brochure Generation System\wkhtmltopdf\bin\wkhtmltopdf.exe"
    
    try:
        if os.path.exists(path_wkhtmltopdf):
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            pdfkit.from_string(html_out, output_path, configuration=config, options={"enable-local-file-access": ""})
        else:
            print(f"Warning: wkhtmltopdf not found at {path_wkhtmltopdf}. Attempting to use system PATH.")
            pdfkit.from_string(html_out, output_path, options={"enable-local-file-access": ""})
    except Exception as e:
        print(f"Error generating PDF: {e}")