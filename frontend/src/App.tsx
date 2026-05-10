import { useState, useCallback } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import MapView from './components/MapView';
import MatchmakerPanel from './components/MatchmakerPanel';
import ClusterDetail from './components/ClusterDetail';
import type { Cluster } from './api';

export default function App() {
  const [activeLayers, setActiveLayers] = useState<string[]>([]);
  const [matchmakerOpen, setMatchmakerOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedCluster, setSelectedCluster] = useState<Cluster | null>(null);

  const toggleLayer = useCallback((layerKey: string) => {
    setActiveLayers((prev) =>
      prev.includes(layerKey) ? prev.filter((k) => k !== layerKey) : [...prev, layerKey]
    );
  }, []);

  return (
    <div className="h-screen w-screen flex flex-col bg-surface overflow-hidden">
      <Header
        onToggleMatchmaker={() => setMatchmakerOpen((v) => !v)}
        onToggleSidebar={() => setSidebarOpen((v) => !v)}
        sidebarOpen={sidebarOpen}
      />

      <div className="flex-1 flex overflow-hidden relative">
        {/* Sidebar */}
        {sidebarOpen && (
          <Sidebar activeLayers={activeLayers} onToggleLayer={toggleLayer} />
        )}

        {/* Map */}
        <main className="flex-1 relative">
          <MapView
            activeLayers={activeLayers}
            onClusterSelect={setSelectedCluster}
          />

          {/* Layer loading indicator */}
          {activeLayers.length > 0 && (
            <div className="absolute top-4 left-4 z-10 glass px-3 py-1.5 rounded-full">
              <span className="text-[11px] text-text-secondary">
                {activeLayers.length} camada{activeLayers.length > 1 ? 's' : ''} ativa{activeLayers.length > 1 ? 's' : ''}
              </span>
            </div>
          )}

          {/* Cluster detail overlay */}
          <ClusterDetail
            cluster={selectedCluster}
            onClose={() => setSelectedCluster(null)}
          />
        </main>
      </div>

      {/* Matchmaker AI Panel */}
      <MatchmakerPanel
        isOpen={matchmakerOpen}
        onClose={() => setMatchmakerOpen(false)}
      />
    </div>
  );
}
