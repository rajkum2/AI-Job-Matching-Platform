"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { apiFetch } from "../../lib/api";

export default function CandidatesPage() {
  const [candidates, setCandidates] = useState<any[]>([]);

  useEffect(() => {
    apiFetch("/candidates").then(setCandidates).catch(() => setCandidates([]));
  }, []);

  return (
    <div>
      <h1>Candidates</h1>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {candidates.map((candidate) => (
              <tr key={candidate._id}>
                <td>
                  <Link href={`/candidates/${candidate._id}`}>{candidate.name}</Link>
                </td>
                <td>{candidate.email || "-"}</td>
                <td>{candidate.created_at || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
