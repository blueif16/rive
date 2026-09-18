import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import Article from './Article';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Article />
  </StrictMode>,
);
