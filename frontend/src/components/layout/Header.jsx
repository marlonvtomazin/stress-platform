import { Bell, Search, Server } from "lucide-react";

export default function Header({ title }) {
  return (
    <header className="h-16 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-6">
      {/* Título da página */}
      <div>
        <h1 className="text-xl font-semibold text-white">{title}</h1>
        <p className="text-xs text-slate-400">
          Stress Platform • Performance Testing Dashboard
        </p>
      </div>

      {/* Lado direito */}
      <div className="flex items-center gap-4">
        <button className="p-2 rounded-lg hover:bg-slate-800 transition-colors">
          <Search size={18} className="text-slate-400" />
        </button>

        <button className="p-2 rounded-lg hover:bg-slate-800 transition-colors">
          <Bell size={18} className="text-slate-400" />
        </button>

        {/* Status do backend */}
        <div className="flex items-center gap-2 bg-slate-800 px-3 py-2 rounded-lg border border-slate-700">
          <Server size={16} className="text-green-400" />

          <span className="text-sm text-green-400 font-medium">
            Backend Online
          </span>
        </div>
      </div>
    </header>
  );
}