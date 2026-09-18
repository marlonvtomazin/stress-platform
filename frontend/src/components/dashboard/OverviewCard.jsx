export default function OverviewCard({
  title,
  value,
  subtitle,
  icon: Icon,
  color = "blue",
}) {
  const colors = {
    blue: "text-blue-400 bg-blue-500/10 border-blue-500/20",
    green: "text-green-400 bg-green-500/10 border-green-500/20",
    orange: "text-orange-400 bg-orange-500/10 border-orange-500/20",
    red: "text-red-400 bg-red-500/10 border-red-500/20",
  };

  return (
    <div className="
      bg-slate-900
      border border-slate-800
      rounded-2xl
      p-5
      hover:border-slate-700
      transition-all duration-200
    ">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-slate-400 text-sm">
            {title}
          </p>

          <h2 className="text-3xl font-bold mt-2 text-white">
            {value}
          </h2>

          <p className="text-slate-500 text-sm mt-3">
            {subtitle}
          </p>
        </div>

        {Icon && (
          <div className={`p-3 rounded-xl border ${colors[color]}`}>
            <Icon size={22} />
          </div>
        )}
      </div>
    </div>
  );
}