import React, { useState, useCallback } from 'react';
import { GoogleMap, useJsApiLoader, Marker, Polyline } from '@react-google-maps/api';

const containerStyle = {
  width: '100%',
  height: '100vh'
};

const defaultCenter = {
  lat: 20,
  lng: 0
};

const OrbitMap = ({ markers, polyline }) => {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: import.meta.env.VITE_MAPS_API_KEY || ""
  });

  const [map, setMap] = useState(null);

  const onLoad = useCallback(function callback(map) {
    setMap(map);
  }, []);

  const onUnmount = useCallback(function callback(map) {
    setMap(null);
  }, []);

  // Center map on markers when they change
  React.useEffect(() => {
    if (map && markers.length > 0) {
      const bounds = new window.google.maps.LatLngBounds();
      markers.forEach(marker => bounds.extend({ lat: marker.lat, lng: marker.lng }));
      map.fitBounds(bounds);
    }
  }, [map, markers]);

  if (!isLoaded) return <div className="w-full h-full skeleton" />;

  return (
    <div className="relative w-full h-full" role="application" aria-label="Interactive travel map">
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={defaultCenter}
        zoom={2}
        onLoad={onLoad}
        onUnmount={onUnmount}
        options={{
            disableDefaultUI: true,
            zoomControl: true,
            styles: [
                {
                    "featureType": "all",
                    "elementType": "labels.text.fill",
                    "stylers": [{"color": "#202124"}]
                },
                {
                    "featureType": "water",
                    "elementType": "geometry",
                    "stylers": [{"color": "#e9e9e9"}]
                },
                {
                    "featureType": "landscape",
                    "elementType": "geometry",
                    "stylers": [{"color": "#f5f5f5"}]
                }
            ]
        }}
      >
        {markers.map((marker, index) => (
          <Marker
            key={index}
            position={{ lat: marker.lat, lng: marker.lng }}
            title={marker.name}
            animation={window.google.maps.Animation.DROP}
          />
        ))}

        {polyline && (
          <Polyline
            path={window.google.maps.geometry.encoding.decodePath(polyline)}
            options={{
              strokeColor: '#1A73E8',
              strokeOpacity: 0.8,
              strokeWeight: 4,
            }}
          />
        )}
      </GoogleMap>
      
      <button 
        className="absolute top-4 left-4 bg-white p-2 rounded shadow focus-ring sr-only focus:not-sr-only"
        onClick={() => document.getElementById('itinerary-list').focus()}
      >
        Skip to List
      </button>
    </div>
  );
};

export default React.memo(OrbitMap);
