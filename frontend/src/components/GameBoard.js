import React, { useState } from 'react';
import axios from 'axios';

const GameBoard = () => {
    const [board, setBoard] = useState([...Array(6)].map(() => Array(6).fill(0))); // Initialize a 6x6 board
    const [turn, setTurn] = useState(1); // Player 1 starts

    const handleCellClick = async (row, col) => {
        try {
            // Prepare the data for the API request
            const moveData = {
                row: row,
                col: col,
                rot: 0 // Change this based on your rotation logic
            };

            // Make the POST request to the Flask API
            const response = await axios.post('/api/move', moveData);

            // Check the response
            if (response.data.success) {
                // Update the board state with the new move
                const newBoard = response.data.board;
                setBoard(newBoard);
                setTurn(turn === 1 ? 2 : 1); // Switch turns
            } else {
                alert(response.data.message); // Show invalid move message
            }
        } catch (error) {
            console.error('Error making move:', error);
            alert('Failed to make move, please try again.'); // Handle error gracefully
        }
    };

    return (
        <div>
            {board.map((row, rowIndex) => (
                <div key={rowIndex} style={{ display: 'flex' }}>
                    {row.map((cell, colIndex) => (
                        <div
                            key={colIndex}
                            onClick={() => handleCellClick(rowIndex, colIndex)} // Handle cell click
                            style={{
                                width: 50,
                                height: 50,
                                backgroundColor: cell === 0 ? 'white' : cell === 1 ? 'red' : 'blue',
                                border: '1px solid black',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                cursor: 'pointer'
                            }}
                        >
                            {cell !== 0 ? (cell === 1 ? 'X' : 'O') : ''}
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};

export default GameBoard;
