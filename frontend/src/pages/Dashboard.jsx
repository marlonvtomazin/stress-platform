import AppLayout from "../components/layout/AppLayout";
import DashboardHeader from "../components/dashboard/DashboardHeader";
import OverviewCards from "../components/dashboard/OverviewCards";
import useExecutions from "../hooks/useExecutions";

export default function Dashboard() {
  const { executions, loading, error } = useExecutions();

  return (
    <AppLayout title="Dashboard">
      <DashboardHeader />

      {loading && (
        <p className="text-slate-400">Loading dashboard...</p>
      )}

      {error && (
        <p className="text-red-500">{error}</p>
      )}

      {!loading && !error && (
        <>
          <OverviewCards executions={executions} />

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <h2 className="text-xl font-semibold text-white mb-2">
              Recent Executions
            </h2>

            <p className="text-slate-400">
              This table will be implemented in the next step.
            </p>
          </div>
        </>
      )}
    </AppLayout>
  );
}