import React from 'react';
import { CheckCircle2, Circle, Navigation, Clock } from 'lucide-react';

const ItineraryList = ({ markers, selectedPoints, onTogglePoint, onGenerate }) => {
  return (
    <div 
      id="itinerary-list"
      className="fixed top-8 left-8 w-80 max-h-[calc(100vh-160px)] overflow-y-auto glass-card p-6 z-40 transition-all duration-300"
      tabIndex="-1"
    >
      <h2 className="text-xl mb-4 flex items-center gap-2">
        <Navigation size={20} className="text-primary" />
        Explore Places
      </h2>
      
      <div className="space-y-3 mb-6">
        {markers.length === 0 ? (
          <div className="text-text-secondary text-sm italic">
            Start typing in the chatbox to find interesting places.
          </div>
        ) : (
          markers.map((marker, idx) => (
            <button
              key={idx}
              onClick={() => onTogglePoint(marker.name)}
              className={`w-full flex items-start gap-3 p-3 rounded-xl transition-all duration-200 text-left
                ${selectedPoints.includes(marker.name) 
                  ? 'bg-primary/10 border-primary/20 ring-1 ring-primary/30' 
                  : 'hover:bg-gray-50 border-transparent'}`}
              aria-pressed={selectedPoints.includes(marker.name)}
            >
              {selectedPoints.includes(marker.name) ? (
                <CheckCircle2 size={18} className="text-primary mt-0.5 shrink-0" />
              ) : (
                <Circle size={18} className="text-gray-300 mt-0.5 shrink-0" />
              )}
              <div>
                <div className="font-medium text-sm">{marker.name}</div>
                <div className="text-xs text-text-secondary line-clamp-1">{marker.description}</div>
              </div>
            </button>
          ))
        )}
      </div>

      {selectedPoints.length > 1 && (
        <button 
          onClick={onGenerate}
          className="btn-primary w-full flex items-center justify-center gap-2 mb-6"
        >
          Generate Itinerary
        </button>
      )}

      {/* Static itinerary directions removed in favor of Gemini Chat */}
    </div>
  );
};

export default ItineraryList;
