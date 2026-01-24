"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { apiFetch, setToken } from "../../lib/api";

export default function LoginPage() {
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const onSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    try {
      const data = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ password })
      });
      setToken(data.token);
      router.push("/overview");
    } catch (err: any) {
      setError(err.message || "Login failed");
    }
  };

  return (
    <div className="content">
      <div className="card" style={{ maxWidth: 400, margin: "120px auto" }}>
        <h2>Admin Login</h2>
        <form onSubmit={onSubmit}>
          <label>Password</label>
          <input
            className="input"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter admin password"
          />
          {error && <p style={{ color: "#b91c1c" }}>{error}</p>}
          <button className="button" type="submit" style={{ marginTop: 12 }}>
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
}
