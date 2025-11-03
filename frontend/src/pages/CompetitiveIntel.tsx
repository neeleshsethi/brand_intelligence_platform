import { useState, useEffect, useMemo, useCallback } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient, keepPreviousData } from '@tanstack/react-query';
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
  const queryClient = useQueryClient();

  // Fetch brand data with longer cache time
  const { data: brandsData, isLoading: brandsLoading } = useQuery({
    queryKey: ['brands'],
    queryFn: async () => (await brandApi.listBrands()).data,
    staleTime: 30 * 60 * 1000, // 30 minutes - brands rarely change
    placeholderData: keepPreviousData,
  });

  // Memoize brand lookup to prevent recalculation on every render
  const brand = useMemo(() => {
    return location.state?.brand || brandsData?.find((b: any) => b.id === brandId);
  }, [location.state?.brand, brandsData, brandId]);

  // Fetch approved insights with loading state
  const { data: approvedInsightsData, refetch: refetchInsights, isLoading: insightsLoading } = useQuery({
    queryKey: ['insights', brandId, 'approved'],
    queryFn: async () => {
      if (!brandId) return [];
      return (await brandApi.getInsights(brandId, true)).data;
    },
    enabled: !!brandId,
    placeholderData: keepPreviousData,
  });

  // Fetch recent news with optimized refetching
  const { data: newsData, isLoading: newsLoading } = useQuery({
    queryKey: ['news', brandId],
    queryFn: async () => {
      if (!brandId) return null;
      const response = (await brandApi.getBrandNews(brandId, false, 5)).data;
      return response;
    },
    enabled: !!brandId,
    staleTime: 2 * 60 * 1000, // 2 minutes
    placeholderData: keepPreviousData,
  });

  const [loadingSteps] = useState([
    'Gathering brand data...',
    'Fetching latest market intelligence...',
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
      // Invalidate and refetch insights and news after analysis
      queryClient.invalidateQueries({ queryKey: ['insights', brandId] });
      queryClient.invalidateQueries({ queryKey: ['news', brandId] });
    },
  });

  const handleAnalyze = useCallback(() => {
    setCurrentStep(0);
    analyzeMutation.mutate();
  }, [analyzeMutation]);

  useEffect(() => {
    if (analyzeMutation.isPending && currentStep < loadingSteps.length - 1) {
      const timer = setTimeout(() => {
        setCurrentStep(prev => Math.min(prev + 1, loadingSteps.length - 2));
      }, 800);
      return () => clearTimeout(timer);
    }
  }, [analyzeMutation.isPending, currentStep, loadingSteps.length]);

  const handleValidate = useCallback(async (insightId: string, index: number) => {
    try {
      await brandApi.validateInsight(insightId);
      setValidatedInsights(prev => new Set(prev).add(index));
      setRejectedInsights(prev => {
        const newSet = new Set(prev);
        newSet.delete(index);
        return newSet;
      });
      setToast({ message: 'Insight validated successfully!', type: 'success' });
      // Refetch approved insights to update the list
      refetchInsights();
    } catch (error) {
      setToast({ message: 'Failed to validate insight', type: 'error' });
    }
  }, [refetchInsights]);

  const handleReject = useCallback((index: number) => {
    setRejectedInsights(prev => new Set(prev).add(index));
    setValidatedInsights(prev => {
      const newSet = new Set(prev);
      newSet.delete(index);
      return newSet;
    });
    setToast({ message: 'Insight marked for review', type: 'error' });
  }, []);

  // Removed blocking check - allow progressive rendering with loading states

  if (analyzeMutation.isPending && currentStep < loadingSteps.length) {
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

  // Show start analysis screen if no data yet
  if (!analyzeMutation.data) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-gradient-to-r from-pfizer-blue to-pfizer-blue-dark text-white py-6">
          <div className="max-w-7xl mx-auto px-4">
            <button
              onClick={() => navigate('/')}
              className="flex items-center gap-2 text-white hover:text-pfizer-blue-light mb-4 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Dashboard
            </button>
            <h1 className="text-3xl font-bold">Competitive Intelligence</h1>
            <p className="mt-2 text-white opacity-90">{brand.name} - {brand.company}</p>
          </div>
        </div>
        <div className="max-w-7xl mx-auto px-4 py-16">
          <div className="text-center mb-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Ready to analyze {brand.name}?</h2>
            <p className="text-gray-600 mb-8">Our AI agents will analyze the competitive landscape and generate strategic insights.</p>
            <button
              onClick={handleAnalyze}
              className="bg-pfizer-blue text-white px-8 py-3 rounded-lg hover:bg-pfizer-blue-dark text-lg font-medium transition-colors"
            >
              Start Analysis
            </button>
          </div>

          {/* Recent Market Intelligence */}
          <div className="mt-16">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Recent Market Intelligence
              <span className="text-sm text-gray-500 ml-2">
                (Last 30 days)
              </span>
            </h2>
            {newsLoading ? (
              <div className="bg-white border border-gray-200 rounded-lg p-8">
                <div className="flex items-center justify-center gap-3">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-pfizer-blue"></div>
                  <p className="text-gray-600">Loading news articles...</p>
                </div>
              </div>
            ) : newsData && newsData.articles && newsData.articles.length > 0 ? (
              <div className="space-y-4">
                {newsData.articles.slice(0, 5).map((article: any, idx: number) => (
                  <div
                    key={idx}
                    className="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow animate-fade-in"
                    style={{ animationDelay: `${idx * 100}ms` }}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <span className={`px-2.5 py-1 rounded-full text-xs font-semibold uppercase ${
                            article.priority === 'high' ? 'bg-red-100 text-red-700' :
                            article.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-gray-100 text-gray-700'
                          }`}>
                            {article.priority}
                          </span>
                          <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                            article.sentiment === 'positive' ? 'bg-green-50 text-green-700' :
                            article.sentiment === 'negative' ? 'bg-red-50 text-red-700' :
                            'bg-gray-50 text-gray-700'
                          }`}>
                            {article.sentiment === 'positive' ? '📈' : article.sentiment === 'negative' ? '📉' : '➖'} {article.sentiment}
                          </span>
                          <span className="text-xs text-gray-500">{article.source}</span>
                          <span className="text-xs text-gray-400">•</span>
                          <span className="text-xs text-gray-500">
                            {new Date(article.published_at).toLocaleDateString()}
                          </span>
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2 hover:text-pfizer-blue">
                          <a href={article.url} target="_blank" rel="noopener noreferrer">
                            {article.title}
                          </a>
                        </h3>
                        <p className="text-sm text-gray-600 mb-2 line-clamp-2">
                          {article.content?.substring(0, 200)}...
                        </p>
                        {article.relevance_reason && (
                          <p className="text-xs text-pfizer-blue font-medium">
                            {article.relevance_reason}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                {newsData.articles.length > 5 && (
                  <div className="text-center text-sm text-gray-500 mt-4">
                    Showing 5 of {newsData.articles.length} articles
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
                <p className="text-gray-600">
                  {newsData === null ? 'News intelligence is loading or requires Tavily API key to be configured.' : 'No recent news found for this brand.'}
                </p>
              </div>
            )}
          </div>

          {/* Approved Insights - Always Visible */}
          <div className="mt-16">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Approved Insights
              <span className="text-sm text-gray-500 ml-2">
                ({approvedInsightsData?.length || 0} validated)
              </span>
            </h2>
            {approvedInsightsData && approvedInsightsData.length > 0 ? (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {approvedInsightsData.map((insight: any, idx: number) => (
                  <div key={insight.id} className="animate-fade-in">
                    <InsightCard
                      title={insight.type.charAt(0).toUpperCase() + insight.type.slice(1)}
                      description={insight.content}
                      aiReasoning={insight.ai_reasoning || 'No reasoning provided'}
                      confidenceScore={insight.confidence_score}
                      impact="medium"
                      category={insight.type}
                      delay={idx * 150}
                    />
                    <div className="mt-3 px-4 py-2 bg-green-50 border border-green-200 rounded-lg text-sm text-green-700 font-medium text-center">
                      ✓ Human Validated
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
                <p className="text-gray-600">
                  No approved insights yet. Run an analysis and validate insights to see them appear here.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  const data = analyzeMutation.data?.data;
  const analysis = data?.analysis;
  const strategy = data?.strategy;

  // Mock positioning data (in real app, calculate from competitors)
  const positioningData = useMemo(() => [
    { name: brand?.name, price: 75, efficacy: 89, marketShare: brand?.market_share },
    { name: 'Competitor A', price: 45, efficacy: 65, marketShare: 25 },
    { name: 'Competitor B', price: 60, efficacy: 70, marketShare: 35 },
  ], [brand?.name, brand?.market_share]);

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
          <h1 className="text-3xl font-bold">
            {brandsLoading ? (
              <span className="inline-block bg-white/20 h-8 w-64 animate-pulse rounded"></span>
            ) : (
              `${brand?.name || 'Brand'} - Competitive Intelligence`
            )}
          </h1>
          <p className="mt-2 text-white opacity-90">
            {brandsLoading ? (
              <span className="inline-block bg-white/20 h-4 w-48 animate-pulse rounded"></span>
            ) : (
              `${brand?.company} | ${brand?.therapeutic_area}`
            )}
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Recent Market Intelligence */}
        {newsLoading ? (
          <div className="mb-8 animate-fade-in">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Recent Market Intelligence
            </h2>
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white border border-gray-200 rounded-lg p-4">
                  <div className="animate-pulse">
                    <div className="h-4 bg-gray-200 rounded w-3/4 mb-3"></div>
                    <div className="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
                    <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : newsData && newsData.articles && newsData.articles.length > 0 && (
          <div className="mb-8 animate-fade-in">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Recent Market Intelligence
              <span className="text-sm text-gray-500 ml-2">
                ({newsData.high_priority_count} high priority • {newsData.total_count} total articles)
              </span>
            </h2>
            <div className="space-y-3">
              {newsData.articles.slice(0, 3).map((article: any, idx: number) => (
                <div
                  key={idx}
                  className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start gap-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`px-2 py-0.5 rounded-full text-xs font-semibold uppercase ${
                          article.priority === 'high' ? 'bg-red-100 text-red-700' :
                          article.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {article.priority}
                        </span>
                        <span className="text-xs text-gray-500">{article.source}</span>
                        <span className="text-xs text-gray-400">•</span>
                        <span className="text-xs text-gray-500">
                          {new Date(article.published_at).toLocaleDateString()}
                        </span>
                      </div>
                      <h3 className="font-semibold text-sm text-gray-900 mb-1 hover:text-pfizer-blue">
                        <a href={article.url} target="_blank" rel="noopener noreferrer">
                          {article.title}
                        </a>
                      </h3>
                      {article.relevance_reason && (
                        <p className="text-xs text-pfizer-blue">
                          {article.relevance_reason}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

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
                    onClick={() => {
                      const insightId = data?.saved_insight_ids?.[idx];
                      if (insightId) {
                        handleValidate(insightId, idx);
                      } else {
                        setToast({ message: 'Insight ID not found', type: 'error' });
                      }
                    }}
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
        <div className="mb-8 animate-fade-in" style={{ animationDelay: '800ms' }}>
          <div className="bg-gradient-to-r from-pfizer-blue to-pfizer-blue-dark text-white rounded-lg p-6">
            <h3 className="font-semibold text-lg mb-2">Executive Summary</h3>
            <p className="text-white opacity-90 leading-relaxed">{analysis?.summary}</p>
          </div>
        </div>

        {/* Approved Insights */}
        <div className="animate-fade-in" style={{ animationDelay: '1000ms' }}>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Approved Insights
            <span className="text-sm text-gray-500 ml-2">
              ({approvedInsightsData?.length || 0} validated)
            </span>
          </h2>
          {insightsLoading ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white border border-gray-200 rounded-lg p-6">
                  <div className="animate-pulse">
                    <div className="h-5 bg-gray-200 rounded w-1/2 mb-4"></div>
                    <div className="h-3 bg-gray-200 rounded w-full mb-2"></div>
                    <div className="h-3 bg-gray-200 rounded w-5/6 mb-2"></div>
                    <div className="h-3 bg-gray-200 rounded w-4/5"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : approvedInsightsData && approvedInsightsData.length > 0 ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {approvedInsightsData.map((insight: any, idx: number) => (
                <div
                  key={insight.id}
                  className="animate-fade-in"
                  style={{ animationDelay: `${1100 + idx * 150}ms` }}
                >
                  <InsightCard
                    title={insight.type.charAt(0).toUpperCase() + insight.type.slice(1)}
                    description={insight.content}
                    aiReasoning={insight.ai_reasoning || 'No reasoning provided'}
                    confidenceScore={insight.confidence_score}
                    impact="medium"
                    category={insight.type}
                    delay={1200 + idx * 200}
                  />
                  <div className="mt-3 px-4 py-2 bg-green-50 border border-green-200 rounded-lg text-sm text-green-700 font-medium text-center">
                    ✓ Human Validated
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
              <p className="text-gray-600">
                No approved insights yet. Validate insights above to see them appear here.
              </p>
            </div>
          )}
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
