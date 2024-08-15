import React from 'react';
import './App.css';

const PigeonEnclosure = ({ pigeons = [] }) => {
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
                            <p>Cost/s: £0.01</p>
                            <p>Income/s: £0.02</p>
                        </div>
                        <div className="column">
                            <button className="options-button">options</button>
                        </div>
                    </div>
                    <div className="thin-break"></div>
                </div>
            ))}
        </div>

    );
}


export default PigeonEnclosure;