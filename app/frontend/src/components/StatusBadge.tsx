interface Props {
  status: "verified" | "flagged" | "abstained" | "pending";
  size?: "sm" | "md" | "lg";
}

const CONFIG = {
  verified: {
    bg: "bg-status-verified-bg",
    text: "text-status-verified",
    ring: "ring-status-verified-ring",
    icon: (
      <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
        <path d="M2 6L4.5 8.5L10 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    ),
    label: "Verified",
  },
  flagged: {
    bg: "bg-status-flagged-bg",
    text: "text-status-flagged",
    ring: "ring-status-flagged-ring",
    icon: (
      <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
        <path d="M6 3V6.5M6 8.5V9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
      </svg>
    ),
    label: "Cần xác nhận",
  },
  abstained: {
    bg: "bg-status-abstained-bg",
    text: "text-status-abstained",
    ring: "ring-status-abstained-ring",
    icon: (
      <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
        <path d="M6 2L10 6L6 10L2 6Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round" fill="none"/>
      </svg>
    ),
    label: "Từ chối",
  },
  pending: {
    bg: "bg-surface-100",
    text: "text-surface-400",
    ring: "ring-surface-200",
    icon: (
      <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
        <circle cx="6" cy="6" r="4" stroke="currentColor" strokeWidth="1.5" fill="none"/>
      </svg>
    ),
    label: "Chờ xử lý",
  },
};

export default function StatusBadge({ status, size = "sm" }: Props) {
  const c = CONFIG[status];
  const s =
    size === "lg"
      ? "gap-2 px-4 py-2 text-sm ring-2"
      : size === "md"
        ? "gap-1.5 px-3 py-1.5 text-xs ring-1"
        : "gap-1 px-2.5 py-1 text-xs ring-1";

  return (
    <span
      className={`inline-flex items-center font-semibold ${c.bg} ${c.text} ${c.ring} ${s}`}
    >
      {c.icon}
      {c.label}
    </span>
  );
}
