import constants
import validation
import unittest


# Test if Piece + PSQT Difference = 0 for equal positions
class PsqtTests(unittest.TestCase):


    def test_case_equal_1(self):
        self.assertEqual(int(validation.calcPieceValueWithPSQT("rnb1kbnr/p4ppp/3q4/1pppp3/3PPPP1/3Q4/PPP4P/RNB1KBNR b KQkq - 0 5")),0,)


    def test_case_eaual_2(self):
        self.assertEqual(int(validation.calcPieceValueWithPSQT("rnbqkbnr/1ppppppp/p7/8/8/7P/PPPPPPP1/RNBQKBNR w KQkq - 0 2")),0,)


    def test_case_equal_3(self):
        self.assertEqual(int(validation.calcPieceValueWithPSQT("r1b1kb1r/ppp2p2/2nq1n2/3pp1pp/PP1PP3/2NQ1N2/2P2PPP/R1B1KB1R b KQkq - 0 7")),0,)


    def test_case_equal_4(self):
        self.assertEqual(int(validation.calcPieceValueWithPSQT("r2qkb2/p1p1p1p1/2n1bn1r/1p1p1p1p/P1P1P1P1/R1NB1N2/1P1P1P1P/2BQK2R b Kkq - 7 8")),0,)

