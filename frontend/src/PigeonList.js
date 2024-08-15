import React from 'react';

const PigeonList = ({ pigeons = [] }) => {
    if (!Array.isArray(pigeons)) {
        return <div>No pigeons available</div>;
    }

    return (
        <div>
            <ul>
                {pigeons.map(pigeon => (
                    <li key={pigeon.id}>{pigeon.name} - Speed: {pigeon.speed}, Stamina: {pigeon.stamina}</li>
                ))}
            </ul>
        </div>
    );
}

export default PigeonList;