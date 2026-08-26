import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ShieldAlert, Activity, Users, AlertTriangle, Search, History, X, Clock, Target, CheckCircle, Server, Activity as ActivityIcon, Menu, Mail, LayoutDashboard, List as ListIcon } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, Legend, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';

const geoUrl = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";
import './index.css';

const API_BASE = 'http://localhost:8000/api';
const HEALTH_API = 'http://localhost:8000/health';

const COLORS = ['#dc3545', '#fd7e14', '#ffc107', '#198754']; // Critical(Danger), High(Orange), Medium(Warning), Low(Success)

function App() {
  const [stats, setStats] = useState(null);
  const [incidents, setIncidents] = useState([]);
  const [logs, setLogs] = useState([]);
  const [health, setHealth] = useState(null);
  const [assets, setAssets] = useState([]);
  const [alertHistory, setAlertHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [backendOnline, setBackendOnline] = useState(true);
  
  // Sidebar state
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeView, setActiveView] = useState('dashboard'); // 'dashboard', 'logs', 'mail'

  // Live refresh state
  const [refreshInterval, setRefreshInterval] = useState(5000); // Default 5s
  const [isLive, setIsLive] = useState(true);

  const [filters, setFilters] = useState({
    startDate: '',
    endDate: '',
    severity: 'All',
    searchIp: '',
    searchEvent: ''
  });

  const fetchData = async () => {
    try {
      const { startDate, endDate, severity, searchIp, searchEvent } = filters;
      const params = {};
      if (startDate) params.start_date = startDate;
      if (endDate) params.end_date = endDate;

      const statsRes = await axios.get(`${API_BASE}/stats`, { params });
      setStats(statsRes.data);

      const incParams = { ...params };
      if (severity !== 'All') incParams.severity = severity;
      const incRes = await axios.get(`${API_BASE}/incidents`, { params: incParams });
      setIncidents(incRes.data);

      const logParams = { ...params, limit: 50 };
      if (searchIp) logParams.source_ip = searchIp;
      if (searchEvent) logParams.event_type = searchEvent;
      const logsRes = await axios.get(`${API_BASE}/logs`, { params: logParams });
      setLogs(logsRes.data);

      const assetsRes = await axios.get(`${API_BASE}/assets`);
      setAssets(assetsRes.data);

      const alertHistoryRes = await axios.get(`${API_BASE}/alert_history`, { params });
      setAlertHistory(alertHistoryRes.data);

      const healthRes = await axios.get(HEALTH_API);
      setHealth(healthRes.data);
      
      setBackendOnline(true);
    } catch (error) {
      console.error("Error fetching data:", error);
      setBackendOnline(false);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
    let intervalId;
    if (isLive && refreshInterval > 0) {
      intervalId = setInterval(fetchData, refreshInterval);
    }
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [filters, isLive, refreshInterval]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const mitreMapping = {
    'SSH_LOGIN_FAILED': 'T1110 (Brute Force)',
    'PASSWORD_SPRAY': 'T1110.003 (Password Spraying)',
    'PORT_SCAN': 'Discovery / Reconnaissance',
    'EXFILTRATION': 'T1041 (Exfiltration Over C2 Protocol)'
  };
  
  const pieData = stats?.severity_counts ? Object.keys(stats.severity_counts).map(key => ({
    name: key, value: stats.severity_counts[key]
  })) : [];

  const getBadgeClass = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical': return 'bg-danger';
      case 'high': return 'bg-warning text-dark';
      case 'medium': return 'bg-info text-dark';
      default: return 'bg-success';
    }
  };

  return (
    <div className="d-flex flex-column vh-100 bg-dark text-white">
      {/* HEADER */}
      <header className="navbar navbar-dark bg-dark border-bottom shadow-sm px-3 flex-shrink-0" style={{ zIndex: 1000, borderColor: '#343a40' }}>
        <div className="d-flex align-items-center">
          <button className="btn btn-outline-secondary me-3 border-0 text-white" onClick={() => setSidebarOpen(!sidebarOpen)}>
            <Menu size={24} />
          </button>
          <a className="navbar-brand d-flex align-items-center" href="#">
            <Target size={28} className="text-primary me-2" />
            <span className="fw-bold tracking-wider">SentinelX</span>
          </a>
          <span className="text-muted ms-2 d-none d-md-inline" style={{ fontSize: '0.85rem', paddingTop: '4px' }}>Enterprise Security Information & Event Management</span>
        </div>
        
        <div className="d-flex align-items-center gap-3">
          <div className="d-flex align-items-center gap-2 bg-dark rounded px-2 py-1 border border-secondary">
            <label className="text-muted small mb-0">Live Refresh:</label>
            <select 
              className="form-select form-select-sm bg-dark text-white border-secondary"
              style={{ width: '130px' }}
              value={refreshInterval} 
              onChange={(e) => {
                const val = parseInt(e.target.value);
                setRefreshInterval(val);
                setIsLive(val > 0);
              }}
            >
              <option value={0}>Off</option>
              <option value={5000}>5 seconds</option>
              <option value={10000}>10 seconds</option>
              <option value={15000}>15 seconds</option>
            </select>
            {isLive && <span className="badge bg-danger rounded-circle p-1 ms-1"><span className="visually-hidden">Live</span></span>}
          </div>
          
          {health && (
            <div className="d-flex gap-2">
              <span title="Database Status"><Server size={20} className={health.database === 'healthy' ? 'text-success' : 'text-danger'} /></span>
              <span title="Queue Status"><ActivityIcon size={20} className={health.queue === 'healthy' ? 'text-success' : 'text-danger'} /></span>
            </div>
          )}
        </div>
      </header>

      <div className="d-flex flex-grow-1 overflow-hidden">
        {/* SIDEBAR */}
        {sidebarOpen && (
          <div className="bg-dark border-end border-secondary d-flex flex-column flex-shrink-0 p-3" style={{ width: '250px' }}>
            <ul className="nav nav-pills flex-column mb-auto gap-2">
              <li className="nav-item">
                <button 
                  className={`nav-link text-start w-100 ${activeView === 'dashboard' ? 'active bg-primary' : 'text-white'}`}
                  onClick={() => setActiveView('dashboard')}
                >
                  <LayoutDashboard size={18} className="me-2" /> Dashboard
                </button>
              </li>
              <li>
                <button 
                  className={`nav-link text-start w-100 ${activeView === 'logs' ? 'active bg-primary' : 'text-white'}`}
                  onClick={() => setActiveView('logs')}
                >
                  <ListIcon size={18} className="me-2" /> Log Activity
                </button>
              </li>
              <li>
                <button 
                  className={`nav-link text-start w-100 ${activeView === 'mail' ? 'active bg-primary' : 'text-white'}`}
                  onClick={() => setActiveView('mail')}
                >
                  <Mail size={18} className="me-2" /> Mail History
                </button>
              </li>
            </ul>
          </div>
        )}

        {/* MAIN CONTENT AREA */}
        <main className="flex-grow-1 overflow-auto p-4" style={{ backgroundColor: '#1a1d20' }}>
          
          {activeView === 'dashboard' && (
            <div className="container-fluid p-0">
              {/* Alert for restart */}
              {!backendOnline && (
                <div className="alert alert-primary d-flex align-items-center shadow-sm" role="alert" style={{backgroundColor: '#052c65', borderColor: '#084298', color: '#cfe2ff'}}>
                  <AlertTriangle size={24} className="me-3" />
                  <div>
                    <strong>Connection Lost:</strong> Start the backend server to view live charts.
                  </div>
                </div>
              )}

              {/* KPI Cards */}
              <div className="row g-3 mb-4">
                <div className="col-12 col-sm-6 col-xl-3">
                  <div className="card bg-dark border-secondary h-100 shadow-sm">
                    <div className="card-body">
                      <h6 className="card-subtitle mb-2 text-muted"><Activity size={16} className="me-1" /> Total Events</h6>
                      <h2 className="card-title text-primary mb-0">{stats?.total_events?.toLocaleString() || 0}</h2>
                    </div>
                  </div>
                </div>
                <div className="col-12 col-sm-6 col-xl-3">
                  <div className="card bg-dark border-secondary h-100 shadow-sm">
                    <div className="card-body">
                      <h6 className="card-subtitle mb-2 text-muted"><AlertTriangle size={16} className="me-1" /> Failed Logins</h6>
                      <h2 className="card-title text-danger mb-0">{stats?.failed_logins?.toLocaleString() || 0}</h2>
                    </div>
                  </div>
                </div>
                <div className="col-12 col-sm-6 col-xl-3">
                  <div className="card bg-dark border-secondary h-100 shadow-sm">
                    <div className="card-body">
                      <h6 className="card-subtitle mb-2 text-muted"><ShieldAlert size={16} className="me-1" /> Active Incidents</h6>
                      <h2 className="card-title text-warning mb-0">{incidents.length}</h2>
                    </div>
                  </div>
                </div>
                <div className="col-12 col-sm-6 col-xl-3">
                  <div className="card bg-dark border-secondary h-100 shadow-sm">
                    <div className="card-body">
                      <h6 className="card-subtitle mb-2 text-muted"><Users size={16} className="me-1" /> Unique Sources</h6>
                      <h2 className="card-title text-success mb-0">{stats?.unique_ips?.toLocaleString() || 0}</h2>
                    </div>
                  </div>
                </div>
              </div>

              {/* Charts Row */}
              <div className="row g-4 mb-4">
                <div className="col-lg-6">
                  <div className="card bg-dark border-secondary h-100 shadow-sm">
                    <div className="card-header border-secondary fw-bold">Incidents by Severity</div>
                    <div className="card-body" style={{ height: '350px' }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie data={pieData} cx="50%" cy="50%" innerRadius={70} outerRadius={100} paddingAngle={2} dataKey="value" stroke="none">
                            {pieData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                          </Pie>
                          <Tooltip 
                            contentStyle={{ backgroundColor: '#212529', borderColor: '#495057', color: '#fff' }} 
                            formatter={(value, name) => {
                              const total = pieData.reduce((sum, entry) => sum + entry.value, 0);
                              const percent = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                              return [`${percent}%`, name];
                            }}
                          />
                          <Legend />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
                
                <div className="col-lg-6">
                  <div className="card bg-dark border-secondary h-100 shadow-sm">
                    <div className="card-header border-secondary fw-bold">Events Over Time</div>
                    <div className="card-body" style={{ height: '350px' }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={stats?.events_over_time || []} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#495057" />
                          <XAxis dataKey="date" stroke="#adb5bd" />
                          <YAxis stroke="#adb5bd" />
                          <Tooltip contentStyle={{ backgroundColor: '#212529', borderColor: '#495057', color: '#fff' }} />
                          <Bar dataKey="count" fill="#0d6efd" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="row g-4 mb-4">
                {/* Global Map */}
                <div className="col-lg-7">
                  <div className="card bg-dark border-secondary h-100 shadow-sm">
                    <div className="card-header border-secondary fw-bold">Global Threat Map</div>
                    <div className="card-body d-flex align-items-center justify-content-center p-0" style={{ height: '400px', overflow: 'hidden' }}>
                      <ComposableMap projection="geoMercator" projectionConfig={{ scale: 140, center: [0, 30] }} style={{ width: '100%', height: '100%' }}>
                        <Geographies geography={geoUrl}>
                          {({ geographies }) => {
                            const activeCountries = stats?.top_ips?.map(m => m.country) || [];
                            return geographies.map((geo) => {
                              const isActive = activeCountries.includes(geo.properties.name);
                              return (
                                <Geography 
                                  key={geo.rsmKey} 
                                  geography={geo} 
                                  fill={isActive ? "#495057" : "#2b3035"} 
                                  stroke="#495057" 
                                  strokeWidth={isActive ? 1 : 0.5} 
                                  style={{ default: { outline: "none" }, hover: { fill: "#6c757d", outline: "none" }, pressed: { outline: "none" } }} 
                                />
                              );
                            });
                          }}
                        </Geographies>
                        {stats?.top_ips?.map((marker, i) => (
                          <Marker key={i} coordinates={[marker.lng, marker.lat]}>
                            <circle r={5} fill="#dc3545" stroke="#fff" strokeWidth={1.5} />
                            <text textAnchor="middle" y={-10} style={{ fontFamily: "system-ui", fill: "#fff", fontSize: 11, fontWeight: "bold" }}>
                              {marker.country === "United States of America" ? "USA" : marker.country}
                            </text>
                          </Marker>
                        ))}
                      </ComposableMap>
                    </div>
                  </div>
                </div>

                {/* Country Attack Distribution */}
                <div className="col-lg-5">
                  <div className="card bg-dark border-secondary h-100 shadow-sm">
                    <div className="card-header border-secondary fw-bold">Attacks by Country (Percentages)</div>
                    <div className="card-body" style={{ height: '400px' }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={stats?.top_ips || []} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#495057" />
                          <XAxis 
                            dataKey="country" 
                            stroke="#adb5bd" 
                            tickFormatter={(val) => val === "United States of America" ? "USA" : val}
                          />
                          <YAxis stroke="#adb5bd" />
                          <Tooltip 
                            contentStyle={{ backgroundColor: '#212529', borderColor: '#495057', color: '#fff' }} 
                            formatter={(value, name) => {
                               const total = stats?.top_ips?.reduce((sum, item) => sum + item.count, 0) || 1;
                               const pct = ((value / total) * 100).toFixed(1);
                               return [`${pct}% (${value} total)`, "Attacks"];
                            }}
                          />
                          <Bar dataKey="count" fill="#ffc107" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              </div>

              {/* MITRE ATT&CK Row */}
              <div className="row g-4 mb-4">
                <div className="col-12">
                  <div className="card bg-dark border-secondary h-100 shadow-sm">
                    <div className="card-header border-secondary fw-bold">MITRE ATT&CK Mapping</div>
                    <div className="card-body p-0" style={{ height: '300px', overflowY: 'auto' }}>
                      <table className="table table-dark table-striped table-hover mb-0">
                        <thead style={{ position: 'sticky', top: 0, zIndex: 1 }}>
                          <tr>
                            <th className="bg-dark text-secondary">Event Type</th>
                            <th className="bg-dark text-secondary">MITRE Technique</th>
                          </tr>
                        </thead>
                        <tbody>
                          {Array.from(new Set(logs.map(l => l.event_type))).map((type, i) => (
                            <tr key={i}>
                              <td className="text-info fw-bold">{type}</td>
                              <td>{mitreMapping[type] || 'TBD (Custom)'}</td>
                            </tr>
                          ))}
                          {logs.length === 0 && (
                            <tr><td colSpan="2" className="text-center text-muted py-4">Waiting for events...</td></tr>
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>

              {/* Timeline and Incidents Row */}
              <div className="row g-4 mb-4">
                <div className="col-lg-6">
                  <div className="card bg-dark border-secondary h-100 shadow-sm">
                    <div className="card-header border-secondary fw-bold d-flex align-items-center">
                      <Clock size={18} className="text-info me-2" /> Attack Timeline View
                    </div>
                    <div className="card-body p-3" style={{ height: '400px', overflowY: 'auto' }}>
                      <ul className="list-unstyled mb-0">
                        {logs.slice(0, 20).map((log, i) => (
                          <li key={i} className="d-flex position-relative mb-3 pb-3 border-bottom border-secondary">
                            <div className="flex-shrink-0 pt-1" style={{ width: '85px' }}>
                              <small className="text-muted">{new Date(log.timestamp).toLocaleTimeString()}</small>
                            </div>
                            <div className="flex-grow-1 ms-3 border-start border-2 border-secondary ps-3 position-relative">
                              <span className={`position-absolute top-50 start-0 translate-middle p-1 rounded-circle border border-dark ${log.risk_score > 50 ? 'bg-danger' : 'bg-info'}`}></span>
                              <div className="fw-bold text-light">{log.event_type}</div>
                              <div className="small text-muted">{log.raw_message}</div>
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
                
                <div className="col-lg-6">
                  <div className="card bg-dark border-secondary h-100 shadow-sm">
                    <div className="card-header border-secondary fw-bold">Detected Incidents</div>
                    <div className="card-body p-0" style={{ height: '400px', overflowY: 'auto' }}>
                      <table className="table table-dark table-striped table-hover mb-0">
                        <thead style={{ position: 'sticky', top: 0, zIndex: 1 }}>
                          <tr>
                            <th className="bg-dark text-secondary">Incident ID</th>
                            <th className="bg-dark text-secondary">Title</th>
                            <th className="bg-dark text-secondary">Severity</th>
                            <th className="bg-dark text-secondary">Attacker IP</th>
                          </tr>
                        </thead>
                        <tbody>
                          {incidents.map((inc, i) => (
                            <tr key={i}>
                              <td className="text-info font-monospace">{inc.incident_id.substring(0, 8)}...</td>
                              <td>{inc.title}</td>
                              <td><span className={`badge ${getBadgeClass(inc.severity)}`}>{inc.severity}</span></td>
                              <td className="font-monospace">{inc.attacker_ip}</td>
                            </tr>
                          ))}
                          {incidents.length === 0 && (
                            <tr><td colSpan="4" className="text-center text-muted py-4">No active incidents. Systems secure.</td></tr>
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Asset Inventory */}
              <div className="card bg-dark border-secondary shadow-sm mb-4">
                <div className="card-header border-secondary fw-bold">Asset Inventory</div>
                <div className="card-body p-0" style={{ maxHeight: '400px', overflowY: 'auto' }}>
                  <table className="table table-dark table-striped table-hover mb-0">
                    <thead style={{ position: 'sticky', top: 0, zIndex: 1 }}>
                      <tr>
                        <th className="bg-dark text-secondary">Asset ID</th>
                        <th className="bg-dark text-secondary">Hostname</th>
                        <th className="bg-dark text-secondary">IP Address</th>
                        <th className="bg-dark text-secondary">Type</th>
                        <th className="bg-dark text-secondary">Criticality</th>
                        <th className="bg-dark text-secondary">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {assets.map((ast, i) => (
                        <tr key={i}>
                          <td className="text-info font-monospace">{ast.id}</td>
                          <td className="fw-semibold">{ast.hostname}</td>
                          <td className="font-monospace">{ast.ip}</td>
                          <td>{ast.type}</td>
                          <td><span className={`badge ${getBadgeClass(ast.criticality)}`}>{ast.criticality}</span></td>
                          <td>
                            <span className={ast.status === 'Active' ? 'text-success fw-semibold' : 'text-muted'}>
                              {ast.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                      {assets.length === 0 && (
                        <tr><td colSpan="6" className="text-center text-muted py-4">No assets found.</td></tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeView === 'logs' && (
            <div className="container-fluid p-0">
              <div className="card bg-dark border-secondary shadow-sm mb-4">
                <div className="card-header border-secondary fw-bold d-flex justify-content-between align-items-center">
                  Log Activity
                  <Search size={16} className="text-muted" />
                </div>
                <div className="card-body">
                  <div className="row g-3 mb-4">
                    <div className="col-md-3">
                      <input type="text" name="searchIp" placeholder="Search Source IP" value={filters.searchIp} onChange={handleFilterChange} className="form-control bg-dark text-white border-secondary" />
                    </div>
                    <div className="col-md-3">
                      <input type="text" name="searchEvent" placeholder="Search Event Type" value={filters.searchEvent} onChange={handleFilterChange} className="form-control bg-dark text-white border-secondary" />
                    </div>
                    <div className="col-md-3">
                      <input type="date" name="startDate" value={filters.startDate} onChange={handleFilterChange} className="form-control bg-dark text-white border-secondary text-muted" />
                    </div>
                    <div className="col-md-3">
                      <input type="date" name="endDate" value={filters.endDate} onChange={handleFilterChange} className="form-control bg-dark text-white border-secondary text-muted" />
                    </div>
                  </div>

                  <div className="table-responsive border border-secondary rounded" style={{ maxHeight: '600px' }}>
                    <table className="table table-dark table-striped table-hover mb-0">
                      <thead style={{ position: 'sticky', top: 0, zIndex: 1 }}>
                        <tr>
                          <th className="bg-dark text-secondary">Time</th>
                          <th className="bg-dark text-secondary">Source IP</th>
                          <th className="bg-dark text-secondary">Target IP</th>
                          <th className="bg-dark text-secondary">Event Type</th>
                          <th className="bg-dark text-secondary">Message</th>
                        </tr>
                      </thead>
                      <tbody>
                        {logs.map((log, i) => (
                          <tr key={i}>
                            <td>{new Date(log.timestamp).toLocaleString()}</td>
                            <td className="font-monospace">{log.source_ip}</td>
                            <td className="font-monospace">{log.destination_ip}</td>
                            <td className="text-info fw-semibold">{log.event_type}</td>
                            <td>{log.raw_message}</td>
                          </tr>
                        ))}
                        {logs.length === 0 && (
                          <tr><td colSpan="5" className="text-center text-muted py-4">No logs match your filter.</td></tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeView === 'mail' && (
            <div className="container-fluid p-0">
              <div className="card bg-dark border-secondary shadow-sm mb-4">
                <div className="card-header border-secondary fw-bold d-flex justify-content-between align-items-center">
                  Mail Sent History
                  <History size={16} className="text-muted" />
                </div>
                <div className="card-body p-0">
                  <div className="table-responsive" style={{ maxHeight: '600px' }}>
                    <table className="table table-dark table-striped table-hover mb-0">
                      <thead style={{ position: 'sticky', top: 0, zIndex: 1 }}>
                        <tr>
                          <th className="bg-dark text-secondary">Date</th>
                          <th className="bg-dark text-secondary">Time</th>
                          <th className="bg-dark text-secondary">Name</th>
                          <th className="bg-dark text-secondary">Recipient</th>
                          <th className="bg-dark text-secondary">Subject</th>
                          <th className="bg-dark text-secondary">Status</th>
                          <th className="bg-dark text-secondary">Report</th>
                        </tr>
                      </thead>
                      <tbody>
                        {alertHistory.map((alert, i) => (
                          <tr key={i}>
                            <td>{alert.Date}</td>
                            <td>{alert.Time}</td>
                            <td className="fw-semibold">{alert.Name || "Unknown"}</td>
                            <td className="text-info">{alert.Recipient}</td>
                            <td>{alert.Subject}</td>
                            <td><span className={`badge ${alert.Status?.includes('Sent') ? 'bg-success' : 'bg-warning text-dark'}`}>{alert.Status}</span></td>
                            <td>
                              {alert.Report_File && alert.Report_File.includes('.pdf') ? (
                                <a href={`http://localhost:8000/reports/${alert.Report_File}`} target="_blank" rel="noreferrer" className="btn btn-sm btn-outline-info py-0">View</a>
                              ) : <span className="text-muted small">N/A</span>}
                            </td>
                          </tr>
                        ))}
                        {alertHistory.length === 0 && (
                          <tr><td colSpan="7" className="text-center text-muted py-4">No mail history found.</td></tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          )}
          
        </main>
      </div>
    </div>
  );
}

export default App;
