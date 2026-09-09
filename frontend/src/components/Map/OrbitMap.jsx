import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap, Tooltip, Pane } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix Leaflet default marker icon broken by webpack/vite bundlers
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

// Custom colored marker icons by place type
const createIcon = (type, isSelected) => {
  const color = isSelected ? '#1A73E8' : '#EA4335'; // Blue when selected, Red otherwise
  const size = 26; // Don't increase size
  const border = isSelected ? '3px solid #FFFFFF' : '3px solid white';
  const scale = isSelected ? 'scale(1.15)' : 'scale(1)';
  const shadow = isSelected 
    ? '0 0 16px rgba(255, 255, 255, 1), 0 4px 12px rgba(0,0,0,0.5)' // White glow
    : '0 2px 8px rgba(0,0,0,0.3)';

  return L.divIcon({
    className: '',
    html: `<div style="
      width: ${size}px; height: ${size}px;
      background: ${color};
      border-radius: 50% 50% 50% 0;
      transform: rotate(-45deg) ${scale};
      border: ${border};
      box-shadow: ${shadow};
      transition: all 0.2s ease-in-out;
    "></div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size],
    popupAnchor: [0, -size - 2],
  });
};

// Sub-component: auto-fits map bounds when markers change
const MapBoundsUpdater = ({ markers }) => {
  const map = useMap();
  useEffect(() => {
    if (markers && markers.length > 0) {
      const bounds = L.latLngBounds(markers.map(m => [m.lat, m.lng]));
      map.fitBounds(bounds, { padding: [40, 40] });
    }
  }, [markers, map]);
  return null;
};

const OrbitMap = ({ markers = [], selectedPoints = [], polyline = null }) => {
  return (
    <div
      style={{ width: '100%', height: '100vh' }}
      role="application"
      aria-label="Interactive travel map"
    >
      <MapContainer
        center={[20, 0]}
        zoom={2}
        style={{ width: '100%', height: '100%' }}
        zoomControl={true}
      >
        <Pane name="highTooltip" style={{ zIndex: 4000 }} />
        {/* OpenStreetMap tiles — free, no API key required */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Auto-fit bounds to markers */}
        <MapBoundsUpdater markers={markers} />

        {/* Place markers */}
        {markers.map((marker, index) => (
          <Marker
            key={index}
            position={[marker.lat, marker.lng]}
            icon={createIcon(marker.type, selectedPoints.includes(marker.name))}
            eventHandlers={{
              mouseover: (e) => e.target.openTooltip(),
              mouseout: (e) => e.target.closeTooltip(),
            }}
          >
            {/* Ensure a high‑z‑index pane exists */}
            <Tooltip direction="auto" offset={[0, -10]} opacity={1} pane="highTooltip">
                <div className="flex flex-col items-center min-w-[350px] max-w-[400px] p-6">
                <img 
                  src={marker.image_keyword ? `https://loremflickr.com/320/240/${marker.image_keyword}` : `https://via.placeholder.com/320x240/cccccc/ffffff?text=Building`} 
                  alt={marker.name} 
                  className="w-full h-64 object-cover rounded-md mb-4 shadow-lg"
                />
                <strong className="text-base font-semibold text-center mb-3 whitespace-normal leading-tight">{marker.name}</strong>
                {marker.description && (
                  <p className="text-sm text-gray-600 text-center mb-4 line-clamp-4 whitespace-normal">{marker.description}</p>
                )}
                <div className="flex items-center gap-1 text-yellow-500 text-lg">
                  {'★'.repeat(Math.floor(marker.rating || 4.5))}
                  {'☆'.repeat(5 - Math.floor(marker.rating || 4.5))}
                  <span className="text-gray-600 text-sm ml-1 font-medium">{(marker.rating || 4.5).toFixed(1)}</span>
                </div>
                </div>
            </Tooltip>
            <Popup>
              <div style={{ maxWidth: '200px' }}>
                <strong>{marker.name}</strong>
                {marker.description && (
                  <p style={{ margin: '4px 0 0', fontSize: '12px', color: '#555' }}>
                    {marker.description}
                  </p>
                )}
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Route polyline — polyline is now [{lat, lng}] array from backend */}
        {polyline && polyline.length > 0 && (
          <Polyline
            positions={polyline.map(p => [p.lat, p.lng])}
            pathOptions={{
              color: '#1A73E8',
              weight: 4,
              opacity: 0.85,
            }}
          />
        )}
      </MapContainer>

      {/* Skip-to-list accessibility link */}
      <button
        className="absolute top-4 left-4 bg-white p-2 rounded shadow sr-only focus:not-sr-only focus:z-[1000]"
        onClick={() => document.getElementById('itinerary-list')?.focus()}
        style={{ position: 'absolute', zIndex: 1000 }}
      >
        Skip to List
      </button>
    </div>
  );
};

export default React.memo(OrbitMap);
