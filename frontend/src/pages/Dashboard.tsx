import { useQuery } from '@tanstack/react-query';
import { brandApi } from '../lib/api';
import { useNavigate } from 'react-router-dom';
import { TrendingUp, Loader2, Sparkles } from 'lucide-react';

export function Dashboard() {
  const navigate = useNavigate();
  const { data: brands, isLoading } = useQuery({
    queryKey: ['brands'],
    queryFn: async () => {
      const response = await brandApi.listBrands();
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-pfizer-blue" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-pfizer-blue to-pfizer-blue-dark text-white py-8">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center gap-3 mb-2">
            <Sparkles className="w-8 h-8" />
            <h1 className="text-3xl font-bold">Pfizer AI Brand Planning</h1>
          </div>
          <p className="mt-2 text-white opacity-90">AI-powered brand intelligence and strategy</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Your Brands</h2>
            <p className="text-gray-600 mt-1">Select a brand to analyze</p>
          </div>
          <button
            onClick={() => navigate('/scenario')}
            className="bg-gradient-to-r from-purple-600 to-purple-700 text-white px-6 py-3 rounded-lg hover:from-purple-700 hover:to-purple-800 font-medium transition-all shadow-md hover:shadow-lg flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            Scenario Modeling
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {brands?.filter((brand: any) => brand.company.includes('Pfizer')).map((brand: any) => (
            <div
              key={brand.id}
              className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900">{brand.name}</h3>
                  <p className="text-gray-600 text-sm mt-1">{brand.company}</p>
                  <p className="text-xs text-gray-500 mt-1">{brand.therapeutic_area}</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-pfizer-blue">{brand.market_share}%</div>
                  <div className="text-xs text-gray-600">Market Share</div>
                </div>
              </div>

              <div className="mb-4">
                <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-pfizer-blue"
                    style={{ width: `${brand.market_share}%` }}
                  />
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => navigate(`/intel/${brand.id}`, { state: { brand } })}
                  className="flex-1 bg-pfizer-blue hover:bg-pfizer-blue-dark text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                >
                  <TrendingUp className="w-4 h-4" />
                  Analyze Brand
                </button>
                <button
                  onClick={() => navigate(`/planner/${brand.id}`, { state: { brand } })}
                  className="flex-1 border border-pfizer-blue text-pfizer-blue hover:bg-pfizer-blue hover:text-white px-4 py-2 rounded-lg font-medium transition-colors"
                >
                  Create Plan
                </button>
              </div>
            </div>
          ))}
        </div>

        {brands && (
          <div className="mt-6 text-center">
            <p className="text-gray-600 text-sm">
              Showing {brands.filter((b: any) => b.company.includes('Pfizer')).length} of {brands.length} brands
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
