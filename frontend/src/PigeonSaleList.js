import React from 'react';
import './App.css';

const PigeonSaleList = ({ pigeons = [] }) => {

    const buyPigeon = (pigeon_name, pigeon_id) => {
        const url = 'http://127.0.0.1:5000/api/buy-pigeon';

        const payload = {
            pigeon_id: pigeon_id
        };

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        })
        .then(response => {
            if (!response.status === 200) {
                if (response.error === 400) {
                    throw new Error('You do not have enough money to buy this pigeon');
                }
                else{
                throw new Error('Failed to buy pigeon');
                }
            }
            return response.json();
        })
        .then(data => {
            alert(`${pigeon_name} has been bought!`);
        })
        .catch(error => {
            alert('Error: ' + error.message);
        });
                
    }

    if (!Array.isArray(pigeons)) {
        return <div>No pigeons available</div>;
    }
    return (
        <div className="container">
            {pigeons.map(pigeon => (
                <div className="pigeon-card" key={pigeon.id}>
                    <div className="row">
                        <div className="column">
                            {/* <img src={pigeon.photoUrl} alt={pigeon.name} style={{ width: '100%', borderRadius: '10px' }} /> */}
                            <p>{pigeon.name}</p>
                        </div>
                        <div className="column">
                            <div className="stats">
                                <p>Speed: {pigeon.speed}</p>
                                <p>Stamina: {pigeon.stamina}</p>
                            </div>
                        </div>
                        <div className="column">
                            <p>£{pigeon.price}</p>
                        </div>
                        <div className="column">
                            <button className="buy-button" onClick={() => buyPigeon(pigeon.name, pigeon.id)}>buy</button>
                        </div>
                    </div>
                    <div className="thin-break"></div>
                </div>
            ))}
        </div>

    );
}

export default PigeonSaleList;