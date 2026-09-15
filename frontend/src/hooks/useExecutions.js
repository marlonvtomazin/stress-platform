import { useEffect, useState } from "react";
import { getExecutions } from "../services/executions";

export default function useExecutions() {
  const [executions, setExecutions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchExecutions = async () => {
    try {
      setLoading(true);

      const data = await getExecutions();

      setExecutions(data);
      setError(null);
    } catch (err) {
      setError(err.message || "Failed to load executions.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExecutions();
  }, []);

  return {
    executions,
    loading,
    error,
    refresh: fetchExecutions,
  };
}