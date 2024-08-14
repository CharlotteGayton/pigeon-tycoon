// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
    const [gameData, setGameData] = useState(null);
    const [pigeons, setPigeons] = useState([]);
    const [newPigeon, setNewPigeon] = useState({ name: '', speed: '', stamina: '' });
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/game-data')
            .then(response => {
                setGameData(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the game data!', error);
            });
    }, []);

    useEffect(() => {
      axios.get('http://127.0.0.1:5000/api/get-pigeons')
          .then(response => {
              setPigeons(response.data);
              console.log(response.data);
          })
          .catch(error => {
              console.error('There was an error fetching the game data!', error);
          });
  }, []);    

    const saveGame = () => {
        axios.post('http://127.0.0.1:5000/api/save-game', gameData)
            .then(response => {
                alert('Game saved!');
            })
            .catch(error => {
                console.error('There was an error saving the game!', error);
            });
    };

    const handleInputChange = (e) => {
      const { name, value } = e.target;
      setNewPigeon(prevState => ({
          ...prevState,
          [name]: value
      }));
  };

    const addPigeon = () => {
      axios.post('http://127.0.0.1:5000/api/add-pigeon', newPigeon)
          .then(response => {
              // Refresh pigeon list
              axios.get('http://127.0.0.1:5000/api/get-pigeons')
                  .then(response => {
                      setPigeons(response.data);
                      setNewPigeon({ name: '', speed: '', stamina: '' }); // Clear form
                      setError(null); // Clear any previous errors
                  });
          })
          .catch(error => {
              setError(error.response?.data?.error || 'There was an error adding the pigeon');
          });
  };

    return (
      <div>
          <h1>Pigeon List</h1>
          {/* {pigeons.length === 0 ? (
          <p>No pigeons available.</p> */}
      {/* ) : ( */}
          <ul>
              {pigeons.map(pigeon => (
                  <li key={pigeon.id}>
                      Name: {pigeon.name}, Speed: {pigeon.speed}, Stamina: {pigeon.stamina}
                  </li>
              ))}
          </ul>

          <h2>Add a New Pigeon</h2>
          <form onSubmit={(e) => { e.preventDefault(); addPigeon(); }}>
              <div>
                  <label>Name:
                      <input
                          type="text"
                          name="name"
                          value={newPigeon.name}
                          onChange={handleInputChange}
                          required
                      />
                  </label>
              </div>
              <div>
                  <label>Speed:
                      <input
                          type="number"
                          name="speed"
                          value={newPigeon.speed}
                          onChange={handleInputChange}
                          required
                      />
                  </label>
              </div>
              <div>
                  <label>Stamina:
                      <input
                          type="number"
                          name="stamina"
                          value={newPigeon.stamina}
                          onChange={handleInputChange}
                          required
                      />
                  </label>
              </div>
              <button type="submit">Add Pigeon</button>
          </form>
          
          {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
  );
}

export default App;