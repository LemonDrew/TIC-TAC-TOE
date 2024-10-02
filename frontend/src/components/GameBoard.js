import React, { useState } from 'react';
import axios from 'axios';

const GameBoard = () => {
    const [board, setBoard] = useState([...Array(6)].map(() => Array(6).fill(0))); // Initialize a 6x6 board
    const [turn, setTurn] = useState(1); // Player 1 starts
    const [errorMessage, setErrorMessage] = useState('');
    const [rotation, setRotation] = useState(0); // State for rotation value
    const [selectedCell, setSelectedCell] = useState({ row: null, col: null }); // State for selected cell

    const handleCellClick = (row, col) => {
        setSelectedCell({ row, col }); // Set the selected cell
        setErrorMessage(''); // Clear any previous error message
    };

    const confirmMove = async () => {
        const { row, col } = selectedCell;

        if (row === null || col === null) {
            setErrorMessage('Please select a cell first!');
            return;
        }

        try {
            const moveData = {
                row: row,
                col: col,
                rot: rotation // Use the rotation state value
            };

            const response = await axios.post('/api/move', moveData);

            if (response.data.success) {
                const newBoard = response.data.board;
                setBoard(newBoard);

                // Check for victory status
                if (response.data.victory) {
                    // Delay the alert to show the move first
                    setTimeout(() => {
                        alert(`Player ${turn} wins!`);
                    }, 500); // Delay of 500 milliseconds (0.5 seconds)
                }

                setTurn(turn === 1 ? 2 : 1); // Switch turns
                setRotation(0); // Reset rotation value after move
                setSelectedCell({ row: null, col: null }); // Reset selected cell
            } else {
                setErrorMessage(response.data.message);
            }
        } catch (error) {
            console.error('Error making move:', error);
            alert('Failed to make move, please try again.');
        }
    };

    const resetBoard = async () => {
        try {
            // Make the POST request to reset the Flask API
            const response = await axios.post('/api/reset');

            // Check the response
            if (response.data.success) {
                // Reset the local board state to the initial state
                setBoard(response.data.board);
                setTurn(1); // Reset the turn to player 1
                setErrorMessage(''); // Clear the error message on reset
            } else {
                setErrorMessage('Failed to reset the game, please try again.');
            }
        } catch (error) {
            console.error('Error resetting game:', error);
            setErrorMessage('Failed to reset the game, please try again.'); // Handle error gracefully
        }
    };

    const handleRotationChange = (e) => {
        const value = e.target.value;
        // Ensure that the input is a valid number
        const numberValue = Number(value);
        if (!isNaN(numberValue)) {
            setRotation(numberValue); // Update rotation state
        } else {
            setRotation(0); // Reset to 0 if invalid input
        }
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-start' }}>
            <div style={{ marginRight: '20px' }}>
                {board.map((row, rowIndex) => (
                    <div key={rowIndex} style={{ display: 'flex' }}>
                        {row.map((cell, colIndex) => (
                            <div
                                key={colIndex}
                                onClick={() => handleCellClick(rowIndex, colIndex)} // Handle cell click
                                style={{
                                    width: 50,
                                    height: 50,
                                    backgroundColor: selectedCell.row === rowIndex && selectedCell.col === colIndex
                                        ? 'lightgreen' // Highlight selected cell
                                        : cell === 0 ? 'white' : cell === 1 ? 'red' : 'blue',
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
                <input
                    type="number"
                    value={rotation} // Bind the input to rotation state
                    onChange={handleRotationChange} // Update rotation state
                    placeholder="Enter rotation value"
                    style={{ marginTop: '10px', width: '150px' }}
                />
                <button onClick={confirmMove} style={{ marginTop: '10px' }}>Confirm Move</button>
            </div>
            <button onClick={resetBoard} style={{ marginTop: '10px' }}>Reset Board</button>
            <div style={{ marginLeft: '20px', alignSelf: 'flex-start' }}>
                {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
            </div>
        </div>
    );
};

export default GameBoard;
