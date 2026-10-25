import { useState } from "react";
import type { GenerationOutput, Verdict } from "@/types";
import StatusBadge from "./StatusBadge";

interface Props {
  output: GenerationOutput;
  verdict: Verdict;
}

type Decision = "approve" | "flag" | "return" | null;

const DECISIONS = {
  approve: {
    label: "Phê duyệt",
    desc: "Giải trình đạt kiểm chứng, sẵn sàng đưa vào báo cáo",
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M4 10L8 14L16 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    ),
    active: "bg-status-verified text-white ring-2 ring-status-verified ring-offset-2 shadow-lg",
    inactive: "bg-white text-status-verified ring-1 ring-status-verified-ring hover:bg-status-verified-bg",
  },
  flag: {
    label: "Cần xem lại",
    desc: "Giải trình cần kiểm tra thêm trước khi sử dụng",
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M10 4V11M10 14V15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
      </svg>
    ),
    active: "bg-status-warning text-white ring-2 ring-status-warning ring-offset-2 shadow-lg",
    inactive: "bg-white text-status-warning ring-1 ring-status-warning-ring hover:bg-status-warning-bg",
  },
  return: {
    label: "Trả lại",
    desc: "Giải trình không đạt yêu cầu, cần sinh lại",
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M6 6L14 14M14 6L6 14" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
      </svg>
    ),
    active: "bg-status-flagged text-white ring-2 ring-status-flagged ring-offset-2 shadow-lg",
    inactive: "bg-white text-status-flagged ring-1 ring-status-flagged-ring hover:bg-status-flagged-bg",
  },
};

function GateSummaryRing({ pass, total, label }: { pass: number; total: number; label: string }) {
  const pct = total === 0 ? 100 : (pass / total) * 100;
  const r = 18;
  const circ = 2 * Math.PI * r;
  const offset = circ - (pct / 100) * circ;
  const ok = pass === total;

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative">
        <svg width="52" height="52" viewBox="0 0 52 52" className="-rotate-90">
          <circle cx="26" cy="26" r={r} fill="none" stroke="#F1F5F9" strokeWidth="3" />
          <circle
            cx="26" cy="26" r={r} fill="none"
            stroke={ok ? "#07734A" : "#C3271C"}
            strokeWidth="3" strokeLinecap="round"
            strokeDasharray={circ} strokeDashoffset={offset}
            className="transition-all duration-700"
          />
        </svg>
        <span className={`absolute inset-0 flex items-center justify-center font-mono text-xs font-bold ${
          ok ? "text-status-verified" : "text-status-flagged"
        }`}>
          {pass}/{total}
        </span>
      </div>
      <span className="text-xs font-medium text-surface-500">{label}</span>
    </div>
  );
}

export default function StepDecision({ output, verdict }: Props) {
  const [decision, setDecision] = useState<Decision>(null);
  const [note, setNote] = useState("");

  const overall =
    verdict.overall === "verified"
      ? "verified"
      : verdict.abstention.ok && verdict.abstention.abstained
        ? "abstained"
        : "flagged";

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Summary card */}
      <div className="card-static overflow-hidden">
        <div className="h-1 bg-accent-500" />
        <div className="p-6">
          <div className="flex flex-wrap items-start justify-between gap-6">
            {/* Left: Overall status */}
            <div>
              <div className="section-title mb-3">Tổng kết kiểm chứng</div>
              <div className="flex items-center gap-3">
                <StatusBadge status={overall} size="lg" />
                <div className="text-sm text-surface-500">
                  <span className="font-mono">{output.mode.toUpperCase()}</span>
                  {" · "}
                  <span className="font-mono">{output.model_id}</span>
                </div>
              </div>
            </div>

            {/* Right: Gate rings */}
            <div className="flex items-center gap-6">
              <GateSummaryRing
                pass={verdict.numbers.filter((n) => n.ok).length}
                total={verdict.numbers.length}
                label="Số liệu"
              />
              <GateSummaryRing
                pass={verdict.citations.filter((c) => c.ok).length}
                total={verdict.citations.length}
                label="Trích dẫn"
              />
              <GateSummaryRing
                pass={verdict.claims.filter((c) => c.supported).length}
                total={verdict.claims.length}
                label="Nhận định"
              />
              <GateSummaryRing
                pass={verdict.abstention.ok ? 1 : 0}
                total={1}
                label="Từ chối"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Decision panel */}
      <div className="card-static p-6">
        <h3 className="mb-5 text-sm font-bold text-ink-900">Quyết định của bạn</h3>
        <div className="grid gap-3 sm:grid-cols-3">
          {(Object.entries(DECISIONS) as [Decision & string, typeof DECISIONS.approve][]).map(
            ([key, d]) => (
              <button
                key={key}
                onClick={() => setDecision(key as Decision)}
                className={`flex flex-col items-center gap-2 rounded-xl px-5 py-5 text-sm font-semibold transition-all duration-200 ${
                  decision === key ? d.active : d.inactive
                }`}
              >
                {d.icon}
                <span>{d.label}</span>
                <span className={`text-xs font-normal ${
                  decision === key ? "text-white/80" : "text-surface-500"
                }`}>
                  {d.desc}
                </span>
              </button>
            ),
          )}
        </div>

        {decision && (
          <div className="mt-5 space-y-4 animate-slide-up">
            <div>
              <label className="section-title mb-2 block">Ghi chú (tùy chọn)</label>
              <textarea
                value={note}
                onChange={(e) => setNote(e.target.value)}
                rows={3}
                className="w-full rounded-xl border border-surface-200 p-4 text-sm shadow-sm transition-all focus:border-accent-400 focus:ring-2 focus:ring-accent-100 focus:outline-none"
                placeholder="Ghi chú cho quyết định này…"
              />
            </div>

            <div className="rounded-xl bg-surface-50 p-5 ring-1 ring-surface-200">
              <div className="flex items-center gap-2 text-sm">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <circle cx="8" cy="8" r="6" stroke="#0F62B3" strokeWidth="1.5"/>
                  <path d="M8 5.5V8.5M8 10.5V11" stroke="#0F62B3" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
                <span className="font-semibold text-ink-900">
                  {decision === "approve"
                    ? "Đã phê duyệt"
                    : decision === "flag"
                      ? "Đã đánh dấu cần xem lại"
                      : "Đã trả lại"}
                </span>
              </div>
              <p className="mt-2 text-xs text-surface-500">
                Trong hệ thống thật, quyết định này sẽ được ghi nhận cùng thông tin phiên
                (model, thời gian, người duyệt) và chuyển tiếp theo quy trình FP&A.
                Đây là bản demo minh họa.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
