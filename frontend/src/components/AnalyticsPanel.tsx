import { motion, AnimatePresence } from 'framer-motion';
import { X, BarChart3, Zap, Building2, ArrowRightCircle, Globe, Wind } from 'lucide-react';
import { useEffect, useState } from 'react';
import { fetchDecarbonizationMetrics, type Cluster, type DecarbonizationMetrics } from '../api';

interface AnalyticsPanelProps {
  cluster: Cluster | null;
  onClose: () => void;
  onOpenMatchmaker: () => void;
}

export default function AnalyticsPanel({ cluster, onClose, onOpenMatchmaker }: AnalyticsPanelProps) {
  const [metrics, setMetrics] = useState<DecarbonizationMetrics | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!cluster) return;
    setLoading(true);
    fetchDecarbonizationMetrics(cluster.id)
      .then(setMetrics)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [cluster]);

  // Deterministic fallbacks for static bar charts
  const baseValue = cluster ? cluster.name.length * 1.5 : 0;
  
  const industries = cluster?.vocations.map((voc, i) => ({
    name: voc,
    value: Math.max(15, 100 - (i * 25) - (cluster.name.length % 10)),
    color: i === 0 ? 'bg-action-orange' : i === 1 ? 'bg-blue-500' : 'bg-emerald-500'
  })) || [];

  return (
    <AnimatePresence>
      {cluster && (
        <motion.aside
          initial={{ x: '100%' }}
          animate={{ x: 0 }}
          exit={{ x: '100%' }}
          transition={{ type: 'spring', damping: 25, stiffness: 120 }}
          className="w-80 h-full glass border-l border-border flex flex-col z-20 absolute right-0 top-0 shadow-2xl"
        >
          {/* Header */}
          <div className="p-4 border-b border-border flex items-center justify-between bg-surface-light/50">
            <div>
              <h2 className="text-sm font-bold text-action-orange uppercase tracking-wider">Painel Estratégico</h2>
              <h1 className="text-lg font-heading font-bold text-text-primary leading-tight truncate max-w-[220px]">{cluster.name}</h1>
            </div>
            <button onClick={onClose} className="p-1.5 rounded-full hover:bg-white/10 transition-colors text-text-muted">
              <X size={20} />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-4 space-y-5">
            
            {loading ? (
               <div className="flex items-center justify-center py-20 text-text-muted animate-pulse text-sm font-medium">
                 Calculando Geo-Métricas...
               </div>
            ) : (
             <>
              {/* Decarbonization Score Indicator */}
              {metrics && (
                <div className="bg-gradient-to-br from-emerald-900/40 to-teal-900/20 p-4 rounded-2xl border border-emerald-500/30 relative overflow-hidden group shadow-[0_8px_20px_rgba(0,0,0,0.2)]">
                   <div className="absolute -right-2 -top-2 opacity-10 transform group-hover:scale-125 transition-transform duration-700">
                     <Wind size={80} />
                   </div>
                   <div className="flex justify-between items-center mb-2">
                     <span className="text-[11px] font-bold uppercase text-emerald-300 tracking-wider flex items-center gap-1.5">
                        <Globe size={12} /> Score Descarbonização
                     </span>
                     <span className="px-2 py-0.5 bg-emerald-500/20 rounded-full text-[10px] text-emerald-200 border border-emerald-500/30 font-bold">
                        LIVE
                     </span>
                   </div>
                   <div className="flex items-baseline gap-2 mb-1">
                      <h2 className="text-3xl font-black text-white font-heading">{metrics.decarbonization_synergy.score_percentage}%</h2>
                      <span className="text-xs text-emerald-300 font-medium">Eficiência</span>
                   </div>
                   <div className="text-[11px] text-teal-100 opacity-90 leading-tight">
                      Impacto estimado em <strong>{metrics.decarbonization_synergy.carbon_offset_tons_year} toneladas</strong> de CO2 compensadas anualmente.
                   </div>
                </div>
              )}

              {/* Top Metrics Cards */}
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-surface-card p-3 rounded-xl border border-border/50 relative overflow-hidden group">
                  <div className="absolute -right-2 -bottom-2 text-white/5 transform rotate-12 group-hover:scale-110 transition-transform duration-500">
                    <Zap size={64} />
                  </div>
                  <div className="text-[10px] font-bold text-text-muted uppercase mb-1">Rede Proxima</div>
                  <div className="text-xl font-heading font-black text-text-primary">
                    {metrics ? `${metrics.proximity_metrics.nearest_transmission_grid_km} km` : '--'}
                  </div>
                  <div className="text-[10px] text-action-orange flex items-center gap-1">
                     Linha EPE • <span className="font-bold text-[9px]">{metrics?.proximity_metrics.grid_connection_cost_est} Custo</span>
                  </div>
                </div>

                <div className="bg-surface-card p-3 rounded-xl border border-border/50 relative overflow-hidden group">
                   <div className="absolute -right-2 -bottom-2 text-white/5 transform rotate-12 group-hover:scale-110 transition-transform duration-500">
                    <Building2 size={64} />
                  </div>
                  <div className="text-[10px] font-bold text-text-muted uppercase mb-1">Atração Est.</div>
                  <div className="text-xl font-heading font-black text-text-primary">
                    ${metrics ? `${metrics.industrial_simulation.attracted_investment_usd_m}M` : '--'}
                  </div>
                  <div className="text-[10px] text-text-muted flex items-center gap-1">US$ Projetado (ROI)</div>
                </div>
              </div>


            {/* Qualitative text injected from legacy Detail view */}
            <div className="px-1 py-0.5">
               <p className="text-xs text-text-secondary leading-relaxed italic opacity-80">
                  "{cluster.description}"
               </p>
            </div>

            {/* Chart Container - Matches user screenshots design */}
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-xs font-bold text-text-secondary uppercase tracking-wider">
                 <BarChart3 size={14} className="text-action-orange" />
                 <span>Sinergias de Consumo</span>
              </div>

              <div className="bg-surface-card/50 p-3 rounded-xl border border-border/30 space-y-4">
                 {industries.map((item) => (
                   <div key={item.name} className="space-y-1.5">
                      <div className="flex justify-between text-xs">
                         <span className="text-text-secondary font-medium">{item.name}</span>
                         <span className="text-text-primary font-bold">{(item.value * (baseValue/10)).toFixed(1)} MWh</span>
                      </div>
                      <div className="h-2 w-full bg-surface-light rounded-full overflow-hidden flex">
                         <motion.div 
                           initial={{ width: 0 }}
                           animate={{ width: `${item.value}%` }}
                           transition={{ duration: 0.8, delay: 0.2 }}
                           className={`h-full ${item.color} rounded-full`} 
                         />
                      </div>
                   </div>
                 ))}
              </div>
            </div>

            {/* Contextual Synergy Checklist (Infra Integration) */}
            <div className="space-y-2.5">
               <h3 className="text-xs font-bold uppercase text-text-muted px-1">Estrutura Regional</h3>
               <div className="space-y-2">
                  <div className="flex gap-3 items-center bg-surface-light/30 p-2.5 rounded-lg border border-white/5 text-sm">
                     <div className="w-2 h-2 rounded-full bg-emerald-500 shrink-0" />
                     <div className="overflow-hidden">
                       <span className="block font-bold text-text-primary text-xs">Porto:</span>
                       <span className="text-xs text-text-muted truncate block">{cluster.port}</span>
                     </div>
                  </div>

                  <div className="flex gap-3 items-center bg-surface-light/30 p-2.5 rounded-lg border border-white/5 text-sm">
                     <div className="w-2 h-2 rounded-full bg-blue-500 shrink-0" />
                     <div className="overflow-hidden">
                       <span className="block font-bold text-text-primary text-xs">Matriz Predominante:</span>
                       <span className="text-xs text-text-muted truncate block">{cluster.energy_sources.join(', ')}</span>
                     </div>
                  </div>
                  
                  {cluster.critical_minerals.length > 0 && (
                     <div className="flex gap-3 items-center bg-surface-light/30 p-2.5 rounded-lg border border-white/5 text-sm">
                        <div className="w-2 h-2 rounded-full bg-purple-500 shrink-0" />
                        <div className="overflow-hidden">
                          <span className="block font-bold text-text-primary text-xs">Minerais Críticos:</span>
                          <span className="text-xs text-text-muted truncate block">{cluster.critical_minerals.join(', ')}</span>
                        </div>
                     </div>
                  )}
               </div>
            </div>

            {/* Matchmaker CTA */}
            <div className="pt-1">
               <button 
                 onClick={onOpenMatchmaker}
                 className="w-full py-3 px-4 bg-gradient-to-r from-action-orange to-orange-600 text-white rounded-xl font-bold text-xs uppercase tracking-wide flex items-center justify-center gap-2 shadow-lg hover:shadow-action-orange/30 transform hover:-translate-y-0.5 transition-all active:scale-95"
               >
                  <span>Matchmaker AI</span>
                  <ArrowRightCircle size={16} />
               </button>
            </div>
           </>
          )}
          </div>

          {/* Small attribution footer matching official logo references */}
          <div className="p-3 border-t border-border/50 bg-surface/50 flex justify-between items-center">
             <span className="text-[9px] text-text-muted font-medium">Fontes: PID / EPE / ANEEL</span>
             <div className="flex gap-2.5 opacity-50 grayscale">
                <span className="text-[8px] font-bold border border-text-muted px-1 py-0.5 rounded">E+</span>
                <span className="text-[8px] font-bold border border-text-muted px-1 py-0.5 rounded">NZIPL</span>
             </div>
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}

