import React, { useState, useEffect } from 'react';
import axios from 'axios';

const GameBoard = () => {
    const [board, setBoard] = useState(Array(6).fill(null).map(() => Array(6).fill(0)));
    const [turn, setTurn] = useState(1); // Player 1 starts

    const handleCellClick = async (row, col) => {
        // Call your backend to apply the move
        const response = await axios.post('http://localhost:5000/api/move', { row, col, turn });
        if (response.data.success) {
            const newBoard = [...board];
            newBoard[row][col] = turn;
            setBoard(newBoard);
            setTurn(turn === 1 ? 2 : 1); // Switch turns
        }
    };

    const renderCell = (row, col) => {
        return (
            <div 
                className={`cell ${board[row][col] === 1 ? 'player1' : board[row][col] === 2 ? 'player2' : ''}`}
                onClick={() => handleCellClick(row, col)}
            >
                {board[row][col] === 1 ? '⚪' : board[row][col] === 2 ? '⚫' : ''}
            </div>
        );
    };

    return (
        <div className="game-board">
            {board.map((row, rowIndex) => (
                <div className="row" key={rowIndex}>
                    {row.map((cell, colIndex) => renderCell(rowIndex, colIndex))}
                </div>
            ))}
        </div>
    );
};

export default GameBoard;
