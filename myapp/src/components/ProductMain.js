import '../css/ProductMain.css';
import { useState, useEffect } from 'react';
import { useNavigate  } from 'react-router-dom';
import Product from './Product';
import image from '../images/anonymous.png'

const ProductMain = ({ products = [] }) => {
    const navigate = useNavigate();
    
    const [productList, setProductList] = useState(products);

    const handleProductClick = (product) => {
        setProductList([...productList, product])
        navigate(`/Product/${product.asin}`, { state: { product } });
        // navigate(`/Product/${product.title}` );
    }

    useEffect(() => {
        
    }, [productList]);

    return (
        <div className='main-content'>
            {products.map((product, index) => (   // Use productList here instead of products
                <div className='card-content' key={index} onClick={() => handleProductClick(product)}>
                    <h4>{product.title}</h4>
                    {product.imageURL ? (
                        <img src={product.imageURL} alt={product.title} />
                        ) : (
                        <img src={image} alt={product.title} />
                    )}
                    <div className="product-info">
                        <div className='product-description'>
                            <p>{product.description}</p>
                        </div>
                        <div className='product-price'>
                            <p> {product.price} baht</p>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default ProductMain;
