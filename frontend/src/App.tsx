import { useState, useCallback, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import MapView from './components/MapView';
import MatchmakerPanel from './components/MatchmakerPanel';
import ClusterDetail from './components/ClusterDetail';
import AnalyticsPanel from './components/AnalyticsPanel';
import DataDashboard from './components/DataDashboard';
import type { Cluster } from './api';

export default function App() {
  const [currentView, setCurrentView] = useState<'map' | 'dashboard'>('map');
  const [activeLayers, setActiveLayers] = useState<string[]>([]);
  const [matchmakerOpen, setMatchmakerOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedCluster, setSelectedCluster] = useState<Cluster | null>(null);
  
  // High tech enhancements
  const [mapEngine, setMapEngine] = useState<'leaflet' | 'maplibre'>('maplibre');
  const [isLightMode, setIsLightMode] = useState(false);

  useEffect(() => {
    if (isLightMode) {
      document.body.classList.add('light-theme');
    } else {
      document.body.classList.remove('light-theme');
    }
  }, [isLightMode]);

  const toggleLayer = useCallback((layerKey: string) => {
    setActiveLayers((prev) =>
      prev.includes(layerKey) ? prev.filter((k) => k !== layerKey) : [...prev, layerKey]
    );
  }, []);

  return (
    <div className={`h-screen w-screen flex flex-col ${isLightMode ? 'bg-slate-50 text-slate-900' : 'bg-surface text-white'} overflow-hidden transition-colors duration-500`}>
      <Header
        currentView={currentView}
        onSetView={setCurrentView}
        onToggleMatchmaker={() => setMatchmakerOpen((v) => !v)}
        onToggleSidebar={() => setSidebarOpen((v) => !v)}
        sidebarOpen={sidebarOpen}
        mapEngine={mapEngine}
        setMapEngine={setMapEngine}
        isLightMode={isLightMode}
        setIsLightMode={setIsLightMode}
      />

      <div className="flex-1 flex overflow-hidden relative w-full h-full">
        
        {/* BACKGROUND LAYER: Persistent Map Rendering like references 1 & 2 */}
        <div className="absolute inset-0 w-full h-full z-0">
          <MapView
            activeLayers={activeLayers}
            onClusterSelect={setSelectedCluster}
            selectedCluster={selectedCluster}
            engine={mapEngine}
            isLightMode={isLightMode}
          />
        </div>

        {/* INTERACTIVE OVERLAY LAYER */}
        <div className="relative z-10 w-full h-full pointer-events-none flex overflow-hidden">
          {currentView === 'map' ? (
            <div className="flex-1 flex overflow-hidden pointer-events-auto">
              {/* Sidebar */}
              {sidebarOpen && (
                <Sidebar activeLayers={activeLayers} onToggleLayer={toggleLayer} />
              )}

              {/* Floating Content Containers */}
              <main className="flex-1 relative">
                {/* Layer loading indicator */}
                {activeLayers.length > 0 && (
                  <div className="absolute top-4 left-4 z-10 glass px-3 py-1.5 rounded-full shadow-lg">
                    <span className="text-[11px] text-cyber-cyan font-bold tracking-wide uppercase drop-shadow-[0_0_5px_rgba(0,240,255,0.5)]">
                      {activeLayers.length} camada{activeLayers.length > 1 ? 's' : ''} ativa{activeLayers.length > 1 ? 's' : ''}
                    </span>
                  </div>
                )}

                {/* Detail & Analytics Panels */}
                <ClusterDetail
                  cluster={selectedCluster}
                  onClose={() => setSelectedCluster(null)}
                />
                
                <AnalyticsPanel
                  cluster={selectedCluster}
                  onClose={() => setSelectedCluster(null)}
                  onOpenMatchmaker={() => setMatchmakerOpen(true)}
                />
              </main>
            </div>
          ) : (
            /* Dashboard Overlay: Spans across the map, allowing visual flow-through */
            <main className="flex-1 overflow-y-auto bg-black/30 backdrop-blur-sm pointer-events-auto w-full h-full">
              <DataDashboard />
            </main>
          )}
        </div>
      </div>

      {/* Matchmaker AI Panel */}
      <MatchmakerPanel
        isOpen={matchmakerOpen}
        onClose={() => setMatchmakerOpen(false)}
      />
    </div>
  );
}
