import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "@/api/client";
import type { VarianceCase, MetaInfo } from "@/types";

function fmt(n: number) {
  return n.toLocaleString("en-US", { maximumFractionDigits: 0 });
}

function pct(n: number | null) {
  if (n == null) return "—";
  return (n * 100).toFixed(1) + "%";
}

function VarianceBar({ value, max }: { value: number; max: number }) {
  const w = Math.min(Math.abs(value) / max * 100, 100);
  const neg = value < 0;
  return (
    <div className="flex items-center gap-2">
      <div className="h-1.5 w-16 rounded-full bg-surface-100 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${
            neg ? "bg-status-flagged/60" : "bg-status-verified/60"
          }`}
          style={{ width: `${w}%` }}
        />
      </div>
    </div>
  );
}

export default function CaseListPage() {
  const navigate = useNavigate();
  const [meta, setMeta] = useState<MetaInfo | null>(null);
  const [cases, setCases] = useState<VarianceCase[]>([]);
  const [month, setMonth] = useState("");
  const [property, setProperty] = useState("");
  const [loading, setLoading] = useState(false);
  const [scanned, setScanned] = useState(false);

  useEffect(() => {
    api.meta().then(setMeta).catch(console.error);
    // Quét sẵn toàn bộ kỳ khi mở trang — màn hình đầu tiên có dữ liệu để đọc
    // thay vì một khung trống chờ người dùng bấm nút.
    scan();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const availableMonths = meta?.months.filter((m) => m >= "2026-05") ?? [];
  const properties = meta?.properties ?? [];

  async function scan() {
    setLoading(true);
    try {
      const data = await api.cases(month || undefined, property || undefined);
      setCases(data.cases);
      setScanned(true);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  const favorable = cases.filter((c) => c.direction === "favorable").length;
  const unfavorable = cases.filter((c) => c.direction === "unfavorable").length;
  const maxVar = cases.length > 0 ? Math.max(...cases.map((c) => Math.abs(c.variance))) : 1;
  const totalVar = cases.reduce((s, c) => s + c.variance, 0);

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 animate-fade-in">
      {/* Page header */}
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-ink-950">
          Quét chênh lệch P&L
        </h1>
        <p className="mt-2 text-sm text-ink-800 max-w-xl">
          Chọn kỳ báo cáo và khu vực để quét. Hệ thống sẽ tìm các chênh lệch
          vượt ngưỡng trọng yếu và sắp xếp theo mức độ.
        </p>
      </div>

      {/* Filters card */}
      <div className="card-static mb-6 p-5">
        <div className="flex flex-wrap items-end gap-5">
          <div className="min-w-[180px]">
            <label className="section-title mb-2 block">
              Kỳ báo cáo
            </label>
            <select
              value={month}
              onChange={(e) => setMonth(e.target.value)}
              className="h-11 w-full rounded-lg border border-surface-200 bg-white px-3.5 text-sm font-medium shadow-sm transition-all focus:border-accent-400 focus:ring-2 focus:ring-accent-100 focus:outline-none"
            >
              <option value="">Tất cả kỳ</option>
              {availableMonths.map((m) => (
                <option key={m} value={m}>{m}</option>
              ))}
            </select>
          </div>

          <div className="min-w-[180px]">
            <label className="section-title mb-2 block">
              Khu vực
            </label>
            <select
              value={property}
              onChange={(e) => setProperty(e.target.value)}
              className="h-11 w-full rounded-lg border border-surface-200 bg-white px-3.5 text-sm font-medium shadow-sm transition-all focus:border-accent-400 focus:ring-2 focus:ring-accent-100 focus:outline-none"
            >
              <option value="">Tất cả khu</option>
              {properties.map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>

          <button onClick={scan} disabled={loading} className="btn-primary h-11">
            {loading ? (
              <>
                <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                Đang quét…
              </>
            ) : (
              <>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M7 12A5 5 0 107 2a5 5 0 000 10zM14 14l-3-3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
                Quét P&L
              </>
            )}
          </button>

          {/* Materiality info */}
          {meta && (
            <div className="ml-auto hidden lg:flex items-center gap-3 text-xs text-surface-500">
              {Object.entries(meta.materiality).map(([side, { abs: a, pct: p }]) => (
                <span key={side} className="rounded-md bg-surface-50 px-2.5 py-1.5 ring-1 ring-surface-200">
                  {side}: ≥${fmt(a)} | ≥{(p * 100).toFixed(0)}%
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Summary KPIs — shown after scan */}
      {scanned && cases.length > 0 && (
        <div className="mb-6 grid gap-4 sm:grid-cols-4 animate-slide-up">
          <div className="card-static p-4">
            <div className="section-title">Tổng case</div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-3xl font-bold text-ink-950">{cases.length}</span>
              <span className="text-sm text-surface-500">trọng yếu</span>
            </div>
          </div>
          <div className="card-static p-4">
            <div className="section-title">Bất lợi</div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-3xl font-bold text-status-flagged">{unfavorable}</span>
              <span className="text-sm text-surface-500">case</span>
            </div>
            <div className="mt-2 h-1 rounded-full bg-surface-100 overflow-hidden">
              <div className="h-full rounded-full bg-status-flagged/50" style={{ width: `${(unfavorable / cases.length) * 100}%` }} />
            </div>
          </div>
          <div className="card-static p-4">
            <div className="section-title">Thuận lợi</div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-3xl font-bold text-status-verified">{favorable}</span>
              <span className="text-sm text-surface-500">case</span>
            </div>
            <div className="mt-2 h-1 rounded-full bg-surface-100 overflow-hidden">
              <div className="h-full rounded-full bg-status-verified/50" style={{ width: `${(favorable / cases.length) * 100}%` }} />
            </div>
          </div>
          <div className="card-static p-4">
            <div className="section-title">Tổng chênh lệch</div>
            <div className="mt-2">
              <span className={`text-2xl font-bold font-mono ${totalVar < 0 ? "text-status-flagged" : "text-status-verified"}`}>
                ${fmt(totalVar)}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Empty state */}
      {scanned && cases.length === 0 && (
        <div className="card-static p-16 text-center animate-fade-in">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-surface-100">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <path d="M16 6L22 14H10L16 6Z" stroke="#94A3B8" strokeWidth="1.5" strokeLinejoin="round"/>
              <path d="M8 18H24V26H8V18Z" stroke="#94A3B8" strokeWidth="1.5" strokeLinejoin="round"/>
            </svg>
          </div>
          <p className="text-surface-500 font-medium">
            Không có chênh lệch trọng yếu nào với bộ lọc hiện tại.
          </p>
        </div>
      )}

      {/* Cases table */}
      {cases.length > 0 && (
        <div className="card-static overflow-hidden animate-slide-up">
          <div className="overflow-x-auto custom-scroll">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-ink-950 text-left text-[13px] font-semibold">
                  <th className="px-5 py-3.5 text-surface-300">Kỳ</th>
                  <th className="px-5 py-3.5 text-surface-300">Khu vực</th>
                  <th className="px-5 py-3.5 text-surface-300">Dòng P&L</th>
                  <th className="px-5 py-3.5 text-right text-surface-300">Ngân sách</th>
                  <th className="px-5 py-3.5 text-right text-surface-300">Thực tế</th>
                  <th className="px-5 py-3.5 text-right text-surface-300">Chênh lệch</th>
                  <th className="px-5 py-3.5 text-right text-surface-300">%</th>
                  <th className="px-5 py-3.5 text-surface-300"></th>
                  <th className="px-5 py-3.5 text-center text-surface-300">Chiều</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-surface-100">
                {cases.map((c, idx) => (
                  <tr
                    key={c.case_id}
                    onClick={() => navigate(`/case/${encodeURIComponent(c.case_id)}`)}
                    className={`cursor-pointer transition-all duration-150 hover:bg-accent-50/50 ${
                      idx % 2 === 0 ? "bg-white" : "bg-surface-50/50"
                    }`}
                  >
                    <td className="px-5 py-3.5 font-mono text-xs text-surface-500">{c.month}</td>
                    <td className="px-5 py-3.5">
                      <span className="inline-flex items-center gap-1.5 font-semibold">
                        <span className="h-2 w-2 rounded-full bg-accent-400" />
                        {c.property}
                      </span>
                    </td>
                    <td className="px-5 py-3.5 font-medium">{c.pl_line}</td>
                    <td className="number px-5 py-3.5 text-surface-500">${fmt(c.budget)}</td>
                    <td className="number px-5 py-3.5 text-surface-500">${fmt(c.actual)}</td>
                    <td className={`number px-5 py-3.5 font-bold ${
                      c.direction === "unfavorable" ? "text-status-flagged" : "text-status-verified"
                    }`}>
                      ${fmt(c.variance)}
                    </td>
                    <td className="number px-5 py-3.5 text-xs text-surface-500">{pct(c.variance_pct)}</td>
                    <td className="px-5 py-3.5">
                      <VarianceBar value={c.variance} max={maxVar} />
                    </td>
                    <td className="px-5 py-3.5 text-center">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-1 text-xs font-semibold ring-1 ${
                        c.direction === "unfavorable"
                          ? "bg-status-flagged-bg text-status-flagged ring-status-flagged-ring"
                          : "bg-status-verified-bg text-status-verified ring-status-verified-ring"
                      }`}>
                        {c.direction === "unfavorable" ? "↓ Bất lợi" : "↑ Thuận lợi"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
