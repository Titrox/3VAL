import validation
import logging

INFINITY = float('inf')
NEG_INFINITY = float('-inf')

counter = 0


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger()


def MINIMAX(chessboard, depth, is_white):

    global counter
    counter += 1
    logger.debug(counter)

    logger.debug(f"MINMAX SEARCH: {counter}")
    logger.debug(chessboard)

    if depth == 0 or validation.game_over(chessboard, is_white):
        logger.debug("TEst")
        return validation.evaluate_position(chessboard)  # Bewertung der Stellung

    if is_white: # Maiximizer

        bestValue = NEG_INFINITY
        for key, value in validation.generate_legal_moves(chessboard, is_white).items():

            for move in value:

                value = MINIMAX(validation.make_move(key, move, chessboard), depth - 1, False)
                bestValue = max(bestValue, value)

        return bestValue

    else: # Minimizer

        bestValue = INFINITY
        for key, value in validation.generate_legal_moves(chessboard, is_white).items():

            for move in value:

                value = MINIMAX(validation.make_move(key, move, chessboard), depth - 1, True)
                bestValue = min(bestValue, value)

        return bestValue