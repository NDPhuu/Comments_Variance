import type { VarianceCase } from "@/types";

function fmt(n: number) {
  return n.toLocaleString("en-US", { maximumFractionDigits: 0 });
}

function pct(n: number | null) {
  if (n == null) return "—";
  return (n * 100).toFixed(1) + "%";
}

interface Props {
  caseData: VarianceCase;
  onNext: () => void;
}

export default function StepOverview({ caseData: c, onNext }: Props) {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* KPI strip */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {[
          { label: "Ngân sách", value: `$${fmt(c.budget)}`, sub: c.pl_line },
          { label: "Thực tế", value: `$${fmt(c.actual)}`, sub: c.month },
          {
            label: "Chênh lệch",
            value: `$${fmt(c.variance)}`,
            color:
              c.direction === "unfavorable"
                ? "text-status-flagged"
                : "text-status-verified",
            accent:
              c.direction === "unfavorable"
                ? "bg-status-flagged"
                : "bg-status-verified",
          },
          { label: "Tỷ lệ chênh lệch", value: pct(c.variance_pct), sub: c.materiality_rule },
        ].map((kpi) => (
          <div key={kpi.label} className="card-static relative overflow-hidden p-5">
            <div className={`absolute top-0 left-0 right-0 h-1 ${kpi.accent ?? "bg-accent-500"}`} />
            <div className="section-title">{kpi.label}</div>
            <div className={`mt-2 font-mono text-2xl font-bold ${kpi.color ?? "text-ink-950"}`}>
              {kpi.value}
            </div>
            {kpi.sub && (
              <div className="mt-1 text-xs text-surface-500">{kpi.sub}</div>
            )}
          </div>
        ))}
      </div>

      {/* Case metadata */}
      <div className="card-static p-5">
        <div className="flex flex-wrap items-center gap-x-8 gap-y-3">
          {[
            { label: "Dòng P&L", value: c.pl_line, bold: true },
            { label: "Khu vực", value: c.property, bold: true },
            { label: "Kỳ", value: c.month, mono: true },
            {
              label: "Chiều",
              value: c.direction === "unfavorable" ? "Bất lợi" : "Thuận lợi",
              color: c.direction === "unfavorable" ? "text-status-flagged" : "text-status-verified",
            },
            { label: "Ngưỡng trọng yếu", value: c.materiality_rule },
          ].map((item) => (
            <div key={item.label} className="text-sm">
              <span className="text-surface-500">{item.label}: </span>
              <span
                className={`${item.bold ? "font-semibold" : ""} ${item.mono ? "font-mono" : ""} ${item.color ?? "text-ink-900"}`}
              >
                {item.value}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Contributors table */}
      <div className="card-static overflow-hidden">
        <div className="flex items-center justify-between border-b border-surface-200 px-5 py-4">
          <h3 className="text-sm font-bold text-ink-900">
            Thành phần chênh lệch
          </h3>
          <span className="bg-accent-50 px-2.5 py-0.5 text-xs font-bold text-accent-600 ring-1 ring-accent-200">
            {c.contributors.length}
          </span>
        </div>
        <div className="overflow-x-auto custom-scroll">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-surface-200 bg-surface-50 text-left">
                <th className="px-5 py-3 section-title">Mã</th>
                <th className="px-5 py-3 section-title">Loại</th>
                <th className="px-5 py-3 section-title">Bên liên quan</th>
                <th className="px-5 py-3 section-title">Ghi chú</th>
                <th className="px-5 py-3 section-title text-right">Giá trị</th>
                <th className="px-5 py-3 section-title text-right">Tỷ trọng</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-100">
              {c.contributors.map((ct) => (
                <tr key={ct.key} className="transition-colors hover:bg-accent-50/30">
                  <td className="px-5 py-3 font-mono text-xs text-accent-600 font-medium">
                    {ct.key}
                  </td>
                  <td className="px-5 py-3">
                    <span className={`inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium ring-1 ${
                      ct.kind === "tenant"
                        ? "bg-accent-50 text-accent-600 ring-accent-200"
                        : "bg-amber-50 text-amber-700 ring-amber-200"
                    }`}>
                      {ct.kind === "tenant" ? "Khách thuê" : "Giao dịch"}
                    </span>
                  </td>
                  <td className="px-5 py-3 font-semibold text-ink-900">{ct.party}</td>
                  <td className="max-w-xs truncate px-5 py-3 text-surface-500">
                    {ct.memo}
                  </td>
                  <td className={`number px-5 py-3 font-bold ${
                    ct.delta < 0 ? "text-status-flagged" : "text-status-verified"
                  }`}>
                    ${fmt(ct.delta)}
                  </td>
                  <td className="number px-5 py-3">
                    <div className="flex items-center justify-end gap-2">
                      <span className="text-xs text-ink-800">
                        {ct.share_of_variance != null
                          ? (ct.share_of_variance * 100).toFixed(1) + "%"
                          : ct.share_of_actual != null
                            ? (ct.share_of_actual * 100).toFixed(1) + "%"
                            : "—"}
                      </span>
                      {ct.share_of_variance != null && (
                        <div className="h-1.5 w-12 rounded-full bg-surface-100 overflow-hidden">
                          <div
                            className="h-full rounded-full bg-accent-400"
                            style={{ width: `${Math.min(Math.abs(ct.share_of_variance) * 100, 100)}%` }}
                          />
                        </div>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="flex justify-end pt-2">
        <button onClick={onNext} className="btn-primary">
          Tiếp theo
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M6 4L10 8L6 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
}
