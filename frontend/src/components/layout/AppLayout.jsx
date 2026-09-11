import Sidebar from "./Sidebar";
import Header from "./Header";

export default function AppLayout({ title, children }) {
  return (
    <div className="flex h-screen bg-slate-950 text-white">
      <Sidebar />

      <div className="flex flex-col flex-1 min-w-0">
        <Header title={title} />

        <main className="flex-1 overflow-y-auto bg-slate-950 p-8">
          {children}
        </main>
      </div>
    </div>
  );
}