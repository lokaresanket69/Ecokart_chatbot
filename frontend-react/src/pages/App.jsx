import React from 'react';
import Container from '@mui/material/Container';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import DarkModeIcon from '@mui/icons-material/Brightness4Rounded';
import LightModeIcon from '@mui/icons-material/LightModeRounded';

import ChatWindow from '../ui/ChatWindow';

export default function App({ darkMode, toggleDark }) {
  return (
    <Container maxWidth="sm" sx={{ minHeight: '100vh', py: 4 }}>
      <Stack spacing={2} sx={{ height: '100%' }}>
        <Stack direction="row" alignItems="center" justifyContent="space-between">
          <Typography variant="h5" fontWeight={600} component="h1">
            EcoKart FAQ Chatbot
          </Typography>
          <Tooltip title="Toggle Dark / Light mode">
            <IconButton onClick={toggleDark} size="large" color="primary">
              {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
          </Tooltip>
        </Stack>

        <ChatWindow />
      </Stack>
    </Container>
  );
}
