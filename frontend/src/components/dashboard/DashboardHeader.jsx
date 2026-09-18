import { Play } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function DashboardHeader() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5 mb-8">
      <div>
        <p className="text-blue-400 text-sm font-medium uppercase tracking-widest">
          Stress Platform
        </p>

        <h1 className="text-4xl font-bold mt-2 text-white">
          Overview
        </h1>

        <p className="text-slate-400 mt-3 max-w-xl">
          Manage your performance tests, executions and reports from a single dashboard.
        </p>
      </div>

      <button
        onClick={() => navigate("/run")}
        className="
          flex items-center justify-center gap-2
          bg-blue-600 hover:bg-blue-700
          px-5 py-3 rounded-xl
          text-white font-medium
          transition-all duration-200
          shadow-lg shadow-blue-600/20
        "
      >
        <Play size={18} />
        Run Test
      </button>
    </div>
  );
}