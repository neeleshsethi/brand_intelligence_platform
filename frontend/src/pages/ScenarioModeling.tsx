import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { brandApi } from '../lib/api';
import { LoadingOverlay } from '../components/LoadingOverlay';
import { ArrowLeft, Sparkles, TrendingDown, AlertTriangle, Package } from 'lucide-react';

const EXAMPLE_SCENARIOS = [
  { icon: TrendingDown, text: 'Competitor launches generic', color: 'text-red-500' },
  { icon: AlertTriangle, text: 'New FDA warning for competitor', color: 'text-orange-500' },
  { icon: Package, text: 'Supply chain disruption', color: 'text-blue-500' },
];

export function ScenarioModeling() {
  const navigate = useNavigate();
  const [scenario, setScenario] = useState('');
  const [selectedBrandId, setSelectedBrandId] = useState<string>('');

  const loadingSteps = [
    'Analyzing scenario...',
    'Assessing market impact...',
    'Generating defensive tactics...',
    'Complete!'
  ];
  const [currentStep, setCurrentStep] = useState(0);

  // Fetch brands
  const { data: brandsData } = useQuery({
    queryKey: ['brands'],
    queryFn: async () => (await brandApi.listBrands()).data,
  });

  const brands = brandsData?.filter((b: any) => b.company.includes('Pfizer')) || [];

  const scenarioMutation = useMutation({
    mutationFn: (data: { brandId: string; scenario: string }) =>
      brandApi.analyzeScenario(data.brandId, data.scenario),
    onSuccess: () => {
      setCurrentStep(loadingSteps.length - 1);
      setTimeout(() => setCurrentStep(loadingSteps.length), 500);
    },
  });

  // Simulate loading progress
  useEffect(() => {
    if (scenarioMutation.isPending && currentStep < loadingSteps.length - 1) {
      const timer = setTimeout(() => {
        setCurrentStep(prev => Math.min(prev + 1, loadingSteps.length - 2));
      }, 600);
      return () => clearTimeout(timer);
    }
  }, [scenarioMutation.isPending, currentStep, loadingSteps.length]);

  const handleSubmit = (scenarioText?: string) => {
    const textToUse = scenarioText || scenario;
    if (!textToUse.trim() || !selectedBrandId) return;

    setCurrentStep(0);
    scenarioMutation.mutate({ brandId: selectedBrandId, scenario: textToUse });
  };

  if (scenarioMutation.isPending) {
    return (
      <LoadingOverlay
        message="Our AI agents are analyzing the scenario..."
        steps={loadingSteps}
        currentStep={currentStep}
      />
    );
  }

  const result = scenarioMutation.data?.data?.scenario;

  const getImpactColor = (risk: string) => {
    switch (risk?.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800 border-red-300';
      case 'medium': return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'low': return 'bg-green-100 text-green-800 border-green-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-pfizer-blue to-pfizer-blue-dark text-white py-6">
        <div className="max-w-4xl mx-auto px-4">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-white hover:text-pfizer-blue-light mb-4 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </button>
          <div className="flex items-center gap-3">
            <Sparkles className="w-8 h-8" />
            <h1 className="text-3xl font-bold">Scenario Modeling</h1>
          </div>
          <p className="mt-2 text-white opacity-90">
            Explore what-if scenarios and get AI-powered strategic recommendations
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Brand Selection */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Brand
          </label>
          <select
            value={selectedBrandId}
            onChange={(e) => setSelectedBrandId(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pfizer-blue focus:border-transparent"
          >
            <option value="">Choose a brand...</option>
            {brands.map((brand: any) => (
              <option key={brand.id} value={brand.id}>
                {brand.name} - {brand.therapeutic_area}
              </option>
            ))}
          </select>
        </div>

        {/* Example Scenarios */}
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">Quick Scenarios</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {EXAMPLE_SCENARIOS.map((example, idx) => {
              const Icon = example.icon;
              return (
                <button
                  key={idx}
                  onClick={() => {
                    setScenario(example.text);
                    if (selectedBrandId) {
                      handleSubmit(example.text);
                    }
                  }}
                  disabled={!selectedBrandId}
                  className="flex items-center gap-3 p-4 bg-white border-2 border-gray-200 rounded-lg hover:border-pfizer-blue hover:shadow-md transition-all disabled:opacity-50 disabled:cursor-not-allowed text-left"
                >
                  <Icon className={`w-5 h-5 ${example.color}`} />
                  <span className="text-sm font-medium text-gray-900">{example.text}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Custom Scenario Input */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Or describe your own scenario
          </label>
          <textarea
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            placeholder="What if competitor reduces price by 20%?"
            rows={4}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pfizer-blue focus:border-transparent resize-none"
          />
          <button
            onClick={() => handleSubmit()}
            disabled={!scenario.trim() || !selectedBrandId || scenarioMutation.isPending}
            className="mt-4 w-full bg-pfizer-blue text-white px-6 py-3 rounded-lg hover:bg-pfizer-blue-dark font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <Sparkles className="w-5 h-5" />
            Analyze Scenario
          </button>
        </div>

        {/* Results */}
        {result && (
          <div className="bg-white rounded-lg shadow-lg border border-gray-200 p-6 animate-fade-in">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Analysis Results</h2>

            {/* Impact Assessment */}
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Impact Assessment</h3>
              <div className={`inline-block px-4 py-2 rounded-full border-2 font-semibold ${getImpactColor(result.risk_level)}`}>
                {result.risk_level?.toUpperCase()} RISK
              </div>
            </div>

            {/* Impact Analysis */}
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Impact Analysis</h3>
              <p className="text-gray-800 leading-relaxed">{result.impact_analysis}</p>
            </div>

            {/* Defensive Tactics */}
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Defensive Tactics</h3>
              <div className="space-y-2">
                {result.defensive_tactics?.map((tacticObj: any, idx: number) => (
                  <div key={idx} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                    <div className="flex-shrink-0 w-6 h-6 bg-pfizer-blue text-white rounded-full flex items-center justify-center text-sm font-bold">
                      {idx + 1}
                    </div>
                    <p className="text-gray-800 flex-1">{tacticObj.tactic || tacticObj.description || tacticObj}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommended Action */}
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Recommended Immediate Action</h3>
              <div className="p-4 bg-green-50 border-l-4 border-green-500 rounded">
                <p className="text-gray-800 font-medium">{result.recommended_action}</p>
              </div>
            </div>

            {/* Confidence Score */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-200">
              <span className="text-sm text-gray-600">Confidence Score</span>
              <div className="flex items-center gap-2">
                <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-pfizer-blue rounded-full"
                    style={{ width: `${(result.confidence_score || 0) * 100}%` }}
                  />
                </div>
                <span className="text-sm font-bold text-gray-900">
                  {Math.round((result.confidence_score || 0) * 100)}%
                </span>
              </div>
            </div>

            {/* Try Another Button */}
            <button
              onClick={() => {
                scenarioMutation.reset();
                setScenario('');
              }}
              className="mt-6 w-full border-2 border-pfizer-blue text-pfizer-blue px-6 py-3 rounded-lg hover:bg-pfizer-blue hover:text-white font-medium transition-colors"
            >
              Analyze Another Scenario
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
