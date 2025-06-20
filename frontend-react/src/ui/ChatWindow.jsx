import React from 'react';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import SendIcon from '@mui/icons-material/SendRounded';
import CircularProgress from '@mui/material/CircularProgress';

import MessageBubble from './MessageBubble';
import ParticlesBg from './ParticlesBg';

// Read backend base URL from build-time env var (set on Render as VITE_BACKEND_URL).
// Fallback to empty string so that relative "/chat" hits same-origin (handled by Vite dev proxy locally).
const API_BASE = import.meta.env.VITE_BACKEND_URL || '';

export default function ChatWindow() {
  const [messages, setMessages] = React.useState([]);
  const [input, setInput] = React.useState('');
  const [loading, setLoading] = React.useState(false);

  const addMessage = (text, sender) => setMessages((prev) => [...prev, { text, sender }]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text) return;
    addMessage(text, 'user');
    setInput('');
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      addMessage(data.response ?? 'No response', 'bot');
    } catch (e) {
      addMessage('Error connecting to chatbot.', 'bot');
    }
    setLoading(false);
  };

  const handleKey = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <Paper elevation={3} sx={{ position: 'relative', flex: 1, overflow: 'hidden' }}>
      <ParticlesBg />
      <Stack spacing={2} sx={{ height: '100%', p: 2 }}>
        <Stack spacing={1} sx={{ flex: 1, overflowY: 'auto' }}>
          {messages.map((m, i) => (
            <MessageBubble key={i} message={m} />
          ))}
          {loading && <CircularProgress size={24} sx={{ alignSelf: 'center', mt: 1 }} />}
        </Stack>

        <Stack direction="row" spacing={1}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Ask a question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
          />
          <IconButton color="primary" onClick={sendMessage} disabled={loading}>
            <SendIcon />
          </IconButton>
        </Stack>
      </Stack>
    </Paper>
  );
}
