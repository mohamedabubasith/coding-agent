import { useState, useEffect, useRef } from 'react'
import './App.css'

const API_URL = 'http://localhost:8000/api/v1';

function App() {
  const [projects, setProjects] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [agentResult, setAgentResult] = useState(null);
  const [wsStatus, setWsStatus] = useState('Disconnected');
  const [wsMessages, setWsMessages] = useState([]);
  const wsRef = useRef(null);

  // --- Project API ---
  const fetchProjects = async () => {
    try {
      const res = await fetch(`${API_URL}/projects/`);
      const data = await res.json();
      setProjects(data);
    } catch (err) {
      console.error("Failed to fetch projects", err);
    }
  };

  const createProject = async () => {
    const name = `proj_${Math.floor(Math.random() * 1000)}`;
    try {
      const res = await fetch(`${API_URL}/projects/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_name: name,
          description: "Test Project from React",
          config: { created_via: "frontend" }
        })
      });
      const data = await res.json();
      alert(`Created Project: ${data.project_name} (ID: ${data.id})`);
      fetchProjects();
    } catch (err) {
      alert("Failed to create project: " + err.message);
    }
  };

  // --- Audit API ---
  const fetchAuditLogs = async () => {
    try {
      const res = await fetch(`${API_URL}/audit/`);
      const data = await res.json();
      setAuditLogs(data);
    } catch (err) {
      console.error("Failed to fetch audit logs", err);
    }
  };

  const createAuditLog = async () => {
    try {
      const res = await fetch(`${API_URL}/audit/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event_type: "FRONTEND_TEST",
          data: { clicked: true },
          source: "react-app"
        })
      });
      const data = await res.json();
      alert(`Created Audit Log: ${data.event_type}`);
      fetchAuditLogs();
    } catch (err) {
      alert("Failed to create audit log");
    }
  };

  // --- Agent API (HTTP) ---
  const runAgentHttp = async () => {
    setAgentResult("Running...");
    try {
      const res = await fetch(`${API_URL}/agent/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_id: projects[0]?.id || "test_proj",
          prompt: "List files in project",
          mode: "autonomous"
        })
      });
      const data = await res.json();
      setAgentResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setAgentResult("Error: " + err.message);
    }
  };

  // --- Agent API (WebSocket) ---
  const connectWs = () => {
    if (wsRef.current) return;
    const ws = new WebSocket('ws://localhost:8000/api/v1/agent/ws');
    
    ws.onopen = () => setWsStatus('Connected');
    ws.onclose = () => {
      setWsStatus('Disconnected');
      wsRef.current = null;
    };
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      setWsMessages(prev => [...prev, msg]);
    };
    
    wsRef.current = ws;
  };

  const sendWsPing = () => {
    if (wsRef.current) {
      wsRef.current.send(JSON.stringify({ action: "ping" }));
    }
  };

  const runAgentWs = () => {
    if (wsRef.current) {
      wsRef.current.send(JSON.stringify({
        action: "run",
        project_id: projects[0]?.id || "test_proj",
        prompt: "Hello via WS",
        mode: "autonomous"
      }));
    }
  };

  useEffect(() => {
    fetchProjects();
    fetchAuditLogs();
  }, []);

  return (
    <div className="App">
      <h1>Coding Agent Plugin - Test Console</h1>
      
      <div className="card">
        <h2>Projects</h2>
        <button onClick={createProject}>Create Random Project</button>
        <button onClick={fetchProjects}>Refresh List</button>
        <ul>
          {projects.map(p => (
            <li key={p.id}>{p.project_name} ({p.id}) - {p.storage_path}</li>
          ))}
        </ul>
      </div>

      <div className="card">
        <h2>Audit Logs</h2>
        <button onClick={createAuditLog}>Create Test Log</button>
        <button onClick={fetchAuditLogs}>Refresh List</button>
        <pre style={{textAlign: 'left', maxHeight: '200px', overflow: 'auto'}}>
          {JSON.stringify(auditLogs, null, 2)}
        </pre>
      </div>

      <div className="card">
        <h2>Agent (HTTP)</h2>
        <button onClick={runAgentHttp} disabled={projects.length === 0}>Run Agent on First Project</button>
        <pre style={{textAlign: 'left'}}>{agentResult}</pre>
      </div>

      <div className="card">
        <h2>Agent (WebSocket)</h2>
        <p>Status: {wsStatus}</p>
        <button onClick={connectWs} disabled={wsStatus === 'Connected'}>Connect</button>
        <button onClick={sendWsPing} disabled={wsStatus !== 'Connected'}>Ping</button>
        <button onClick={runAgentWs} disabled={wsStatus !== 'Connected' || projects.length === 0}>Run Agent</button>
        <div style={{textAlign: 'left', maxHeight: '200px', overflow: 'auto', border: '1px solid #ccc'}}>
          {wsMessages.map((m, i) => (
            <div key={i}>{JSON.stringify(m)}</div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App
