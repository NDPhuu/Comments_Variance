import { useState } from "react";
import { api } from "@/api/client";
import type { GenerationOutput, Verdict } from "@/types";
import StatusBadge from "./StatusBadge";

interface Props {
  caseId: string;
  output: GenerationOutput;
  verdict: Verdict | null;
  onVerdict: (v: Verdict) => void;
  onNext: () => void;
}

function GateCard({
  name,
  description,
  items,
  ok,
  icon,
}: {
  name: string;
  description: string;
  items: { label: string; ok: boolean; detail?: string }[];
  ok: boolean;
  icon: React.ReactNode;
}) {
  const [open, setOpen] = useState(true);
  const passCount = items.filter((i) => i.ok).length;

  return (
    <div className={`card-static overflow-hidden transition-all duration-200 ${
      ok ? "ring-1 ring-status-verified-ring" : "ring-1 ring-status-flagged-ring"
    }`}>
      {/* Gate header */}
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center gap-4 px-5 py-4 text-left transition-colors hover:bg-surface-50/50"
      >
        <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${
          ok ? "bg-status-verified-bg text-status-verified" : "bg-status-flagged-bg text-status-flagged"
        }`}>
          {icon}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-bold text-ink-900">{name}</span>
            <span className={`px-2 py-0.5 text-xs font-bold ${
              ok
                ? "bg-status-verified-bg text-status-verified"
                : "bg-status-flagged-bg text-status-flagged"
            }`}>
              {passCount}/{items.length}
            </span>
          </div>
          <p className="mt-0.5 text-xs text-surface-500 truncate">{description}</p>
        </div>
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"
          className={`shrink-0 text-surface-300 transition-transform duration-200 ${open ? "rotate-180" : ""}`}>
          <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>

      {/* Gate items */}
      {open && (
        <div className="border-t border-surface-100 divide-y divide-surface-100">
          {items.length === 0 ? (
            <div className="px-5 py-4 text-sm text-surface-400">
              Không có mục nào cần kiểm tra
            </div>
          ) : (
            items.map((it, i) => (
              <div
                key={i}
                className={`flex items-start gap-3 px-5 py-3 text-sm transition-colors ${
                  it.ok ? "hover:bg-surface-50" : "bg-status-flagged-bg/30"
                }`}
              >
                <span className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-xs font-bold text-white ${
                  it.ok ? "bg-status-verified" : "bg-status-flagged"
                }`}>
                  {it.ok ? "✓" : "✗"}
                </span>
                <div className="flex-1 min-w-0">
                  <span className="font-mono text-xs text-ink-800">{it.label}</span>
                  {it.detail && (
                    <span className="ml-2 text-xs text-surface-400">— {it.detail}</span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default function StepVerification({
  caseId,
  output,
  verdict,
  onVerdict,
  onNext,
}: Props) {
  const [verifying, setVerifying] = useState(false);
  const [error, setError] = useState("");

  async function runVerify() {
    setVerifying(true);
    setError("");
    try {
      const v = await api.verify(caseId, output as unknown as Record<string, unknown>);
      onVerdict(v);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Lỗi kiểm chứng");
    } finally {
      setVerifying(false);
    }
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Run verification */}
      {!verdict && (
        <div className="card-static p-6 text-center">
          <h3 className="text-lg font-bold text-ink-950">Kiểm chứng kết quả</h3>
          <p className="mx-auto mt-2 max-w-md text-sm text-ink-800">
            Chạy 4 cổng kiểm tra trên kết quả giải trình: số liệu, trích dẫn, nhận định và cơ chế từ chối.
            Quá trình hoàn toàn xác định — không dùng LLM.
          </p>
          <button
            onClick={runVerify}
            disabled={verifying}
            className="btn-primary mt-5"
          >
            {verifying ? (
              <>
                <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                Đang kiểm chứng…
              </>
            ) : (
              <>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M8 2L13 5V8.5C13 11.8 10.8 14.7 8 15.5C5.2 14.7 3 11.8 3 8.5V5L8 2Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                </svg>
                Chạy kiểm chứng
              </>
            )}
          </button>
          {error && (
            <div className="mt-4 rounded-lg bg-status-flagged-bg p-3.5 text-sm text-status-flagged ring-1 ring-status-flagged-ring">
              {error}
            </div>
          )}
        </div>
      )}

      {/* Verdict results */}
      {verdict && (
        <>
          {/* Overall badge */}
          <div className="flex items-center gap-4 animate-slide-up">
            <h3 className="text-lg font-bold text-ink-950">Kết quả kiểm chứng</h3>
            <StatusBadge
              status={
                verdict.overall === "verified"
                  ? "verified"
                  : verdict.abstention.ok && verdict.abstention.abstained
                    ? "abstained"
                    : "flagged"
              }
              size="lg"
            />
          </div>

          {/* 4 gates */}
          <div className="space-y-3">
            <GateCard
              name="Cổng số liệu"
              description="Mỗi con số trong giải trình phải khớp với nguồn tất định (engine hoặc tài liệu đã trích dẫn)"
              ok={verdict.numbers.every((n) => n.ok)}
              icon={<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 17H17M5 13V17M9 9V17M13 5V17M17 1V17" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/></svg>}
              items={verdict.numbers.map((n) => ({
                label: n.raw,
                ok: n.ok,
                detail: n.ok ? `khớp ${n.matched}` : "không khớp trường nào",
              }))}
            />
            <GateCard
              name="Cổng trích dẫn"
              description="[EV-xxx] phải tồn tại, đúng property và kỳ không vượt quá tháng case"
              ok={verdict.citations.every((c) => c.ok)}
              icon={<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M4 4H16V16H4V4Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/><path d="M7 8H13M7 12H11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/></svg>}
              items={verdict.citations.map((c) => ({
                label: c.id,
                ok: c.ok,
                detail: c.ok ? "hợp lệ" : c.reason,
              }))}
            />
            <GateCard
              name="Cổng nhận định"
              description="Mỗi nguyên nhân xác nhận (driver_confirmed) phải có ≥1 trích dẫn hợp lệ"
              ok={verdict.claims.every((c) => c.supported)}
              icon={<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2L18 6V10C18 15.5 14.5 19.5 10 20.5C5.5 19.5 2 15.5 2 10V6L10 2Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/></svg>}
              items={verdict.claims.map((c) => ({
                label: c.text.slice(0, 80) + (c.text.length > 80 ? "…" : ""),
                ok: c.supported,
                detail: c.supported ? "có bằng chứng" : "không có trích dẫn hợp lệ",
              }))}
            />
            <GateCard
              name="Cổng từ chối"
              description="Khi bằng chứng yếu (không có tài liệu liên kết), hệ thống phải từ chối đưa ra nguyên nhân"
              ok={verdict.abstention.ok}
              icon={<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 4L16 10L10 16L4 10Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/></svg>}
              items={[
                {
                  label: verdict.abstention.evidence_weak ? "Bằng chứng yếu" : "Bằng chứng đủ",
                  ok: true,
                  detail: verdict.abstention.evidence_weak ? "không có tài liệu liên kết" : "có tài liệu liên kết",
                },
                {
                  label: verdict.abstention.abstained ? "Đã từ chối đưa nguyên nhân" : "Có đưa nguyên nhân",
                  ok: verdict.abstention.ok,
                  detail: !verdict.abstention.ok
                    ? "bằng chứng yếu nhưng vẫn nêu nguyên nhân"
                    : verdict.abstention.over_abstain
                      ? "từ chối quá mức (bằng chứng đủ)"
                      : "",
                },
              ]}
            />
          </div>

          <div className="flex justify-end pt-2">
            <button onClick={onNext} className="btn-primary">
              Tiếp theo
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M6 4L10 8L6 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        </>
      )}
    </div>
  );
}
