import { useEffect, useState } from "react";
import { api } from "@/api/client";

interface SummaryRow {
  metric: string;
  m0: string;
  m1: string;
  m2: string;
}

const METRICS: { key: string; label: string; lowerBetter?: boolean }[] = [
  { key: "numeric_accuracy", label: "Số liệu chính xác" },
  { key: "citation_precision", label: "Trích dẫn đúng" },
  { key: "citation_recall", label: "Trích dẫn đủ" },
  { key: "unsupported_claim_rate", label: "Nhận định thiếu bằng chứng", lowerBetter: true },
  { key: "prohibited_claim_rate", label: "Nhận định cấm", lowerBetter: true },
  { key: "abstain_recall(trap)", label: "Phát hiện case bẫy" },
  { key: "coverage", label: "Phạm vi giải trình" },
  { key: "risk_on_asserted", label: "Rủi ro trên case xác nhận", lowerBetter: true },
  { key: "retrieval_P@5", label: "Truy xuất Precision@5" },
  { key: "retrieval_R@5", label: "Truy xuất Recall@5" },
];

function parseVal(s: string): { num: number | null; mean: string; sd: string } {
  if (!s || s === "n/a") return { num: null, mean: "—", sd: "" };
  const parts = s.split("±");
  return {
    num: parseFloat(parts[0]),
    mean: parts[0],
    sd: parts[1] ? "± " + parts[1] : "",
  };
}

const MODE_CARDS = [
  {
    mode: "M0",
    title: "Chỉ dùng LLM",
    bar: "bg-surface-400",
    textColor: "text-surface-500",
    findings: [
      "100% nhận định thiếu bằng chứng",
      "Không phát hiện case bẫy",
      "Không có trích dẫn nguồn",
    ],
  },
  {
    mode: "M1",
    title: "Có tài liệu, chưa kiểm chứng",
    bar: "bg-status-warning",
    textColor: "text-amber-600",
    findings: [
      "~29% nhận định thiếu bằng chứng",
      "Không phát hiện case bẫy",
      "Có trích dẫn nhưng chưa kiểm tra",
    ],
  },
  {
    mode: "M2",
    title: "Có tài liệu + kiểm chứng",
    bar: "bg-accent-500",
    textColor: "text-accent-600",
    findings: [
      "~5% nhận định thiếu bằng chứng",
      "Phát hiện 100% case bẫy",
      "0% rủi ro trên case đã xác nhận",
    ],
  },
];

export default function ResearchPage() {
  const [summary, setSummary] = useState<SummaryRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .benchmarkSummary()
      .then((data) => setSummary(data.summary as unknown as SummaryRow[]))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const rowMap = Object.fromEntries(summary.map((r) => [r.metric, r]));

  if (loading) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6 animate-fade-in">
        <div className="space-y-6">
          <div className="h-10 skeleton rounded-xl w-1/3" />
          <div className="grid grid-cols-3 gap-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-40 skeleton rounded-xl" />
            ))}
          </div>
          <div className="h-72 skeleton rounded-xl" />
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 animate-fade-in">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-ink-950">Kết quả đánh giá</h1>
        <p className="mt-2 text-sm text-ink-800">
          So sánh 3 chế độ trên 34 case, mỗi chế độ chạy 3 lần. Model: gemini-3.5-flash-lite.
        </p>
      </div>

      {/* Finding cards */}
      <div className="mb-8 grid gap-4 sm:grid-cols-3">
        {MODE_CARDS.map((card) => (
          <div key={card.mode} className="card-static overflow-hidden">
            <div className={`h-1.5 ${card.bar}`} />
            <div className="p-5">
              <div className="flex items-center gap-2 mb-4">
                <span className={`text-lg font-bold ${card.textColor}`}>{card.mode}</span>
                <span className="text-sm font-semibold text-ink-900">{card.title}</span>
              </div>
              <div className="space-y-2.5">
                {card.findings.map((f, i) => (
                  <div key={i} className="flex items-start gap-2 text-sm">
                    <span className={`mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full ${card.bar}`} />
                    <span className="text-ink-800">{f}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Table */}
      <div className="card-static overflow-hidden mb-6">
        <table className="w-full border-collapse">
          <colgroup>
            <col className="w-[34%]" />
            <col className="w-[22%]" />
            <col className="w-[22%]" />
            <col className="w-[22%]" />
          </colgroup>
          <thead>
            <tr className="bg-ink-950">
              <th className="px-5 py-3 text-left text-[13px] font-bold text-white/70">
                Chỉ số
              </th>
              <th className="px-5 py-3 text-center text-[13px] font-bold text-white/50">
                M0
              </th>
              <th className="px-5 py-3 text-center text-[13px] font-bold text-status-warning-ring">
                M1
              </th>
              <th className="px-5 py-3 text-center text-[13px] font-bold text-accent-200">
                M2
              </th>
            </tr>
          </thead>
          <tbody>
            {METRICS.map((def, idx) => {
              const row = rowMap[def.key];
              if (!row) return null;

              const v0 = parseVal(row.m0);
              const v1 = parseVal(row.m1);
              const v2 = parseVal(row.m2);
              const nums = [v0.num, v1.num, v2.num].filter(
                (v): v is number => v != null,
              );
              const best =
                nums.length > 0
                  ? def.lowerBetter
                    ? Math.min(...nums)
                    : Math.max(...nums)
                  : null;

              const cells = [v0, v1, v2];

              return (
                <tr
                  key={def.key}
                  className={`border-t border-surface-100 ${
                    idx % 2 === 0 ? "bg-white" : "bg-surface-50/50"
                  }`}
                >
                  <td className="px-5 py-3 text-sm font-medium text-ink-900">
                    {def.label}
                    {def.lowerBetter && (
                      <span className="ml-1 text-xs text-surface-500">thấp = tốt</span>
                    )}
                  </td>
                  {cells.map((c, i) => (
                    <td key={i} className="px-5 py-3 text-center">
                      {c.num == null ? (
                        <span className="text-sm text-surface-400">—</span>
                      ) : (
                        <div>
                          <div
                            className={`font-mono text-sm ${
                              c.num === best
                                ? "font-bold text-accent-600"
                                : "text-ink-900"
                            }`}
                          >
                            {c.mean}
                          </div>
                          {c.sd && (
                            <div className="font-mono text-xs text-surface-500">
                              {c.sd}
                            </div>
                          )}
                        </div>
                      )}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Methodology strip */}
      <div className="mb-6 grid gap-3 sm:grid-cols-4">
        {[
          { label: "Case trọng yếu", value: "34" },
          { label: "Tài liệu chứng từ", value: "170" },
          { label: "Lần chạy / chế độ", value: "3" },
          { label: "Tổng bản ghi", value: "306" },
        ].map((item) => (
          <div
            key={item.label}
            className="flex items-center gap-3 rounded-xl bg-surface-50 px-4 py-3 ring-1 ring-surface-200"
          >
            <span className="text-xl font-bold text-ink-950 font-mono">{item.value}</span>
            <span className="text-xs text-surface-500">{item.label}</span>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="flex items-start gap-3 rounded-xl bg-surface-50 p-4 ring-1 ring-surface-200">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="mt-0.5 shrink-0 text-surface-500">
          <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.2" />
          <path d="M8 5.5V8.5M8 10.5V11" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
        </svg>
        <p className="text-xs text-surface-500">
          <strong className="text-ink-900">Dữ liệu mô phỏng · Không dùng cho báo cáo thực tế.</strong>{" "}
          Hiệu suất trên dữ liệu thực tế có thể khác biệt.
        </p>
      </div>
    </div>
  );
}
