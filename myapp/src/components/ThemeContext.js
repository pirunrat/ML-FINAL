import { createContext } from 'react';

export const ThemeContext = createContext({
  className: 'main-background',  // default value, can be expanded for more styles
});
