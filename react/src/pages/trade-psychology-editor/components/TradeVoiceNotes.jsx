import React, { useState, useEffect } from 'react';
import api from '../../../auth/api';
import Icon from '../../../components/AppIcon';

const TradeVoiceNotes = ({ tradeId }) => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!tradeId) return;

    const fetchVoiceNotes = async () => {
      try {
        setLoading(true);
        // Using the updated proxy /api/v1 prefix from axios instance
        const response = await api.get(`/voice-notes/trade/${tradeId}`);
        setNotes(response.data);
      } catch (error) {
        console.error('Error fetching voice notes:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchVoiceNotes();
  }, [tradeId]);

  if (loading) {
    return (
      <div className="space-y-3 animate-pulse">
        <div className="h-4 w-24 bg-muted rounded"></div>
        <div className="h-20 bg-muted rounded-lg"></div>
      </div>
    );
  }

  if (notes.length === 0) return null;

  return (
    <div className="space-y-4 pt-4 border-t border-border">
      <h4 className="text-sm font-semibold text-foreground flex items-center gap-2">
        <Icon name="Mic" size={16} />
        Voice Notes ({notes.length})
      </h4>
      <div className="space-y-3">
        {notes.map((note) => (
          <div key={note.id} className="bg-muted/40 border border-border/50 rounded-lg p-3 space-y-2 hover:bg-muted/60 transition-colors">
            <div className="flex items-center justify-between text-[10px] md:text-xs text-muted-foreground">
              <span className="flex items-center gap-1">
                <Icon name="Calendar" size={12} />
                {new Date(note.created_at).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
              </span>
              <span className="px-2 py-0.5 bg-primary/10 text-primary rounded-full text-[10px] uppercase font-bold tracking-wider">
                {note.trade_state_at_time}
              </span>
            </div>
            <audio 
              controls 
              src={`/${note.file_path}`} 
              className="w-full h-8 accent-primary opacity-90 hover:opacity-100 transition-opacity"
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default TradeVoiceNotes;
