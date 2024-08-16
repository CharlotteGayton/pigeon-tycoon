import { useState, useEffect } from 'react';
import axios from 'axios';

const usePigeonsForSale = () => {
    const [pigeonsForSale, setPigeonsForSale] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPigeonsForSale = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/get-pigeons-for-sale');
                setPigeonsForSale(response.data);
            } catch (error) {
                setError(error);
                console.error("Error fetching pigeons for sale:", error);
            }
        };

        fetchPigeonsForSale();
    }, []);

    const refreshPigeonsForSale = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/get-pigeons-for-sale');
            setPigeonsForSale(response.data);
        } catch (error) {
            setError(error);
            console.error("Error refreshing pigeons for sale:", error);
        }
    };

    return { pigeonsForSale, error, refreshPigeonsForSale };
};

export default usePigeonsForSale;
