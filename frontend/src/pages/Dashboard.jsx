import AppLayout from "../components/layout/AppLayout";

export default function Dashboard() {
  return (
    <AppLayout title="Dashboard">
      <h2 className="text-2xl font-bold">Welcome to Stress Platform 🚀</h2>

      <p className="text-slate-400 mt-2">
        Your performance testing dashboard starts here.
      </p>
    </AppLayout>
  );
}