#!/usr/bin/env python3
"""Terminal Chess - Main entry point."""

import sys
from chess import Game, render_board, display_message, get_user_input, parse_algebraic


def main() -> int:
    """Run the terminal chess game."""
    print("Welcome to Terminal Chess!")
    print("Enter moves in algebraic notation (e.g., 'e2e4', 'Ke8', 'O-O', 'O-O-O')")
    print("Type 'quit' or 'q' to exit")
    print()
    
    game = Game()
    
    while True:
        render_board(game.board)
        display_game_info(game)
        
        move_input = get_user_input(f"{game.current_player.capitalize()}'s move: ")
        
        if move_input.lower() in ('quit', 'q', 'exit'):
            display_message("Game exited.", 'info')
            break
        
        # Parse the move
        try:
            if move_input in ('O-O', 'O-O-O'):
                # Castling notation
                from_sq = 'e1' if game.current_player == 'white' else 'e8'
                to_sq = 'g1' if game.current_player == 'white' else 'g8'
                if move_input == 'O-O-O':
                    to_sq = 'c1' if game.current_player == 'white' else 'c8'
                result = game.play_move(from_sq, to_sq)
            else:
                # Standard move parsing
                from_sq, to_sq = parse_algebraic(move_input)
                if from_sq:
                    result = game.play_move(from_sq, to_sq)
                else:
                    # Parse full destination from move_str
                    result = game.play_move('', to_sq)
            
            if not result:
                display_message("Invalid move. Try again.", 'error')
                continue
            
            # Check game state
            state = game.get_game_state()
            if state == 'checkmate':
                render_board(game.board)
                winner = game.get_winner()
                display_message(f"Checkmate! {winner.capitalize()} wins!", 'success')
                break
            elif state == 'stalemate':
                render_board(game.board)
                display_message("Stalemate! The game is a draw.", 'info')
                break
                
        except ValueError as e:
            display_message(str(e), 'error')
            continue
        except KeyboardInterrupt:
            display_message("\nGame interrupted.", 'info')
            break
    
    return 0


def display_game_info(game) -> None:
    """Display current game information."""
    print(f"\n--- Move {game.move_number} ---")
    print(f"Current player: {game.current_player.capitalize()}")
    
    # Check status
    if game.is_in_check():
        display_message("Check!", 'warning')


if __name__ == '__main__':
    sys.exit(main())
