import { Outlet, NavLink, useLocation } from "react-router-dom";

export default function Layout() {
  const { pathname } = useLocation();
  const isLanding = pathname === "/";

  return (
    <div className="min-h-screen flex flex-col bg-page">
      <header className="sticky top-0 z-40 bg-ink-950">
        <div className="mx-auto flex h-14 max-w-7xl items-center gap-8 px-4 sm:px-6">
          <NavLink
            to="/"
            className="text-xs font-extrabold uppercase tracking-[0.04em] text-white"
          >
            Variance Workbench
          </NavLink>

          <nav className="flex items-center gap-1">
            <NavLink
              to="/workbench"
              className={({ isActive }) =>
                `flex h-10 items-center px-3.5 text-sm font-semibold transition-colors duration-150 ${
                  isActive
                    ? "bg-accent-500 text-white"
                    : "text-surface-300 hover:text-white"
                }`
              }
            >
              Phân tích
            </NavLink>
            <NavLink
              to="/research"
              className={({ isActive }) =>
                `flex h-10 items-center px-3.5 text-sm font-semibold transition-colors duration-150 ${
                  isActive
                    ? "bg-accent-500 text-white"
                    : "text-surface-300 hover:text-white"
                }`
              }
            >
              Đánh giá
            </NavLink>
          </nav>

          <div className="ml-auto hidden sm:block">
            <span className="text-xs font-medium text-surface-300">
              gemini-3.5-flash-lite
            </span>
          </div>
        </div>
      </header>

      <main className="flex-1">
        <Outlet />
      </main>

      {!isLanding && (
        <footer className="border-t border-surface-200 bg-white py-4">
          <div className="mx-auto max-w-7xl px-4 sm:px-6">
            <span className="text-xs text-surface-500">
              Dữ liệu mô phỏng · Không dùng cho báo cáo thực tế
            </span>
          </div>
        </footer>
      )}
    </div>
  );
}
