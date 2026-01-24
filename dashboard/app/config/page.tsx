"use client";

import { useEffect, useState } from "react";

import { apiFetch } from "../../lib/api";

export default function ConfigPage() {
  const [weights, setWeights] = useState<any>({});
  const [thresholds, setThresholds] = useState<any>({});
  const [versions, setVersions] = useState<any[]>([]);
  const [message, setMessage] = useState<string | null>(null);

  const load = async () => {
    const [config, versionList] = await Promise.all([
      apiFetch("/config/matching"),
      apiFetch("/config/matching/versions")
    ]);
    setWeights(config?.weights || {});
    setThresholds(config?.thresholds || {});
    setVersions(versionList || []);
  };

  useEffect(() => {
    load();
  }, []);

  const save = async () => {
    setMessage(null);
    try {
      await apiFetch("/config/matching", {
        method: "POST",
        body: JSON.stringify({ weights, thresholds })
      });
      setMessage("Config saved as new version");
      await load();
    } catch (err: any) {
      setMessage(err.message || "Failed to save");
    }
  };

  return (
    <div>
      <h1>Matching Config</h1>
      {message && <div className="card">{message}</div>}
      <div className="card">
        <h2>Weights</h2>
        {Object.keys(weights).map((key) => (
          <div key={key} style={{ marginBottom: 8 }}>
            <label>{key}</label>
            <input
              className="input"
              type="number"
              step="0.05"
              value={weights[key]}
              onChange={(e) => setWeights({ ...weights, [key]: Number(e.target.value) })}
            />
          </div>
        ))}
      </div>
      <div className="card">
        <h2>Thresholds</h2>
        {Object.keys(thresholds).map((key) => (
          <div key={key} style={{ marginBottom: 8 }}>
            <label>{key}</label>
            <input
              className="input"
              type="number"
              step="0.05"
              value={thresholds[key]}
              onChange={(e) => setThresholds({ ...thresholds, [key]: Number(e.target.value) })}
            />
          </div>
        ))}
      </div>
      <button className="button" onClick={save}>Save New Version</button>

      <div className="card" style={{ marginTop: 16 }}>
        <h2>Config Versions</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Version</th>
              <th>Updated</th>
            </tr>
          </thead>
          <tbody>
            {versions.map((version) => (
              <tr key={version._id}>
                <td>{version.version}</td>
                <td>{version.updated_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
