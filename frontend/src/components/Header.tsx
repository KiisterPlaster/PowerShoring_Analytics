import { Brain, Menu, Map as MapIcon, LayoutDashboard, Sun, Moon, Layers, Zap } from 'lucide-react';
import { PIDLogo } from '../assets/Logo';

interface HeaderProps {
  currentView: 'map' | 'dashboard';
  onSetView: (view: 'map' | 'dashboard') => void;
  onToggleMatchmaker: () => void;
  onToggleSidebar: () => void;
  sidebarOpen: boolean;
  mapEngine: 'leaflet' | 'maplibre';
  setMapEngine: (engine: 'leaflet' | 'maplibre') => void;
  isLightMode: boolean;
  setIsLightMode: (v: boolean) => void;
}

export default function Header({ 
  currentView, 
  onSetView, 
  onToggleMatchmaker, 
  onToggleSidebar, 
  sidebarOpen,
  mapEngine,
  setMapEngine,
  isLightMode,
  setIsLightMode
}: HeaderProps) {
  return (
    <header className={`h-16 glass flex items-center justify-between px-6 border-b ${isLightMode ? 'border-slate-200 bg-white/80' : 'border-border bg-slate-950/80'} backdrop-blur-xl z-30 relative transition-colors`}>
      {/* Left */}
      <div className="flex items-center gap-4">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-lg hover:bg-surface-hover transition-colors lg:hidden"
        >
          <Menu size={20} className={isLightMode ? 'text-slate-600' : 'text-text-secondary'} />
        </button>

        <div className="flex items-center gap-3 cursor-pointer hover:opacity-90 transition-opacity">
          <div className="h-10 w-32">
             <PIDLogo className="h-full w-full object-contain" />
          </div>
        </div>
      </div>

      {/* Center: Main Navigation Tabs */}
      <div className={`flex items-center ${isLightMode ? 'bg-slate-100' : 'bg-slate-900/50'} p-1 rounded-xl border ${isLightMode ? 'border-slate-200' : 'border-white/5'} shadow-inner space-x-1`}>
        <button
          onClick={() => onSetView('map')}
          className={`flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
            currentView === 'map' 
            ? 'bg-action-orange text-white shadow-lg shadow-action-orange/30' 
            : isLightMode ? 'text-slate-600 hover:bg-slate-200' : 'text-slate-400 hover:text-white hover:bg-white/10'
          }`}
        >
          <MapIcon size={16} /> <span className="hidden md:inline tracking-wide">Mapa Estratégico</span>
        </button>
        <button
          onClick={() => onSetView('dashboard')}
          className={`flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
            currentView === 'dashboard' 
            ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/30' 
            : isLightMode ? 'text-slate-600 hover:bg-slate-200' : 'text-slate-400 hover:text-white hover:bg-white/10'
          }`}
        >
          <LayoutDashboard size={16} /> <span className="hidden md:inline tracking-wide">Hub de Dados</span>
        </button>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-4">
        
        {/* Theme & Engine Switcher Groups */}
        <div className="hidden lg:flex items-center bg-surface-card/30 p-1 rounded-xl border border-white/5 gap-1">
           
           {/* Mode Engine Toggle */}
           <button
             onClick={() => setMapEngine(mapEngine === 'maplibre' ? 'leaflet' : 'maplibre')}
             title={mapEngine === 'maplibre' ? "Usando WebGL 3D" : "Usando Raster 2D"}
             className={`p-2 rounded-lg transition-colors flex items-center gap-2 text-xs font-bold ${
               mapEngine === 'maplibre' 
               ? 'text-action-orange bg-action-orange/10' 
               : isLightMode ? 'text-slate-500 hover:bg-slate-200' : 'text-text-muted hover:bg-white/5'
             }`}
           >
             {mapEngine === 'maplibre' ? <Zap size={16} /> : <Layers size={16} />}
             <span>{mapEngine === 'maplibre' ? 'VEC' : 'RAS'}</span>
           </button>

           <div className="w-px h-4 bg-border/50 mx-1" />

           {/* Theme Toggle */}
           <button
             onClick={() => setIsLightMode(!isLightMode)}
             className={`p-2 rounded-lg transition-colors ${isLightMode ? 'text-amber-500 hover:bg-amber-50' : 'text-text-muted hover:bg-white/5'}`}
           >
             {isLightMode ? <Sun size={18} /> : <Moon size={18} />}
           </button>
        </div>

        <button
          onClick={onToggleMatchmaker}
          className="flex items-center gap-2 px-5 py-2.5 bg-action-orange hover:bg-orange-500 rounded-xl text-sm font-bold text-white transition-all shadow-lg shadow-action-orange/20 active:scale-95 ring-1 ring-white/20"
        >
          <Brain size={18} className="animate-pulse" />
          <span className="hidden sm:inline tracking-wide uppercase text-[11px]">Matchmaker IA</span>
        </button>
      </div>
    </header>
  );
}
