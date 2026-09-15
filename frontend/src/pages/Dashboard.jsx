import AppLayout from "../components/layout/AppLayout";
import useExecutions from "../hooks/useExecutions";

export default function Dashboard() {
  const { executions, loading, error, refresh } = useExecutions();

  return (
    <AppLayout title="Dashboard">
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold">
            Welcome to Stress Platform 🚀
          </h2>

          <p className="text-slate-400 mt-2">
            Connected to FastAPI backend.
          </p>
        </div>

        <button
          onClick={refresh}
          className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
        >
          Refresh Executions
        </button>

        {loading && (
          <p className="text-yellow-400">Loading executions...</p>
        )}

        {error && (
          <p className="text-red-500">
            Error: {error}
          </p>
        )}

        {!loading && !error && (
          <>
            <p className="text-green-400 font-semibold">
              {executions.length} execution(s) found.
            </p>

            <div className="space-y-4">
              {executions.map((execution) => (
                <div
                  key={execution.execution_id}
                  className="bg-slate-900 border border-slate-800 rounded-xl p-5"
                >
                  <div className="flex justify-between items-center">
                    <h3 className="text-lg font-semibold">
                      {execution.test_name}
                    </h3>

                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        execution.status === "SUCCESS"
                          ? "bg-green-600/20 text-green-400"
                          : execution.status === "THRESHOLD_FAILED"
                          ? "bg-red-600/20 text-red-400"
                          : "bg-yellow-600/20 text-yellow-400"
                      }`}
                    >
                      {execution.status}
                    </span>
                  </div>

                  <p className="text-slate-400 text-sm mt-1">
                    {execution.application} • {execution.environment}
                  </p>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 text-sm">
                    <div>
                      <p className="text-slate-500">Requests</p>
                      <p className="font-semibold">
                        {execution.total_requests}
                      </p>
                    </div>

                    <div>
                      <p className="text-slate-500">Error Rate</p>
                      <p className="font-semibold">
                        {execution.error_rate}%
                      </p>
                    </div>

                    <div>
                      <p className="text-slate-500">Avg Response</p>
                      <p className="font-semibold">
                        {execution.avg_response_time} ms
                      </p>
                    </div>

                    <div>
                      <p className="text-slate-500">P95</p>
                      <p className="font-semibold">
                        {execution.p95} ms
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </AppLayout>
  );
}