"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { apiFetch } from "../../lib/api";

export default function JobsPage() {
  const [jobs, setJobs] = useState<any[]>([]);

  useEffect(() => {
    apiFetch("/jobs").then(setJobs).catch(() => setJobs([]));
  }, []);

  return (
    <div>
      <h1>Jobs</h1>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Company</th>
              <th>Title</th>
              <th>Updated</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job) => (
              <tr key={job._id}>
                <td>{job.company}</td>
                <td>
                  <Link href={`/jobs/${job._id}`}>{job.title}</Link>
                </td>
                <td>{job.updated_at || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
