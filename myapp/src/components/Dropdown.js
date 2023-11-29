import React from 'react';
import '../css/Dropdown.css'
function Dropdown({ title, options, onSelect }) {
    return (
        <div className="dropdown-menu" onClick={e => e.stopPropagation()}>
            <ul>
                {options.map((option, index) => (
                    <li key={index} onClick={() => onSelect(option)}>
                        {option}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Dropdown;