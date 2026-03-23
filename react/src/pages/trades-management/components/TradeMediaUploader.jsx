import React, { useState, useEffect, useRef } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const TradeMediaUploader = ({ media = [], onChange, disabled = false }) => {
  const [previews, setPreviews] = useState(media || []);

  const previewsRef = useRef(previews);
  useEffect(() => {
    previewsRef.current = previews;
  }, [previews]);

  const onChangeRef = useRef(onChange);
  useEffect(() => {
    onChangeRef.current = onChange;
  }, [onChange]);

  const processFiles = (files) => {
    if (files?.length === 0) return;

    const newPreviews = files?.map(file => ({
      id: `${Date.now()}-${Math.random()}`,
      file,
      type: file?.type?.startsWith('image/') ? 'image' : 'audio',
      url: URL.createObjectURL(file),
      name: file?.name,
      size: file?.size
    }));

    const updated = [...previewsRef.current, ...newPreviews];
    setPreviews(updated);
    onChangeRef.current?.(updated);
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e?.target?.files || []);
    processFiles(files);
  };

  useEffect(() => {
    const handleGlobalPaste = (e) => {
      if (disabled) return;

      const items = e.clipboardData?.items;
      if (!items) return;

      const pastedFiles = [];
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.startsWith('image/')) {
          const file = items[i].getAsFile();
          if (file) {
            const ext = file.type === 'image/jpeg' ? 'jpg' : file.type === 'image/png' ? 'png' : 'img';
            const newFile = new File([file], `Pasted-Image-${Date.now()}.${ext}`, { type: file.type });
            pastedFiles.push(newFile);
          }
        }
      }

      if (pastedFiles.length > 0) {
        if (!['INPUT', 'TEXTAREA'].includes(e.target.tagName)) {
           e.preventDefault();
        }
        processFiles(pastedFiles);
      }
    };

    window.addEventListener('paste', handleGlobalPaste);
    return () => window.removeEventListener('paste', handleGlobalPaste);
  }, [disabled]);

  const handleRemove = (id) => {
    const updated = previews?.filter(p => p?.id !== id);
    setPreviews(updated);
    onChange?.(updated);
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024)?.toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024))?.toFixed(1)} MB`;
  };

  const images = previews?.filter(p => p?.type === 'image') || [];
  const audios = previews?.filter(p => p?.type === 'audio') || [];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <label className="text-sm font-medium text-foreground">
          Media Attachments
        </label>
        <label className={`cursor-pointer ${disabled ? 'opacity-50 pointer-events-none' : ''}`}>
          <input
            type="file"
            multiple
            accept="image/*,audio/*"
            onChange={handleFileSelect}
            disabled={disabled}
            className="hidden"
          />
          <Button
            type="button"
            variant="outline"
            size="sm"
            iconName="Upload"
            iconPosition="left"
            disabled={disabled}
            asChild
          >
            <span>Add Media</span>
          </Button>
        </label>
      </div>

      {images?.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-muted-foreground mb-2 flex items-center gap-2">
            <Icon name="Image" size={16} />
            Images ({images?.length})
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {images?.map((img) => (
              <div key={img?.id} className="relative group">
                <img
                  src={img?.url}
                  alt={img?.name}
                  className="w-full h-32 object-cover rounded-lg border border-border"
                />
                <button
                  type="button"
                  onClick={() => handleRemove(img?.id)}
                  disabled={disabled}
                  className="absolute top-2 right-2 bg-destructive text-destructive-foreground rounded-full p-1.5 opacity-0 group-hover:opacity-100 transition-opacity disabled:opacity-50"
                >
                  <Icon name="X" size={14} />
                </button>
                <div className="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-xs p-1.5 rounded-b-lg truncate">
                  {img?.name}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {audios?.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-muted-foreground mb-2 flex items-center gap-2">
            <Icon name="Mic" size={16} />
            Voice Notes ({audios?.length})
          </h4>
          <div className="space-y-2">
            {audios?.map((audio) => (
              <div key={audio?.id} className="flex items-center gap-3 p-3 bg-muted/50 rounded-lg border border-border">
                <Icon name="Music" size={20} className="text-primary flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-foreground truncate">{audio?.name}</p>
                  <p className="text-xs text-muted-foreground">{formatFileSize(audio?.size)}</p>
                </div>
                <audio controls className="h-8 flex-shrink-0">
                  <source src={audio?.url} type={audio?.file?.type} />
                </audio>
                <button
                  type="button"
                  onClick={() => handleRemove(audio?.id)}
                  disabled={disabled}
                  className="flex-shrink-0 text-destructive hover:text-destructive/80 disabled:opacity-50"
                >
                  <Icon name="Trash2" size={18} />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {previews?.length === 0 && (
        <div className="border-2 border-dashed border-border rounded-lg p-8 text-center bg-muted/20">
          <Icon name="Upload" size={32} className="mx-auto text-muted-foreground mb-2" />
          <p className="text-sm text-foreground font-medium mb-1">Click "Add Media" or Paste Any Image From Clipboard</p>
          <p className="text-xs text-muted-foreground">Ctrl+V anywhere on this page will instantly attach the image here</p>
        </div>
      )}
    </div>
  );
};

export default TradeMediaUploader;