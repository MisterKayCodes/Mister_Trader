import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../auth/api';
import AuthenticatedHeader from '../../components/layout/AuthenticatedHeader';
import PrimaryNavigation from '../../components/layout/PrimaryNavigation';
import AccountContextBar from '../../components/layout/AccountContextBar';
import Button from '../../components/ui/Button';
import Icon from '../../components/AppIcon';
import RichTextEditor from './components/RichTextEditor';
import DecisionQualityRating from './components/DecisionQualityRating';
import EmotionTagSelector from './components/EmotionTagSelector';
import MarketConditionAssessment from './components/MarketConditionAssessment';
import TemplatePrompts from './components/TemplatePrompts';
import TradeReferencePanel from './components/TradeReferencePanel';

const TradePsychologyEditor = () => {
  const navigate = useNavigate();
  const [selectedAccount, setSelectedAccount] = useState('');
  const [activeView, setActiveView] = useState('history'); // Default to history since you need to pick a trade first
  
  // History State
  const [trades, setTrades] = useState([]);
  const [isLoadingTrades, setIsLoadingTrades] = useState(false);
  
  // Editor State
  const [selectedTrade, setSelectedTrade] = useState(null);
  const [psychologyId, setPsychologyId] = useState(null); // Keep track of existing record ID
  const [autoSaveStatus, setAutoSaveStatus] = useState('saved');
  const [lastSaved, setLastSaved] = useState(new Date());

  const [psychologyEntry, setPsychologyEntry] = useState({
    discipline: 'MEDIUM',
    confidence: 'MEDIUM',
    followed_plan: true,
    decision_quality: 3,
    emotions: [],
    market_condition: '',
    volatility_level: '',
    notes: ''
  });

  // Fetch trades when account changes or view switches to history
  useEffect(() => {
    if (selectedAccount && activeView === 'history') {
      fetchTrades();
    }
  }, [selectedAccount, activeView]);

  const fetchTrades = async () => {
    setIsLoadingTrades(true);
    try {
      const response = await api.get(`/trades?account_id=${selectedAccount}`);
      // Sort by open_timestamp descending
      const sortedTrades = response.data.sort((a, b) => 
        new Date(b.open_timestamp || b.created_at) - new Date(a.open_timestamp || a.created_at)
      );
      setTrades(sortedTrades);
    } catch (err) {
      console.error("Failed to fetch trades:", err);
    } finally {
      setIsLoadingTrades(false);
    }
  };

  // When a user selects a trade from history to edit its psychology
  const handleSelectTrade = async (trade) => {
    setSelectedTrade(trade);
    setActiveView('editor');
    setAutoSaveStatus('saving');
    
    // Attempt to load existing psychology for this trade
    try {
      const response = await api.get(`/trade-psychology/trade/${trade.id}`);
      setPsychologyEntry({
        discipline: response.data.discipline,
        confidence: response.data.confidence,
        followed_plan: response.data.followed_plan,
        decision_quality: response.data.decision_quality || 3,
        emotions: response.data.emotions ? response.data.emotions.split(',') : [],
        market_condition: response.data.market_condition || '',
        volatility_level: response.data.volatility_level || '',
        notes: response.data.notes || ''
      });
      setPsychologyId(response.data.id);
      setAutoSaveStatus('saved');
      setLastSaved(new Date());
    } catch (err) {
      // 404 means no psychology exists yet, so reset form for new entry
      setPsychologyEntry({
        discipline: 'MEDIUM',
        confidence: 'MEDIUM',
        followed_plan: true,
        decision_quality: 3,
        emotions: [],
        market_condition: '',
        volatility_level: '',
        notes: ''
      });
      setPsychologyId(null);
      setAutoSaveStatus('unsaved');
    }
  };

  const handleFieldChange = (field, value) => {
    setPsychologyEntry(prev => ({ ...prev, [field]: value }));
    setAutoSaveStatus('unsaved');
  };

  const savePsychologyToBackend = async () => {
    if (!selectedTrade) return false;
    
    setAutoSaveStatus('saving');
    try {
      const payload = {
        trade_id: selectedTrade.id,
        discipline: psychologyEntry.discipline,
        confidence: psychologyEntry.confidence,
        followed_plan: psychologyEntry.followed_plan,
        decision_quality: psychologyEntry.decision_quality,
        emotions: psychologyEntry.emotions.join(','),
        market_condition: psychologyEntry.market_condition,
        volatility_level: psychologyEntry.volatility_level,
        notes: psychologyEntry.notes || ""
      };

      if (psychologyId) {
        // Update existing
        const response = await api.put(`/trade-psychology/${psychologyId}/`, payload);
        // We don't change the ID here since it's an update, but update lastSaved
      } else {
        // Create new
        const response = await api.post('/trade-psychology/', payload);
        setPsychologyId(response.data.id); // Save the newly created ID
      }
      
      setAutoSaveStatus('saved');
      setLastSaved(new Date());
      return true;
    } catch (err) {
      console.error("Failed to save psychology:", err);
      setAutoSaveStatus('error');
      alert(err.response?.data?.detail || "Failed to save psychology entry.");
      return false;
    }
  };

  const handleSave = async () => {
    await savePsychologyToBackend();
  };

  const handleTemplateSelect = (template) => {
    let templateText = `## ${template.name}\n\n`;
    template.sections.forEach(section => {
      templateText += `### ${section.title}\n> ${section.prompt}\n\n\n`;
    });
    
    // SMART REPLACE: If notes already contain a template, or are just a few words, replace.
    // Otherwise, ask user? or append at bottom?
    // Let's go with REPLACE by default if it looks like they are "selecting" the template.
    setPsychologyEntry(prev => ({
      ...prev,
      notes: templateText
    }));

    // FEEDBACK: Scroll to the notes editor so they see it worked
    setTimeout(() => {
      const editorElement = document.getElementById('psychology-notes-editor');
      if (editorElement) {
        editorElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 100);
  };

  const handleAutofillMock = () => {
    setPsychologyEntry({
      discipline: 'HIGH',
      confidence: 'HIGH',
      followed_plan: true,
      decision_quality: 5,
      emotions: ['confidence', 'calm', 'excitement'],
      market_condition: 'trending-up',
      volatility_level: 'medium',
      notes: "This is a mock trade review. I followed the plan perfectly, entered on a clean retest of the VWAP level, and exited at my target R:R of 2.0. Mental state was calm throughout."
    });
    setAutoSaveStatus('unsaved');
  };

  const navigateToTrades = () => {
    navigate('/trades-management');
  };

  const handlePublish = async () => {
    const success = await savePsychologyToBackend();
    if (success) {
      navigate('/trades-management');
    }
  };

  const formatLastSaved = () => {
    const now = new Date();
    const diff = Math.floor((now - lastSaved) / 1000);
    
    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)} min ago`;
    return lastSaved?.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  };

  const getAutoSaveIcon = () => {
    switch (autoSaveStatus) {
      case 'saving': return 'Loader';
      case 'saved': return 'Check';
      case 'error': return 'XCircle';
      default: return 'AlertCircle';
    }
  };

  const getAutoSaveColor = () => {
    switch (autoSaveStatus) {
      case 'saving': return 'text-warning';
      case 'saved': return 'text-success';
      case 'error': return 'text-error';
      default: return 'text-muted-foreground';
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <AuthenticatedHeader />
      <PrimaryNavigation />
      <AccountContextBar onAccountChange={setSelectedAccount} />
      <main className="main-content with-account-context">
        <div className="main-content-container">
          <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 mb-6 md:mb-8">
            <div>
              <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold text-foreground mb-2">
                Trade Psychology Editor
              </h1>
              <p className="text-sm md:text-base text-muted-foreground">
                Review specific trades and log your mental state and discipline
              </p>
            </div>

            <div className="flex items-center gap-3 w-full lg:w-auto">
              {activeView === 'editor' && selectedTrade && (
                <div className={`flex items-center gap-2 text-xs md:text-sm ${getAutoSaveColor()}`}>
                  <Icon 
                    name={getAutoSaveIcon()} 
                    size={16} 
                    className={autoSaveStatus === 'saving' ? 'animate-spin' : ''} 
                  />
                  <span>
                    {autoSaveStatus === 'saved' ? `Saved ${formatLastSaved()}` : 
                     autoSaveStatus === 'saving' ? 'Saving...' : 
                     autoSaveStatus === 'error' ? 'Save Failed' : 'Unsaved changes'}
                  </span>
                </div>
              )}
              <Button
                variant="outline"
                size="default"
                onClick={handleSave}
                iconName="Save"
                iconPosition="left"
                disabled={autoSaveStatus === 'saving' || !selectedTrade || activeView !== 'editor'}
                className="flex-1 lg:flex-initial"
              >
                Save
              </Button>
              <Button
                variant="outline"
                size="default"
                onClick={handleAutofillMock}
                iconName="Zap"
                disabled={activeView !== 'editor'}
                title="Populate with realistic mock data for testing"
              >
                Mock Data
              </Button>
              <Button
                variant="default"
                size="default"
                onClick={handlePublish}
                iconName="CheckCircle"
                iconPosition="left"
                disabled={autoSaveStatus === 'saving' || !selectedTrade || activeView !== 'editor'}
                className="flex-1 lg:flex-initial"
                title="Saves your notes and returns to the trade list"
              >
                {autoSaveStatus === 'saving' ? 'Saving...' : 'Complete & Review'}
              </Button>
            </div>
          </div>

          <div className="flex gap-2 mb-6 border-b border-border">
            <button
              onClick={() => setActiveView('history')}
              className={`px-4 md:px-6 py-3 text-sm md:text-base font-medium transition-all duration-250 border-b-2 ${
                activeView === 'history' ? 'text-primary border-primary' : 'text-muted-foreground border-transparent hover:text-foreground'
              }`}
            >
              <Icon name="List" size={18} className="inline mr-2" />
              Trade List
            </button>
            <button
              onClick={() => setActiveView('editor')}
              disabled={!selectedTrade}
              className={`px-4 md:px-6 py-3 text-sm md:text-base font-medium transition-all duration-250 border-b-2 ${
                activeView === 'editor' ? 'text-primary border-primary' : 'text-muted-foreground border-transparent hover:text-foreground'
              } ${!selectedTrade ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <Icon name="Edit" size={18} className="inline mr-2" />
              Editor
            </button>
          </div>

          {activeView === 'history' ? (
            <div className="space-y-6">
              <div className="bg-card border border-border rounded-lg p-4 md:p-6 mb-6">
                 <p className="text-muted-foreground text-sm">Select a trade below to document its psychology, discipline, and lessons learned.</p>
              </div>

              {isLoadingTrades ? (
                 <div className="text-center py-10 text-muted-foreground animate-pulse">Loading trades...</div>
              ) : trades.length === 0 ? (
                 <div className="text-center py-10 bg-card border border-border rounded-lg text-muted-foreground">
                    No trades found for this account. Go to Trades to add some.
                 </div>
              ) : (
                <div className="grid grid-cols-1 gap-4 md:gap-6">
                  {trades.map((entry) => (
                    <div
                      key={entry.id}
                      className="bg-card border border-border rounded-lg p-4 md:p-6 hover:border-accent/50 transition-all duration-250 cursor-pointer"
                      onClick={() => handleSelectTrade(entry)}
                    >
                      <div className="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-2">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <h3 className="text-base md:text-lg font-semibold text-foreground">{entry.symbol}</h3>
                            <span className={`text-xs md:text-sm font-medium px-2 py-0.5 rounded-full ${entry.side?.toUpperCase() === 'BUY' || entry.side?.toUpperCase() === 'LONG' ? 'bg-success/10 text-success' : 'bg-error/10 text-error'}`}>
                              {entry.side?.toUpperCase()}
                            </span>
                            <span className={`text-sm md:text-base font-semibold ${entry.pnl >= 0 ? 'text-success' : 'text-error'}`}>
                              {entry.pnl !== null && entry.pnl !== undefined ? `${entry.pnl >= 0 ? '+' : ''}$${Math.abs(entry.pnl).toFixed(2)}` : 'Open'}
                            </span>
                          </div>
                          <p className="text-xs md:text-sm text-muted-foreground">
                            {new Date(entry.open_timestamp || entry.created_at).toLocaleDateString('en-US', { 
                              month: 'short', 
                              day: 'numeric', 
                              year: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </p>
                        </div>
                        <div className="flex items-center gap-2">
                           <Button variant="outline" size="sm" iconName="Edit">
                             Write Journal
                           </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8">
              <div className="lg:col-span-2 space-y-6 md:space-y-8">
                
                {selectedTrade && (
                  <>
                    {/* Trade Reference Section */}
                    <TradeReferencePanel tradeData={selectedTrade} />

                    {/* Psychology Entry Form */}
                    <div className="bg-card border border-border rounded-lg p-4 md:p-6 space-y-6 md:space-y-8">
                  
                  {/* Discipline and Confidence Pickers */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-foreground mb-2">Discipline Level</label>
                      <select 
                        className="w-full px-3 py-2 bg-background border border-input rounded-lg text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                        value={psychologyEntry.discipline}
                        onChange={(e) => handleFieldChange('discipline', e.target.value)}
                      >
                        <option value="LOW">Low (Emotional / Impulsive)</option>
                        <option value="MEDIUM">Medium (Mostly controlled)</option>
                        <option value="HIGH">High (Calculated / Strict)</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-foreground mb-2">Confidence Level</label>
                      <select 
                        className="w-full px-3 py-2 bg-background border border-input rounded-lg text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                        value={psychologyEntry.confidence}
                        onChange={(e) => handleFieldChange('confidence', e.target.value)}
                      >
                        <option value="LOW">Low (Uncertain / Fearful)</option>
                        <option value="MEDIUM">Medium (Normal conviction)</option>
                        <option value="HIGH">High (Absolute conviction)</option>
                      </select>
                    </div>
                  </div>

                  {/* Decision Quality Rating */}
                  <DecisionQualityRating 
                    rating={psychologyEntry.decision_quality}
                    onRatingChange={(val) => handleFieldChange('decision_quality', val)}
                  />

                  {/* Emotion Tag Selector */}
                  <EmotionTagSelector 
                    selectedEmotions={psychologyEntry.emotions}
                    onEmotionToggle={(id) => {
                      const current = [...psychologyEntry.emotions];
                      if (current.includes(id)) {
                        handleFieldChange('emotions', current.filter(e => e !== id));
                      } else {
                        handleFieldChange('emotions', [...current, id]);
                      }
                    }}
                  />

                  {/* Market Condition Assessment */}
                  <MarketConditionAssessment 
                    marketCondition={psychologyEntry.market_condition}
                    onConditionChange={(val) => handleFieldChange('market_condition', val)}
                    volatility={psychologyEntry.volatility_level}
                    onVolatilityChange={(val) => handleFieldChange('volatility_level', val)}
                  />

                  {/* Template Prompts */}
                  <div className="pt-6 border-t border-border">
                    <TemplatePrompts onTemplateSelect={handleTemplateSelect} />
                  </div>

                  {/* Followed Plan Toggle */}
                  <div className="flex items-center justify-between py-4 border-t border-b border-border">
                    <div>
                      <h4 className="font-medium text-foreground">Followed Trading Plan</h4>
                      <p className="text-sm text-muted-foreground">Did you strictly stick to your predetermined plan for this trade?</p>
                    </div>
                    <button 
                      type="button"
                      onClick={() => handleFieldChange('followed_plan', !psychologyEntry.followed_plan)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${psychologyEntry.followed_plan ? 'bg-success' : 'bg-muted'}`}
                    >
                      <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${psychologyEntry.followed_plan ? 'translate-x-6' : 'translate-x-1'}`} />
                    </button>
                  </div>
                </div>

                <div id="psychology-notes-editor" className="bg-card border border-border rounded-lg p-4 md:p-6 space-y-6">
                  <RichTextEditor
                    label="End of Trade Notes & Lessons"
                    value={psychologyEntry.notes}
                    onChange={(value) => handleFieldChange('notes', value)}
                    placeholder="Document your mindset, mistakes to learn from, and what you did well during this trade..."
                  />
                  </div>
                </>
              )}
            </div>

            <div className="space-y-6">
              <div className="bg-card border border-border rounded-lg p-4 md:p-6">
                <h3 className="text-base md:text-lg font-semibold text-foreground mb-4">Quick Tips</h3>
                  <div className="space-y-3">
                    <div className="flex items-start gap-3">
                      <Icon name="Lightbulb" size={18} className="text-warning flex-shrink-0 mt-0.5" />
                      <p className="text-xs md:text-sm text-muted-foreground">
                        Be honest about deviation from your plan - this journal is for your improvement.
                      </p>
                    </div>
                    <div className="flex items-start gap-3">
                      <Icon name="Target" size={18} className="text-success flex-shrink-0 mt-0.5" />
                      <p className="text-xs md:text-sm text-muted-foreground">
                        Focus on building discipline over hitting high PnL targets. Good decisions often have bad results in a probabilistic system.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default TradePsychologyEditor;