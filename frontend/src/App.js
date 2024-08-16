import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import PigeonSaleList from './PigeonSaleList';
import PigeonEnclosure from './PigeonEnclosure';
import CurrentBalance from './CurrentBalance';
import CurrentIncome from './Income';
import useFetch from './UseFetch';
import graph from './assets/image.png';

function App() {
    const {data: pigeons, error:pigeonsError } = useFetch('http://127.0.0.1:5000/api/get-pigeons');
    const {data: pigeonsForSale, error:pigeonsForSaleError } = useFetch('http://127.0.0.1:5000/api/get-pigeons-for-sale');
    const {data: initialBalance, error:currentBalanceError } = useFetch('http://127.0.0.1:5000/api/get-balance');
    const {data: currentIncome, error:currentIncomeError } = useFetch('http://127.0.0.1:5000/api/get-income');

    const [currentBalance, setCurrentBalance] = useState(initialBalance);

    useEffect(() => {
        const fetchBalance = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/get-balance');
                setCurrentBalance(response.data);
            } catch (error) {
                console.error('Error fetching balance:', error);
            }
        };
        const MINUTE_MS = 1000;

        const interval = setInterval(fetchBalance, MINUTE_MS);

        // Cleanup on unmount
        return () => clearInterval(interval);
    }, []);


    return (   
        <div className="padding-container">
            <div className="curved-box">
                <div className="App">
                    <header className="App-header">
                        <h1>Pigeon Tycoon</h1>
                    </header>
                    <div class="page-break"></div>
                    <div class="container">
                        <div class="page-column">
                            <div class="sub-column-container">
                                <div class="column">
                                    <div class="invisible-break"></div>
                                    <div class="subtitle">Balance</div>
                                    <div class="info-box">
                                        <CurrentBalance balance={currentBalance}/>
                                    </div>
                                </div>
                                <div class="column">
                                    <div class="invisible-break"></div>
                                    <div class="subtitle">Income</div>
                                    <div class="info-box">
                                        <CurrentIncome income={currentIncome}/>
                                    </div>
                                </div>
                                {/* <div class="column">
                                    <div class="invisible-break"></div>
                                    <div class="subtitle">Events</div>
                                    <div class="info-box">
                                        <p>Storm</p>
                                    </div>
                                </div> */}
                            </div>
                            <div class="sub-column-container">
                                <div class="column">
                                    <div class="invisible-break"></div>
                                    <div class="subtitle">Fiances</div>
                                </div>
                                <div class="column">
                                    <div class="invisible-break"></div>
                                    <div class="subtitle">Events</div>
                                </div>
                            </div>
                            <div class="invisible-break"></div>
                            <div class="subtitle">More Management Things</div>
                        </div>
                        <div class="page-column">
                            <div class="invisible-break"></div>
                            <div class="subtitle">Enclosures</div>
                            <div class="enclosure-box">
                                <PigeonEnclosure pigeons={pigeons} />
                            </div>
                        </div>
                        <div class="page-column">
                            <div class="invisible-break"></div>
                            <div class="subtitle">Stocks</div>
                            <img src={graph} width={350} height={250} ></img>
                            <div class="invisible-break"></div>
                            <div class="subtitle">Market</div>
                            <div class="for-sale-box">
                                <PigeonSaleList pigeons={pigeonsForSale} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;