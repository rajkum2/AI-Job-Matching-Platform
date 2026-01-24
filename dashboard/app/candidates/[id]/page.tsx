"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

import { apiFetch } from "../../../lib/api";

export default function CandidateDetailPage() {
  const params = useParams();
  const candidateId = params?.id as string;
  const [candidate, setCandidate] = useState<any>(null);
  const [resume, setResume] = useState<any>(null);
  const [matches, setMatches] = useState<any[]>([]);
  const [message, setMessage] = useState<string | null>(null);

  const load = async () => {
    const data = await apiFetch(`/candidates/${candidateId}`);
    const allMatches = await apiFetch("/matches");
    setCandidate(data.candidate);
    setResume(data.resume);
    setMatches(allMatches.filter((m: any) => m.candidate_id === candidateId));
  };

  useEffect(() => {
    if (candidateId) {
      load();
    }
  }, [candidateId]);

  const runMatching = async () => {
    setMessage(null);
    try {
      await apiFetch(`/admin/match/candidate/${candidateId}`, { method: "POST" });
      setMessage("Matching completed");
      await load();
    } catch (err: any) {
      setMessage(err.message || "Failed to match candidate");
    }
  };

  if (!candidate) return <div>Loading...</div>;

  return (
    <div>
      <h1>{candidate.name}</h1>
      {message && <div className="card">{message}</div>}
      <div className="card">
        <h2>Raw Resume</h2>
        <p>{resume?.raw_text || "-"}</p>
      </div>
      <div className="card">
        <h2>Parsed Profile</h2>
        <pre>{JSON.stringify(resume?.parsed_profile || {}, null, 2)}</pre>
      </div>
      <div className="card">
        <button className="button" onClick={runMatching}>Run Matching for Candidate</button>
      </div>
      <div className="card">
        <h2>Top Matches</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Job</th>
              <th>Score</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {matches.map((match) => (
              <tr key={match._id}>
                <td>{match.job_id}</td>
                <td>{match.final_score.toFixed(2)}</td>
                <td>{match.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
