export default function StatusBadge({ status }) {
  const styles = {
    SUCCESS: "bg-green-500/15 text-green-400 border-green-500/30",
    THRESHOLD_FAILED: "bg-red-500/15 text-red-400 border-red-500/30",
    FAILED: "bg-red-500/15 text-red-400 border-red-500/30",
    RUNNING: "bg-blue-500/15 text-blue-400 border-blue-500/30",
    PENDING: "bg-yellow-500/15 text-yellow-400 border-yellow-500/30",
  };

  return (
    <span
      className={`
        px-3 py-1 rounded-full text-xs font-semibold border
        ${styles[status] || "bg-slate-700 text-slate-300 border-slate-600"}
      `}
    >
      {status.replace("_", " ")}
    </span>
  );
}