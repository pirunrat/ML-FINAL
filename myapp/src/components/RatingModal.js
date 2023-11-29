import React, { useState, useRef, useEffect } from 'react';
import '../css/RatingModal.css';

const RatingModal = ({ isOpen, onClose, product, onRate }) => {
    const [rating, setRating] = useState(null);

    // Use a ref to get the modal container element
    const modalRef = useRef(null);

    // Listen for clicks outside the modal
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (modalRef.current && !modalRef.current.contains(event.target)) {
                onClose();
            }
        };

        if (isOpen) {
            document.addEventListener('mousedown', handleClickOutside);
        } else {
            document.removeEventListener('mousedown', handleClickOutside);
        }

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [isOpen, onClose]);

    const handleRate = (rate) => {
        setRating(rate);
        onRate(product.asin, rate);
    };

    if (!isOpen || !product) return null;

    return (
        <div className="modal-overlay">
            <div className="rating-modal" ref={modalRef}>
                <button className="close-btn" onClick={onClose}>✖</button>
                <h3>Rate the product</h3>
                <div>
                    <h4>{product.title}</h4>
                    <div className="rating-buttons">
                        {[1, 2, 3, 4, 5].map(rateValue => (
                            <button
                                key={rateValue}
                                onClick={() => handleRate(rateValue)}
                                className={rating === rateValue ? 'active-rating' : ''}
                            >
                                {rateValue}
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RatingModal;
