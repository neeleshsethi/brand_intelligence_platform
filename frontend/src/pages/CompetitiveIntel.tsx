import { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { brandApi } from '../lib/api';
import { LoadingOverlay } from '../components/LoadingOverlay';
import { SWOTAnalysis } from '../components/SWOTAnalysis';
import { PositioningMatrix } from '../components/PositioningMatrix';
import { InsightCard } from '../components/InsightCard';
import { Toast } from '../components/Toast';
import { ArrowLeft, ThumbsUp, ThumbsDown } from 'lucide-react';

export function CompetitiveIntel() {
  const { brandId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const brand = location.state?.brand;

  const [loadingSteps] = useState([
    'Gathering brand data...',
    'Analyzing competitive landscape...',
    'Evaluating market position...',
    'Generating strategic insights...',
    'Complete!'
  ]);
  const [currentStep, setCurrentStep] = useState(0);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);
  const [validatedInsights, setValidatedInsights] = useState<Set<number>>(new Set());
  const [rejectedInsights, setRejectedInsights] = useState<Set<number>>(new Set());

  const analyzeMutation = useMutation({
    mutationFn: () => brandApi.analyzeBrand(brandId!, true),
    onSuccess: () => {
      setCurrentStep(loadingSteps.length - 1);
      setTimeout(() => setCurrentStep(loadingSteps.length), 500);
    },
  });

  useEffect(() => {
    if (!brand) {
      navigate('/');
      return;
    }
    analyzeMutation.mutate();
  }, []);

  useEffect(() => {
    if (analyzeMutation.isPending && currentStep < loadingSteps.length - 1) {
      const timer = setTimeout(() => {
        setCurrentStep(prev => Math.min(prev + 1, loadingSteps.length - 2));
      }, 800);
      return () => clearTimeout(timer);
    }
  }, [analyzeMutation.isPending, currentStep, loadingSteps.length]);

  const handleValidate = (index: number) => {
    setValidatedInsights(prev => new Set(prev).add(index));
    setRejectedInsights(prev => {
      const newSet = new Set(prev);
      newSet.delete(index);
      return newSet;
    });
    setToast({ message: 'Insight validated successfully!', type: 'success' });
  };

  const handleReject = (index: number) => {
    setRejectedInsights(prev => new Set(prev).add(index));
    setValidatedInsights(prev => {
      const newSet = new Set(prev);
      newSet.delete(index);
      return newSet;
    });
    setToast({ message: 'Insight marked for review', type: 'error' });
  };

  if (analyzeMutation.isPending || currentStep < loadingSteps.length) {
    return (
      <LoadingOverlay
        message="Our AI agents are analyzing the competitive landscape..."
        steps={loadingSteps}
        currentStep={currentStep}
      />
    );
  }

  if (analyzeMutation.isError) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Analysis Failed</h2>
          <p className="text-gray-600 mb-4">Unable to analyze brand. Please try again.</p>
          <button
            onClick={() => navigate('/')}
            className="bg-pfizer-blue text-white px-6 py-2 rounded-lg hover:bg-pfizer-blue-dark"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const data = analyzeMutation.data?.data;
  const analysis = data?.analysis;
  const strategy = data?.strategy;

  // Mock positioning data (in real app, calculate from competitors)
  const positioningData = [
    { name: brand?.name, price: 75, efficacy: 89, marketShare: brand?.market_share },
    { name: 'Competitor A', price: 45, efficacy: 65, marketShare: 25 },
    { name: 'Competitor B', price: 60, efficacy: 70, marketShare: 35 },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-pfizer-blue to-pfizer-blue-dark text-white py-6">
        <div className="max-w-7xl mx-auto px-4">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-white hover:text-pfizer-blue-light mb-4 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </button>
          <h1 className="text-3xl font-bold">{brand?.name} - Competitive Intelligence</h1>
          <p className="mt-2 text-white opacity-90">{brand?.company} | {brand?.therapeutic_area}</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Top Section: Positioning & SWOT */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <PositioningMatrix brands={positioningData} highlightBrand={brand?.name} />
          <SWOTAnalysis swot={strategy?.swot} />
        </div>

        {/* Competitive Positioning */}
        <div className="mb-8 animate-fade-in" style={{ animationDelay: '200ms' }}>
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h3 className="font-semibold text-lg text-gray-900 mb-2">Competitive Positioning</h3>
            <p className="text-gray-700 leading-relaxed">{strategy?.competitive_positioning}</p>

            <div className="mt-4">
              <h4 className="font-medium text-gray-900 mb-2">Key Differentiators</h4>
              <ul className="space-y-2">
                {strategy?.key_differentiators?.map((diff: string, idx: number) => (
                  <li
                    key={idx}
                    className="flex items-start gap-2 text-sm text-gray-700 animate-slide-in"
                    style={{ animationDelay: `${300 + idx * 100}ms` }}
                  >
                    <span className="text-pfizer-blue mt-1">✓</span>
                    <span>{diff}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Key Insights */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">AI-Generated Insights</h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {analysis?.key_insights?.slice(0, 3).map((insight: any, idx: number) => (
              <div
                key={idx}
                className="relative animate-fade-in"
                style={{ animationDelay: `${400 + idx * 150}ms` }}
              >
                <InsightCard
                  title={insight.category.charAt(0).toUpperCase() + insight.category.slice(1)}
                  description={insight.description}
                  aiReasoning={`Based on competitive analysis and market data, this insight scores ${(0.85 + idx * 0.02).toFixed(2)} confidence.`}
                  confidenceScore={0.85 + idx * 0.02}
                  impact={insight.impact}
                  category={insight.category}
                  delay={600 + idx * 200}
                />

                {/* Validate/Reject Buttons */}
                <div className="mt-3 flex gap-2">
                  <button
                    onClick={() => handleValidate(idx)}
                    disabled={validatedInsights.has(idx)}
                    className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                      validatedInsights.has(idx)
                        ? 'bg-green-100 text-green-700 border-2 border-green-500'
                        : 'bg-green-50 text-green-700 hover:bg-green-100 border border-green-200'
                    }`}
                  >
                    <ThumbsUp className="w-4 h-4" />
                    {validatedInsights.has(idx) ? 'Validated' : 'Validate'}
                  </button>
                  <button
                    onClick={() => handleReject(idx)}
                    disabled={rejectedInsights.has(idx)}
                    className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                      rejectedInsights.has(idx)
                        ? 'bg-red-100 text-red-700 border-2 border-red-500'
                        : 'bg-red-50 text-red-700 hover:bg-red-100 border border-red-200'
                    }`}
                  >
                    <ThumbsDown className="w-4 h-4" />
                    {rejectedInsights.has(idx) ? 'Rejected' : 'Reject'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Market Summary */}
        <div className="animate-fade-in" style={{ animationDelay: '800ms' }}>
          <div className="bg-gradient-to-r from-pfizer-blue to-pfizer-blue-dark text-white rounded-lg p-6">
            <h3 className="font-semibold text-lg mb-2">Executive Summary</h3>
            <p className="text-white opacity-90 leading-relaxed">{analysis?.summary}</p>
          </div>
        </div>
      </div>

      {/* Toast Notifications */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}
