import { useEffect } from 'react';

/**
 * Handles text selection and provides "Ask AI" functionality
 */
const SelectionHandler = ({ onAskQuestion }) => {
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const selectedText = selection.toString().trim();

      if (selectedText && selectedText.length > 10) {
        // You can add a floating "Ask AI" button here if needed
        // For now, we'll just store the selection
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('touchend', handleSelection);
    };
  }, [onAskQuestion]);

  return null; // This component doesn't render anything
};

export default SelectionHandler;
