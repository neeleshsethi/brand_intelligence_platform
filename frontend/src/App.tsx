import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Dashboard } from './pages/Dashboard';
import './App.css';

// Lazy load heavy pages for better initial load performance
const CompetitiveIntel = lazy(() => import('./pages/CompetitiveIntel').then(m => ({ default: m.CompetitiveIntel })));
const BrandPlanner = lazy(() => import('./pages/BrandPlanner').then(m => ({ default: m.BrandPlanner })));
const ScenarioModeling = lazy(() => import('./pages/ScenarioModeling').then(m => ({ default: m.ScenarioModeling })));

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// Loading fallback component
const PageLoader = () => (
  <div className="flex items-center justify-center min-h-screen bg-gray-50">
    <div className="text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pfizer-blue mx-auto"></div>
      <p className="mt-4 text-gray-600">Loading...</p>
    </div>
  </div>
);

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/intel/:brandId" element={<CompetitiveIntel />} />
            <Route path="/planner/:brandId" element={<BrandPlanner />} />
            <Route path="/scenario" element={<ScenarioModeling />} />
          </Routes>
        </Suspense>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
