import { useEffect, useState } from 'react';

interface AnimatedConfidenceProps {
  score: number;
  delay?: number;
  showPercentage?: boolean;
}

export function AnimatedConfidence({ score, delay = 0, showPercentage = true }: AnimatedConfidenceProps) {
  const [displayScore, setDisplayScore] = useState(0);
  const [hasAnimated, setHasAnimated] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setHasAnimated(true);
      let current = 0;
      const increment = score / 50; // 50 steps
      const interval = setInterval(() => {
        current += increment;
        if (current >= score) {
          setDisplayScore(score);
          clearInterval(interval);
        } else {
          setDisplayScore(current);
        }
      }, 20);

      return () => clearInterval(interval);
    }, delay);

    return () => clearTimeout(timer);
  }, [score, delay]);

  const getColor = (value: number) => {
    if (value >= 0.8) return 'bg-green-500';
    if (value >= 0.6) return 'bg-blue-500';
    if (value >= 0.4) return 'bg-yellow-500';
    return 'bg-orange-500';
  };

  const getTextColor = (value: number) => {
    if (value >= 0.8) return 'text-green-700';
    if (value >= 0.6) return 'text-blue-700';
    if (value >= 0.4) return 'text-yellow-700';
    return 'text-orange-700';
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-700">AI Confidence</span>
        {showPercentage && (
          <span className={`text-sm font-bold ${getTextColor(displayScore)} animate-count-up`}>
            {Math.round(displayScore * 100)}%
          </span>
        )}
      </div>
      <div className="relative w-full h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`absolute top-0 left-0 h-full ${getColor(displayScore)} transition-all duration-300 ease-out`}
          style={{
            width: `${hasAnimated ? displayScore * 100 : 0}%`,
            transition: hasAnimated ? 'width 1s ease-out' : 'none',
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-transparent to-white opacity-30"></div>
        </div>
      </div>
    </div>
  );
}
