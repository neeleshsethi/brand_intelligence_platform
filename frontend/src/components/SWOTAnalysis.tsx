interface SWOTAnalysisProps {
  swot: {
    strengths: string[];
    weaknesses: string[];
    opportunities: string[];
    threats: string[];
  };
}

export function SWOTAnalysis({ swot }: SWOTAnalysisProps) {
  const quadrants = [
    { title: 'Strengths', items: swot.strengths, bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-900', icon: '💪' },
    { title: 'Weaknesses', items: swot.weaknesses, bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-900', icon: '⚠️' },
    { title: 'Opportunities', items: swot.opportunities, bg: 'bg-blue-50', border: 'border-blue-200', text: 'text-blue-900', icon: '🎯' },
    { title: 'Threats', items: swot.threats, bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-900', icon: '⚡' },
  ];

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <div className="bg-pfizer-blue text-white px-6 py-4">
        <h3 className="font-semibold text-lg">SWOT Analysis</h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-gray-200">
        {quadrants.map((quadrant, index) => (
          <div
            key={quadrant.title}
            className={`${quadrant.bg} p-6 animate-fade-in`}
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="flex items-center gap-2 mb-4">
              <span className="text-2xl">{quadrant.icon}</span>
              <h4 className={`font-semibold text-lg ${quadrant.text}`}>
                {quadrant.title}
              </h4>
            </div>
            <ul className="space-y-2">
              {quadrant.items.map((item, idx) => (
                <li
                  key={idx}
                  className={`text-sm ${quadrant.text} flex items-start gap-2 animate-slide-in`}
                  style={{ animationDelay: `${(index * 100) + (idx * 50)}ms` }}
                >
                  <span className="mt-1">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
