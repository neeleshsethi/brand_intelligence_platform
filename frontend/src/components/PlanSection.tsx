import { ChevronDown, ChevronUp, Sparkles } from 'lucide-react';
import { useState } from 'react';

interface PlanSectionProps {
  title: string;
  content: string | string[];
  defaultExpanded?: boolean;
  delay?: number;
}

export function PlanSection({ title, content, defaultExpanded = false, delay = 0 }: PlanSectionProps) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  const renderContent = () => {
    if (Array.isArray(content)) {
      return (
        <ul className="space-y-2">
          {content.map((item, idx) => (
            <li key={idx} className="flex items-start gap-2 text-gray-700">
              <span className="text-pfizer-blue mt-1">•</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      );
    }
    return <p className="text-gray-700 leading-relaxed whitespace-pre-line">{content}</p>;
  };

  return (
    <div
      className="bg-white border border-gray-200 rounded-lg overflow-hidden animate-fade-in"
      style={{ animationDelay: `${delay}ms` }}
    >
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <h3 className="font-semibold text-lg text-gray-900">{title}</h3>
          <span className="inline-flex items-center gap-1 px-2 py-1 bg-pfizer-blue bg-opacity-10 text-pfizer-blue text-xs font-medium rounded-full">
            <Sparkles className="w-3 h-3" />
            AI Generated
          </span>
        </div>
        {isExpanded ? (
          <ChevronUp className="w-5 h-5 text-gray-400" />
        ) : (
          <ChevronDown className="w-5 h-5 text-gray-400" />
        )}
      </button>

      {isExpanded && (
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 animate-slide-in">
          {renderContent()}
        </div>
      )}
    </div>
  );
}
