"use client";

import { useEffect, useState } from "react";

import { apiFetch } from "../../lib/api";

export default function AuditPage() {
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    apiFetch("/audit").then(setEvents).catch(() => setEvents([]));
  }, []);

  return (
    <div>
      <h1>Audit Log</h1>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Actor</th>
              <th>Action</th>
              <th>Entity</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event) => (
              <tr key={event._id}>
                <td>{event.created_at}</td>
                <td>{event.actor}</td>
                <td>{event.action}</td>
                <td>{event.entity_type}:{event.entity_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
