import React from 'react';
import './App.css';

const CurrentBalance = ({ balance }) => {
    if (balance === null) {
        return <div>Balance not available</div>;
    }

    return (
        <p>£{Math.round(balance.balance * 100) / 100}</p> // Ensure proper formatting with rounding
    );
}

export default CurrentBalance;