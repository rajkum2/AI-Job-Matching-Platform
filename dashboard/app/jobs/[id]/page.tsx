"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

import { apiFetch } from "../../../lib/api";

export default function JobDetailPage() {
  const params = useParams();
  const jobId = params?.id as string;
  const [job, setJob] = useState<any>(null);
  const [message, setMessage] = useState<string | null>(null);

  const load = async () => {
    const data = await apiFetch(`/jobs/${jobId}`);
    setJob(data);
  };

  useEffect(() => {
    if (jobId) {
      load();
    }
  }, [jobId]);

  const runNormalize = async () => {
    setMessage(null);
    try {
      await apiFetch("/admin/normalize/all", { method: "POST" });
      setMessage("Normalization completed");
      await load();
    } catch (err: any) {
      setMessage(err.message || "Failed to normalize");
    }
  };

  const runEmbed = async () => {
    setMessage(null);
    try {
      await apiFetch("/admin/embed/jobs", { method: "POST" });
      setMessage("Embedding completed");
      await load();
    } catch (err: any) {
      setMessage(err.message || "Failed to embed");
    }
  };

  if (!job) return <div>Loading...</div>;

  return (
    <div>
      <h1>{job.title}</h1>
      {message && <div className="card">{message}</div>}
      <div className="card">
        <h2>Raw Job Text</h2>
        <p>{job.raw_text}</p>
      </div>
      <div className="card">
        <h2>Parsed Job</h2>
        <pre>{JSON.stringify(job.parsed_job || {}, null, 2)}</pre>
      </div>
      <div className="card">
        <button className="button" onClick={runNormalize}>Re-normalize Job</button>
        <button className="button secondary" onClick={runEmbed} style={{ marginLeft: 8 }}>Re-embed Job</button>
      </div>
    </div>
  );
}
