import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import TradeMediaUploader from './TradeMediaUploader';

const TradeDetailsView = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [loading, setLoading] = useState(true);
  const [trade, setTrade] = useState(null);
  const [showMediaUploader, setShowMediaUploader] = useState(false);
  const [newMedia, setNewMedia] = useState([]);
  const [uploadingMedia, setUploadingMedia] = useState(false);

  useEffect(() => {
    fetchTrade();
  }, [id]);

  const fetchTrade = async () => {
    try {
      const token = localStorage.getItem('trader_token');
      const response = await axios?.get(
        `${import.meta.env?.VITE_API_BASE_URL}/api/v1/trades/${id}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setTrade(response?.data);
    } catch (error) {
      console.error('Failed to fetch trade:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadMedia = async () => {
    if (newMedia?.length === 0) return;

    setUploadingMedia(true);
    try {
      const token = localStorage.getItem('trader_token');
      const formData = new FormData();
      
      newMedia?.forEach((item) => {
        if (item?.file) {
          formData?.append('files', item?.file);
        }
      });

      await axios?.post(
        `${import.meta.env?.VITE_API_BASE_URL}/api/v1/trades/${id}/media`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      setNewMedia([]);
      setShowMediaUploader(false);
      fetchTrade();
    } catch (error) {
      console.error('Failed to upload media:', error);
    } finally {
      setUploadingMedia(false);
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    })?.format(value || 0);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '—';
    return new Date(dateString)?.toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const images = trade?.media?.filter(m => m?.type === 'image') || [];
  const audios = trade?.media?.filter(m => m?.type === 'audio') || [];

  if (loading) {
    return (
      <div className="bg-card border border-border rounded-lg p-12 text-center">
        <div className="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
        <p className="text-sm text-muted-foreground">Loading trade details...</p>
      </div>
    );
  }

  if (!trade) {
    return (
      <div className="bg-card border border-border rounded-lg p-12 text-center">
        <Icon name="AlertCircle" size={48} className="mx-auto text-destructive mb-4" />
        <h3 className="text-lg font-semibold text-foreground mb-2">Trade not found</h3>
        <Button variant="outline" onClick={() => navigate('/trades-management')}>Back to Trades</Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-card border border-border rounded-lg p-6">
        <div className="flex items-start justify-between mb-6">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h2 className="text-3xl font-bold text-foreground">{trade?.symbol}</h2>
              <span className={`text-sm px-3 py-1 rounded ${
                trade?.side === 'BUY' ? 'bg-success/10 text-success' : 'bg-destructive/10 text-destructive'
              }`}>
                {trade?.side}
              </span>
            </div>
            <p className="text-sm text-muted-foreground">Trade ID: {trade?.id}</p>
          </div>
          <Button
            variant="outline"
            iconName="Edit"
            iconPosition="left"
            onClick={() => navigate(`/trades-management/edit/${id}`)}
          >
            Edit Trade
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-muted/50 rounded-lg p-4">
            <p className="text-sm text-muted-foreground mb-1">Quantity</p>
            <p className="text-2xl font-bold text-foreground">{trade?.quantity}</p>
          </div>
          <div className="bg-muted/50 rounded-lg p-4">
            <p className="text-sm text-muted-foreground mb-1">Entry Price</p>
            <p className="text-2xl font-bold text-foreground">{formatCurrency(trade?.entry_price)}</p>
          </div>
          <div className="bg-muted/50 rounded-lg p-4">
            <p className="text-sm text-muted-foreground mb-1">Risk/Reward</p>
            <p className="text-2xl font-bold text-foreground">{trade?.risk_reward}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <h3 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
              <Icon name="TrendingUp" size={16} />
              Strategy & Plan
            </h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Strategy:</span>
                <span className="text-sm font-medium text-foreground">{trade?.strategy?.name || '—'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Plan:</span>
                <span className="text-sm font-medium text-foreground">{trade?.plan?.name || '—'}</span>
              </div>
            </div>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
              <Icon name="Heart" size={16} />
              Psychology
            </h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Pre-Trade Emotion:</span>
                <span className="text-sm font-medium text-foreground capitalize">{trade?.pre_trade_emotion}</span>
              </div>
            </div>
          </div>
        </div>

        {trade?.notes && (
          <div>
            <h3 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
              <Icon name="FileText" size={16} />
              Trade Notes
            </h3>
            <div className="bg-muted/50 rounded-lg p-4">
              <p className="text-sm text-foreground whitespace-pre-wrap">{trade?.notes}</p>
            </div>
          </div>
        )}
      </div>

      <div className="bg-card border border-border rounded-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-foreground">Media Attachments</h3>
          <Button
            variant="outline"
            size="sm"
            iconName="Plus"
            iconPosition="left"
            onClick={() => setShowMediaUploader(!showMediaUploader)}
          >
            Add More Media
          </Button>
        </div>

        {showMediaUploader && (
          <div className="mb-6 p-4 bg-muted/30 rounded-lg border border-border">
            <TradeMediaUploader media={newMedia} onChange={setNewMedia} />
            <div className="flex gap-3 mt-4">
              <Button
                variant="default"
                size="sm"
                onClick={handleUploadMedia}
                loading={uploadingMedia}
                disabled={newMedia?.length === 0}
              >
                Upload Media
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  setShowMediaUploader(false);
                  setNewMedia([]);
                }}
              >
                Cancel
              </Button>
            </div>
          </div>
        )}

        {images?.length > 0 && (
          <div className="mb-6">
            <h4 className="text-sm font-medium text-muted-foreground mb-3 flex items-center gap-2">
              <Icon name="Image" size={16} />
              Screenshots ({images?.length})
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {images?.map((img, index) => (
                <div key={index} className="relative group cursor-pointer">
                  <img
                    src={img?.url}
                    alt={img?.name || `Screenshot ${index + 1}`}
                    className="w-full h-48 object-cover rounded-lg border border-border hover:border-primary transition-colors"
                  />
                  <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity rounded-lg flex items-center justify-center">
                    <Icon name="ZoomIn" size={32} className="text-white" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {audios?.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-muted-foreground mb-3 flex items-center gap-2">
              <Icon name="Mic" size={16} />
              Voice Notes ({audios?.length})
            </h4>
            <div className="space-y-3">
              {audios?.map((audio, index) => (
                <div key={index} className="flex items-center gap-4 p-4 bg-muted/50 rounded-lg border border-border">
                  <Icon name="Music" size={24} className="text-primary flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground truncate">{audio?.name || `Voice Note ${index + 1}`}</p>
                    <p className="text-xs text-muted-foreground">{formatDate(audio?.created_at)}</p>
                  </div>
                  <audio controls className="h-10">
                    <source src={audio?.url} />
                  </audio>
                </div>
              ))}
            </div>
          </div>
        )}

        {images?.length === 0 && audios?.length === 0 && !showMediaUploader && (
          <div className="text-center py-12">
            <Icon name="Upload" size={48} className="mx-auto text-muted-foreground mb-4" />
            <p className="text-sm text-muted-foreground mb-4">No media attached to this trade</p>
            <Button
              variant="outline"
              size="sm"
              iconName="Plus"
              iconPosition="left"
              onClick={() => setShowMediaUploader(true)}
            >
              Add Media
            </Button>
          </div>
        )}
      </div>

      <div className="flex gap-3">
        <Button
          variant="outline"
          iconName="ArrowLeft"
          iconPosition="left"
          onClick={() => navigate('/trades-management')}
        >
          Back to Trades
        </Button>
      </div>
    </div>
  );
};

export default TradeDetailsView;