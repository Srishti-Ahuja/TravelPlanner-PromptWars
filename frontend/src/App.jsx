import React, { useState } from 'react';
import axios from 'axios';
import OrbitMap from './components/Map/OrbitMap';
import ChatBox from './components/Chat/ChatBox';
import ItineraryList from './components/Itinerary/ItineraryList';
import { Sun, Moon } from 'lucide-react';

function App() {
  const [markers, setMarkers] = useState([]);
  const [intent, setIntent] = useState('');
  const [selectedPoints, setSelectedPoints] = useState([]);
  const [itinerary, setItinerary] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(false);

  const togglePoint = (name) => {
    setSelectedPoints(prev => 
      prev.includes(name) ? prev.filter(p => p !== name) : [...prev, name]
    );
  };

  const generateItinerary = async () => {
    try {
      const response = await axios.post('https://orbit-backend-122423798285.us-central1.run.app/api/itinerary', { 
        points: selectedPoints 
      });
      setItinerary(response.data);
    } catch (error) {
      console.error("Error generating itinerary:", error);
    }
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <div className={`relative w-full h-screen overflow-hidden ${isDarkMode ? 'dark' : ''}`}>
      {/* Background Map */}
      <OrbitMap 
        markers={markers} 
        polyline={itinerary?.map_polyline} 
      />

      {/* Floating UI Elements */}
      <nav className="fixed top-8 right-8 z-50 flex items-center gap-4">
        <button 
          onClick={toggleDarkMode}
          className="glass-card p-3 focus-ring"
          aria-label="Toggle theme"
        >
          {isDarkMode ? <Sun size={20} className="text-accent" /> : <Moon size={20} className="text-primary" />}
        </button>
        <div className="glass-card px-6 py-2 flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm font-semibold tracking-wider uppercase opacity-80">Orbit Engine</span>
        </div>
      </nav>

      <ItineraryList 
        markers={markers}
        selectedPoints={selectedPoints}
        onTogglePoint={togglePoint}
        onGenerate={generateItinerary}
        itinerary={itinerary}
      />

      <ChatBox 
        onMarkersUpdate={setMarkers} 
        onIntentUpdate={setIntent} 
      />

      {/* Accessibility Skip Links */}
      <div className="sr-only">
        <a href="#itinerary-list" className="focus:not-sr-only focus:fixed focus:top-0 focus:left-0 focus:bg-white focus:p-4 focus:z-[100]">
          Skip to Itinerary
        </a>
      </div>
    </div>
  );
}

export default App;
