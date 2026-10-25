const BASE =
  import.meta.env.VITE_API_URL ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`API ${res.status}: ${body}`);
  }
  return res.json();
}

export const api = {
  meta: () => request<import("@/types").MetaInfo>("/api/meta"),

  cases: (month?: string, property?: string) => {
    const params = new URLSearchParams();
    if (month) params.set("month", month);
    if (property) params.set("property", property);
    const qs = params.toString();
    return request<{ cases: import("@/types").VarianceCase[]; total: number }>(
      `/api/cases${qs ? `?${qs}` : ""}`,
    );
  },

  caseDetail: (id: string) =>
    request<import("@/types").VarianceCase>(`/api/cases/${encodeURIComponent(id)}`),

  evidence: (id: string) =>
    request<import("@/types").EvidencePack>(
      `/api/cases/${encodeURIComponent(id)}/evidence`,
    ),

  records: (id: string) =>
    request<import("@/types").CaseRecords>(
      `/api/cases/${encodeURIComponent(id)}/records`,
    ),

  generate: (id: string, mode: string) =>
    request<import("@/types").GenerationOutput>(
      `/api/cases/${encodeURIComponent(id)}/generate`,
      { method: "POST", body: JSON.stringify({ mode }) },
    ),

  verify: (id: string, output: Record<string, unknown>) =>
    request<import("@/types").Verdict>(
      `/api/cases/${encodeURIComponent(id)}/verify`,
      { method: "POST", body: JSON.stringify({ output }) },
    ),

  benchmarkSummary: () =>
    request<{ summary: Record<string, string>[]; byRep: Record<string, string>[] }>(
      "/api/benchmark/summary",
    ),

  benchmarkByScenario: () =>
    request<{ byScenario: Record<string, string>[] }>(
      "/api/benchmark/by-scenario",
    ),

  evidenceDoc: (docId: string) =>
    request<import("@/types").EvidenceDoc>(
      `/api/evidence/${encodeURIComponent(docId)}`,
    ),
};
