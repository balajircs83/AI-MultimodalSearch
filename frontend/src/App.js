import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  TextField, 
  Button, 
  Grid, 
  Paper,
  Box,
  Tab,
  Tabs
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

function App() {
  const [searchType, setSearchType] = useState('text');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg']
    },
    maxFiles: 1,
    onDrop: async (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        await handleImageSearch(acceptedFiles[0]);
      }
    }
  });

  const handleTextSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/search/text', {
        query: query
      });
      setResults(response.data);
    } catch (error) {
      console.error('Error searching:', error);
    }
    setLoading(false);
  };

  const handleImageSearch = async (file) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await axios.post('http://localhost:8000/search/image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResults(response.data);
    } catch (error) {
      console.error('Error searching:', error);
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Multimodal Search Engine
        </Typography>

        <Tabs
          value={searchType}
          onChange={(e, newValue) => setSearchType(newValue)}
          centered
          sx={{ mb: 4 }}
        >
          <Tab label="Text Search" value="text" />
          <Tab label="Image Search" value="image" />
        </Tabs>

        {searchType === 'text' ? (
          <form onSubmit={handleTextSearch}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Enter your search query"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12}>
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  fullWidth
                  disabled={loading}
                >
                  Search
                </Button>
              </Grid>
            </Grid>
          </form>
        ) : (
          <Paper
            {...getRootProps()}
            sx={{
              p: 4,
              textAlign: 'center',
              cursor: 'pointer',
              bgcolor: isDragActive ? 'action.hover' : 'background.paper'
            }}
          >
            <input {...getInputProps()} />
            <Typography>
              {isDragActive
                ? 'Drop the image here'
                : 'Drag and drop an image here, or click to select'}
            </Typography>
          </Paper>
        )}

        {loading && (
          <Box sx={{ textAlign: 'center', my: 2 }}>
            <Typography>Searching...</Typography>
          </Box>
        )}

        {results.length > 0 && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" gutterBottom>
              Results
            </Typography>
            <Grid container spacing={2}>
              {results.map((result, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="subtitle1">
                      {result.type === 'image' ? '[Image]' : result.content}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Score: {result.score.toFixed(4)}
                    </Typography>
                    {result.metadata && (
                      <Typography variant="body2" color="text.secondary">
                        Metadata: {JSON.stringify(result.metadata)}
                      </Typography>
                    )}
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
      </Box>
    </Container>
  );
}

export default App; 