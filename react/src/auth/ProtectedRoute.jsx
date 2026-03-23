import React, { useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";
import api from "./api";
import { getToken } from "./auth";

const ProtectedRoute = () => {
  const [loading, setLoading] = useState(true);
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      const token = getToken();
      if (!token) {
        setAuthorized(false);
        setLoading(false);
        return;
      }

      try {
        await api.get("/users/me"); // verify token validity
        setAuthorized(true);
      } catch {
        setAuthorized(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!authorized) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;
