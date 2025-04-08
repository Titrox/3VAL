import validation
import unittest


# Test if Piece + PSQT Difference = 0 for equal positions
class Psqt_tests(unittest.TestCase):

    def test_case_1(self):

        chessboad = [
            ['r', 'n', 'b',  0, 'k', 'b', 'n', 'r'],
            ['p',  0,  0,  0,  0, 'p', 'p', 'p'],
            [ 0,  0,  0, 'q',  0,  0,  0,  0],
            [ 0, 'p', 'p', 'p', 'p',  0,  0,  0],
            [ 0,  0,  0, 'P', 'P', 'P', 'P',  0],
            [ 0,  0,  0, 'Q',  0,  0,  0,  0],
            ['P', 'P', 'P',  0,  0,  0,  0, 'P'],
            ['R', 'N', 'B',  0, 'K', 'B', 'N', 'R']
        ]

        self.assertEqual(validation.calc_piece_value_with_psqt(chessboad),0)

    def test_case_2(self):

        chessboard = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            [0, 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['p', 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 'P'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 0],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]


        self.assertEqual(validation.calc_piece_value_with_psqt(chessboard),0)


    def test_case_3(self):

        chessboard = [[0 for _ in range(8)] for _ in range(8)]

        self.assertEqual(validation.calc_piece_value_with_psqt(chessboard),0)

    def test_case_4(self):

        chessboard = [
            ['q', 'q', 'q', 'q', 'q', 'q', 'q', 'q'],
            ['k', 'k', 'k', 'k', 'k', 'k', 'k', 'k'],
            [0,  0,  0,  0,  0,  0,  0,  0],
            [0,  0,  0,  0,  0,  0,  0,  0],
            [0,  0,  0,  0,  0,  0,  0,  0],
            [0,  0,  0,  0,  0,  0,  0,  0],
            ['K', 'K', 'K', 'K', 'K', 'K', 'K', 'K'],
            ['Q', 'Q', 'Q', 'Q', 'Q', 'Q', 'Q', 'Q']
        ]


        self.assertEqual(validation.calc_piece_value_with_psqt(chessboard),0)




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


class Knight_move_tests(unittest.TestCase):
   
    def test_case_1(self): # All possible moves

        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,'k',0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [(3, 2), (3, 4), (2, 3), (4, 3), (2, 2), (2, 4), (4, 2), (4, 4)]

        self.assertEqual(expected, validation.king_moves(3, 3, False, chessboard))



    def test_case_2(self): # Fully blocked
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,'p','p','p',0,0,0],
            [0,0,'p','k','p',0,0,0],
            [0,0,'p','p','p',0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = []

        self.assertEqual(expected, validation.king_moves(3, 3, False, chessboard))



    def test_case_3(self): # Only takes
        
        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,'P','P','P',0,0,0],
            [0,0,'P','k','P',0,0,0],
            [0,0,'P','P','P',0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [(3, 2), (3, 4), (2, 3), (4, 3), (2, 2), (2, 4), (4, 2), (4, 4)]

        self.assertEqual(expected, validation.king_moves(3, 3, False, chessboard))




    def test_case_4(self): # Out of bound
        
        chessboard = [
            ['k',0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected = [(0, 1), (1, 0), (1, 1)]

        self.assertEqual(expected, validation.king_moves(0, 0, False, chessboard))



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
    

class Castling_move_tests(unittest.TestCase):

    def test_case_1(self):
        chessboard = [
                ['r',0,0,0,'k',0,0,'r'],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ]

        expected =  [(0, 2), (0, 6)]

        self.assertEqual(expected, validation.legal_castling_moves("qk", chessboard, False))


    def test_case_2(self):
        chessboard = [
                ['r',0,0,0,'k',0,0,'r'],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ]

        expected =  [(0, 6)]

        self.assertEqual(expected, validation.legal_castling_moves("k", chessboard, False))



    def test_case_3(self):
        chessboard = [
                ['r',0,0,0,'k',0,0,'r'],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ]

        expected =  [(0, 2)]

        self.assertEqual(expected, validation.legal_castling_moves("q", chessboard, False))



    def test_case_4(self):
        chessboard = [
                ['r',0,0,0,'k',0,0,'r'],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ]

        expected = []

        self.assertEqual(expected, validation.legal_castling_moves("-", chessboard, False))


    def test_case_4(self):

        chessboard = [
                ['r',0,0,0,'k',0,0,'r'],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,'Q'],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ]

        expected = []

        self.assertEqual(expected, validation.legal_castling_moves("k", chessboard, False))



class En_passant_move_tests(unittest.TestCase):

    def test_case_1(self):
        
        chessboard = [
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,'p','P',0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ]

        expected =  {(4, 1): [(5, 2)]}

        self.assertEqual(expected, validation.legal_en_passant_moves("c3", chessboard, False))


    def test_case_2(self):

        chessboard = [
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,'p','P','p',0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ]
        expected =  {(4, 1): [(5, 2)], (4, 3): [(5, 2)]}

        self.assertEqual(expected, validation.legal_en_passant_moves("c3", chessboard, False))


    def test_case_3(self):

        chessboard = [
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,'k',0,0,0,0,0,0],
                [0,'p','P','p',0,0,0,0],
                [0,'Q',0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ]
        expected =  {(4, 3): [(5, 2)]}

        self.assertEqual(expected, validation.legal_en_passant_moves("c3", chessboard, False))


    def test_case_4(self):

        chessboard = [
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,'k',0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,'p','P','p',0,0,0,0],
                [0,'Q',0,0,'B',0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ]
        expected =  {}

        self.assertEqual(expected, validation.legal_en_passant_moves("c3", chessboard, False))



class Legal_move_tests(unittest.TestCase):


    def test_case_1(self):

        chessboard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,'k',0,0,0,0],
            [0,0,0,0,'P',0,0,0],
            [0,0,'P','q','P',0,0,0],
            [0,0,0,'Q',0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]


        chessboard_object = validation.Chessboard_state(chessboard, "-", "-")

        expected = {(1, 3): [(1, 2), (1, 4), (0, 3), (0, 2), (0, 4), (2, 2), (2, 4)]}

        self.assertEqual(expected, validation.generate_legal_moves(chessboard_object, False))


    def test_case_2(self):
            
            chessboard = [
                ['r', 0, 'b', 0, 'q', 'b', 0, 'r'], 
                ['p', 0, 0, 'n', 'k', 'p', 0, 'p'], 
                [0, 'p', 'p', 0, 0, 0, 'p', 'n'], 
                [0, 'B', 0, 'P', 'p', 0, 0, 'P'], 
                [0, 0, 0, 0, 0, 'P', 0, 0], 
                ['P', 0, 'P', 0, 0, 0, 0, 0], 
                [0, 'P', 0, 'P', 'Q', 0, 'P', 0], 
                ['R', 'N', 'B', 0, 'K', 0, 'N', 'R']
            ]

            chessboard_object = validation.Chessboard_state(chessboard, "-", "-")


            expected = {
                (0, 0): [(0, 1)],
                (0, 2): [(1, 1), (2, 0)],
                (0, 4): [(0, 3)],
                (0, 5): [(1, 6)],
                (0, 7): [(0, 6)],
                (1, 0): [(2, 0), (3, 0)],
                (1, 3): [(3, 2), (0, 1), (2, 5)],
                (1, 4): [(0, 3), (2, 3), (2, 5)],
                (1, 5): [(2, 5), (3, 5)],
                (2, 2): [(3, 2), (3, 1), (3, 3)],
                (2, 6): [(3, 6), (3, 7)],
                (2, 7): [(0, 6), (4, 6), (3, 5)],
                (3, 4): [(4, 4)]
                }
                        
            self.assertEqual(expected, validation.generate_legal_moves(chessboard_object, False))


    
    def test_case_3(self):
            
            chessboard = [
                ['r', 0, 'b', 0, 0, 'b', 0, 'r'], 
                ['p', 0, 'P', 'k', 0, 'p', 0, 'p'], 
                [0, 'p', 0, 0, 0, 0, 'p', 'n'], 
                [0, 'q', 0, 'n', 'p', 'P', 0, 'P'], 
                ['P', 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 'P', 'Q', 0, 0, 'P', 0], 
                [0, 'P', 0, 'P', 0, 0, 0, 0], 
                ['R', 'N', 'B', 0, 'K', 0, 'N', 'R']
            ]

            chessboard_object = validation.Chessboard_state(chessboard, "-", "-")

            expected = {
                (0, 0): [(0, 1)], 
                (0, 2): [(1, 1), (2, 0)], 
                (0, 5): [(1, 4), (2, 3), (3, 2), (4, 1), (5, 0), (1, 6)], 
                (0, 7): [(0, 6)], 
                (1, 0): [(2, 0), (3, 0)], 
                (1, 3): [(1, 2), (1, 4), (2, 3), (0, 4), (2, 2)], 
                (1, 5): [(2, 5)], (2, 6): [(3, 6), (3, 5), (3, 7)], 
                (2, 7): [(0, 6), (4, 6), (3, 5)], 
                (3, 1): [(3, 0), (3, 2), (4, 1), (5, 1), (6, 1), (2, 0), (2, 2), (4, 0), (4, 2), (5, 3)], 
                (3, 4): [(4, 4)]}
                        
            self.assertEqual(expected, validation.generate_legal_moves(chessboard_object, False))


    def test_case_4(self):

        chessboard = [
            ['r', 0, 'b', 0, 0, 0, 0, 'r'], 
            ['p', 0, 0, 'k', 0, 'n', 0, 'p'], 
            [0, 'p', 0, 0, 0, 'p', 'p', 0], 
            [0, 'q', 'b', 'n', 0, 'P', 'B', 'P'], 
            ['P', 0, 0, 0, 0, 'Q', 0, 0], 
            ['N', 0, 'P', 'p', 0, 0, 'P', 0], 
            [0, 'P', 0, 0, 0, 0, 0, 0], 
            [0, 0, 'K', 0, 'R', 0, 'N', 'R']
        ]

        chessboard_object = validation.Chessboard_state(chessboard, "-", "-")

        excepted = {
            (0, 0): [(0, 1)], 
            (0, 2): [(1, 1), (2, 0)], 
            (0, 7): [(0, 6), (0, 5), (0, 4), (0, 3)], 
            (1, 0): [(2, 0), (3, 0)], 
            (1, 3): [(0, 3), (2, 2)], 
            (1, 5): [(3, 4), (3, 6), (0, 3), (2, 3), (2, 7)], 
            (1, 7): [(2, 7)], 
            (2, 5): [(3, 6)], 
            (2, 6): [(3, 5), (3, 7)], 
            (3, 1): [(3, 0), (4, 1), (5, 1), (6, 1), (2, 0), (2, 2), (4, 0), (4, 2)], 
            (3, 2): [(2, 3), (1, 4), (0, 5), (4, 1), (5, 0), (4, 3), (5, 4), (6, 5), (7, 6)], 
            (3, 3): [(1, 2), (1, 4), (5, 2), (5, 4), (4, 1), (4, 5)], 
            (5, 3): [(6, 3)]
            }
        

        self.assertEqual(excepted, validation.generate_legal_moves(chessboard_object, False))



    def test_case_5(self):
        
        chessboard = [
            ['r', 0, 'b', 0, 0, 'n', 'n', 'r'], 
            [0, 0, 'P', 0, 'b', 'p', 'p', 0], 
            ['p', 0, 0, 'k', 0, 'B', 0, 'p'], 
            [0, 'P', 0, 0, 'p', 0, 0, 0], 
            [0, 'P', 'B', 'q', 0, 0, 0, 'P'], 
            ['N', 0, 0, 'Q', 'P', 'N', 0, 0], 
            [0, 0, 'K', 'P', 0, 'P', 'P', 0], 
            [0, 0, 0, 'R', 0, 0, 0, 'R']
        ]

        chessboard_object = validation.Chessboard_state(chessboard, "-", "-")

        expected = {
            (0, 0): [(0, 1), (1, 0)], 
            (0, 2): [(1, 1), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7)], 
            (0, 5): [(2, 4), (2, 6), (1, 3), (1, 7)], 
            (0, 6): [(2, 5)], 
            (0, 7): [(1, 7)], 
            (1, 4): [(0, 3), (2, 5)], 
            (1, 6): [(2, 6), (3, 6), (2, 5)], 
            (2, 0): [(3, 0), (3, 1)], 
            (2, 3): [(1, 3), (1, 2)], 
            (2, 7): [(3, 7)], 
            (3, 4): [(4, 4)], 
            (4, 3): [(3, 3), (5, 3)]
            }
        

        self.assertEqual(expected, validation.generate_legal_moves(chessboard_object, False))



    def test_case_6(self): # Castling both sides
        
        chessboard = [
            ['r', 0, 0, 0, 'k', 0, 0, 'r'], 
            [0, 0, 'P', 0, 'b', 'p', 'p', 0], 
            ['p', 0, 0, 'k', 0, 'B', 0, 'p'], 
            [0, 'P', 0, 0, 'p', 0, 0, 0], 
            [0, 'P', 'B', 'q', 0, 0, 0, 'P'], 
            ['N', 0, 0, 'Q', 'P', 'N', 0, 0], 
            [0, 0, 'K', 'P', 0, 'P', 'P', 0], 
            [0, 0, 0, 'R', 0, 0, 0, 'R']
        ]

        chessboard_object = validation.Chessboard_state(chessboard, "kq", "-")

        expected = {
            (0, 0): [(0, 1), (0, 2), (0, 3), (1, 0)], 
            (0, 4): [(0, 5), (1, 3), (0, 2), (0, 6)], 
            (0, 7): [(0, 6), (0, 5), (1, 7)], 
            (1, 4): [(0, 3), (0, 5), (2, 5)], 
            (1, 6): [(2, 6), (3, 6), (2, 5)], 
            (2, 0): [(3, 0), (3, 1)], 
            (2, 3): [(2, 2), (2, 4), (1, 3), (3, 3), (1, 2), (3, 2)], 
            (2, 7): [(3, 7)], 
            (3, 4): [(4, 4)], 
            (4, 3): [(4, 2), (4, 4), (4, 5), (4, 6), (4, 7), (3, 3), (5, 3), (3, 2), (2, 1), (1, 0), (5, 2), (6, 1), (7, 0), (5, 4)]}
        

        self.assertEqual(expected, validation.generate_legal_moves(chessboard_object, False))


    
    def test_case_7(self): # Castling q side
        
        chessboard = [
            ['r', 0, 0, 0, 'k', 0, 0, 'r'], 
            [0, 0, 'P', 0, 'b', 'p', 'p', 0], 
            ['p', 0, 0, 'k', 0, 'B', 0, 'p'], 
            [0, 'P', 0, 0, 'p', 0, 0, 0], 
            [0, 'P', 'B', 'q', 0, 0, 0, 'P'], 
            ['N', 0, 0, 'Q', 'P', 'N', 0, 0], 
            [0, 0, 'K', 'P', 0, 'P', 'P', 0], 
            [0, 0, 0, 'R', 0, 0, 0, 'R']
        ]

        chessboard_object = validation.Chessboard_state(chessboard, "q", "-")

        expected = {
            (0, 0): [(0, 1), (0, 2), (0, 3), (1, 0)], 
            (0, 4): [(0, 5), (1, 3), (0, 2)], 
            (0, 7): [(0, 6), (0, 5), (1, 7)], 
            (1, 4): [(0, 3), (0, 5), (2, 5)], 
            (1, 6): [(2, 6), (3, 6), (2, 5)], 
            (2, 0): [(3, 0), (3, 1)], 
            (2, 3): [(2, 2), (2, 4), (1, 3), (3, 3), (1, 2), (3, 2)], 
            (2, 7): [(3, 7)], 
            (3, 4): [(4, 4)], 
            (4, 3): [(4, 2), (4, 4), (4, 5), (4, 6), (4, 7), (3, 3), (5, 3), (3, 2), (2, 1), (1, 0), (5, 2), (6, 1), (7, 0), (5, 4)]}
        

        self.assertEqual(expected, validation.generate_legal_moves(chessboard_object, False)) 




    def test_case_8(self): # Castling k side
        
        chessboard = [
            ['r', 0, 0, 0, 'k', 0, 0, 'r'], 
            [0, 0, 'P', 0, 'b', 'p', 'p', 0], 
            ['p', 0, 0, 'k', 0, 'B', 0, 'p'], 
            [0, 'P', 0, 0, 'p', 0, 0, 0], 
            [0, 'P', 'B', 'q', 0, 0, 0, 'P'], 
            ['N', 0, 0, 'Q', 'P', 'N', 0, 0], 
            [0, 0, 'K', 'P', 0, 'P', 'P', 0], 
            [0, 0, 0, 'R', 0, 0, 0, 'R']
        ]

        chessboard_object = validation.Chessboard_state(chessboard, "k", "-")

        expected = {
            (0, 0): [(0, 1), (0, 2), (0, 3), (1, 0)], 
            (0, 4): [(0, 5), (1, 3), (0, 6)], 
            (0, 7): [(0, 6), (0, 5), (1, 7)], 
            (1, 4): [(0, 3), (0, 5), (2, 5)], 
            (1, 6): [(2, 6), (3, 6), (2, 5)], 
            (2, 0): [(3, 0), (3, 1)], 
            (2, 3): [(2, 2), (2, 4), (1, 3), (3, 3), (1, 2), (3, 2)], 
            (2, 7): [(3, 7)], 
            (3, 4): [(4, 4)], 
            (4, 3): [(4, 2), (4, 4), (4, 5), (4, 6), (4, 7), (3, 3), (5, 3), (3, 2), (2, 1), (1, 0), (5, 2), (6, 1), (7, 0), (5, 4)]}
        

        self.assertEqual(expected, validation.generate_legal_moves(chessboard_object, False)) 