import { motion, AnimatePresence } from 'framer-motion';
import { X, MapPin, Zap, Factory, Gem, Droplets } from 'lucide-react';
import type { Cluster } from '../api';

interface ClusterDetailProps {
  cluster: Cluster | null;
  onClose: () => void;
}

export default function ClusterDetail({ cluster, onClose }: ClusterDetailProps) {
  return (
    <AnimatePresence>
      {cluster && (
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 30 }}
          transition={{ type: 'spring', stiffness: 400, damping: 30 }}
          className="absolute bottom-6 left-1/2 -translate-x-1/2 w-[600px] max-w-[90vw] glass-card p-5 z-20"
        >
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-xs text-action-orange font-semibold uppercase tracking-wider">
                Cluster Industrial
              </p>
              <h3 className="text-xl font-heading font-bold text-text-primary mt-1">
                {cluster.name}
              </h3>
            </div>
            <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-surface-hover transition-colors">
              <X size={18} className="text-text-muted" />
            </button>
          </div>

          <p className="text-sm text-text-secondary mb-4 leading-relaxed">
            {cluster.description}
          </p>

          <div className="grid grid-cols-2 gap-3">
            <InfoCard
              icon={<MapPin size={14} />}
              label="Porto"
              value={cluster.port}
            />
            <InfoCard
              icon={<Zap size={14} />}
              label="Energia"
              value={cluster.energy_sources.join(', ')}
            />
            <InfoCard
              icon={<Factory size={14} />}
              label="Vocacoes"
              value={cluster.vocations.join(', ')}
            />
            <InfoCard
              icon={<Gem size={14} />}
              label="Minerais"
              value={cluster.critical_minerals.join(', ')}
            />
          </div>

          <div className="mt-3">
            <InfoCard
              icon={<Droplets size={14} />}
              label="Potencial H2"
              value={cluster.hydrogen_potential}
            />
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function InfoCard({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="bg-surface-light/50 rounded-lg p-3 border border-border/50">
      <div className="flex items-center gap-1.5 mb-1">
        <span className="text-action-orange">{icon}</span>
        <span className="text-[10px] font-semibold text-text-muted uppercase tracking-wider">{label}</span>
      </div>
      <p className="text-xs text-text-secondary leading-relaxed">{value}</p>
    </div>
  );
}
