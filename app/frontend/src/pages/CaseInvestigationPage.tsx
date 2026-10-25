import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "@/api/client";
import type {
  VarianceCase,
  EvidencePack,
  GenerationOutput,
  Verdict,
  StepId,
} from "@/types";
import ProgressBar from "@/components/ProgressBar";
import StepOverview from "@/components/StepOverview";
import StepEvidence from "@/components/StepEvidence";
import StepCommentary from "@/components/StepCommentary";
import StepVerification from "@/components/StepVerification";
import StepDecision from "@/components/StepDecision";

function fmt(n: number) {
  return n.toLocaleString("en-US", { maximumFractionDigits: 0 });
}

function LoadingSkeleton() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 animate-fade-in">
      <div className="space-y-6">
        <div className="h-16 skeleton rounded-xl" />
        <div className="grid grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => <div key={i} className="h-28 skeleton rounded-xl" />)}
        </div>
        <div className="h-64 skeleton rounded-xl" />
      </div>
    </div>
  );
}

export default function CaseInvestigationPage() {
  const { caseId } = useParams<{ caseId: string }>();
  const navigate = useNavigate();

  const [caseData, setCaseData] = useState<VarianceCase | null>(null);
  const [pack, setPack] = useState<EvidencePack | null>(null);
  const [output, setOutput] = useState<GenerationOutput | null>(null);
  const [verdict, setVerdict] = useState<Verdict | null>(null);
  const [step, setStep] = useState<StepId>(1);
  const [unlocked, setUnlocked] = useState<StepId>(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!caseId) return;
    setLoading(true);
    setError("");
    Promise.all([
      api.caseDetail(caseId),
      api.evidence(caseId),
    ])
      .then(([c, e]) => {
        setCaseData(c);
        setPack(e);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Lỗi tải dữ liệu"))
      .finally(() => setLoading(false));
  }, [caseId]);

  function goStep(s: StepId) {
    setStep(s);
  }

  function advance(next: StepId) {
    if (next > unlocked) setUnlocked(next);
    setStep(next);
  }

  if (loading) return <LoadingSkeleton />;

  if (error || !caseData) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-20 text-center animate-fade-in">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-status-flagged-bg ring-1 ring-status-flagged-ring">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <path d="M14 8V15M14 19V20" stroke="#DC2626" strokeWidth="2" strokeLinecap="round"/>
            <circle cx="14" cy="14" r="11" stroke="#DC2626" strokeWidth="1.5"/>
          </svg>
        </div>
        <p className="text-lg font-semibold text-status-flagged">{error || "Không tìm thấy case"}</p>
        <button onClick={() => navigate("/workbench")} className="btn-secondary mt-6">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M10 4L6 8L10 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          Về danh sách
        </button>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6">
      {/* Sticky case header */}
      {/* Trên điện thoại thanh này cao và xuống dòng, dính lại sẽ che số liệu bên dưới. */}
      <div className="relative sm:sticky sm:top-14 z-30 -mx-4 mb-6 border-b border-surface-200 bg-white px-4 py-3.5 sm:-mx-6 sm:px-6">
        <div className="flex flex-wrap items-center gap-4">
          <button
            onClick={() => navigate("/workbench")}
            className="flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-sm text-surface-500 transition-colors hover:bg-surface-100 hover:text-ink-900"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M10 4L6 8L10 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Danh sách
          </button>

          <div className="h-6 w-px bg-surface-200" />

          <div className="flex items-center gap-3">
            <h1 className="text-lg font-bold text-ink-950">{caseData.pl_line}</h1>
            <div className="flex items-center gap-2 rounded-lg bg-surface-50 px-2.5 py-1 ring-1 ring-surface-200">
              <span className="h-2 w-2 rounded-full bg-accent-400" />
              <span className="font-mono text-xs text-ink-800">
                {caseData.property}
              </span>
              <span className="text-surface-300">·</span>
              <span className="font-mono text-xs text-ink-800">
                {caseData.month}
              </span>
            </div>
            <span
              className={`font-mono text-sm font-bold ${
                caseData.direction === "unfavorable"
                  ? "text-status-flagged"
                  : "text-status-verified"
              }`}
            >
              ${fmt(caseData.variance)}
            </span>
          </div>

          <div className="ml-auto">
            <ProgressBar current={step} unlocked={unlocked} onStep={goStep} />
          </div>
        </div>
      </div>

      {/* Step content */}
      <div key={step}>
        {step === 1 && (
          <StepOverview caseData={caseData} onNext={() => advance(2)} />
        )}
        {step === 2 && pack && (
          <StepEvidence pack={pack} onNext={() => advance(3)} />
        )}
        {step === 3 && (
          <StepCommentary
            caseId={caseData.case_id}
            liveOutput={output}
            onGenerate={(o) => {
              setOutput(o);
              setVerdict(null);
            }}
            onNext={() => advance(4)}
          />
        )}
        {step === 4 && output && (
          <StepVerification
            caseId={caseData.case_id}
            output={output}
            verdict={verdict}
            onVerdict={(v) => {
              setVerdict(v);
              if (v) setUnlocked(5);
            }}
            onNext={() => advance(5)}
          />
        )}
        {step === 5 && output && verdict && (
          <StepDecision output={output} verdict={verdict} />
        )}
      </div>
    </div>
  );
}
