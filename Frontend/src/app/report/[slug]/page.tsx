"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { ChevronDown, Loader2 } from "lucide-react";
import { notFound } from "next/navigation";
import { ReportView } from "@/components/report/ReportView";
import { Navbar } from "@/components/layout/Navbar";
import { ReportSidebar } from "@/components/report/ReportSidebar";
import { getAuthSession, isAdmin, clearAuthSession } from "@/lib/auth";
import { FREE_SECTION_IDS } from "@/types/report";
import type { Report } from "@/types/report";

interface SiteSwitcherItem {
  report_id: string;
  site_id: string;
  site_name: string;
  site_address: string;
}

export default function ReportPage() {
  const params = useParams();
  const router = useRouter();
  const searchParams = useSearchParams();
  const slug = params.slug as string;
  const accountParam = searchParams.get("account");

  const [report, setReport]         = useState<Report | null>(null);
  const [loading, setLoading]       = useState(true);
  const [notFoundFlag, setNotFound] = useState(false);

  const [siteList, setSiteList]           = useState<SiteSwitcherItem[]>([]);
  const [switcherOpen, setSwitcherOpen]   = useState(false);
  const [adminUser, setAdminUser]         = useState(false);

  useEffect(() => { setAdminUser(isAdmin()); }, []);

  async function fetchReport() {
    setLoading(true);
    setNotFound(false);
    const session = getAuthSession();
    const headers: Record<string, string> = {};
    if (session) headers["Authorization"] = `Bearer ${session.access_token}`;

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/reports/${slug}`,
        { headers }
      );
      if (res.status === 404) { setNotFound(true); return; }
      if (!res.ok) throw new Error(`Failed to load report (${res.status})`);
      const data: Report = await res.json();

      // If we sent a token but got back locked sections, the JWT has expired.
      // Clear it immediately so the UI is honest — don't leave the user
      // appearing signed-in while actually being blocked.
      if (session) {
        const gated = data.sections.filter(
          (s) => !(FREE_SECTION_IDS as readonly string[]).includes(s.id)
        );
        const gotContent =
          gated.length === 0 || gated.some((s) => s.body.trim().length > 0);
        if (!gotContent) {
          clearAuthSession();
          window.location.reload();
          return;
        }
      }

      setReport(data);

      // Fire site list fetch in parallel immediately — don't wait for re-render
      if (data.account_id) {
        fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/reports/by-account/${data.account_id}`,
          { headers }
        )
          .then((r) => (r.ok ? r.json() : null))
          .then((list: SiteSwitcherItem[] | null) => {
            if (list) setSiteList(list);
          })
          .catch(() => {});
      }
    } catch {
      // silently fail
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchReport();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug]);

  if (notFoundFlag || !report) {
    if (!loading) notFound();
  }

  const siteSwitcher = siteList.length > 1 ? (
    <div className="relative">
      <button
        onClick={() => setSwitcherOpen((o) => !o)}
        className="flex items-center gap-1.5 text-sm text-ink-mid hover:text-ink border border-ink/10 rounded-lg px-3 py-1.5 bg-surface hover:bg-white transition-colors"
      >
        Switch site
        <ChevronDown className={`w-3.5 h-3.5 transition-transform ${switcherOpen ? "rotate-180" : ""}`} />
      </button>
      {switcherOpen && (
        <div className="absolute right-0 top-full mt-1 z-50 bg-white border border-ink/10 rounded-xl shadow-lg py-1 min-w-56 max-h-72 overflow-y-auto">
          {siteList.map((s) => (
            <button
              key={s.report_id}
              onClick={() => {
                setSwitcherOpen(false);
                const dest = accountParam
                  ? `/report/${s.report_id}?account=${accountParam}`
                  : `/report/${s.report_id}`;
                router.push(dest);
              }}
              className={`w-full text-left px-4 py-2.5 hover:bg-surface transition-colors ${
                s.report_id === slug ? "bg-orange/5 text-orange font-medium" : "text-ink"
              }`}
            >
              <p className="text-sm truncate">{s.site_name}</p>
              {s.site_address && (
                <p className="text-xs text-ink-soft truncate mt-0.5">{s.site_address}</p>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  ) : null;

  return (
    <div className="flex flex-col h-screen">
      <Navbar />
      <div className="flex flex-1 min-h-0">
        <ReportSidebar
          slug={slug}
          isAdmin={adminUser}
        />
        <main className="flex-1 overflow-y-auto relative">
          {loading ? (
            <div className="flex h-full items-center justify-center">
              <Loader2 className="w-6 h-6 text-ink-soft animate-spin" />
            </div>
          ) : (
            <ReportView
              report={report!}
              slug={slug}
              onUnlock={fetchReport}
              siteSwitcher={siteSwitcher}
            />
          )}
        </main>
      </div>
    </div>
  );
}

