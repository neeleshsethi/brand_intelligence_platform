import { Loader2, Brain } from 'lucide-react';
import { useEffect, useState } from 'react';

interface LoadingOverlayProps {
  message?: string;
  steps?: string[];
  currentStep?: number;
}

export function LoadingOverlay({ message = "Processing...", steps, currentStep }: LoadingOverlayProps) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (currentStep !== undefined && steps) {
      setProgress(((currentStep + 1) / steps.length) * 100);
    }
  }, [currentStep, steps]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4 shadow-2xl">
        <div className="flex flex-col items-center">
          <div className="relative">
            <Brain className="w-16 h-16 text-pfizer-blue animate-pulse" />
            <Loader2 className="w-6 h-6 text-pfizer-blue-dark animate-spin absolute -bottom-1 -right-1" />
          </div>

          <h3 className="mt-6 text-xl font-semibold text-gray-900">
            AI Agents Thinking...
          </h3>
          <p className="mt-2 text-gray-600 text-center">{message}</p>

          {steps && steps.length > 0 && (
            <div className="mt-6 w-full">
              <div className="mb-2 h-2 w-full bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-pfizer-blue transition-all duration-500 ease-out"
                  style={{ width: `${progress}%` }}
                />
              </div>

              <div className="space-y-2">
                {steps.map((step, index) => (
                  <div
                    key={index}
                    className={`flex items-center text-sm ${
                      index === currentStep
                        ? 'text-pfizer-blue font-medium'
                        : index < (currentStep || 0)
                        ? 'text-green-600'
                        : 'text-gray-400'
                    }`}
                  >
                    <div className="w-5 h-5 mr-2 flex items-center justify-center">
                      {index < (currentStep || 0) ? (
                        <span className="text-green-600">✓</span>
                      ) : index === currentStep ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        <span className="text-gray-300">○</span>
                      )}
                    </div>
                    {step}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
