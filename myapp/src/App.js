import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom';
import HomePage from './components/HomePage';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Footer from './components/Footer';
import Basket from './components/Basket';
import Contact from './components/Contact';
import Product from './components/Product';
import Register from './components/Register';
import useLocalStorage from './components/useLocalStorage';
import '../src/css/Footer.css'

function App() {
  return (
      <Router>
          <AppContent />
      </Router>
  );
}

function AppContent() {
  const [authenticated, setAuthenticated] = useState(false);
  const [productAdded, setproductAdded] = useLocalStorage('productAdded', []);



  useEffect(() => {
      const token = localStorage.getItem('token');
      if (token) {
          setAuthenticated(true);
      }
  }, []);



  const handleSetAuthenticated = (value) => {
      setAuthenticated(value);
  }
  

  let location = useLocation();

  return (
    <div>
        {authenticated ? (
          <div className='App'>
            <Navbar /> {/* If you want the Navbar to always show, you can place it here. */}
            <Routes>
              <Route path="/" element={ <HomePage setAuthenticated={handleSetAuthenticated}/> } />
              <Route path="/Basket" element={ <Basket  setAuthenticated={handleSetAuthenticated} setproductAdded={setproductAdded} productAdded={productAdded}/> } />
              <Route path="/Contact" element={ <Contact setAuthenticated={handleSetAuthenticated} /> } />
              <Route path="/Product/:productName" element={ <Product setAuthenticated={handleSetAuthenticated} setproductAdded={setproductAdded} productAdded={productAdded}/> } />    
            </Routes>
            <Footer/>
          </div>
        ) :  (
          // Checking if the current location is /register to decide which component to render
          location.pathname === "/Register" ? 
            <Register setAuthenticated={handleSetAuthenticated} />
          :
            <Login setAuthenticated={handleSetAuthenticated} />
        )}
    </div>
  );
}

export default App;
