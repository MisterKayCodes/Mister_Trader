import React, { useState, useRef, useEffect } from 'react';

import Button from '../../../components/ui/Button';

const RichTextEditor = ({ value, onChange, placeholder, label }) => {
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef(null);

  const formatText = (command) => {
    const textarea = textareaRef?.current;
    if (!textarea) return;

    const start = textarea?.selectionStart;
    const end = textarea?.selectionEnd;
    const selectedText = value?.substring(start, end);
    let newText = value;

    switch (command) {
      case 'bold':
        newText = value?.substring(0, start) + `**${selectedText}**` + value?.substring(end);
        break;
      case 'italic':
        newText = value?.substring(0, start) + `*${selectedText}*` + value?.substring(end);
        break;
      case 'heading':
        newText = value?.substring(0, start) + `### ${selectedText}` + value?.substring(end);
        break;
      case 'bullet':
        newText = value?.substring(0, start) + `\n• ${selectedText}` + value?.substring(end);
        break;
      default:
        break;
    }

    onChange(newText);
    setTimeout(() => {
      textarea?.focus();
      textarea?.setSelectionRange(start, end);
    }, 0);
  };

  const handleKeyDown = (e) => {
    if (e?.key === 'Tab') {
      e?.preventDefault();
      const start = e?.target?.selectionStart;
      const end = e?.target?.selectionEnd;
      const newValue = value?.substring(0, start) + '    ' + value?.substring(end);
      onChange(newValue);
      setTimeout(() => {
        e.target.selectionStart = e.target.selectionEnd = start + 4;
      }, 0);
    }
  };

  return (
    <div className="space-y-2">
      {label && (
        <label className="block text-sm font-medium text-foreground">
          {label}
        </label>
      )}
      <div className={`border-2 rounded-lg transition-all duration-250 ${
        isFocused ? 'border-accent' : 'border-border'
      }`}>
        <div className="flex items-center gap-1 p-2 border-b border-border bg-muted/30">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => formatText('bold')}
            iconName="Bold"
            iconSize={16}
            type="button"
            className="h-8 w-8"
          />
          <Button
            variant="ghost"
            size="sm"
            onClick={() => formatText('italic')}
            iconName="Italic"
            iconSize={16}
            type="button"
            className="h-8 w-8"
          />
          <Button
            variant="ghost"
            size="sm"
            onClick={() => formatText('heading')}
            iconName="Heading"
            iconSize={16}
            type="button"
            className="h-8 w-8"
          />
          <Button
            variant="ghost"
            size="sm"
            onClick={() => formatText('bullet')}
            iconName="List"
            iconSize={16}
            type="button"
            className="h-8 w-8"
          />
          <div className="flex-1" />
          <span className="text-xs text-muted-foreground px-2">
            {value?.length} characters
          </span>
        </div>
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => onChange(e?.target?.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className="w-full min-h-[200px] md:min-h-[300px] p-4 bg-transparent text-foreground placeholder:text-muted-foreground resize-none focus:outline-none text-sm md:text-base"
          style={{ fontFamily: 'inherit' }}
        />
      </div>
    </div>
  );
};

export default RichTextEditor;