import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Dashboard } from './pages/Dashboard';
import { CompetitiveIntel } from './pages/CompetitiveIntel';
import { BrandPlanner } from './pages/BrandPlanner';
import './App.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/intel/:brandId" element={<CompetitiveIntel />} />
          <Route path="/planner/:brandId" element={<BrandPlanner />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
