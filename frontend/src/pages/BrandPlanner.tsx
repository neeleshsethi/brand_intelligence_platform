import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import { brandApi } from '../lib/api';
import { LoadingOverlay } from '../components/LoadingOverlay';
import { PlanSection } from '../components/PlanSection';
import { Toast } from '../components/Toast';
import { ConfettiEffect } from '../components/ConfettiEffect';
import { ArrowLeft, Download, Sparkles } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export function BrandPlanner() {
  const { brandId } = useParams();
  const navigate = useNavigate();
  const [selectedMarket, setSelectedMarket] = useState('US');
  const [strategicGoals, setStrategicGoals] = useState('');
  const [currentStep, setCurrentStep] = useState(0);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);
  const [showConfetti, setShowConfetti] = useState(false);

  const loadingSteps = [
    'Researching market...',
    'Formulating strategy...',
    'Creating projections...',
    'Finalizing plan...',
    'Complete!'
  ];

  // Fetch all brands for dropdown
  const { data: brandsResponse } = useQuery({
    queryKey: ['brands'],
    queryFn: async () => (await brandApi.listBrands()).data,
  });

  const brands = brandsResponse || [];
  const selectedBrand = brands.find((b: any) => b.id === brandId);

  // Generate plan mutation
  const generateMutation = useMutation({
    mutationFn: () => brandApi.generatePlan(brandId!, 5000000, '12 months', strategicGoals || undefined),
    onSuccess: () => {
      setCurrentStep(loadingSteps.length - 1);
      setTimeout(() => {
        setCurrentStep(loadingSteps.length);
        setShowConfetti(true);
        setTimeout(() => setShowConfetti(false), 3000);
      }, 500);
    },
  });

  // Simulate loading progress
  useEffect(() => {
    if (generateMutation.isPending && currentStep < loadingSteps.length - 1) {
      const timer = setTimeout(() => {
        setCurrentStep(prev => Math.min(prev + 1, loadingSteps.length - 2));
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [generateMutation.isPending, currentStep, loadingSteps.length]);

  const handleGenerate = () => {
    setCurrentStep(0);
    generateMutation.mutate();
  };

  const handleExportPDF = () => {
    setToast({ message: 'Plan exported to PDF successfully!', type: 'success' });
  };

  // Mock market share projection data
  const projectionData = [
    { month: 'Jan', marketShare: selectedBrand?.market_share || 42 },
    { month: 'Feb', marketShare: (selectedBrand?.market_share || 42) + 1.2 },
    { month: 'Mar', marketShare: (selectedBrand?.market_share || 42) + 2.1 },
    { month: 'Apr', marketShare: (selectedBrand?.market_share || 42) + 3.5 },
    { month: 'May', marketShare: (selectedBrand?.market_share || 42) + 4.2 },
    { month: 'Jun', marketShare: (selectedBrand?.market_share || 42) + 5.8 },
    { month: 'Jul', marketShare: (selectedBrand?.market_share || 42) + 6.9 },
    { month: 'Aug', marketShare: (selectedBrand?.market_share || 42) + 8.1 },
    { month: 'Sep', marketShare: (selectedBrand?.market_share || 42) + 9.3 },
    { month: 'Oct', marketShare: (selectedBrand?.market_share || 42) + 10.2 },
    { month: 'Nov', marketShare: (selectedBrand?.market_share || 42) + 11.5 },
    { month: 'Dec', marketShare: (selectedBrand?.market_share || 42) + 12.8 },
  ];

  // Show loading while brand data is being fetched
  if (!selectedBrand && !generateMutation.data) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pfizer-blue mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading brand data...</p>
        </div>
      </div>
    );
  }

  if (generateMutation.isPending && currentStep < loadingSteps.length) {
    return (
      <LoadingOverlay
        message="Our AI agents are generating your brand plan..."
        steps={loadingSteps}
        currentStep={currentStep}
      />
    );
  }

  if (generateMutation.isError) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-lg max-w-md">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Error Generating Plan</h2>
          <p className="text-gray-700 mb-4">{(generateMutation.error as any)?.response?.data?.detail || 'An error occurred while generating the brand plan.'}</p>
          <button
            onClick={() => navigate('/')}
            className="w-full bg-pfizer-blue text-white py-2 px-4 rounded-md hover:bg-pfizer-blue-dark transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  const planData = generateMutation.data?.data;

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
          <h1 className="text-3xl font-bold">Brand Plan Generator</h1>
          <p className="mt-2 text-white opacity-90">AI-Powered Strategic Planning</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Form Section */}
        {!planData && (
          <div className="bg-white border border-gray-200 rounded-lg p-8 max-w-2xl mx-auto">
            <div className="flex items-center gap-3 mb-6">
              <Sparkles className="w-6 h-6 text-pfizer-blue" />
              <h2 className="text-2xl font-bold text-gray-900">Generate Strategic Plan</h2>
            </div>

            <div className="space-y-6">
              {/* Brand Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select Brand
                </label>
                <select
                  value={brandId}
                  onChange={(e) => navigate(`/planner/${e.target.value}`)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pfizer-blue focus:border-transparent"
                >
                  {brands.map((brand: any) => (
                    <option key={brand.id} value={brand.id}>
                      {brand.name} - {brand.company}
                    </option>
                  ))}
                </select>
              </div>

              {/* Market Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Target Market
                </label>
                <div className="flex gap-4">
                  {['US', 'EU', 'Japan'].map((market) => (
                    <label key={market} className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="market"
                        value={market}
                        checked={selectedMarket === market}
                        onChange={(e) => setSelectedMarket(e.target.value)}
                        className="w-4 h-4 text-pfizer-blue focus:ring-pfizer-blue"
                      />
                      <span className="text-gray-700">{market}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Strategic Goals */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Strategic Goals
                </label>
                <textarea
                  value={strategicGoals}
                  onChange={(e) => setStrategicGoals(e.target.value)}
                  placeholder="e.g., Increase market share by 5%, Launch in new geography, Defend against generic competition"
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pfizer-blue focus:border-transparent resize-none"
                />
                <p className="mt-1 text-sm text-gray-500">
                  Describe your key objectives to get a tailored strategic plan
                </p>
              </div>

              {/* Brand Info Display */}
              {selectedBrand && (
                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-900 mb-2">{selectedBrand.name}</h3>
                  <p className="text-sm text-gray-600">{selectedBrand.company}</p>
                  <p className="text-sm text-gray-600">{selectedBrand.therapeutic_area}</p>
                  <p className="text-sm text-pfizer-blue font-medium mt-2">
                    Current Market Share: {selectedBrand.market_share}%
                  </p>
                </div>
              )}

              {/* Generate Button */}
              <button
                onClick={handleGenerate}
                disabled={!brandId}
                className="w-full bg-pfizer-blue text-white px-6 py-3 rounded-lg hover:bg-pfizer-blue-dark transition-colors font-medium flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Sparkles className="w-5 h-5" />
                Generate AI-Powered Plan
              </button>
            </div>
          </div>
        )}

        {/* Results Section */}
        {planData && (
          <div className="space-y-6">
            {/* Header with Export */}
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">
                  Strategic Plan: {selectedBrand?.name}
                </h2>
                <p className="text-gray-600 mt-1">Market: {selectedMarket} | Timeframe: 12 months</p>
              </div>
              <button
                onClick={handleExportPDF}
                className="flex items-center gap-2 bg-pfizer-blue text-white px-6 py-3 rounded-lg hover:bg-pfizer-blue-dark transition-colors font-medium"
              >
                <Download className="w-5 h-5" />
                Export to PDF
              </button>
            </div>

            {/* Market Share Projection Chart */}
            <div className="bg-white border border-gray-200 rounded-lg p-6 animate-fade-in">
              <h3 className="font-semibold text-lg text-gray-900 mb-4 flex items-center gap-2">
                Market Share Projection
                <span className="inline-flex items-center gap-1 px-2 py-1 bg-pfizer-blue bg-opacity-10 text-pfizer-blue text-xs font-medium rounded-full">
                  <Sparkles className="w-3 h-3" />
                  AI Projected
                </span>
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={projectionData}>
                  <defs>
                    <linearGradient id="colorShare" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0093D0" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#0093D0" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis dataKey="month" stroke="#6B7280" />
                  <YAxis stroke="#6B7280" label={{ value: 'Market Share (%)', angle: -90, position: 'insideLeft' }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#fff', border: '1px solid #E5E7EB', borderRadius: '8px' }}
                  />
                  <Area
                    type="monotone"
                    dataKey="marketShare"
                    stroke="#0093D0"
                    strokeWidth={3}
                    fillOpacity={1}
                    fill="url(#colorShare)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            {/* Plan Sections */}
            <div className="space-y-4">
              <PlanSection
                title="Executive Summary"
                content={planData.executive_summary || "A comprehensive strategic plan designed to increase market share and strengthen brand positioning through targeted initiatives and measurable outcomes."}
                defaultExpanded={true}
                delay={100}
              />

              <PlanSection
                title="Market Analysis"
                content={[
                  `Current market share: ${selectedBrand?.market_share}%`,
                  `Projected market share (12 months): ${(parseFloat(selectedBrand?.market_share || '0') + 12.8).toFixed(1)}%`,
                  `Total addressable market: $${(Math.random() * 10 + 5).toFixed(1)}B`,
                  `Key growth drivers: Innovation pipeline, market expansion, competitive advantage`
                ]}
                delay={200}
              />

              <PlanSection
                title="Strategic Objectives"
                content={planData.objectives || [
                  "Increase market share by 12+ percentage points within 12 months",
                  "Strengthen brand awareness in key physician segments by 35%",
                  "Launch 2 new indication studies to expand addressable market",
                  "Improve patient adherence rates by 25% through support programs"
                ]}
                delay={300}
              />

              <PlanSection
                title="Tactical Initiatives"
                content={planData.tactics || [
                  "Digital marketing campaign targeting key HCP segments ($1.2M budget)",
                  "Patient education program with multimedia content ($800K)",
                  "Key opinion leader engagement series (15 events, $500K)",
                  "Competitive differentiation study publication ($300K)",
                  "Sales force training on new positioning (Q1-Q2)"
                ]}
                delay={400}
              />

              <PlanSection
                title="Key Performance Indicators"
                content={[
                  "Market Share Growth: +12.8% (baseline: " + selectedBrand?.market_share + "%)",
                  "Brand Awareness: +35% among target HCPs",
                  "Prescription Volume: +28% year-over-year",
                  "Patient Adherence: +25% vs. current rate",
                  "ROI: 3.2x on marketing investment"
                ]}
                delay={500}
              />

              <PlanSection
                title="Budget Allocation"
                content={[
                  "Digital Marketing: $1,200,000 (24%)",
                  "Patient Programs: $800,000 (16%)",
                  "Medical Affairs: $750,000 (15%)",
                  "Sales Enablement: $650,000 (13%)",
                  "Market Research: $500,000 (10%)",
                  "Clinical Studies: $600,000 (12%)",
                  "Contingency: $500,000 (10%)",
                  "Total Budget: $5,000,000"
                ]}
                delay={600}
              />

              <PlanSection
                title="Implementation Timeline"
                content={[
                  "Q1 (Months 1-3): Campaign launch, sales training, baseline measurement",
                  "Q2 (Months 4-6): Patient program rollout, KOL events, mid-point assessment",
                  "Q3 (Months 7-9): Optimization based on data, expansion initiatives",
                  "Q4 (Months 10-12): Final push, results analysis, planning for Year 2"
                ]}
                delay={700}
              />

              <PlanSection
                title="Risk Mitigation"
                content={[
                  "Competitive Response: Monitor competitor activity weekly, prepared counter-tactics",
                  "Regulatory Changes: Legal review of all materials, compliance monitoring",
                  "Budget Constraints: Prioritized initiatives, quarterly reviews for reallocation",
                  "Market Dynamics: Quarterly strategic reviews, agile adjustment process"
                ]}
                delay={800}
              />
            </div>

            {/* Generate New Plan Button */}
            <div className="flex justify-center pt-6">
              <button
                onClick={() => {
                  generateMutation.reset();
                  setCurrentStep(0);
                }}
                className="bg-white border-2 border-pfizer-blue text-pfizer-blue px-6 py-3 rounded-lg hover:bg-pfizer-blue hover:text-white transition-colors font-medium"
              >
                Generate New Plan
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Toast Notifications */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      {/* Confetti Effect */}
      <ConfettiEffect trigger={showConfetti} />
    </div>
  );
}
