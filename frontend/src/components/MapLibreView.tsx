import { useEffect, useRef, useState, useCallback, useMemo } from 'react';
import Map, { Source, Layer, Marker, NavigationControl, FullscreenControl, Popup } from 'react-map-gl/maplibre';
import type { MapRef, MapMouseEvent } from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';
import { fetchLayerGeoJSON, fetchClusters, type Cluster, type GeoJSONResponse } from '../api';

const MAP_STYLES = {
  dark: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
  light: "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
};

interface MapLibreViewProps {
  activeLayers: string[];
  isLightMode: boolean;
  onClusterSelect?: (cluster: Cluster) => void;
  selectedCluster?: Cluster | null;
}

interface FeaturePopupInfo {
  longitude: number;
  latitude: number;
  properties: Record<string, any>;
  layerId: string;
}

const getLayerColor = (layerKey: string): string => {
  const colors: Record<string, string> = {
    portos: '#FA441A',
    ferrovias: '#F5F749',
    estradas: '#F89069',
    rodovias: '#F89069',
    hidrovias: '#06b6d4',
    aeroportos: '#FFFFFF',
    gasodutos: '#60a5fa',
    linhas_transmissao: '#fbbf24',
    solar_uv: '#f59e0b',
    solar_uv_existente: '#f59e0b',
    solar_uv_planejada: '#fbbf24',
    eolica_existente: '#34d399',
    biomassa: '#22c55e',
    usinas_hidreletricas: '#3b82f6',
    hubs_h2: '#00f5d4',
    minerais_criticos: '#a855f7',
    unidades_conservacao: '#10b981',
    terras_indigenas: '#f97316',
    terras_quilombolas: '#ec4899',
    infraestrutura: '#94a3b8',
    pastagens_inter: '#84cc16',
    pastagens_severa: '#ea580c',
  };
  return colors[layerKey] || '#FA441A';
};

export default function MapLibreView({ 
  activeLayers, 
  isLightMode, 
  onClusterSelect,
  selectedCluster 
}: MapLibreViewProps) {
  const mapRef = useRef<MapRef>(null);
  const [clusters, setClusters] = useState<Cluster[]>([]);
  const [layerData, setLayerData] = useState<Record<string, GeoJSON.FeatureCollection>>({});
  const [featurePopup, setFeaturePopup] = useState<FeaturePopupInfo | null>(null);
  const [cursor, setCursor] = useState<string>('grab');
  
  const [viewport] = useState({
    latitude: -14.235,
    longitude: -51.9253,
    zoom: 4,
    pitch: 0,
    bearing: 0
  });

  // Gather list of all current layer IDs we want to listen to clicks on
  const interactiveLayerIds = useMemo(() => {
    return activeLayers.flatMap(layerKey => [
      `${layerKey}-layer`,
      `${layerKey}-line`,
      `${layerKey}-fill`
    ]);
  }, [activeLayers]);

  // Boot clusters
  useEffect(() => {
    fetchClusters().then(setClusters).catch(console.error);
  }, []);

  // Live Camera Kinematics (FlyTo)
  useEffect(() => {
    if (selectedCluster && mapRef.current) {
      mapRef.current.flyTo({
        center: [selectedCluster.lng, selectedCluster.lat],
        zoom: 9.5,
        pitch: 55,
        bearing: -20,
        duration: 2500,
        essential: true
      });
    } else if (!selectedCluster && mapRef.current) {
       mapRef.current.flyTo({
        center: [-51.9253, -14.235],
        zoom: 4,
        pitch: 0,
        bearing: 0,
        duration: 1500
       });
    }
  }, [selectedCluster]);

  // Streaming Data Hydration
  useEffect(() => {
    activeLayers.forEach((layerKey) => {
      if (!layerData[layerKey]) {
        fetchLayerGeoJSON(layerKey)
          .then((res: GeoJSONResponse) => {
            setLayerData((prev) => ({ ...prev, [layerKey]: res.geojson }));
          })
          .catch(console.error);
      }
    });
  }, [activeLayers, layerData]);

  // Unified click management for vector layers
  const onClick = useCallback((event: MapMouseEvent) => {
    const { features, lngLat } = event;
    const feature = features && features[0];
    
    if (feature) {
       setFeaturePopup({
          longitude: lngLat.lng,
          latitude: lngLat.lat,
          properties: feature.properties as Record<string, any>,
          layerId: feature.layer.id
       });
    } else {
       setFeaturePopup(null);
    }
  }, []);

  const onMouseEnter = useCallback(() => setCursor('pointer'), []);
  const onMouseLeave = useCallback(() => setCursor('grab'), []);

  return (
    <div className="w-full h-full relative">
      <Map
        ref={mapRef}
        initialViewState={viewport}
        mapStyle={isLightMode ? MAP_STYLES.light : MAP_STYLES.dark}
        style={{ width: '100%', height: '100%' }}
        attributionControl={false}
        interactiveLayerIds={interactiveLayerIds}
        cursor={cursor}
        onClick={onClick}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
      >
        <FullscreenControl position="top-right" />
        <NavigationControl position="top-right" />

        {/* Dynamically Render GeoJSON Layers */}
        {activeLayers.map(layerKey => {
          const geo = layerData[layerKey];
          if (!geo) return null;
          
          const color = getLayerColor(layerKey);
          
          // Inspect actual feature collection for prevalent geometry type to dynamically select layer stack
          const sampleFeature = geo.features.find(f => f.geometry);
          const geometryType = sampleFeature?.geometry?.type || '';
          
          const isPoint = geometryType.includes("Point");
          const isLine = geometryType.includes("LineString");
          const isPolygon = geometryType.includes("Polygon");

          return (
            <Source key={layerKey} type="geojson" data={geo}>
              {isPoint && (
                <Layer 
                  id={`${layerKey}-layer`} 
                  type="circle" 
                  paint={{
                    'circle-radius': 6,
                    'circle-color': color,
                    'circle-stroke-width': 1,
                    'circle-stroke-color': '#fff',
                    'circle-opacity': 0.8
                  }}
                />
              )}
              
              {(isPolygon || isLine) && (
                 <Layer 
                    id={`${layerKey}-line`} 
                    type="line" 
                    paint={{
                      'line-color': color,
                      'line-width': 2,
                      'line-opacity': 0.7
                    }}
                  />
              )}

              {isPolygon && (
                 <Layer 
                    id={`${layerKey}-fill`} 
                    type="fill" 
                    paint={{
                      'fill-color': color,
                      'fill-opacity': 0.15
                    }}
                  />
              )}
            </Source>
          );
        })}

        {/* Active Cluster Interactive Markers */}
        {clusters.map((c) => (
          <Marker
            key={c.id}
            latitude={c.lat}
            longitude={c.lng}
            anchor="bottom"
            onClick={(e) => {
              e.originalEvent.stopPropagation();
              onClusterSelect?.(c);
              // Hide layer popups when selecting cluster
              setFeaturePopup(null);
            }}
          >
            <div className="relative cursor-pointer transform transition-transform hover:scale-125 group">
               <div className={`cluster-marker ${selectedCluster?.id === c.id ? 'ring-4 ring-white scale-110' : ''}`} />
               
               {/* Modern Hover Label */}
               <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none z-50">
                  <div className="glass-card px-3 py-1.5 text-xs font-bold whitespace-nowrap shadow-2xl text-white flex flex-col gap-0.5">
                    <span>{c.name}</span>
                    <span className="text-action-orange font-normal text-[10px] opacity-80">{c.port}</span>
                  </div>
               </div>
            </div>
          </Marker>
        ))}

        {/* Popup 1: Full Cluster Summary (Equivalent to original leaflet marker popup) */}
        {selectedCluster && (
          <Popup
             longitude={selectedCluster.lng}
             latitude={selectedCluster.lat}
             anchor="top"
             onClose={() => onClusterSelect?.(null as any)}
             closeOnClick={false}
             className="z-40 custom-popup"
             maxWidth="300px"
          >
             <div className={`p-2 text-sm ${isLightMode ? 'text-slate-900' : 'text-white'}`}>
               <h3 className="text-action-orange font-bold text-base mb-2">{selectedCluster.name}</h3>
               <p className="mb-1"><b>Porto:</b> {selectedCluster.port}</p>
               <p className="mb-1"><b>Vocacoes:</b> {selectedCluster.vocations.join(', ')}</p>
               <p className="mb-1"><b>Energia:</b> {selectedCluster.energy_sources.join(', ')}</p>
               <p><b>H2:</b> {selectedCluster.hydrogen_potential}</p>
             </div>
          </Popup>
        )}

        {/* Popup 2: Dynamic Vector Features (Matches exact original logic) */}
        {featurePopup && (
          <Popup
             longitude={featurePopup.longitude}
             latitude={featurePopup.latitude}
             anchor="bottom"
             onClose={() => setFeaturePopup(null)}
             closeButton={true}
             className="z-50 custom-popup"
             maxWidth="280px"
          >
             <div className={`p-2 text-[13px] ${isLightMode ? 'text-slate-800' : 'text-white'}`}>
                <b className="text-base text-action-orange block mb-2 truncate">
                  {featurePopup.properties.NOME || 
                   featurePopup.properties.nome || 
                   featurePopup.properties.Name || 
                   featurePopup.properties.name || 
                   featurePopup.properties.NM_UC || 
                   featurePopup.layerId.replace('-fill', '').replace('-line', '').replace('-layer', '')}
                </b>
                <div className="flex flex-col gap-1 max-h-[200px] overflow-y-auto">
                  {Object.entries(featurePopup.properties)
                    .filter(([k]) => !k.startsWith('Shape') && !k.startsWith('OBJECTID'))
                    .slice(0, 8)
                    .map(([k, v]) => (
                       <div key={k} className="flex flex-col gap-0.5 border-b border-white/10 pb-1 last:border-0">
                          <span className="text-[10px] font-bold uppercase text-text-muted opacity-70">{k}</span>
                          <span className="font-medium">{String(v)}</span>
                       </div>
                    ))
                  }
                </div>
             </div>
          </Popup>
        )}

      </Map>
    </div>
  );
}
