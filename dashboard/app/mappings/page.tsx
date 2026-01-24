"use client";

import { useEffect, useState } from "react";

import { apiFetch } from "../../lib/api";

export default function MappingsPage() {
  const [skillAliases, setSkillAliases] = useState<any[]>([]);
  const [titleAliases, setTitleAliases] = useState<any[]>([]);
  const [skillForm, setSkillForm] = useState({ alias: "", canonical: "" });
  const [titleForm, setTitleForm] = useState({ alias: "", canonical: "", seniority_band: "" });

  const load = async () => {
    const [skills, titles] = await Promise.all([apiFetch("/mappings/skills"), apiFetch("/mappings/titles")]);
    setSkillAliases(skills);
    setTitleAliases(titles);
  };

  useEffect(() => {
    load();
  }, []);

  const addSkill = async () => {
    await apiFetch("/mappings/skills", {
      method: "POST",
      body: JSON.stringify(skillForm)
    });
    setSkillForm({ alias: "", canonical: "" });
    await load();
  };

  const addTitle = async () => {
    await apiFetch("/mappings/titles", {
      method: "POST",
      body: JSON.stringify(titleForm)
    });
    setTitleForm({ alias: "", canonical: "", seniority_band: "" });
    await load();
  };

  const deleteSkill = async (id: string) => {
    await apiFetch(`/mappings/skills/${id}`, { method: "DELETE" });
    await load();
  };

  const deleteTitle = async (id: string) => {
    await apiFetch(`/mappings/titles/${id}`, { method: "DELETE" });
    await load();
  };

  return (
    <div>
      <h1>Mappings</h1>

      <div className="card">
        <h2>Skill Aliases</h2>
        <div className="grid" style={{ gridTemplateColumns: "1fr 1fr auto" }}>
          <input
            className="input"
            placeholder="Alias"
            value={skillForm.alias}
            onChange={(e) => setSkillForm({ ...skillForm, alias: e.target.value })}
          />
          <input
            className="input"
            placeholder="Canonical"
            value={skillForm.canonical}
            onChange={(e) => setSkillForm({ ...skillForm, canonical: e.target.value })}
          />
          <button className="button" onClick={addSkill}>Add</button>
        </div>
        <table className="table" style={{ marginTop: 12 }}>
          <thead>
            <tr>
              <th>Alias</th>
              <th>Canonical</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {skillAliases.map((item) => (
              <tr key={item._id}>
                <td>{item.alias}</td>
                <td>{item.canonical}</td>
                <td>
                  <button className="button secondary" onClick={() => deleteSkill(item._id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h2>Title Aliases</h2>
        <div className="grid" style={{ gridTemplateColumns: "1fr 1fr 1fr auto" }}>
          <input
            className="input"
            placeholder="Alias"
            value={titleForm.alias}
            onChange={(e) => setTitleForm({ ...titleForm, alias: e.target.value })}
          />
          <input
            className="input"
            placeholder="Canonical"
            value={titleForm.canonical}
            onChange={(e) => setTitleForm({ ...titleForm, canonical: e.target.value })}
          />
          <input
            className="input"
            placeholder="Seniority band"
            value={titleForm.seniority_band}
            onChange={(e) => setTitleForm({ ...titleForm, seniority_band: e.target.value })}
          />
          <button className="button" onClick={addTitle}>Add</button>
        </div>
        <table className="table" style={{ marginTop: 12 }}>
          <thead>
            <tr>
              <th>Alias</th>
              <th>Canonical</th>
              <th>Seniority</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {titleAliases.map((item) => (
              <tr key={item._id}>
                <td>{item.alias}</td>
                <td>{item.canonical}</td>
                <td>{item.seniority_band || "-"}</td>
                <td>
                  <button className="button secondary" onClick={() => deleteTitle(item._id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
