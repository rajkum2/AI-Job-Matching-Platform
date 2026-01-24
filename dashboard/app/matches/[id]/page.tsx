"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

import { apiFetch } from "../../../lib/api";

export default function MatchDetailPage() {
  const params = useParams();
  const matchId = params?.id as string;
  const [match, setMatch] = useState<any>(null);
  const [candidate, setCandidate] = useState<any>(null);
  const [resume, setResume] = useState<any>(null);
  const [job, setJob] = useState<any>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [comparison, setComparison] = useState<any[]>([]);
  const [rejectCodes, setRejectCodes] = useState<string>("");
  const [rejectNotes, setRejectNotes] = useState<string>("");

  const load = async () => {
    const matchData = await apiFetch(`/matches/${matchId}`);
    const candidateData = await apiFetch(`/candidates/${matchData.candidate_id}`);
    const jobData = await apiFetch(`/jobs/${matchData.job_id}`);
    setMatch(matchData);
    setCandidate(candidateData.candidate);
    setResume(candidateData.resume);
    setJob(jobData);
  };

  useEffect(() => {
    if (matchId) {
      load();
    }
  }, [matchId]);

  const approve = async () => {
    setMessage(null);
    try {
      await apiFetch(`/matches/${matchId}/approve`, {
        method: "POST",
        body: JSON.stringify({ reviewer_notes: "Approved" })
      });
      setMessage("Match approved");
      await load();
    } catch (err: any) {
      setMessage(err.message || "Failed to approve");
    }
  };

  const reject = async () => {
    setMessage(null);
    try {
      await apiFetch(`/matches/${matchId}/reject`, {
        method: "POST",
        body: JSON.stringify({
          reject_reason_codes: rejectCodes.split(",").map((code) => code.trim()).filter(Boolean),
          reviewer_notes: rejectNotes
        })
      });
      setMessage("Match rejected");
      await load();
    } catch (err: any) {
      setMessage(err.message || "Failed to reject");
    }
  };

  const addSkillAlias = async (alias: string, canonical: string) => {
    await apiFetch("/mappings/skills", {
      method: "POST",
      body: JSON.stringify({ alias, canonical })
    });
    setMessage(`Added skill alias ${alias} → ${canonical}`);
  };

  const addTitleAlias = async (alias: string, canonical: string, seniority_band?: string) => {
    await apiFetch("/mappings/titles", {
      method: "POST",
      body: JSON.stringify({ alias, canonical, seniority_band })
    });
    setMessage(`Added title alias ${alias} → ${canonical}`);
  };

  const suggestFixes = () => {
    const suggestions = [] as any[];
    const resumeText = resume?.raw_text?.toLowerCase() || "";
    if (resumeText.includes("k8s")) {
      suggestions.push({ type: "skill", alias: "k8s", canonical: "kubernetes" });
    }
    if (resumeText.includes("sde ii") || resumeText.includes("sde2")) {
      suggestions.push({ type: "title", alias: "sde ii", canonical: "software engineer (mid)", seniority: "mid" });
    }
    return suggestions;
  };

  const runCompare = async () => {
    setMessage(null);
    try {
      const data = await apiFetch(`/admin/match/candidate/${match.candidate_id}`, { method: "POST" });
      setComparison(data.comparison || []);
      setMessage("Matching rerun completed with comparison");
    } catch (err: any) {
      setMessage(err.message || "Failed to rerun matching");
    }
  };

  if (!match) return <div>Loading...</div>;

  const fixes = suggestFixes();

  return (
    <div>
      <h1>Match Workbench</h1>
      {message && <div className="card">{message}</div>}

      <div className="card">
        <p><strong>Candidate:</strong> {candidate?.name}</p>
        <p><strong>Job:</strong> {job?.title}</p>
        <p><strong>Final Score:</strong> {match.final_score.toFixed(2)}</p>
        <p><strong>Retrieval Rank:</strong> {match.retrieval_rank || "-"}</p>
      </div>

      <div className="grid" style={{ gridTemplateColumns: "1fr 1fr" }}>
        <div className="card">
          <h3>Candidate Parsed Profile</h3>
          <pre>{JSON.stringify(resume?.parsed_profile || {}, null, 2)}</pre>
        </div>
        <div className="card">
          <h3>Job Parsed Profile</h3>
          <pre>{JSON.stringify(job?.parsed_job || {}, null, 2)}</pre>
        </div>
      </div>

      <div className="card">
        <h3>Score Breakdown</h3>
        <pre>{JSON.stringify(match.score_breakdown || {}, null, 2)}</pre>
        <h3>Reasons</h3>
        <ul>
          {(match.reasons || []).map((reason: string) => (
            <li key={reason}>{reason}</li>
          ))}
        </ul>
      </div>

      <div className="card">
        <h3>Review Actions</h3>
        <button className="button" onClick={approve}>Approve</button>
        <div style={{ marginTop: 12 }}>
          <input
            className="input"
            placeholder="Reject reason codes (comma-separated)"
            value={rejectCodes}
            onChange={(e) => setRejectCodes(e.target.value)}
          />
          <textarea
            className="input"
            placeholder="Reviewer notes"
            value={rejectNotes}
            onChange={(e) => setRejectNotes(e.target.value)}
            style={{ marginTop: 8, minHeight: 80 }}
          />
          <button className="button secondary" onClick={reject} style={{ marginTop: 8 }}>
            Reject
          </button>
        </div>
      </div>

      <div className="card">
        <h3>Suggest Fixes</h3>
        {fixes.length === 0 && <p>No suggestions detected.</p>}
        {fixes.map((fix) => (
          <div key={`${fix.type}-${fix.alias}`} style={{ marginBottom: 8 }}>
            <span>{fix.type} alias: {fix.alias} → {fix.canonical}</span>
            {fix.type === "skill" ? (
              <button className="button secondary" style={{ marginLeft: 8 }} onClick={() => addSkillAlias(fix.alias, fix.canonical)}>
                Add Skill Alias
              </button>
            ) : (
              <button className="button secondary" style={{ marginLeft: 8 }} onClick={() => addTitleAlias(fix.alias, fix.canonical, fix.seniority)}>
                Add Title Alias
              </button>
            )}
          </div>
        ))}
      </div>

      <div className="card">
        <h3>Rerun Matching & Compare</h3>
        <button className="button" onClick={runCompare}>Rerun Matching for Candidate</button>
        {comparison.length > 0 && (
          <table className="table" style={{ marginTop: 12 }}>
            <thead>
              <tr>
                <th>Job</th>
                <th>Before Rank</th>
                <th>After Rank</th>
                <th>Before Score</th>
                <th>After Score</th>
              </tr>
            </thead>
            <tbody>
              {comparison.map((row) => (
                <tr key={row.job_id}>
                  <td>{row.job_id}</td>
                  <td>{row.before_rank ?? "-"}</td>
                  <td>{row.after_rank ?? "-"}</td>
                  <td>{row.before_score ?? "-"}</td>
                  <td>{row.after_score ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
