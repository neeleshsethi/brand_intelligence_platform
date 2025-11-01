import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, Label } from 'recharts';

interface Brand {
  name: string;
  price: number; // 0-100
  efficacy: number; // 0-100
  marketShare?: number;
}

interface PositioningMatrixProps {
  brands: Brand[];
  highlightBrand?: string;
}

export function PositioningMatrix({ brands, highlightBrand }: PositioningMatrixProps) {
  const data = brands.map(brand => ({
    name: brand.name,
    x: brand.price,
    y: brand.efficacy,
    z: brand.marketShare || 20,
  }));

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 animate-fade-in">
      <h3 className="font-semibold text-lg text-gray-900 mb-4">Competitive Positioning</h3>
      <p className="text-sm text-gray-600 mb-6">Price vs. Efficacy Matrix</p>

      <ResponsiveContainer width="100%" height={400}>
        <ScatterChart margin={{ top: 20, right: 20, bottom: 40, left: 40 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis
            type="number"
            dataKey="x"
            name="Price Point"
            domain={[0, 100]}
            stroke="#6B7280"
          >
            <Label value="Price Point (Lower ← → Higher)" position="bottom" offset={0} style={{ fill: '#6B7280', fontSize: 12 }} />
          </XAxis>
          <YAxis
            type="number"
            dataKey="y"
            name="Efficacy"
            domain={[0, 100]}
            stroke="#6B7280"
          >
            <Label value="Efficacy" angle={-90} position="left" style={{ fill: '#6B7280', fontSize: 12 }} />
          </YAxis>
          <Tooltip
            cursor={{ strokeDasharray: '3 3' }}
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload;
                return (
                  <div className="bg-white border border-gray-200 rounded shadow-lg p-3">
                    <p className="font-semibold text-gray-900">{data.name}</p>
                    <p className="text-sm text-gray-600">Price Point: {data.x}</p>
                    <p className="text-sm text-gray-600">Efficacy: {data.y}</p>
                    {data.z && <p className="text-sm text-gray-600">Market Share: {data.z}%</p>}
                  </div>
                );
              }
              return null;
            }}
          />
          <Scatter name="Brands" data={data} fill="#8884d8">
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.name === highlightBrand ? '#0093D0' : '#94A3B8'}
                r={entry.name === highlightBrand ? 12 : 8}
                className="transition-all duration-300"
              />
            ))}
          </Scatter>
        </ScatterChart>
      </ResponsiveContainer>

      <div className="mt-4 flex gap-4 justify-center text-xs text-gray-600">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-pfizer-blue"></div>
          <span>Your Brand</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-slate-400"></div>
          <span>Competitors</span>
        </div>
      </div>
    </div>
  );
}
