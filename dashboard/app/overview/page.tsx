"use client";

import { useEffect, useState } from "react";

import { apiFetch } from "../../lib/api";

export default function OverviewPage() {
  const [kpis, setKpis] = useState({
    candidates: 0,
    jobs: 0,
    matches: 0,
    reviewedPct: 0,
    approvedPct: 0,
    rejected: 0
  });
  const [pipeline, setPipeline] = useState<any>({});
  const [message, setMessage] = useState<string | null>(null);

  const load = async () => {
    const [candidates, jobs, matches, audit] = await Promise.all([
      apiFetch("/candidates"),
      apiFetch("/jobs"),
      apiFetch("/matches"),
      apiFetch("/audit")
    ]);
    const reviewed = matches.filter((m: any) => m.status !== "unreviewed");
    const approved = matches.filter((m: any) => m.status === "approved");
    const rejected = matches.filter((m: any) => m.status === "rejected");

    setKpis({
      candidates: candidates.length,
      jobs: jobs.length,
      matches: matches.length,
      reviewedPct: matches.length ? Math.round((reviewed.length / matches.length) * 100) : 0,
      approvedPct: matches.length ? Math.round((approved.length / matches.length) * 100) : 0,
      rejected: rejected.length
    });

    const pipelineActions = ["seed", "normalize_all", "embed_jobs", "match_all", "match_candidate"];
    const latest: any = {};
    pipelineActions.forEach((action) => {
      const event = audit.find((e: any) => e.action === action);
      if (event) {
        latest[action] = event.created_at;
      }
    });
    setPipeline(latest);
  };

  useEffect(() => {
    load();
  }, []);

  const runAction = async (path: string) => {
    setMessage(null);
    try {
      await apiFetch(path, { method: "POST" });
      setMessage("Action completed");
      await load();
    } catch (err: any) {
      setMessage(err.message || "Action failed");
    }
  };

  return (
    <div>
      <h1>Overview</h1>
      {message && <div className="card">{message}</div>}

      <div className="grid kpi">
        <div className="card">
          <h3>Candidates</h3>
          <p>{kpis.candidates}</p>
        </div>
        <div className="card">
          <h3>Jobs</h3>
          <p>{kpis.jobs}</p>
        </div>
        <div className="card">
          <h3>Matches</h3>
          <p>{kpis.matches}</p>
        </div>
        <div className="card">
          <h3>% Reviewed</h3>
          <p>{kpis.reviewedPct}%</p>
        </div>
        <div className="card">
          <h3>% Approved</h3>
          <p>{kpis.approvedPct}%</p>
        </div>
        <div className="card">
          <h3>Rejected</h3>
          <p>{kpis.rejected}</p>
        </div>
      </div>

      <div className="card">
        <h2>Latest Pipeline Runs</h2>
        <p>Seed: {pipeline.seed || "-"}</p>
        <p>Normalize: {pipeline.normalize_all || "-"}</p>
        <p>Embed Jobs: {pipeline.embed_jobs || "-"}</p>
        <p>Match All: {pipeline.match_all || "-"}</p>
      </div>

      <div className="card">
        <h2>Quick Actions</h2>
        <div className="grid">
          <button className="button" onClick={() => runAction("/admin/seed")}>Seed Data</button>
          <button className="button secondary" onClick={() => runAction("/admin/normalize/all")}>Normalize All</button>
          <button className="button secondary" onClick={() => runAction("/admin/embed/jobs")}>Embed Jobs</button>
          <button className="button" onClick={() => runAction("/admin/match/all")}>Run Matching All</button>
        </div>
      </div>
    </div>
  );
}
