import type { StepId } from "@/types";
import { STEP_LABELS } from "@/types";

interface Props {
  current: StepId;
  unlocked: StepId;
  onStep: (s: StepId) => void;
}

const STEPS: StepId[] = [1, 2, 3, 4, 5];

export default function ProgressBar({ current, unlocked, onStep }: Props) {
  return (
    <nav className="flex items-center" aria-label="Tiến trình điều tra">
      {STEPS.map((s, i) => {
        const done = s < current;
        const active = s === current;
        const locked = s > unlocked;

        return (
          <div key={s} className="flex items-center">
            {/* Connector line */}
            {i > 0 && (
              <div className="relative mx-1 h-0.5 w-8 sm:w-12 overflow-hidden rounded-full bg-surface-200">
                {s <= unlocked && (
                  <div
                    className="absolute inset-y-0 left-0 rounded-full bg-accent-500 transition-all duration-500"
                    style={{ width: done || active ? "100%" : "0%" }}
                  />
                )}
              </div>
            )}

            {/* Step button */}
            <button
              onClick={() => !locked && onStep(s)}
              disabled={locked}
              className={`group relative flex items-center gap-2 rounded-full transition-all duration-200 ${
                active
                  ? "pl-1 pr-4 py-1"
                  : "p-1"
              } ${locked ? "cursor-not-allowed" : "cursor-pointer"}`}
            >
              {/* Circle */}
              <span
                className={`relative flex h-8 w-8 items-center justify-center rounded-full text-xs font-bold transition-all duration-200 ${
                  active
                    ? "bg-accent-500 text-white"
                    : done
                      ? "bg-accent-500 text-white"
                      : locked
                        ? "bg-surface-100 text-surface-300"
                        : "bg-surface-100 text-surface-500 group-hover:bg-accent-50 group-hover:text-accent-600"
                }`}
              >
                {done ? (
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M2.5 7L5.5 10L11.5 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                ) : (
                  s
                )}
              </span>

              {/* Label — only shown for active step */}
              {active && (
                <span className="hidden sm:block text-sm font-semibold text-accent-700 animate-fade-in">
                  {STEP_LABELS[s]}
                </span>
              )}

              {/* Tooltip for non-active */}
              {!active && !locked && (
                <span className="pointer-events-none absolute -bottom-8 left-1/2 -translate-x-1/2 whitespace-nowrap bg-ink-900 px-2 py-1 text-xs text-white opacity-0 transition-opacity group-hover:opacity-100">
                  {STEP_LABELS[s]}
                </span>
              )}
            </button>
          </div>
        );
      })}
    </nav>
  );
}
