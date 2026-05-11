import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LineChart, Line, AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  Cell
} from 'recharts';
import {
  TrendingUp, BarChart2, Globe, Zap, Leaf, Table as TableIcon,
  ChevronRight, Filter, RefreshCcw, AlertCircle, Download,
  Factory, ShieldCheck, Cpu, Gauge, Layers
} from 'lucide-react';

import { ibgeService } from '../services/ibgeService';
import { internationalService } from '../services/internationalService';
import { energyService } from '../services/energyService';

// --- Master Mock Data matching image reference aesthetic ---
const INDUSTRY_CONSUMPTION_DATA = [
  { name: 'Alumínio', consumo: 12.4, color: '#10b981' },
  { name: 'Aço', consumo: 8.2, color: '#0ea5e9' },
  { name: 'Química', consumo: 5.1, color: '#6366f1' },
  { name: 'Papel/Celul.', consumo: 3.5, color: '#f59e0b' },
  { name: 'Cimento', consumo: 1.8, color: '#ec4899' },
  { name: 'Vidro', consumo: 0.9, color: '#8b5cf6' },
];

const CROSS_COMPARISON_DATA = [
  { subject: 'Energia Renovável', 'Camaçari': 85, 'Pecém': 95, 'Sudeste': 70 },
  { subject: 'Logística Portuária', 'Camaçari': 90, 'Pecém': 85, 'Sudeste': 92 },
  { subject: 'Baixo Risco Ambiental', 'Camaçari': 75, 'Pecém': 90, 'Sudeste': 65 },
  { subject: 'Cadeia de Suprimentos', 'Camaçari': 92, 'Pecém': 60, 'Sudeste': 98 },
  { subject: 'Infraestrutura de H2', 'Camaçari': 80, 'Pecém': 95, 'Sudeste': 60 },
];

type TopTab = 'cross_analytics' | 'indicators';

export default function DataDashboard() {
  const [topTab, setTopTab] = useState<TopTab>('cross_analytics');
  const [activeTab, setActiveTab] = useState<'socioeconomic' | 'energy' | 'environmental' | 'international'>('socioeconomic');
  const [selectedSource, setSelectedSource] = useState('pib');

  // React Queries for Tab 2
  const { data: pibData } = useQuery({
    queryKey: ['ibge', 'pib'],
    queryFn: () => ibgeService.fetchPib(),
    enabled: topTab === 'indicators' && activeTab === 'socioeconomic' && selectedSource === 'pib',
  });

  let chartData2: any[] = [];
  if (pibData && selectedSource === 'pib') {
    chartData2 = pibData.data.map(d => ({ label: d.D3N || '?', value: parseFloat(d.V || '0'), unit: 'BRL' })).reverse();
  }

  return (
    <div className="flex flex-col w-full min-h-full bg-black/20 text-slate-100 p-8 space-y-6 overflow-x-hidden backdrop-blur-[2px]">

      {/* MASTER HEADER WITH VIEW TOGGLE */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-4 border-b border-slate-800/60 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-emerald-500/10 rounded-xl border border-emerald-500/20">
            <Gauge className="text-emerald-400 w-7 h-7" />
          </div>
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent tracking-tight">
              Inteligência Geoespacial
            </h1>
            <p className="text-slate-400 text-sm">Plataforma de Cruzamento e Correlação de Dados Ambientais e Industriais.</p>
          </div>
        </div>

        <div className="flex p-1 bg-slate-900/80 border border-slate-800 rounded-xl backdrop-blur">
          <button
            onClick={() => setTopTab('cross_analytics')}
            className={`px-6 py-2.5 text-sm font-bold rounded-lg transition-all flex items-center gap-2 ${topTab === 'cross_analytics' ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <Layers size={16} /> Cruzamento PowerShoring
          </button>
          <button
            onClick={() => setTopTab('indicators')}
            className={`px-6 py-2.5 text-sm font-bold rounded-lg transition-all flex items-center gap-2 ${topTab === 'indicators' ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <TrendingUp size={16} /> Indicadores Nacionais
          </button>
        </div>
      </div>

      <AnimatePresence mode="wait">
        {topTab === 'cross_analytics' ? (
          <motion.div
            key="cross"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="flex flex-col space-y-6"
          >
            {/* KPI ROW INSPIRADO NA IMAGEM 4 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <KPICard title="Consumo Total Projetado" value="30.4 M" unit="MWh/ano" icon={<Zap className="text-amber-400" />} color="amber" />
              <KPICard title="Total de Indústrias Ativas" value="326" unit="unidades" icon={<Factory className="text-cyan-400" />} color="cyan" />
              <KPICard title="Fator Médio Decarbonização" value="89.4%" unit="Score ESG" icon={<ShieldCheck className="text-emerald-400" />} color="emerald" />
              <KPICard title="Potencial Energético Ócio" value="12.1 GW" unit="Capacidade" icon={<Cpu className="text-fuchsia-400" />} color="fuchsia" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

              {/* LEFT: A ESTRELA INOVADORA (CRUZAMENTO RADAR) */}
              <div className="lg:col-span-5 bg-slate-900/40 border border-slate-800/80 backdrop-blur-xl rounded-2xl p-6 flex flex-col relative overflow-hidden">
                <div className="absolute -right-24 -top-24 w-64 h-64 bg-emerald-500/10 blur-[100px] rounded-full pointer-events-none" />
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-lg font-bold flex items-center gap-2 text-slate-100">
                      <Globe className="text-emerald-400" size={18} /> Análise Comparativa de Clusters
                    </h3>
                    <p className="text-xs text-slate-400 mt-1">Cruzamento multivariado de prontidão e risco.</p>
                  </div>
                </div>

                <div className="flex-1 min-h-[350px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart cx="50%" cy="50%" outerRadius="80%" data={CROSS_COMPARISON_DATA}>
                      <PolarGrid stroke="#334155" />
                      <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                      <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} stroke="#334155" />
                      <Radar name="Pecém (CE)" dataKey="Pecém" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
                      <Radar name="Camaçari (BA)" dataKey="Camaçari" stroke="#0ea5e9" fill="#0ea5e9" fillOpacity={0.3} />
                      <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }} />
                      <Legend />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* RIGHT: O GRÁFICO DE CONSUMO PEDIDO (REFERENCIA IMAGEM 4) */}
              <div className="lg:col-span-7 bg-slate-900/40 border border-slate-800/80 backdrop-blur-xl rounded-2xl p-6 flex flex-col">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-lg font-bold flex items-center gap-2 text-slate-100">
                      <BarChart2 className="text-cyan-400" size={18} /> Consumo Elétrico por Tipo de Indústria
                    </h3>
                    <p className="text-xs text-slate-400 mt-1">Demandas agregadas em base instalada nacional.</p>
                  </div>
                </div>

                <div className="flex-1 min-h-[350px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={INDUSTRY_CONSUMPTION_DATA} layout="vertical" margin={{ left: 20, right: 20 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                      <XAxis type="number" stroke="#64748b" tick={{ fontSize: 12 }} unit="M" />
                      <YAxis dataKey="name" type="category" stroke="#64748b" width={80} tick={{ fontSize: 12, fill: '#e2e8f0', fontWeight: 500 }} />
                      <Tooltip
                        cursor={{ fill: '#ffffff08' }}
                        formatter={(v: any) => [`${v} MWh`, 'Consumo']}
                        contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }}
                      />
                      <Bar dataKey="consumo" radius={[0, 4, 4, 0]} barSize={30}>
                        {INDUSTRY_CONSUMPTION_DATA.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>

            {/* BOTTOM GRID: ENVIRONMENTAL RISK VS INDUSTRIAL POTENTIAL */}
            <div className="bg-slate-900/40 border border-slate-800/80 rounded-2xl overflow-hidden">
              <div className="px-6 py-4 border-b border-slate-800 bg-slate-900/60 flex items-center justify-between">
                <h3 className="font-bold text-slate-200 flex items-center gap-2"><Leaf size={18} className="text-emerald-400" /> Cruzamento Ambiental: Distância para Terras Indígenas & Unidades de Conservação</h3>
                <span className="text-xs bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-full font-medium border border-emerald-500/20">Correlação Geoespacial</span>
              </div>
              <div className="overflow-x-auto p-6">
                <table className="w-full text-left text-sm">
                  <thead className="text-slate-400 uppercase text-xs tracking-wider border-b border-slate-800">
                    <tr>
                      <th className="pb-3">Cluster</th>
                      <th className="pb-3">Terras Indígenas Próximas</th>
                      <th className="pb-3">Conflito de Área</th>
                      <th className="pb-3 text-right">Status de Licenciamento</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 text-slate-200">
                    <tr className="hover:bg-white/[0.02]">
                      <td className="py-4 font-medium">Cluster Norte (PA)</td>
                      <td className="py-4">4 Unidades (&lt; 50km)</td>
                      <td className="py-4 text-amber-400">Moderado</td>
                      <td className="py-4 text-right"><span className="px-2 py-1 rounded bg-amber-500/20 text-amber-400 text-xs">Atenção Exigida</span></td>
                    </tr>
                    <tr className="hover:bg-white/[0.02]">
                      <td className="py-4 font-medium">Cluster Nordeste (CE)</td>
                      <td className="py-4">0 Unidades (&lt; 50km)</td>
                      <td className="py-4 text-emerald-400">Mínimo</td>
                      <td className="py-4 text-right"><span className="px-2 py-1 rounded bg-emerald-500/20 text-emerald-400 text-xs">Livre / Facilitado</span></td>
                    </tr>
                    <tr className="hover:bg-white/[0.02]">
                      <td className="py-4 font-medium">Cluster Sudeste (MG)</td>
                      <td className="py-4">1 Unidade (&lt; 50km)</td>
                      <td className="py-4 text-emerald-400">Mínimo</td>
                      <td className="py-4 text-right"><span className="px-2 py-1 rounded bg-emerald-500/20 text-emerald-400 text-xs">Livre / Facilitado</span></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </motion.div>
        ) : (
          /* OLD MACRO VIEW PRESERVED AS TAB 2 */
          <motion.div
            key="indicators"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="flex flex-col gap-6"
          >
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              <div className="lg:col-span-1 bg-slate-900 border border-slate-800 rounded-xl p-4 h-fit">
                <h4 className="text-slate-400 text-xs uppercase font-bold tracking-wider mb-4">Dataset Principal</h4>
                <div className="flex flex-col gap-2">
                  <SourceBtn icon={<BarChart2 />} label="Socioeconômico (PIB)" active={activeTab === 'socioeconomic'} onClick={() => setActiveTab('socioeconomic')} />
                  <SourceBtn icon={<Zap />} label="Matriz Energética" active={activeTab === 'energy'} onClick={() => setActiveTab('energy')} />
                  <SourceBtn icon={<Globe />} label="Benchmarks Globais" active={activeTab === 'international'} onClick={() => setActiveTab('international')} />
                </div>
              </div>

              <div className="lg:col-span-3 bg-slate-900 border border-slate-800 rounded-xl p-6 min-h-[400px] flex flex-col">
                <div className="flex justify-between items-center mb-6">
                  <h3 className="text-xl font-bold text-white">Evolução Temporal</h3>
                </div>
                {chartData2.length > 0 ? (
                  <ResponsiveContainer width="100%" height={350}>
                    <AreaChart data={chartData2}>
                      <defs>
                        <linearGradient id="cVal" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                          <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                      <XAxis dataKey="label" stroke="#64748b" />
                      <YAxis stroke="#64748b" tickFormatter={(v) => v.toLocaleString('pt-BR', { notation: 'compact' })} />
                      <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none' }} />
                      <Area type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} fill="url(#cVal)" />
                    </AreaChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="flex-1 flex flex-col items-center justify-center text-slate-500 italic">
                    <RefreshCcw size={40} className="animate-spin text-slate-700 mb-2" />
                    Carregando série temporal...
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

// Reusable Component for KPIs
function KPICard({ title, value, unit, icon, color }: any) {
  const colorMap: any = {
    amber: 'border-amber-500/20 from-amber-500/5',
    emerald: 'border-emerald-500/20 from-emerald-500/5',
    cyan: 'border-cyan-500/20 from-cyan-500/5',
    fuchsia: 'border-fuchsia-500/20 from-fuchsia-500/5',
  };

  return (
    <motion.div
      whileHover={{ y: -4 }}
      className={`bg-gradient-to-br ${colorMap[color]} to-slate-900/90 border rounded-2xl p-6 relative shadow-lg transition-all`}
    >
      <div className="absolute top-6 right-6 bg-slate-800/50 p-2 rounded-lg border border-white/5">
        {icon}
      </div>
      <p className="text-slate-400 text-sm font-medium">{title}</p>
      <div className="mt-4 flex items-baseline gap-2">
        <h2 className="text-3xl font-bold text-white tracking-tight">{value}</h2>
        <span className="text-slate-500 text-xs uppercase font-semibold">{unit}</span>
      </div>
    </motion.div>
  );
}

function SourceBtn({ icon, label, active, onClick }: any) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-3 p-3 w-full rounded-lg border text-sm font-medium transition-all ${active ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'border-transparent text-slate-400 hover:bg-slate-800/50 hover:text-white'}`}
    >
      {icon} {label}
    </button>
  );
}

