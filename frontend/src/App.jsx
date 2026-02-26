import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import Home from './pages/Home';
import FurnitureList from './pages/FurnitureList';
import FurnitureDetail from './pages/FurnitureDetail';
import UploadRoom from './pages/UploadRoom';
import AISuggestions from './pages/AISuggestions';
import ARViewer from './pages/ARViewer';
import NotFound from './pages/NotFound';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="furniture" element={<FurnitureList />} />
        <Route path="furniture/:id" element={<FurnitureDetail />} />
        <Route path="upload" element={<UploadRoom />} />
        <Route path="suggestions" element={<AISuggestions />} />
        <Route path="ar" element={<ARViewer />} />
        <Route path="ar/:id" element={<ARViewer />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
