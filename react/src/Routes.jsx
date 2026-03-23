import React from "react";
import { BrowserRouter, Routes as RouterRoutes, Route } from "react-router-dom";

import ScrollToTop from "./components/ScrollToTop";
import ErrorBoundary from "./components/ErrorBoundary";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./auth/ProtectedRoute"; // ensure correct import path

import Login from "./pages/login";
import TradesManagement from "./pages/trades-management";
import TradePsychologyEditor from "./pages/trade-psychology-editor";
import Dashboard from "./pages/dashboard";
import AccountsManagement from "./pages/accounts-management";
import Analytics from "./pages/trading-analytics-dashboard";

import TradeCreatePage from "./pages/trades-management/components/TradeCreatePage";
import TradeEditPage from "./pages/trades-management/components/TradeEditPage";
import TradeDetailsPage from "./pages/trades-management/components/TradeDetailsPage";

const Routes = () => {
  return (
    <BrowserRouter>
      <ErrorBoundary>
        <ScrollToTop />

        <RouterRoutes>
          {/* Public */}
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />

          {/* Protected routes nested inside ProtectedRoute */}
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/accounts-management" element={<AccountsManagement />} />
            <Route path="/trades-management" element={<TradesManagement />} />
            <Route path="/trades-management/create" element={<TradeCreatePage />} />
            <Route path="/trades-management/edit/:id" element={<TradeEditPage />} />
            <Route path="/trades-management/details/:id" element={<TradeDetailsPage />} />
            <Route path="/trade-psychology-editor" element={<TradePsychologyEditor />} />
            <Route path="/trading-analytics-dashboard" element={<Analytics />} />
          </Route>

          {/* Fallback */}
          <Route path="*" element={<NotFound />} />
        </RouterRoutes>
      </ErrorBoundary>
    </BrowserRouter>
  );
};

export default Routes;
