import React from 'react';
import { CaptionConfig } from '@/hooks/useCaptions';

interface Props {
  config: CaptionConfig | null;
  onUpdate: (data: Partial<CaptionConfig>) => void;
}

const PRESETS = [
  { id: 'tiktok_modern', name: 'TikTok Modern' },
  { id: 'bold_yellow', name: 'Bold Yellow Glow' },
  { id: 'minimalist', name: 'Minimalist' },
];

export function CaptionStylePanel({ config, onUpdate }: Props) {
  if (!config) return null;

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-bold text-gray-900 mb-2">Caption Styling</h2>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Preset</label>
        <select 
          className="w-full border-gray-300 rounded-md shadow-sm text-sm"
          value={config.preset_name}
          onChange={(e) => onUpdate({ preset_name: e.target.value })}
        >
          {PRESETS.map(p => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Text Color</label>
        <input 
          type="color" 
          className="h-8 w-full cursor-pointer"
          value={config.text_color || '#ffffff'}
          onChange={(e) => onUpdate({ text_color: e.target.value })}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Highlight Color</label>
        <input 
          type="color" 
          className="h-8 w-full cursor-pointer"
          value={config.highlight_color || '#ffff00'}
          onChange={(e) => onUpdate({ highlight_color: e.target.value })}
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Background Color</label>
        <input 
          type="color" 
          className="h-8 w-full cursor-pointer"
          value={config.bg_color || '#000000'}
          onChange={(e) => onUpdate({ bg_color: e.target.value })}
        />
      </div>
    </div>
  );
}
