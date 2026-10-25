import { useState } from "react";
import { api } from "@/api/client";
import type { GenerationOutput } from "@/types";

type Mode = "m0" | "m1" | "m2";

const MODE_INFO: Record<Mode, { label: string; desc: string; color: string }> = {
  m0: { label: "M0", desc: "Chỉ dùng LLM, không có tài liệu tham chiếu", color: "from-surface-400 to-surface-300" },
  m1: { label: "M1", desc: "Có tài liệu tham chiếu, chưa kiểm chứng", color: "from-amber-400 to-amber-500" },
  m2: { label: "M2", desc: "Có tài liệu + cấu trúc trích dẫn + kiểm chứng", color: "from-accent-400 to-accent-600" },
};

interface Props {
  caseId: string;
  liveOutput: GenerationOutput | null;
  onGenerate: (output: GenerationOutput) => void;
  onNext: () => void;
}

function CitationChip({ id }: { id: string }) {
  return (
    <span className="inline-flex items-center rounded-md border border-accent-200 bg-accent-50 px-2 py-0.5 font-mono text-xs font-semibold text-accent-600 transition-colors hover:bg-accent-100">
      {id}
    </span>
  );
}

function OutputView({ output }: { output: GenerationOutput }) {
  const evIds = output.draft_comment?.match(/\[EV-\d+\]/g)?.map((m) => m.slice(1, -1)) ?? [];

  return (
    <div className="space-y-4 animate-slide-up">
      {output.abstained && (
        <div className="flex items-start gap-3 rounded-xl bg-status-abstained-bg p-4 ring-1 ring-status-abstained-ring">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" className="mt-0.5 shrink-0 text-status-abstained">
            <path d="M10 3L17 10L10 17L3 10Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
            <path d="M10 7.5V10.5M10 13V13.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
          <div className="text-sm text-status-abstained">
            <strong>Từ chối:</strong> Không đủ tài liệu liên kết để xác định nguyên nhân cụ thể.
          </div>
        </div>
      )}

      {/* Draft comment */}
      <div className="card-static p-5">
        <div className="section-title mb-3">Bản giải trình</div>
        <p className="whitespace-pre-wrap text-sm leading-relaxed text-ink-800">
          {output.draft_comment || "(Hệ thống đã từ chối đưa ra giải trình do thiếu bằng chứng)"}
        </p>
        {evIds.length > 0 && (
          <div className="mt-4 flex flex-wrap gap-1.5 border-t border-surface-100 pt-3">
            {evIds.map((id, i) => <CitationChip key={`${id}-${i}`} id={id} />)}
          </div>
        )}
      </div>

      {/* M2 structured fields */}
      {output.observed_facts && (
        <div className="card-static p-5">
          <div className="section-title mb-2">Dữ kiện quan sát</div>
          <p className="text-sm text-ink-800">{output.observed_facts}</p>
        </div>
      )}

      {output.drivers_confirmed && output.drivers_confirmed.length > 0 && (
        <div className="card-static p-5">
          <div className="section-title mb-3">
            Nguyên nhân xác nhận ({output.drivers_confirmed.length})
          </div>
          <div className="space-y-3">
            {output.drivers_confirmed.map((d, i) => (
              <div key={i} className="rounded-lg bg-status-verified-bg/50 p-3.5 ring-1 ring-status-verified-ring/50">
                <p className="text-sm text-ink-800">{d.text}</p>
                <div className="mt-2 flex gap-1.5">
                  {d.evidence_ids.map((id) => <CitationChip key={id} id={id} />)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {output.drivers_possible && output.drivers_possible.length > 0 && (
        <div className="card-static p-5">
          <div className="section-title mb-3">
            Nguyên nhân có thể ({output.drivers_possible.length})
          </div>
          <div className="space-y-2">
            {output.drivers_possible.map((d, i) => (
              <div key={i} className="rounded-lg bg-surface-50 p-3 text-sm text-ink-800">
                {d.text}
              </div>
            ))}
          </div>
        </div>
      )}

      {output.forward_note && (
        <div className="card-static border-l-4 border-l-status-warning p-5">
          <div className="section-title mb-1 text-status-warning">Ghi chú theo dõi</div>
          <p className="text-sm text-ink-800">{output.forward_note}</p>
        </div>
      )}
    </div>
  );
}

export default function StepCommentary({
  caseId,
  liveOutput,
  onGenerate,
  onNext,
}: Props) {
  const [generating, setGenerating] = useState(false);
  const [mode, setMode] = useState<Mode>("m2");
  const [error, setError] = useState("");

  async function handleGenerate() {
    setGenerating(true);
    setError("");
    try {
      const output = await api.generate(caseId, mode);
      onGenerate(output);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Lỗi sinh giải trình");
    } finally {
      setGenerating(false);
    }
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Generate controls */}
      <div className="card-static p-5">
        <div className="flex flex-wrap items-center gap-5">
          {/* Mode selector */}
          <div>
            <div className="section-title mb-2">Chế độ</div>
            <div className="flex rounded-xl bg-surface-100 p-1">
              {(["m0", "m1", "m2"] as Mode[]).map((m) => {
                const info = MODE_INFO[m];
                return (
                  <button
                    key={m}
                    onClick={() => setMode(m)}
                    className={`relative rounded-lg px-5 py-2.5 text-sm font-semibold transition-all duration-200 ${
                      mode === m
                        ? "bg-accent-500 text-white"
                        : "text-surface-500 hover:text-ink-800"
                    }`}
                  >
                    {info.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Mode description */}
          <div className="flex-1 min-w-[200px]">
            <div className="rounded-lg bg-surface-50 px-4 py-3 text-sm text-ink-800">
              {MODE_INFO[mode].desc}
            </div>
          </div>

          {/* Generate button */}
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="btn-primary h-11"
          >
            {generating ? (
              <>
                <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                Đang tạo giải trình…
              </>
            ) : (
              <>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M8 2V14M2 8H14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
                Tạo giải trình
              </>
            )}
          </button>
        </div>
        {error && (
          <div className="mt-4 rounded-lg bg-status-flagged-bg p-3.5 text-sm text-status-flagged ring-1 ring-status-flagged-ring">
            {error}
          </div>
        )}
      </div>

      {/* Live output */}
      {liveOutput && (
        <div>
          <div className="mb-4 flex items-center gap-3">
            <h3 className="text-sm font-bold text-ink-900">
              Kết quả {liveOutput.mode.toUpperCase()}
            </h3>
            <span className="flex items-center gap-1.5 bg-accent-50 px-3 py-1 text-xs font-semibold text-accent-600 ring-1 ring-accent-200">
              <span className="h-1.5 w-1.5 rounded-full bg-accent-500 animate-pulse-soft" />
              Kết quả trực tiếp
            </span>
            <span className="font-mono text-xs text-surface-500">
              {liveOutput.model_id}
            </span>
          </div>
          <OutputView output={liveOutput} />
        </div>
      )}

      <div className="flex justify-end pt-2">
        <button onClick={onNext} disabled={!liveOutput} className="btn-primary">
          Tiếp theo
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M6 4L10 8L6 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
}
