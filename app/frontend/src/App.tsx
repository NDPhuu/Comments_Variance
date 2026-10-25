import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import LandingPage from "./pages/LandingPage";
import CaseListPage from "./pages/CaseListPage";
import CaseInvestigationPage from "./pages/CaseInvestigationPage";
import ResearchPage from "./pages/ResearchPage";

export default function App() {
  return (
    <Routes>
      <Route index element={<LandingPage />} />
      <Route element={<Layout />}>
        <Route path="/workbench" element={<CaseListPage />} />
        <Route path="/case/:caseId" element={<CaseInvestigationPage />} />
        <Route path="/research" element={<ResearchPage />} />
      </Route>
    </Routes>
  );
}
