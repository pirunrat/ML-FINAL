import React from 'react';
import '../css/Card.css';
import { useNavigate } from 'react-router-dom';
import image from '../images/anonymous.png'
const SliderCard = ({ products, slideIndex, slide }) => {

  const navigate = useNavigate();
  
  const handleProductClick = (product) => {
    navigate(`/Product/${product.asin}`, { state: { product } });
  };


  const renderCard = (product, index) => (
    <div key={`${product.title}-${index}`} className="card">
      <img src={product.ImageURL} alt={product.title} />
      <h3>{product.title}</h3>
      <p>{product.description}</p>
      <p>{product.price}</p>
    </div>
  );

  return (
    <div className="slider-container">
      <button className="slide-btn prev-btn" onClick={() => slide(-5)}>❮</button>
        <div className="slider" style={{ transform: `translateX(-${slideIndex * 240}px)` }}>

            {/* {products.map((product, index) => renderCard(product, index))} */}

            {products.map((product) => (
            <div 
              key={product.id} 
              className="card" 
              onClick={() => handleProductClick(product)}
            >
              {product.imageURL ? (
                        <img src={product.imageURL} alt={product.title} />
                        ) : (
                        <img src={image} alt={product.title} />
                    )}
              <h3>{product.title}</h3>
              <p>{product.description}</p>
              <p>{product.price}</p>
            </div>
          ))}

        </div>
      <button className="slide-btn next-btn" onClick={() => slide(5)}>❯</button>
    </div>
  );
};

export default SliderCard;