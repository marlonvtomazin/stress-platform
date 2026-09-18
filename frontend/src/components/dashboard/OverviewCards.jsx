import {
  Activity,
  TriangleAlert,
  Gauge,
  Clock,
} from "lucide-react";

import OverviewCard from "./OverviewCard";

export default function OverviewCards({ executions }) {
  const totalExecutions = executions.length;

  const failedExecutions = executions.filter(
    execution => execution.status !== "SUCCESS"
  ).length;

  const failureRate =
    totalExecutions === 0
      ? 0
      : ((failedExecutions / totalExecutions) * 100).toFixed(1);

  const averageDuration =
    totalExecutions === 0
      ? 0
      : (
          executions.reduce(
            (total, execution) => total + execution.duration_seconds,
            0
          ) / totalExecutions
        ).toFixed(1);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5 mb-8">
      <OverviewCard
        title="Total Executions"
        value={totalExecutions}
        subtitle="Stored executions"
        icon={Activity}
        color="blue"
      />

      <OverviewCard
        title="Failed Executions"
        value={failedExecutions}
        subtitle="Threshold or runtime errors"
        icon={TriangleAlert}
        color="red"
      />

      <OverviewCard
        title="Failure Rate"
        value={`${failureRate}%`}
        subtitle="Across all executions"
        icon={Gauge}
        color="orange"
      />

      <OverviewCard
        title="Average Duration"
        value={`${averageDuration}s`}
        subtitle="Average runtime"
        icon={Clock}
        color="green"
      />
    </div>
  );
}