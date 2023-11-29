import React, { useEffect, useState } from 'react';
import '../css/Register.css';
import RatingModal from './RatingModal';
import HttpRequestUtils from './HttpRequest';
import { useNavigate } from 'react-router-dom';


function Register({setAuthenticated}) {

    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        interest:[]
    });

  
    const navigate = useNavigate();
    const [openModalProductIndex, setOpenModalProductIndex] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(null);
    const [Products, setProducts] = useState([]);
    const [ratedProducts, setRatedProducts] = useState([]);
    const [recommendedProduct, setRecommendedProduct] = useState({})
   


    const isModalOpenForProduct = (index) => {
        return isModalOpen && openModalProductIndex === index;
    };



    const onRate = (productId, rateValue) => {
       
        setRatedProducts(prevRated => [
            ...prevRated,
            { productId: productId, rateValue: rateValue,}
        ]);

        if(ratedProducts.length !== 5){
          setOpenModalProductIndex((prevIndex) => prevIndex + 1);
        }

      };



      useEffect(() => {
        console.log(ratedProducts.length)

        if(ratedProducts.length === 5){

          setIsModalOpen(false);

          setOpenModalProductIndex(null);

          setRecommendedProduct({
            username : formData.username,
            ratedproduct : ratedProducts
          })      

         

        }
    }, [openModalProductIndex]);
        


    useEffect(() =>{
      if(isModalOpen === false){
        HttpRequestUtils.post('/product_rated_recommend', recommendedProduct)
          .then((response) => {
            console.log(response.data);

          })
          .catch((error) => {
            console.error('Error:', error);
          });

      }
       
    },[isModalOpen])

  


    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevState) => ({
            ...prevState,
            [name]: value,
        }));
    };



    const handleSubmit = (e) => {
        e.preventDefault();

      HttpRequestUtils.post('/Register', formData)
          .then((response) => {
            console.log(response.data);

            setFormData({
              username: '',
              email: '',
              password: '',
              confirmPassword: '',
              interest:[]
            })

          })
          .catch((error) => {
            console.error('Error:', error);
          });

        if (Products.length > 0) {
            setOpenModalProductIndex(0); 
            setIsModalOpen(true);
        }

    };

  



    useEffect(() =>{
        HttpRequestUtils.get('/product_recommend_register').then(response =>{
        setProducts(response.data);
      })
      
      },[])



    return (
    <div className='register-main'>
        <div className="register">
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input type="text" name="username" value={formData.username} onChange={handleChange} required />
                </div>
                <div>
                    <label>Email:</label>
                    <input type="email" name="email" value={formData.email} onChange={handleChange} required />
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" name="password" value={formData.password} onChange={handleChange} required />
                </div>
                <div>
                    <label>Confirm Password:</label>
                    <input type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} required />
                </div>
                <button type="submit">Register</button>
            </form>
        </div>
             {/* Modal */}

             {isModalOpen && (
                <div className='modal'>
                    {Products.map((product, index) => (
                    <RatingModal 
                        key={product.asin}
                        isOpen={isModalOpenForProduct(index)}
                        onClose={() => setOpenModalProductIndex(null)}
                        product={product}
                        onRate={onRate}
                    />
                    ))}
                   
                </div>
             )}
    </div>   
    );
}

export default Register;
