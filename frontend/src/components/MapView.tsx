import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { fetchLayerGeoJSON, fetchClusters, type Cluster, type GeoJSONResponse } from '../api';
import MapLibreView from './MapLibreView';

// Fix Leaflet default marker icons
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
delete (L.Icon.Default.prototype as unknown as Record<string, unknown>)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

const clusterIcon = new L.DivIcon({
  className: 'cluster-marker',
  iconSize: [32, 32],
  iconAnchor: [16, 16],
  popupAnchor: [0, -20],
});

interface MapViewProps {
  activeLayers: string[];
  onClusterSelect?: (cluster: Cluster) => void;
  selectedCluster?: Cluster | null;
  engine?: 'leaflet' | 'maplibre';
  isLightMode?: boolean;
}

function LeafletController({ selectedCluster }: { selectedCluster?: Cluster | null }) {
  const map = useMap();
  useEffect(() => {
    if (selectedCluster) {
      map.flyTo([selectedCluster.lat, selectedCluster.lng], 9, {
        animate: true,
        duration: 1.5
      });
    }
  }, [selectedCluster, map]);
  return null;
}

function FitBrazil() {
  const map = useMap();
  useEffect(() => {
    map.setView([-14.235, -51.9253], 4);
  }, [map]);
  return null;
}

export default function MapView({ 
  activeLayers, 
  onClusterSelect, 
  selectedCluster,
  engine = 'maplibre',
  isLightMode = false 
}: MapViewProps) {
  const [clusters, setClusters] = useState<Cluster[]>([]);
  const [layerData, setLayerData] = useState<Record<string, GeoJSON.FeatureCollection>>({});
  const [loadingLayers, setLoadingLayers] = useState<Set<string>>(new Set());

  // Load clusters
  useEffect(() => {
    fetchClusters().then(setClusters).catch(console.error);
  }, []);

  // Load active layers
  useEffect(() => {
    activeLayers.forEach((layerKey) => {
      if (!layerData[layerKey] && !loadingLayers.has(layerKey)) {
        setLoadingLayers((prev) => new Set(prev).add(layerKey));
        fetchLayerGeoJSON(layerKey)
          .then((res: GeoJSONResponse) => {
            setLayerData((prev) => ({ ...prev, [layerKey]: res.geojson }));
          })
          .catch(console.error)
          .finally(() => {
            setLoadingLayers((prev) => {
              const next = new Set(prev);
              next.delete(layerKey);
              return next;
            });
          });
      }
    });
  }, [activeLayers, layerData, loadingLayers]);

  if (engine === 'maplibre') {
    return (
      <MapLibreView 
        activeLayers={activeLayers}
        onClusterSelect={onClusterSelect}
        selectedCluster={selectedCluster}
        isLightMode={isLightMode}
      />
    );
  }

  const getLayerColor = (layerKey: string): string => {
    const colors: Record<string, string> = {
      portos: '#FA441A',
      ferrovias: '#F5F749',
      rodovias: '#F89069',
      gasodutos: '#60a5fa',
      linhas_transmissao: '#fbbf24',
      solar_uv: '#f59e0b',
      eolica_existente: '#34d399',
      biomassa: '#22c55e',
      usinas_hidreletricas: '#3b82f6',
      hubs_h2: '#06b6d4',
      minerais_criticos: '#a855f7',
      unidades_conservacao: '#10b981',
      terras_indigenas: '#f97316',
      terras_quilombolas: '#ec4899',
      infraestrutura: '#94a3b8',
    };
    return colors[layerKey] || '#ffffff';
  };

  return (
    <MapContainer
      center={[-14.235, -51.9253]}
      zoom={4}
      className="w-full h-full z-0"
      zoomControl={true}
    >
      <FitBrazil />
      <LeafletController selectedCluster={selectedCluster} />
      
      <TileLayer
        attribution='&copy; <a href="https://carto.com">CARTO</a>'
        url={isLightMode 
          ? "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png" 
          : "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        }
      />

      {/* Render active GeoJSON layers */}
      {activeLayers.map((layerKey) =>
        layerData[layerKey] ? (
          <GeoJSON
            key={`${layerKey}-${Date.now()}`}
            data={layerData[layerKey]}
            style={() => ({
              color: getLayerColor(layerKey),
              weight: 2,
              opacity: 0.7,
              fillOpacity: 0.15,
            })}
            pointToLayer={(_feature, latlng) =>
              L.circleMarker(latlng, {
                radius: 5,
                fillColor: getLayerColor(layerKey),
                color: getLayerColor(layerKey),
                weight: 1,
                opacity: 0.8,
                fillOpacity: 0.6,
              })
            }
            onEachFeature={(feature, layer) => {
              if (feature.properties) {
                const props = feature.properties;
                const name = props.NOME || props.nome || props.Name || props.name || props.NM_UC || '';
                const info = Object.entries(props)
                  .filter(([k]) => !k.startsWith('Shape') && !k.startsWith('OBJECTID'))
                  .slice(0, 6)
                  .map(([k, v]) => `<b>${k}:</b> ${v}`)
                  .join('<br/>');
                layer.bindPopup(
                  `<div style="max-width:280px;font-size:13px;"><b style="font-size:15px;color:#FA441A;">${name || layerKey}</b><br/><br/>${info}</div>`
                );
              }
            }}
          />
        ) : null
      )}

      {/* Cluster markers */}
      {clusters.map((cluster) => (
        <Marker
          key={cluster.id}
          position={[cluster.lat, cluster.lng]}
          icon={clusterIcon}
          eventHandlers={{
            click: () => onClusterSelect?.(cluster),
          }}
        >
          <Popup>
            <div style={{ maxWidth: 300, fontSize: 13 }}>
              <h3 style={{ color: '#FA441A', marginBottom: 8, fontSize: 15 }}>{cluster.name}</h3>
              <p style={{ marginBottom: 6 }}><b>Porto:</b> {cluster.port}</p>
              <p style={{ marginBottom: 6 }}><b>Vocacoes:</b> {cluster.vocations.join(', ')}</p>
              <p style={{ marginBottom: 6 }}><b>Energia:</b> {cluster.energy_sources.join(', ')}</p>
              <p><b>H2:</b> {cluster.hydrogen_potential}</p>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
