import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import PigeonList from './PigeonList';
import useFetch from './UseFetch';

function App() {
    const {data: pigeons, error:pigeonsError } = useFetch('http://127.0.0.1:5000/api/get-pigeons');
    const {data: pigeonsForSale, error:pigeonsForSaleError } = useFetch('http://127.0.0.1:5000/api/get-pigeons-for-sale');
    const {data: currentBalance, error:currentBalanceError } = useFetch('http://127.0.0.1:5000/api/get-balance');

    return (   
        <div className="padding-container">
            <div className="curved-box">
                <div className="App">
                    <header className="App-header">
                        <h1>Pigeon Tycoon</h1>
                    </header>
                    <div class="page-break"></div>
                    <div class="container">
                        <div class="column">
                            <div class="sub-column-container">
                                <div class="column">
                                    <div class="invisible-break"></div>
                                    <div class="subtitle">Balance</div>
                                </div>
                                <div class="column">
                                    <div class="invisible-break"></div>
                                    <div class="subtitle">Income</div>
                                </div>
                            </div>
                        </div>
                        <div class="column">
                            <div class="invisible-break"></div>
                            <div class="subtitle">Enclosures</div>
                            <div class="enclosure-box">
                                <PigeonList pigeons={pigeons} />
                            </div>
                        </div>
                        <div class="column">
                            <div class="invisible-break"></div>
                            <div class="subtitle">Stocks</div>
                            <div class="invisible-break"></div>
                            <div class="subtitle">Market</div>
                            <div class="for-sale-box">
                                <PigeonList pigeons={pigeonsForSale} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;