import { Switch, Route, Router } from "wouter";
import { useHashLocation } from "wouter/use-hash-location";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { AuthProvider, useAuth } from "@/lib/auth";
import Login from "@/pages/login";
import Dashboard from "@/pages/dashboard";

function Gate() {
  const { authed } = useAuth();
  if (!authed) return <Login />;
  return (
    <Router hook={useHashLocation}>
      <Switch>
        <Route path="/" component={Dashboard} />
        <Route component={Dashboard} />
      </Switch>
    </Router>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <AuthProvider>
          <Toaster />
          <Gate />
        </AuthProvider>
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
