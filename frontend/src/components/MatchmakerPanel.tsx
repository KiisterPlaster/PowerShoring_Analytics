import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Loader2, MapPin, Zap, Truck, Users, Scale, X } from 'lucide-react';
import { runMatchmaker, type MatchmakerResponse } from '../api';

interface MatchmakerPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function MatchmakerPanel({ isOpen, onClose }: MatchmakerPanelProps) {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState<MatchmakerResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (query.length < 10) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await runMatchmaker(query);
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao conectar com a IA');
    } finally {
      setLoading(false);
    }
  };

  const suggestions = [
    'Quero instalar uma planta de quimica verde para producao de e-metanol no Brasil',
    'Represento um fundo de investimentos e procuro o melhor local para uma fabrica de aco verde',
    'Estou buscando uma regiao para instalar uma usina de biometano a partir de residuos agropecuarios',
    'Preciso de um local para uma fabrica de polissilicio fotovoltaico com energia limpa e barata',
  ];

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ x: '100%' }}
          animate={{ x: 0 }}
          exit={{ x: '100%' }}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          className="fixed top-0 right-0 w-[480px] h-full glass z-50 flex flex-col shadow-2xl"
        >
          {/* Header */}
          <div className="p-5 border-b border-border flex items-center justify-between">
            <div>
              <h2 className="text-xl font-heading font-bold text-text-primary">
                Matchmaker IA
              </h2>
              <p className="text-xs text-text-muted mt-1">
                Recomendacao inteligente de clusters industriais
              </p>
            </div>
            <button onClick={onClose} className="p-2 rounded-lg hover:bg-surface-hover transition-colors">
              <X size={20} className="text-text-secondary" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-5 space-y-4">
            {/* Input */}
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">
                Descreva seu projeto industrial:
              </label>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ex: Quero instalar uma fabrica de aco verde usando hidrogenio como redutor..."
                className="w-full h-28 bg-surface-light border border-border rounded-xl p-4 text-sm text-text-primary placeholder-text-muted resize-none focus:outline-none focus:border-action-orange/50 transition-colors"
              />
              <button
                onClick={handleSubmit}
                disabled={loading || query.length < 10}
                className="mt-3 w-full py-3 bg-action-orange hover:bg-action-orange/90 disabled:bg-surface-hover disabled:text-text-muted rounded-xl text-sm font-semibold text-white flex items-center justify-center gap-2 transition-all"
              >
                {loading ? (
                  <>
                    <Loader2 size={16} className="animate-spin" />
                    Analisando com IA...
                  </>
                ) : (
                  <>
                    <Send size={16} />
                    Encontrar Cluster Ideal
                  </>
                )}
              </button>
            </div>

            {/* Suggestions */}
            {!result && !loading && (
              <div>
                <p className="text-xs font-medium text-text-muted mb-2">Sugestoes:</p>
                <div className="space-y-2">
                  {suggestions.map((s, i) => (
                    <button
                      key={i}
                      onClick={() => setQuery(s)}
                      className="w-full text-left text-xs p-3 rounded-lg bg-surface-light/50 border border-border/50 text-text-secondary hover:border-action-orange/30 hover:text-text-primary transition-all"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Error */}
            {error && (
              <div className="p-4 bg-wine/20 border border-wine/40 rounded-xl text-sm text-peach">
                {error}
              </div>
            )}

            {/* Result */}
            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-4"
              >
                {/* Recommended cluster */}
                <div className="glass-card p-5">
                  <div className="flex items-start gap-3 mb-3">
                    <div className="p-2 bg-action-orange/20 rounded-lg">
                      <MapPin size={20} className="text-action-orange" />
                    </div>
                    <div>
                      <p className="text-xs text-text-muted">Cluster Recomendado</p>
                      <h3 className="text-lg font-heading font-bold text-action-orange">
                        {result.cluster_recommended}
                      </h3>
                      <p className="text-sm text-text-secondary mt-1">{result.location}</p>
                    </div>
                  </div>
                </div>

                {/* Details */}
                <div className="glass-card p-4 space-y-4">
                  <DetailSection icon={<Scale size={16} />} title="Justificativa" content={result.justification} />
                  <DetailSection icon={<Zap size={16} />} title="Perfil Energetico" content={result.energy_profile} />
                  <DetailSection icon={<Truck size={16} />} title="Logistica" content={result.logistics} />
                  <DetailSection icon={<Users size={16} />} title="Impacto Socioeconomico" content={result.socioeconomic_impact} />
                  <DetailSection icon={<Scale size={16} />} title="Transicao Justa" content={result.transition_justa} />
                </div>

                <p className="text-[10px] text-text-muted text-center">
                  Modelo: {result.raw_model} | Dados: Atlas do Futuro Industrial 2025
                </p>
              </motion.div>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function DetailSection({ icon, title, content }: { icon: React.ReactNode; title: string; content: string }) {
  return (
    <div>
      <div className="flex items-center gap-2 mb-1">
        <span className="text-action-orange">{icon}</span>
        <h4 className="text-sm font-semibold text-text-primary">{title}</h4>
      </div>
      <p className="text-xs text-text-secondary leading-relaxed pl-6">{content}</p>
    </div>
  );
}
