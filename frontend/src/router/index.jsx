import { createBrowserRouter } from "react-router-dom";

import Dashboard from "../pages/Dashboard";
import Executions from "../pages/Executions";
import ExecutionDetails from "../pages/ExecutionDetails";
import RunTest from "../pages/RunTest";
import Reports from "../pages/Reports";
import Scripts from "../pages/Scripts";
import Settings from "../pages/Settings";

export const router = createBrowserRouter([
  { path: "/", element: <Dashboard /> },
  { path: "/run", element: <RunTest /> },
  { path: "/executions", element: <Executions /> },
  { path: "/executions/:executionId", element: <ExecutionDetails /> },
  { path: "/reports", element: <Reports /> },
  { path: "/scripts", element: <Scripts /> },
  { path: "/settings", element: <Settings /> },
]);