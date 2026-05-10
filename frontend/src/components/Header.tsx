import { Brain, Menu } from 'lucide-react';

interface HeaderProps {
  onToggleMatchmaker: () => void;
  onToggleSidebar: () => void;
  sidebarOpen: boolean;
}

export default function Header({ onToggleMatchmaker, onToggleSidebar, sidebarOpen }: HeaderProps) {
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

      {/* Center badge */}
      <div className="hidden md:flex items-center gap-2 bg-surface-card/50 px-3 py-1.5 rounded-full border border-border">
        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
        <span className="text-[11px] text-text-muted">Dados em tempo real | PID ArcGIS</span>
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
