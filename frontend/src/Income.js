import React from 'react';
import './App.css';

const Income = ({ income }) => {
    if (income === null) {
        return <div>Income not available</div>;
    }
    return (
        <p>£{income.income}/s</p>
    );
}

export default Income;
