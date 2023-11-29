import '../css/Product.css'
import Navbar from './Navbar';
import { useLocation, useParams } from 'react-router-dom';
import image from '../images/anonymous.png';

const Product = ({ setAuthenticated, setproductAdded, productAdded }) => {
  const location = useLocation();
  const params = useParams();

  // Encode the productName parameter
  const productNameFromURL = encodeURIComponent(params.productName);

  const productData = location.state?.product;

  // Check if productData is defined
  if (!productData) {
    return <div>No product data found!</div>;
  }

  const handleAddToCart = (prod) => {
    if (Array.isArray(productAdded)) {
      setproductAdded([...productAdded, prod]);
    } else {
      console.error('productAdded is not an array:', productAdded);
    }
  }

  return (
    <div className='main-background-product'>
      <Navbar setAuthenticated={setAuthenticated} />
      <div className='main-product-content'>
        <div className='product-content'>
          <h4>{productData.title}</h4>
          {
            productData.imageURL ? (
              <img src={productData.imageURL} alt={productData.title} />
            ) : (
              <img src={image} alt={productData.title} />
            )
          }
          <div className="product-info">
            <div className='product-description'>
              <p>{productData.description}</p>
            </div>
            <div className='product-price'>
              <p>{productData.price} baht</p>
            </div>
            <div className='product-add'>
              <button onClick={() => handleAddToCart(productData)}>Add to Cart</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Product;
