import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './pages/App';

import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider, createTheme } from '@mui/material/styles';

const root = ReactDOM.createRoot(document.getElementById('root'));

const AppWrapper = () => {
  const [darkMode, setDarkMode] = React.useState(false);

  const toggleDark = () => setDarkMode((p) => !p);

  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode: darkMode ? 'dark' : 'light',
          primary: {
            main: '#43c06d',
          },
          secondary: {
            main: '#29984a',
          },
        },
        shape: { borderRadius: 16 },
      }),
    [darkMode]
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App darkMode={darkMode} toggleDark={toggleDark} />
    </ThemeProvider>
  );
};

root.render(<AppWrapper />);
