
import validation
import unittest


# Test if Piece + PSQT Difference = 0 for equal positions
class Psqt_tests(unittest.TestCase):

    def test_case_1(self):
        self.assertEqual(int(validation.calcPieceValueWithPSQT("rnb1kbnr/p4ppp/3q4/1pppp3/3PPPP1/3Q4/PPP4P/RNB1KBNR b KQkq - 0 5")),0,)

    def test_case_2(self):
        self.assertEqual(int(validation.calcPieceValueWithPSQT("rnbqkbnr/1ppppppp/p7/8/8/7P/PPPPPPP1/RNBQKBNR w KQkq - 0 2")),0,)

    def test_case_3(self):
        self.assertEqual(int(validation.calcPieceValueWithPSQT("r2qkb2/p1p1p1p1/2n1bn1r/1p1p1p1p/P1P1P1P1/R1NB1N2/1P1P1P1P/2BQK2R b Kkq - 7 8")),0,)

    def test_case_4(self):
        self.assertEqual(int(validation.calcPieceValueWithPSQT("8/8/8/8/8/8/8/8 b Kkq - 7 8")),0,)

    def test_case_5(self):
        self.assertEqual(int(validation.calcPieceValueWithPSQT("qqqqqqqq/kkkkkkkk/8/8/8/8/KKKKKKKK/QQQQQQQQ b Kkq - 7 8")),0,)




class Chessboard_from_fen_tests(unittest.TestCase):
    
    def test_case_1(self):
        expected = [[0 for _ in range(8)] for _ in range(8)]
        result = validation.fen_to_array("8/8/8/8/8/8/8/8 b Kkq - 7 8")
        self.assertEqual(expected, result)


    def test_case_2(self):

        expected = [
            ['r', 'n', 'b',  0, 'k', 'b', 'n', 'r'],
            ['p',  0,  0,  0,  0, 'p', 'p', 'p'],
            [ 0,  0,  0, 'q',  0,  0,  0,  0],
            [ 0, 'p', 'p', 'p', 'p',  0,  0,  0],
            [ 0,  0,  0, 'P', 'P', 'P', 'P',  0],
            [ 0,  0,  0, 'Q',  0,  0,  0,  0],
            ['P', 'P', 'P',  0,  0,  0,  0, 'P'],
            ['R', 'N', 'B',  0, 'K', 'B', 'N', 'R']
        ]

        result = validation.fen_to_array("rnb1kbnr/p4ppp/3q4/1pppp3/3PPPP1/3Q4/PPP4P/RNB1KBNR b KQkq - 0 5")
        self.assertEqual(expected, result)


    def test_case_3(self):

        expected = [
            ['r',  0,  0, 'q', 'k', 'b',  0,  0],
            ['p',  0, 'p',  0, 'p',  0, 'p',  0],
            [ 0,  0, 'n',  0, 'b', 'n',  0, 'r'],
            [ 0, 'p',  0, 'p',  0, 'p',  0, 'p'],
            ['P',  0, 'P',  0, 'P',  0, 'P',  0],
            ['R',  0, 'N', 'B',  0, 'N',  0,  0],
            [ 0, 'P',  0, 'P',  0, 'P',  0, 'P'],
            [ 0,  0, 'B', 'Q', 'K',  0,  0, 'R']
        ]

        result = validation.fen_to_array("r2qkb2/p1p1p1p1/2n1bn1r/1p1p1p1p/P1P1P1P1/R1NB1N2/1P1P1P1P/2BQK2R b Kkq - 7 8")
        self.assertEqual(expected, result)


class Pawn_move_tests(unittest.TestCase):
   
    def test_case_1(self): # All possible moves

        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,'p',0,0,0],
            [0,0,0,'P',0,'P',0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [(2,4), (3,4), (2,3), (2,5)]

        self.assertEqual(expected, validation.pawn_moves(1, 4, False, chessboard))


    def test_case_2(self): # No takes possible
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,'p',0,0,0],
            [0,0,0,'p',0,'p',0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [(2,4), (3,4)]

        self.assertEqual(expected, validation.pawn_moves(1, 4, False, chessboard))


    def test_case_3(self): # Fully blocked
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,'p',0,0,0],
            [0,0,0,'p','p','p',0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = []

        self.assertEqual(expected, validation.pawn_moves(1, 4, False, chessboard))



    def test_case_4(self): # Only takes
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,'p',0,0,0],
            [0,0,0,'P','p','P',0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [(2,3), (2,5)]

        self.assertEqual(expected, validation.pawn_moves(1, 4, False, chessboard))


class Knight_move_tests(unittest.TestCase):
   
    def test_case_1(self): # All possible moves

        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,'n',0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [(1, 2), (1, 4), (5, 2), (5, 4), (2, 1), (2, 5), (4, 1), (4, 5)]

        self.assertEqual(expected, validation.knight_moves(3, 3, False, chessboard))



    def test_case_2(self): # Fully blocked
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,'p',0,'p',0,0,0],
            [0,'p',0,0,0,'p',0,0],
            [0,0,0,'n',0,0,0,0],
            [0,'p',0,0,0,'p',0,0],
            [0,0,'p',0,'p',0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = []

        self.assertEqual(expected, validation.knight_moves(3, 3, False, chessboard))



    def test_case_3(self): # Only takes
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,'P',0,'P',0,0,0],
            [0,'P',0,0,0,'P',0,0],
            [0,0,0,'n',0,0,0,0],
            [0,'P',0,0,0,'P',0,0],
            [0,0,'P',0,'P',0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [(1, 2), (1, 4), (5, 2), (5, 4), (2, 1), (2, 5), (4, 1), (4, 5)]

        self.assertEqual(expected, validation.knight_moves(3, 3, False, chessboard))




    def test_case_4(self): # Out of bound
        
        chessboard = [
            ['n',0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [(2, 1), (1, 2)]

        self.assertEqual(expected, validation.knight_moves(0, 0, False, chessboard))


class Queen_move_tests(unittest.TestCase):
   
    
    def test_case_1(self): # All possible moves & out of bound

        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,'q',0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [
            (3, 2), (3, 1), (3, 0), (3, 4), (3, 5), (3, 6), (3, 7),
            (2, 3), (1, 3), (0, 3), (4, 3), (5, 3), (6, 3), (7, 3),
            (2, 2), (1, 1), (0, 0), (2, 4), (1, 5), (0, 6),
            (4, 2), (5, 1), (6, 0), (4, 4), (5, 5), (6, 6), (7, 7)
        ]


        self.assertEqual(expected, validation.queen_moves(3, 3, False, chessboard))



    def test_case_2(self): # Fully blocked
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,'p','p','p',0,0,0],
            [0,0,'p','q','p',0,0,0],
            [0,0,'p','p','p',0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = []

        self.assertEqual(expected, validation.queen_moves(3, 3, False, chessboard))



    def test_case_3(self): # Only takes
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,'P','P','P',0,0,0],
            [0,0,'P','q','P',0,0,0],
            [0,0,'P','P','P',0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [(3, 2), (3, 4), (2, 3), (4, 3), (2, 2), (2, 4), (4, 2), (4, 4)]

        self.assertEqual(expected, validation.queen_moves(3, 3, False, chessboard))


class Bishop_move_tests(unittest.TestCase):
   
    
    def test_case_1(self): # All possible moves & out of bound

        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,'b',0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [
            (2, 2), (1, 1), (0, 0), (2, 4), (1, 5), (0, 6),
            (4, 2), (5, 1), (6, 0), (4, 4), (5, 5), (6, 6), (7, 7)
        ]


        self.assertEqual(expected, validation.bishop_moves(3, 3, False, chessboard))



    def test_case_2(self): # Fully blocked
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,'p','p','p',0,0,0],
            [0,0,'p','q','p',0,0,0],
            [0,0,'p','p','p',0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = []

        self.assertEqual(expected, validation.bishop_moves(3, 3, False, chessboard))



    def test_case_3(self): # Only takes
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,'P',0,'P',0,0,0],
            [0,0,0,'q',0,0,0,0],
            [0,0,'P',0,'P',0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [(2, 2), (2, 4), (4, 2), (4, 4)]

        self.assertEqual(expected, validation.bishop_moves(3, 3, False, chessboard))


class Rook_move_tests(unittest.TestCase):
   
    
    def test_case_1(self): # All possible moves & out of bound

        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,'r',0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [
            (3, 2), (3, 1), (3, 0), (3, 4), (3, 5), (3, 6), (3, 7),
            (2, 3), (1, 3), (0, 3), (4, 3), (5, 3), (6, 3), (7, 3),
        ]


        self.assertEqual(expected, validation.rook_moves(3, 3, False, chessboard))



    def test_case_2(self): # Fully blocked
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,'p',0,0,0,0],
            [0,0,'p','r','p',0,0,0],
            [0,0,0,'p',0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]

        expected = []

        self.assertEqual(expected, validation.rook_moves(3, 3, False, chessboard))



    def test_case_3(self): # Only takes
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,'P',0,0,0,0],
            [0,0,'P','r','P',0,0,0],
            [0,0,0,'P',0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected =  [(3, 2), (3, 4), (2, 3), (4, 3)]

        self.assertEqual(expected, validation.rook_moves(3, 3, False, chessboard))