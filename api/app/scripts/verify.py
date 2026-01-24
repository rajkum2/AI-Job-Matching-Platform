import json
import os
import sys
from urllib import request

API_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


def call(path: str, method: str = "GET", payload: dict | None = None, token: str | None = None):
    url = f"{API_URL}{path}"
    data = None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers=headers, method=method)
    with request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body) if body else {}


def main() -> int:
    try:
        login = call("/auth/login", method="POST", payload={"password": ADMIN_PASSWORD})
        token = login["token"]

        call("/admin/seed", method="POST", token=token)
        call("/admin/normalize/all", method="POST", token=token)
        call("/admin/embed/jobs", method="POST", token=token)
        call("/admin/match/all", method="POST", token=token)

        candidates = call("/candidates", token=token)
        candidate_id = candidates[0]["_id"]

        matches = call("/matches", token=token)
        match_id = matches[0]["_id"]

        call(f"/matches/{match_id}/approve", method="POST", payload={"reviewer_notes": "Approved in verification"}, token=token)
        call("/mappings/skills", method="POST", payload={"alias": "k8s", "canonical": "kubernetes"}, token=token)

        compare = call(f"/admin/match/candidate/{candidate_id}", method="POST", token=token)
        if "comparison" not in compare:
            raise RuntimeError("Comparison missing")

        print("Verification completed successfully")
        return 0
    except Exception as exc:
        print(f"Verification failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
