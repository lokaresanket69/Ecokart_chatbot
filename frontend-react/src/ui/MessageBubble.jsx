import React from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import { useTheme } from '@mui/material/styles';

export default function MessageBubble({ message }) {
  const theme = useTheme();
  const isUser = message.sender === 'user';
  const isDark = theme.palette.mode === 'dark';

  const bgColor = isUser
    ? theme.palette.primary.main
    : isDark
    ? theme.palette.grey[800]
    : theme.palette.grey[100];

  const textColor = isUser
    ? theme.palette.primary.contrastText
    : isDark
    ? theme.palette.grey[100]
    : theme.palette.text.primary;

  return (
    <Box display="flex" justifyContent={isUser ? 'flex-end' : 'flex-start'}>
      <Paper
        sx={{
          p: 1.2,
          px: 1.8,
          maxWidth: '80%',
          bgcolor: bgColor,
          color: textColor,
          borderBottomRightRadius: isUser ? 4 : 2,
          borderBottomLeftRadius: isUser ? 2 : 4,
          whiteSpace: 'pre-wrap',
        }}
      >
        <Typography variant="body2">{message.text}</Typography>
      </Paper>
    </Box>
  );
}
