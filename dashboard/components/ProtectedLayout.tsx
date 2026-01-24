"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";

import Sidebar from "./Sidebar";
import { getToken } from "../lib/api";

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    if (pathname === "/login") return;
    const token = getToken();
    if (!token) {
      router.push("/login");
    }
  }, [pathname, router]);

  if (pathname === "/login") {
    return <>{children}</>;
  }

  return (
    <div className="layout">
      <Sidebar />
      <main className="content">{children}</main>
    </div>
  );
}
