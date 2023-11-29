import React, { useState } from 'react'; 
import Dropdown from './Dropdown';  
import Basket from './Basket'
import { Link } from 'react-router-dom';

const Navbar = ({setAuthenticated}) => {
    const [selectedOption, setSelectedOption] = useState(null);
    const [isDropdownOpen, setDropdownOpen] = useState(false);
    

    const navbarComponents = [
        { label: 'Home' },
        { label: 'Services', dropdown: ['Service 1', 'Service 2', 'Service 3'] },
        { label: 'Products', dropdown: ['Product 1', 'Product 2'] },
        { label: 'Contact' },
        { label: 'Logout' },
        { label: 'Basket' }  
    ];


    const handleLogout = () => {
        localStorage.removeItem('token');  
        setDropdownOpen(false); 
        setAuthenticated(false);
    };

    const handleSelect = option => {
        setSelectedOption(option);
        setDropdownOpen(false); 
    };

    const handleDropdownClick = (item, e) => {
        e.stopPropagation();
        if (item.label === 'Logout') {
            handleLogout();
            return;  
        }
        if (item.dropdown) {
            setDropdownOpen(isDropdownOpen && isDropdownOpen.label === item.label ? null : item);
        } else {
            setDropdownOpen(null); 
        }
    };

    return (
        <div className="navbar" onClick={() => setDropdownOpen(false)}>
            {navbarComponents.map((item, index) => (
                <div className="navbar-item" key={index}>
                    {item.label === 'Basket' ? (
                        <Link to="/basket">{item.label}</Link>
                    ) : item.label === 'Contact' ? (
                        <Link to="/Contact">{item.label}</Link>
                    )    : item.label === 'Home' ? (
                            <Link to="/">{item.label}</Link>
                    ) : (
                        <a onClick={(e) => handleDropdownClick(item, e)}>{item.label}</a>
                    )}
                    {isDropdownOpen && isDropdownOpen.label === item.label && (
                        <Dropdown title={item.label} options={item.dropdown} onSelect={handleSelect} />
                    )}
                </div>
            ))}
        </div>
    );
}

export default Navbar;
