import { Brain, TrendingUp, AlertTriangle } from 'lucide-react';
import { AnimatedConfidence } from './AnimatedConfidence';

interface InsightCardProps {
  title: string;
  description: string;
  aiReasoning?: string;
  confidenceScore?: number;
  impact?: 'high' | 'medium' | 'low';
  category?: string;
  delay?: number;
}

export function InsightCard({
  title,
  description,
  aiReasoning,
  confidenceScore,
  impact,
  category,
  delay = 0
}: InsightCardProps) {
  const getImpactColor = (level?: string) => {
    switch (level) {
      case 'high': return 'text-red-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          {category === 'opportunity' && <TrendingUp className="w-5 h-5 text-green-600" />}
          {category === 'threat' && <AlertTriangle className="w-5 h-5 text-red-600" />}
          {category === 'trend' && <Brain className="w-5 h-5 text-pfizer-blue" />}
          <h3 className="font-semibold text-gray-900">{title}</h3>
        </div>
        {impact && (
          <span className={`text-xs font-medium ${getImpactColor(impact)} uppercase`}>
            {impact} impact
          </span>
        )}
      </div>

      <p className="text-gray-700 mb-4 text-sm leading-relaxed">{description}</p>

      {confidenceScore !== undefined && (
        <div className="mb-3">
          <AnimatedConfidence score={confidenceScore} delay={delay} />
        </div>
      )}

      {aiReasoning && (
        <details className="mt-3 text-xs">
          <summary className="cursor-pointer text-pfizer-blue hover:text-pfizer-blue-dark font-medium flex items-center gap-1">
            <Brain className="w-3 h-3" />
            View AI Reasoning
          </summary>
          <p className="mt-2 text-gray-600 bg-gray-50 p-3 rounded border border-gray-200">
            {aiReasoning}
          </p>
        </details>
      )}
    </div>
  );
}
