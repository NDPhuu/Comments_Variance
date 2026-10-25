import type { EvidencePack, EvidenceDoc } from "@/types";

interface Props {
  pack: EvidencePack;
  onNext: () => void;
}

const AUTH_CONFIG: Record<number, { label: string; color: string; icon: string }> = {
  1: { label: "Cao", color: "bg-emerald-50 text-emerald-700 ring-emerald-200", icon: "★" },
  2: { label: "Trung bình", color: "bg-amber-50 text-amber-700 ring-amber-200", icon: "◆" },
  3: { label: "Thấp", color: "bg-surface-100 text-surface-500 ring-surface-200", icon: "○" },
};

const TYPE_LABELS: Record<string, string> = {
  termination_notice: "Thông báo chấm dứt",
  work_order: "Lệnh công việc",
  insurance_letter: "Thư bảo hiểm",
  handover_minutes: "Biên bản bàn giao",
  contract_annex: "Phụ lục hợp đồng",
  approval_email: "Email phê duyệt",
  vendor_invoice: "Hóa đơn nhà cung cấp",
  rate_notice: "Thông báo giá",
  accounting_memo: "Ghi chú kế toán",
  loan_memo: "Ghi chú vay",
  distractor_memo: "Tài liệu nhiễu",
  ops_memo: "Ghi chú vận hành",
};

function DocCard({ doc, index }: { doc: EvidenceDoc; index: number }) {
  const auth = AUTH_CONFIG[doc.authority] ?? AUTH_CONFIG[3];

  return (
    <div
      className={`card-static overflow-hidden transition-all duration-200 animate-slide-up ${
        doc.linked
          ? "ring-1 ring-accent-200 hover:ring-accent-300"
          : "opacity-75 hover:opacity-90"
      }`}
      style={{ animationDelay: `${index * 60}ms` }}
    >
      {doc.linked && (
        <div className="h-1 bg-accent-500" />
      )}
      <div className="p-5">
        {/* Header row */}
        <div className="mb-3 flex flex-wrap items-center gap-2">
          <span className="font-mono text-sm font-bold text-accent-600">
            {doc.doc_id}
          </span>
          <span className="rounded-md bg-surface-50 px-2 py-0.5 text-xs font-medium text-ink-800 ring-1 ring-surface-200">
            {TYPE_LABELS[doc.type] ?? doc.type.replace(/_/g, " ")}
          </span>
          <span className={`rounded-md px-2 py-0.5 text-xs font-semibold ring-1 ${auth.color}`}>
            {auth.icon} Tin cậy: {auth.label}
          </span>
          {doc.linked ? (
            <span className="rounded-md bg-accent-50 px-2 py-0.5 text-xs font-semibold text-accent-600 ring-1 ring-accent-200">
              Liên kết
            </span>
          ) : (
            <span className="rounded-md bg-surface-50 px-2 py-0.5 text-xs text-surface-500 ring-1 ring-surface-200">
              Không liên kết
            </span>
          )}
        </div>

        {/* Title */}
        <h4 className="mb-2 font-semibold text-ink-900">{doc.title}</h4>

        {/* Metadata */}
        <div className="mb-3 flex gap-4 text-xs text-surface-500">
          <span className="flex items-center gap-1">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><rect x="1" y="1" width="10" height="10" rx="2" stroke="currentColor" strokeWidth="1.2"/></svg>
            {doc.property}
          </span>
          <span className="flex items-center gap-1">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><circle cx="6" cy="6" r="4.5" stroke="currentColor" strokeWidth="1.2"/><path d="M6 3.5V6L8 7.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/></svg>
            {doc.period}
          </span>
          {doc.rrf != null && (
            <span className="font-mono">
              Điểm xếp hạng: {doc.rrf.toFixed(4)}
            </span>
          )}
        </div>

        {/* Text content */}
        <div className={`rounded-lg p-3.5 text-sm leading-relaxed ${
          doc.linked ? "bg-accent-50/50 text-ink-800" : "bg-surface-50 text-ink-800"
        }`}>
          {doc.text}
        </div>
      </div>
    </div>
  );
}

export default function StepEvidence({ pack, onNext }: Props) {
  const linked = pack.docs.filter((d) => d.linked);
  const unlinked = pack.docs.filter((d) => !d.linked);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Summary strip */}
      <div className="card-static p-5">
        <div className="flex flex-wrap items-center gap-6">
          <div>
            <div className="section-title">Tài liệu truy xuất</div>
            <div className="mt-1 text-2xl font-bold text-ink-950">{pack.docs.length}</div>
          </div>
          <div className="h-10 w-px bg-surface-200" />
          <div>
            <div className="section-title">Liên kết nội dung</div>
            <div className="mt-1 flex items-baseline gap-1">
              <span className={`text-2xl font-bold ${pack.linked_any ? "text-accent-600" : "text-status-flagged"}`}>
                {linked.length}
              </span>
              <span className="text-sm text-surface-500">/ {pack.docs.length}</span>
            </div>
          </div>
          <div className="h-10 w-px bg-surface-200" />
          <div>
            <div className="section-title">Phương pháp</div>
            <div className="mt-1 text-sm font-medium text-ink-800">
              BM25{pack.dense_used ? " + Dense" : ""} + Xếp hạng kết hợp
            </div>
          </div>
          {!pack.linked_any && (
            <div className="ml-auto rounded-lg bg-status-warning-bg px-4 py-2.5 ring-1 ring-status-warning-ring">
              <div className="flex items-center gap-2 text-sm font-semibold text-status-warning">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M8 2L14 13H2L8 2Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                  <path d="M8 7V9.5M8 11.5V12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
                Không có tài liệu liên kết — hệ thống sẽ từ chối đưa nguyên nhân
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Linked docs */}
      {linked.length > 0 && (
        <div>
          <h3 className="mb-4 flex items-center gap-2 text-sm font-bold text-ink-900">
            <span className="flex h-5 w-5 items-center justify-center rounded bg-accent-500 text-[10px] font-bold text-white">
              {linked.length}
            </span>
            Tài liệu liên kết
          </h3>
          <div className="space-y-3">
            {linked.map((d, i) => <DocCard key={d.doc_id} doc={d} index={i} />)}
          </div>
        </div>
      )}

      {/* Unlinked docs */}
      {unlinked.length > 0 && (
        <div>
          <h3 className="mb-4 flex items-center gap-2 text-sm font-semibold text-surface-500">
            <span className="flex h-5 w-5 items-center justify-center rounded bg-surface-200 text-[10px] font-bold text-surface-500">
              {unlinked.length}
            </span>
            Tài liệu không liên kết
          </h3>
          <div className="space-y-3">
            {unlinked.map((d, i) => <DocCard key={d.doc_id} doc={d} index={i} />)}
          </div>
        </div>
      )}

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
