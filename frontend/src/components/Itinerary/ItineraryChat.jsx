import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Bot, User, ArrowLeft, Loader2 } from 'lucide-react';

const ItineraryChat = ({ selectedPoints, markers, onBack }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    // Initial greeting and first itinerary generation
    const initialPrompt = "Please generate an initial itinerary for my selected places.";
    handleSendMessage(initialPrompt, true);
  }, []); // Run once on mount

  const prevPointsRef = useRef(selectedPoints.map(p => p).join(','));
  useEffect(() => {
    const currentStr = selectedPoints.map(p => p).join(',');
    if (prevPointsRef.current !== currentStr) {
      prevPointsRef.current = currentStr;
      const prompt = `I have updated my selected places. The new places are: ${selectedPoints.join(', ')}. Please adjust the itinerary to focus specifically on these places.`;
      handleSendMessage(prompt, false);
    }
  }, [selectedPoints]);

  const handleSendMessage = async (text, isInitial = false) => {
    if (!text.trim() && !isInitial) return;

    const userMessage = text;
    if (!isInitial) {
      setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
      setInput('');
    }
    
    setIsLoading(true);

    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000';
      const pointsWithCoords = selectedPoints.map(name => {
        const marker = markers.find(m => m.name === name);
        return { name: marker.name, lat: marker.lat, lng: marker.lng };
      });

      // Filter out internal state structure, only keep role and content for API
      const chatHistory = messages.map(m => ({ role: m.role, content: m.content }));

      const response = await axios.post(`${backendUrl}/api/itinerary/chat`, {
        points: pointsWithCoords,
        chat_history: chatHistory,
        user_message: isInitial ? "Can you suggest an itinerary for these places?" : userMessage
      });

      setMessages(prev => [...prev, { role: 'model', content: response.data.message }]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev => [...prev, { 
        role: 'model', 
        content: "I'm sorry, I encountered an error connecting to the travel engine." 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white/50 backdrop-blur-md rounded-2xl border border-white/20 shadow-xl overflow-hidden animate-in fade-in zoom-in-95 duration-300">
      {/* Header */}
      <div className="flex items-center gap-3 p-4 border-b border-gray-100 bg-white/80">
        <button 
          onClick={onBack}
          className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          title="Back to list"
        >
          <ArrowLeft size={18} className="text-gray-600" />
        </button>
        <div>
          <h3 className="font-semibold text-gray-800 flex items-center gap-2">
            <Bot size={18} className="text-primary" />
            Orbit Agent
          </h3>
          <p className="text-xs text-text-secondary">Planning {selectedPoints.length} places</p>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && isLoading && (
          <div className="flex items-center justify-center h-full text-text-secondary">
            <Loader2 className="animate-spin mr-2" size={20} /> Crafting your perfect itinerary...
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
              msg.role === 'user' ? 'bg-primary text-white' : 'bg-accent/20 text-accent'
            }`}>
              {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
            </div>
            <div className={`px-4 py-3 rounded-2xl max-w-[85%] text-sm ${
              msg.role === 'user' 
                ? 'bg-primary text-white rounded-tr-none' 
                : 'bg-white border border-gray-100 shadow-sm rounded-tl-none text-gray-800'
            }`}>
              {msg.role === 'user' ? (
                <p>{msg.content}</p>
              ) : (
                <div 
                  className="prose prose-sm prose-p:my-1 prose-ul:my-1 prose-li:my-0"
                  dangerouslySetInnerHTML={{ __html: msg.content }} 
                />
              )}
            </div>
          </div>
        ))}
        {isLoading && messages.length > 0 && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-accent/20 text-accent flex items-center justify-center shrink-0">
              <Bot size={16} />
            </div>
            <div className="px-4 py-3 rounded-2xl bg-white border border-gray-100 shadow-sm rounded-tl-none flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-3 border-t border-gray-100 bg-white/80">
        <form 
          onSubmit={(e) => { e.preventDefault(); handleSendMessage(input); }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask to change the itinerary..."
            className="flex-1 input-field py-2 text-sm"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            disabled={!input.trim() || isLoading}
            className="p-2 bg-primary text-white rounded-xl hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ItineraryChat;
