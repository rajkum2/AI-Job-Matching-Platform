"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { apiFetch } from "../../lib/api";

export default function MatchesPage() {
  const [status, setStatus] = useState<string>("all");
  const [matches, setMatches] = useState<any[]>([]);

  const load = async (value: string) => {
    const query = value === "all" ? "" : `?status=${value}`;
    const data = await apiFetch(`/matches${query}`);
    setMatches(data);
  };

  useEffect(() => {
    load(status);
  }, [status]);

  return (
    <div>
      <h1>Matches</h1>
      <div className="card">
        <label>Filter: </label>
        <select className="input" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="all">All</option>
          <option value="unreviewed">Unreviewed</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
        </select>
      </div>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Candidate</th>
              <th>Job</th>
              <th>Score</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {matches.map((match) => (
              <tr key={match._id}>
                <td>{match.candidate_id}</td>
                <td>
                  <Link href={`/matches/${match._id}`}>{match.job_id}</Link>
                </td>
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
