import React from 'react';
import { CssBaseline, Container, Typography, Box } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import FlightSearchForm from './components/FlightSearchForm';

const theme = createTheme({
  palette: {
    primary: {
      main: '#FF6B00', // Orange theme as specified
    },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md">
        <Box sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center', 
          mt: 4 
        }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Flight Booking Search
          </Typography>
          <FlightSearchForm />
        </Box>
      </Container>
    </ThemeProvider>
  );
};

export default App;