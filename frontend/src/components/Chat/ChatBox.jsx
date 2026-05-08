import React, { useState, useEffect, useCallback } from 'react';
import { Send, MapPin, Loader2 } from 'lucide-react';
import axios from 'axios';

const ChatBox = ({ onMarkersUpdate, onIntentUpdate }) => {
  const [query, setQuery] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Debounce logic
  useEffect(() => {
    const timer = setTimeout(() => {
      if (query.trim().length > 5) {
        handleSearch(query);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [query]);

  const handleSearch = async (text) => {
    setIsLoading(true);
    try {
      const response = await axios.post('https://orbit-backend-122423798285.us-central1.run.app/api/intent', { query: text });
      onMarkersUpdate(response.data.markers);
      onIntentUpdate(response.data.intent);
    } catch (error) {
      console.error("Error fetching intent:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-8 left-1/2 -translate-x-1/2 w-full max-w-2xl px-4 z-50">
      <div className="glass-card p-2 flex items-center gap-2 group focus-within:ring-2 focus-within:ring-primary transition-all">
        <div className="pl-4">
          <MapPin className="text-primary w-5 h-5" />
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Where would you like to go?"
          className="flex-1 bg-transparent border-none focus:ring-0 py-3 text-lg placeholder:text-text-secondary outline-none"
          aria-label="Trip planning chatbox"
        />
        <button 
          onClick={() => handleSearch(query)}
          className="btn-primary p-3 aspect-square flex items-center justify-center"
          disabled={isLoading}
          aria-label="Send query"
        >
          {isLoading ? <Loader2 className="animate-spin" /> : <Send size={20} />}
        </button>
      </div>
      
      {/* Visual indicator for typing/thinking */}
      {isLoading && (
        <div className="mt-4 flex justify-center">
          <div className="bg-white/80 backdrop-blur px-4 py-2 rounded-full text-sm font-medium shadow-sm flex items-center gap-2 animate-bounce">
            <span className="w-2 h-2 bg-primary rounded-full"></span>
            Orbit is exploring possibilities...
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatBox;
