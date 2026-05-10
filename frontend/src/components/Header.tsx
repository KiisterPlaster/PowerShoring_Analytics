import { Brain, Menu, Map as MapIcon, LayoutDashboard } from 'lucide-react';

interface HeaderProps {
  currentView: 'map' | 'dashboard';
  onSetView: (view: 'map' | 'dashboard') => void;
  onToggleMatchmaker: () => void;
  onToggleSidebar: () => void;
  sidebarOpen: boolean;
}

export default function Header({ currentView, onSetView, onToggleMatchmaker, onToggleSidebar, sidebarOpen }: HeaderProps) {
  return (
    <header className="h-14 glass flex items-center justify-between px-4 border-b border-border z-30 relative">
      {/* Left */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-lg hover:bg-surface-hover transition-colors lg:hidden"
        >
          <Menu size={20} className="text-text-secondary" />
        </button>

        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-action-orange flex items-center justify-center">
            <span className="text-white font-bold text-sm">P</span>
          </div>
          <div>
            <h1 className="text-sm font-heading font-bold text-text-primary leading-tight">
              PowerShoring Analytics
            </h1>
            <p className="text-[10px] text-text-muted leading-tight">
              Neoindustrializacao Verde do Brasil
            </p>
          </div>
        </div>
      </div>

      {/* Center: Main Navigation Tabs */}
      <div className="flex items-center bg-surface-card/50 p-1 rounded-xl border border-border space-x-1">
        <button
          onClick={() => onSetView('map')}
          className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm transition-all ${
            currentView === 'map' 
            ? 'bg-action-orange/20 text-action-orange font-bold border border-action-orange/30' 
            : 'text-text-secondary hover:text-text-primary hover:bg-surface-hover'
          }`}
        >
          <MapIcon size={16} /> <span className="hidden md:inline">Mapa Estratégico</span>
        </button>
        <button
          onClick={() => onSetView('dashboard')}
          className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm transition-all ${
            currentView === 'dashboard' 
            ? 'bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30' 
            : 'text-text-secondary hover:text-text-primary hover:bg-surface-hover'
          }`}
        >
          <LayoutDashboard size={16} /> <span className="hidden md:inline">Hub de Dados</span>
        </button>
      </div>

      {/* Right */}
      <button
        onClick={onToggleMatchmaker}
        className="flex items-center gap-2 px-4 py-2 bg-action-orange hover:bg-action-orange/90 rounded-xl text-sm font-semibold text-white transition-all pulse-glow"
      >
        <Brain size={16} />
        <span className="hidden sm:inline">Matchmaker IA</span>
      </button>
    </header>
  );
}
