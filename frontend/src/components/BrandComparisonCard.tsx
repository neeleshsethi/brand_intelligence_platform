interface BrandComparisonCardProps {
  brands: Array<{
    name: string;
    company: string;
    marketShare: number;
    therapeuticArea: string;
  }>;
}

export function BrandComparisonCard({ brands }: BrandComparisonCardProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <div className="bg-pfizer-blue text-white px-6 py-4">
        <h3 className="font-semibold text-lg">Brand Comparison</h3>
      </div>

      <div className="divide-y divide-gray-200">
        {brands.map((brand, index) => (
          <div key={index} className="p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h4 className="font-semibold text-gray-900 text-lg">{brand.name}</h4>
                <p className="text-sm text-gray-600">{brand.company}</p>
              </div>
              <span className="text-2xl font-bold text-pfizer-blue">
                {brand.marketShare}%
              </span>
            </div>

            <div className="mb-3">
              <div className="flex justify-between items-center mb-1">
                <span className="text-xs text-gray-600">Market Share</span>
              </div>
              <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-pfizer-blue transition-all"
                  style={{ width: `${brand.marketShare}%` }}
                />
              </div>
            </div>

            <div className="text-xs text-gray-600">
              <span className="font-medium">Area:</span> {brand.therapeuticArea}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
