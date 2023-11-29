import React from 'react';
import { render } from '@testing-library/react';
import Login from './components/Login'; // Adjust the import path as needed


test('renders Login component without crashing', () => {
  render(<Login />);
});
