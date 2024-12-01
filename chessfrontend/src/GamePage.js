import { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const GamePage = ({ authToken }) => {
  const { gameId } = useParams(); // Extract the gameId from the URL parameters
  const [game, setGame] = useState(null);
  const [selectedCells, setSelectedCells] = useState([]); // Store selected cells
  const [move, setMove] = useState(''); // Store the move in string format

  const pieceSymbols = {
    'Rw': '♖', 'Hw': '♘', 'Bw': '♗', 'Qw': '♕', 'Kw': '♔', 'pw': '♙',
    'Rb': '♖', 'Hb': '♘', 'Bb': '♗', 'Qb': '♕', 'Kb': '♔', 'pb': '♙',
    '.': '.', // Empty square
  };

  useEffect(() => {
    if (selectedCells.length === 2) {
      const moveString = `${selectedCells[0]} ${selectedCells[1]}`;
      setMove(moveString);
      console.log('Move string:', moveString);

      putMove(moveString);

      setSelectedCells([]);
    }
  }, [selectedCells]);

  const handleCellClick = (row, col) => {
    if (selectedCells.length === 2) {
      setSelectedCells([]);
    }
    setSelectedCells((prev) => [...prev, `${row} ${col}`]);
  };

  const putMove = async (move) => {
    try {
      const response = await axios.put(`http://localhost:8000/${gameId}/`, { move }, {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
      console.log('Move updated:', response.data);
      
    } catch (error) {
      console.error('Error updating move:', error);
    }
  };


  const renderBoard = (serializedBoard) => {
    // Split the serialized board into an array of squares (64 squares)
    const boardArray = serializedBoard.split(' ');
    console.log(boardArray);

    // Create 8 rows of 8 squares each
    const rows = [];
    for (let i = 0; i < 8; i++) {
      const row = [];
      for (let j = 0; j < 8; j++) {
        const piece = boardArray[i * 8 + j];
        row.push(
          <td key={j} className={((i + j) % 2 === 0) ? 'white-square' : 'black-square'} onClick={() => handleCellClick(i, j)}>
            {pieceSymbols[piece] || piece}  {/* Map piece to symbol */}
          </td>
        );
      }
      rows.push(<tr key={i}>{row}</tr>);
    }

    return <table className="chessboard">{rows}</table>;
  };

  // Fetch the game's details
  console.log("Auth Token:", authToken);
  useEffect(() => {
    const fetchGameDetails = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/${gameId}`, {
          headers: {
            Authorization: `Bearer ${authToken}`, // Send token for authentication
          },
        });
        setGame(response.data);
      } catch (error) {
        console.error("Error fetching game details", error);
      }
    };
    fetchGameDetails();
  }, [gameId, authToken]);

  if (!game) return <p>Loading...</p>;

  return (
    <div>
      <h2>Game Details</h2>
      <p><strong>White:</strong> {game.white}</p>
      <p><strong>Black:</strong> {game.black}</p>
      <p><strong>Status:</strong> {game.status}</p>
      <p><strong>Current Turn:</strong> {game.current_turn}</p>

      {/* Render the chessboard */}
       <h3>Board:</h3>
      {renderBoard(game.serializedboard)}

      {/* Add more details or actions for the game here */}
    </div>
  );
};

export default GamePage;