import React from 'react';

interface FramingSelectorProps {
  currentMode: string;
  onChangeMode: (mode: string) => void;
}

const MODES = [
  { id: 'ORIGINAL', label: 'Original', description: 'Maintain source aspect ratio' },
  { id: 'FACE_TRACK_9_16', label: '9:16 Vertical', description: 'Auto-track faces for TikTok/Shorts' },
  { id: 'SPLIT_SCREEN', label: 'Split Screen', description: 'Stack videos vertically' }
];

export const FramingSelector: React.FC<FramingSelectorProps> = ({
  currentMode,
  onChangeMode
}) => {
  return (
    <div className="bg-white border rounded-lg p-4">
      <h3 className="font-semibold mb-4 text-gray-900">Framing Mode</h3>
      <div className="space-y-3">
        {MODES.map((mode) => (
          <label 
            key={mode.id} 
            className={`flex items-start p-3 border rounded-lg cursor-pointer transition-colors ${
              currentMode === mode.id ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200 hover:bg-gray-50'
            }`}
          >
            <div className="flex items-center h-5">
              <input
                type="radio"
                name="framingMode"
                value={mode.id}
                checked={currentMode === mode.id}
                onChange={() => onChangeMode(mode.id)}
                className="w-4 h-4 text-indigo-600 border-gray-300 focus:ring-indigo-500"
              />
            </div>
            <div className="ml-3 text-sm">
              <span className={`block font-medium ${currentMode === mode.id ? 'text-indigo-900' : 'text-gray-900'}`}>
                {mode.label}
              </span>
              <span className="block text-gray-500">
                {mode.description}
              </span>
            </div>
          </label>
        ))}
      </div>
    </div>
  );
};
