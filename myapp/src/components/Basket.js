import React, { useState, useEffect } from 'react';
import '../css/Basket.css';
import '../css/HomePage.css';
import '../css/App.css';
import Navbar from './Navbar';
import RatingModal from './RatingModal';
import HttpRequestUtils from './HttpRequest';

const Basket = ({ setAuthenticated, productAdded, setproductAdded }) => {

    const [openModalProductIndex, setOpenModalProductIndex] = useState(null);
    const [ratedProducts, setRatedProducts] = useState([]);
    const[isModelOpen, setIsModalOpen] = useState(false);
    const [lastRatedProduct, setLastRatedProduct] = useState(0)
    const [recommendedProduct, setRecommendedProduct] = useState({})





    const isModalOpenForProduct = (index) => {
        return isModelOpen && openModalProductIndex === index;
    };



    const onRate = (productId, rateValue) => {
    
        // Update the state with the new rating
        setRatedProducts(prevRated => [
            ...prevRated,
            { productId: productId, rateValue: rateValue }
        ]);
    }


    useEffect(() => {

        const token = localStorage.getItem('token');
        HttpRequestUtils.setToken(token);

        // Check if this is the last product in the list
        const isLastProduct = ratedProducts.length === productAdded.length;
      
        if (isLastProduct) {
          setIsModalOpen(false); // Close the modal
          setOpenModalProductIndex(null); // Reset the modal index
          setLastRatedProduct(1);
      
          setRecommendedProduct({
            username: localStorage.getItem('username'),
            ratedproduct: ratedProducts,
          });
        } else {
          setOpenModalProductIndex((prevIndex) => prevIndex + 1); // Move to the next product
        }
      }, [ratedProducts]);



    useEffect(() => {
        if (lastRatedProduct === 1) {
        
          const token = localStorage.getItem('token');
          HttpRequestUtils.setToken(token);

          HttpRequestUtils.post('/Update_Rated_Recommend', recommendedProduct)
            .then((response) => {
              console.log(response.data);
            })
            .catch((error) => {
              console.error('Error:', error);
            });

            setLastRatedProduct(0);
        }
      }, [lastRatedProduct, recommendedProduct])



    const deleteProductFromCart = (index) => {
        const newItems = [...productAdded];
        newItems.splice(index, 1);
        setproductAdded(newItems);
    };




    return (
        <div className='main-background-basket'>
            <Navbar setAuthenticated={setAuthenticated} />
            <div className='main-basket-content'>
                <h2>Available Items</h2>
                <button className='buy-button' onClick={() => {
                    
                    if (productAdded.length > 0) {
                        setOpenModalProductIndex(0);  
                        setIsModalOpen(true);
                    }
                }}>
                    Buy
                </button>
                <ul>
                    {productAdded.map((product, index) => (
                        <li key={index}>
                            {product.title}
                            <button onClick={() => deleteProductFromCart(index)}>Delete</button>
                        </li>
                    ))}
                </ul>
            </div>
            {productAdded.map((product, index) => (
                <RatingModal 
                    key={product.asin}
                    isOpen={isModalOpenForProduct(index)}
                    onClose={() => setOpenModalProductIndex(null)}
                    product={product}
                    onRate={onRate}
                />
            ))}
        </div>
    );
};


export default Basket;
