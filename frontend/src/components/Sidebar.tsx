import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Layers, ChevronDown, ChevronRight, Loader2 } from 'lucide-react';
import { fetchLayerCatalog, type LayerInfo } from '../api';

interface SidebarProps {
  activeLayers: string[];
  onToggleLayer: (layerKey: string) => void;
}

export default function Sidebar({ activeLayers, onToggleLayer }: SidebarProps) {
  const [layers, setLayers] = useState<LayerInfo[]>([]);
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set(['Energia', 'Logistica']));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLayerCatalog()
      .then((res) => setLayers(res.layers))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const categories = [...new Set(layers.map((l) => l.category))];

  const toggleCategory = (cat: string) => {
    setExpandedCategories((prev) => {
      const next = new Set(prev);
      next.has(cat) ? next.delete(cat) : next.add(cat);
      return next;
    });
  };

  return (
    <aside className="w-72 h-full glass flex flex-col overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center gap-2 mb-1">
          <Layers size={20} className="text-action-orange" />
          <h2 className="text-lg font-heading font-bold text-text-primary">Camadas</h2>
        </div>
        <p className="text-xs text-text-muted">
          {activeLayers.length} ativa{activeLayers.length !== 1 ? 's' : ''} | Dados reais PID
        </p>
      </div>

      {/* Layer list */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="animate-spin text-action-orange" size={24} />
          </div>
        ) : (
          categories.map((cat) => (
            <div key={cat} className="mb-1">
              <button
                onClick={() => toggleCategory(cat)}
                className="w-full flex items-center gap-2 py-2 px-3 rounded-lg text-sm font-semibold text-text-secondary hover:bg-surface-hover transition-colors"
              >
                {expandedCategories.has(cat) ? (
                  <ChevronDown size={14} />
                ) : (
                  <ChevronRight size={14} />
                )}
                {cat}
                <span className="ml-auto text-xs text-text-muted">
                  {layers.filter((l) => l.category === cat).length}
                </span>
              </button>

              <AnimatePresence>
                {expandedCategories.has(cat) && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                    className="overflow-hidden"
                  >
                    {layers
                      .filter((l) => l.category === cat)
                      .map((layer) => {
                        const isActive = activeLayers.includes(layer.layer_key);
                        return (
                          <button
                            key={layer.layer_key}
                            onClick={() => onToggleLayer(layer.layer_key)}
                            className={`w-full flex items-center gap-3 py-2 px-4 rounded-lg text-sm transition-all duration-200 ${
                              isActive
                                ? 'bg-action-orange/15 text-action-orange border border-action-orange/30'
                                : 'text-text-secondary hover:bg-surface-hover'
                            }`}
                          >
                            <span className="text-base">{layer.icon}</span>
                            <span className="truncate">{layer.display_name}</span>
                            {isActive && (
                              <span className="ml-auto w-2 h-2 rounded-full bg-action-orange pulse-glow" />
                            )}
                          </button>
                        );
                      })}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))
        )}
      </div>

      {/* Footer */}
      <div className="p-3 border-t border-border">
        <p className="text-[10px] text-text-muted text-center">
          Fonte: PID ArcGIS FeatureServer (real-time)
        </p>
      </div>
    </aside>
  );
}
