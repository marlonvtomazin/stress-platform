import {
  LayoutDashboard,
  Rocket,
  History,
  FileText,
  FolderOpen,
  Settings,
  Activity,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const menuItems = [
  {
    title: "Dashboard",
    icon: LayoutDashboard,
    path: "/",
  },
  {
    title: "Run Test",
    icon: Rocket,
    path: "/run",
  },
  {
    title: "Executions",
    icon: History,
    path: "/executions",
  },
  {
    title: "Reports",
    icon: FileText,
    path: "/reports",
  },
  {
    title: "Scripts",
    icon: FolderOpen,
    path: "/scripts",
  },
  {
    title: "Settings",
    icon: Settings,
    path: "/settings",
  },
];

export default function Sidebar() {
  return (
    <aside className="w-56 h-screen bg-slate-950 border-r border-slate-800 flex flex-col">
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-5 border-b border-slate-800">
        <div className="bg-blue-600 p-2 rounded-lg">
          <Activity size={22} color="white" />
        </div>

        <div>
          <h1 className="text-white font-bold text-lg">
            Stress Platform
          </h1>

          <p className="text-slate-400 text-xs">
            v1.0-alpha
          </p>
        </div>
      </div>

      {/* Menu */}
      <nav className="flex-1 p-3 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200
                ${
                  isActive
                    ? "bg-blue-600 text-white"
                    : "text-slate-400 hover:bg-slate-900 hover:text-white"
                }`
              }
            >
              <Icon size={20} />
              <span className="text-sm font-medium">
                {item.title}
              </span>
            </NavLink>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-slate-800">
        <p className="text-xs text-slate-500">
          Developed by Marlon Tomazin
        </p>
      </div>
    </aside>
  );
}