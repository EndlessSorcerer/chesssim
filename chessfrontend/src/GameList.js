import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const GameList = ({ authToken }) => {
  const [games, setGames] = useState([]);
  const [opponentUsername, setOpponentUsername] = useState('');

  // Fetch the user's games
  useEffect(() => {
    const fetchGames = async () => {
      try {
        const response = await axios.get('http://localhost:8000/', {
          headers: {
            Authorization: `Bearer ${authToken}`, // Send token for authentication
          },
        });
        setGames(response.data);
      } catch (error) {
        console.error("Error fetching games", error);
      }
    };
    fetchGames();
  }, [authToken]);

  // Create a new game with an opponent
  const createGame = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://localhost:8000/', 
        { opponent: opponentUsername },
        {
          headers: {
            Authorization: `Bearer ${authToken}`, // Send token for authentication
          },
        }
      );
      console.log("Game created:", response.data);
      setGames([...games, response.data]); // Add the new game to the list
      setOpponentUsername(''); // Reset opponent input field
    } catch (error) {
      console.error("Error creating game", error);
    }
  };

  return (
    <div>
      <h2>Your Games</h2>
      <ul>
        {games.map((game) => (
          <li key={game.id}>
            {game.white} vs {game.black} - Status: {game.status}
            <Link to={`/games/${game.id}`}>
              <button>View Game</button>
            </Link>
          </li>
        ))}
      </ul>

      <h3>Create a New Game</h3>
      <form onSubmit={createGame}>
        <input
          type="text"
          placeholder="Enter opponent's username"
          value={opponentUsername}
          onChange={(e) => setOpponentUsername(e.target.value)}
        />
        <button type="submit">Create Game</button>
      </form>
    </div>
  );
};

export default GameList;