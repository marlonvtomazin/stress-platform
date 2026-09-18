import { BarChart3, FileText, RotateCcw, ChevronRight } from "lucide-react";
import { useNavigate } from "react-router-dom";
import StatusBadge from "./StatusBadge";

export default function RecentExecutions({ executions }) {
  const navigate = useNavigate();

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
      {/* Header */}
      <div className="flex justify-between items-center px-6 py-5 border-b border-slate-800">
        <div>
          <h2 className="text-xl font-semibold text-white">
            Recent Executions
          </h2>

          <p className="text-slate-400 text-sm mt-1">
            Latest performance tests executed on the platform.
          </p>
        </div>

        <button
          onClick={() => navigate("/executions")}
          className="text-blue-400 hover:text-blue-300 text-sm flex items-center gap-2"
        >
          View all
          <ChevronRight size={16} />
        </button>
      </div>

      {/* Tabela */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="text-slate-400 border-b border-slate-800">
            <tr>
              <th className="text-left px-6 py-4 font-medium">Test Name</th>
              <th className="text-left px-4 py-4 font-medium">Status</th>
              <th className="text-left px-4 py-4 font-medium">Environment</th>
              <th className="text-left px-4 py-4 font-medium">Started At</th>
              <th className="text-left px-4 py-4 font-medium">Duration</th>
              <th className="text-right px-6 py-4 font-medium">Actions</th>
            </tr>
          </thead>

          <tbody>
            {executions.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-10 text-slate-500">
                  No executions found.
                </td>
              </tr>
            ) : (
              executions.slice(0, 5).map((execution) => (
                <tr
                  key={execution.execution_id}
                  className="border-b border-slate-800 hover:bg-slate-800/40 transition-colors"
                >
                  <td className="px-6 py-5">
                    <div>
                      <p className="font-medium text-white">
                        {execution.test_name}
                      </p>

                      <p className="text-slate-500 text-xs mt-1">
                        {execution.application}
                      </p>
                    </div>
                  </td>

                  <td className="px-4 py-5">
                    <StatusBadge status={execution.status} />
                  </td>

                  <td className="px-4 py-5 text-slate-300 capitalize">
                    {execution.environment}
                  </td>

                  <td className="px-4 py-5 text-slate-300">
                    {new Date(execution.started_at).toLocaleString("pt-BR")}
                  </td>

                  <td className="px-4 py-5 text-slate-300">
                    {execution.duration_seconds.toFixed(1)}s
                  </td>

                  <td className="px-6 py-5">
                    <div className="flex justify-end gap-3 text-slate-400">
                      <button className="hover:text-blue-400">
                        <BarChart3 size={18} />
                      </button>

                      <button className="hover:text-green-400">
                        <FileText size={18} />
                      </button>

                      <button className="hover:text-orange-400">
                        <RotateCcw size={18} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}