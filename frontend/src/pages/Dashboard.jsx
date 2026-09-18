import AppLayout from "../components/layout/AppLayout";
import DashboardHeader from "../components/dashboard/DashboardHeader";
import OverviewCards from "../components/dashboard/OverviewCards";
import useExecutions from "../hooks/useExecutions";

import RecentExecutions from "../components/execution/RecentExecutions";

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

          <RecentExecutions executions={executions} />
        </>
      )}
    </AppLayout>
  );
}