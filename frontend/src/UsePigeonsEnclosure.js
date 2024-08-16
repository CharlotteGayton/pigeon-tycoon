import { useState, useEffect } from 'react';
import axios from 'axios';

const usePigeonsEnclosure = () => {
    const [pigeonsEnclosure, setPigeonsEnclosure] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPigeonsEnclosure = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/get-pigeons');
                setPigeonsEnclosure(response.data);
            } catch (error) {
                setError(error);
                console.error("Error fetching pigeons for sale:", error);
            }
        };

        fetchPigeonsEnclosure();
    }, []);

    const refreshPigeonsEnclosure = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/get-pigeons');
            setPigeonsEnclosure(response.data);
        } catch (error) {
            setError(error);
            console.error("Error refreshing pigeons for sale:", error);
        }
    };

    return { pigeonsEnclosure, error, refreshPigeonsEnclosure };
};

export default usePigeonsEnclosure;
