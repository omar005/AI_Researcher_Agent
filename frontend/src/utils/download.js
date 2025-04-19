// frontend/src/utils/download.js
import { jsPDF } from 'jspdf';

// Function to convert HTML to plain text
const htmlToText = (html) => {
  const temp = document.createElement('div');
  temp.innerHTML = html;
  return temp.textContent || temp.innerText || '';
};

// Download as plain text
export const downloadAsText = (content, filename) => {
  const text = typeof content === 'string' ? content : JSON.stringify(content, null, 2);
  const blob = new Blob([text], { type: 'text/plain' });
  downloadBlob(blob, filename || 'research-results.txt');
};

// Download as PDF
export const downloadAsPDF = (content, title, filename) => {
  const doc = new jsPDF();
  
  // Add title
  doc.setFontSize(16);
  doc.text(title, 20, 20);
  
  // Add content
  doc.setFontSize(12);
  const text = typeof content === 'string' ? content : JSON.stringify(content, null, 2);
  
  // Split text into lines to fit page width
  const textLines = doc.splitTextToSize(text, 180);
  doc.text(textLines, 20, 30);
  
  // Save PDF
  doc.save(filename || 'research-results.pdf');
};

// Download as JSON
export const downloadAsJSON = (content, filename) => {
  const json = typeof content === 'object' ? content : JSON.parse(content);
  const blob = new Blob([JSON.stringify(json, null, 2)], { type: 'application/json' });
  downloadBlob(blob, filename || 'research-results.json');
};

// Download as Markdown
export const downloadAsMarkdown = (content, title, filename) => {
  let markdown = `# ${title}\n\n`;
  markdown += content;
  
  const blob = new Blob([markdown], { type: 'text/markdown' });
  downloadBlob(blob, filename || 'research-results.md');
};

// Helper function to trigger download of a Blob
const downloadBlob = (blob, filename) => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};