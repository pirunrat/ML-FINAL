import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Navbar from './Navbar';
import '../css/HomePage.css';
import '../css/Card.css';
import '../css/Main_Content.css';
import '../css/Navbar.css'
import SliderCard from './SliderCard';
import ProductMain from './ProductMain';
import HttpRequestUtils from './HttpRequest';


const HomePage = ({ setAuthenticated  }) => {

  const [slideIndex, setSlideIndex] = useState(0);
  const [products, setProducts] = useState([]);
  const [recommendedProducts, setRecommendedProduct]  = useState([])
  


  useEffect(() =>{

    HttpRequestUtils.get('/product_normal').then(response =>{
    setProducts(response.data);
  })


  const username = localStorage.getItem('username')
  // HttpRequestUtils.post('/make_recommendations',username).then(response =>{
  //   setRecommendedProduct(response.data);
  // })

  axios.post('http://localhost:5000/make_recommendations',username).then((res)=>{

    console.log(res.data)
    setRecommendedProduct(res.data)

  }).catch((error)=>{
  
    console.error('POST request failed:', error);
  });

  
  },[])
  
  

  const slide = (n) => {
    let newIndex = slideIndex + n;
  
    if (newIndex > products.length - 5) {
      newIndex = 0;
    } else if (newIndex < 0) {
      newIndex = products.length - 5;
    }
    
    setSlideIndex(newIndex);
  }


  
  return (
            <div className='main-background'>
              <Navbar setAuthenticated={setAuthenticated} />
                <div className='content'>
                  <h1>Recommend</h1>
                  <SliderCard products={recommendedProducts} slideIndex={slideIndex} slide={slide} />
                  <ProductMain products={products}/>
                </div>
              </div>
          );
        };

export default HomePage;
