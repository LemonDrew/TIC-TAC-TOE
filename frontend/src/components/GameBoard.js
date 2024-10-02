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
                if (response.data.victory) {
                    // Delay the alert to show the move first
                    setTimeout(() => {
                        alert(`Player ${turn} wins!`);
                    }, 500); // Delay of 500 milliseconds (0.5 seconds)
                }
                setTurn(turn === 1 ? 2 : 1); // Switch turns
            } else {
                alert(response.data.message); // Show invalid move message
            }
        } catch (error) {
            console.error('Error making move:', error);
            alert('Failed to make move, please try again.'); // Handle error gracefully
        }
    };

    const handleReset = async () => {
        try {
            // Make the POST request to reset the Flask API
            const response = await axios.post('/api/reset');
    
            // Check the response
            if (response.data.success) {
                // Reset the local board state to the initial state
                setBoard(response.data.board);
                setTurn(1); // Reset the turn to player 1
            } else {
                alert('Failed to reset the game, please try again.');
            }
        } catch (error) {
            console.error('Error resetting game:', error);
            alert('Failed to reset the game, please try again.'); // Handle error gracefully
        }
    };

    return (
        <div style={styles.container}>
            <div style={styles.board}>
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
            <button style={styles.resetButton} onClick={handleReset}>Reset Game</button>
        </div>
    );
};

// CSS styles for centering
const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh', // Full viewport height
        transform: 'translateY(-100px)', // Move the board up by 30 pixels
    },
    board: {
        display: 'flex',
        flexDirection: 'column',
        border: '2px solid black', // Optional: add a border around the board
        padding: '10px', // Optional: add padding around the board
    },
    resetButton: {
        marginTop: '20px', // Add some space above the button
        padding: '10px 20px',
        fontSize: '16px',
        cursor: 'pointer',
    },
};

export default GameBoard;
