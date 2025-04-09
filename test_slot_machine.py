import unittest
import random
from unittest.mock import patch
from slot_machine import Symbol, SlotMachine, Player, Game

class TestSymbol(unittest.TestCase):
    def test_symbol_initialization(self):
        """Test that Symbol objects are initialized with correct attributes"""
        symbol = Symbol("A", 2, 5)
        self.assertEqual(symbol.name, "A")
        self.assertEqual(symbol.frequency, 2)
        self.assertEqual(symbol.value, 5)

class TestSlotMachine(unittest.TestCase):
    def setUp(self):
        """Set up a test slot machine instance before each test"""
        self.slot_machine = SlotMachine()
    
    def test_init(self):
        """Test slot machine initialization"""
        self.assertEqual(self.slot_machine.rows, 3)
        self.assertEqual(self.slot_machine.cols, 3)
        self.assertEqual(len(self.slot_machine.symbols), 4)  # A,B,C,D symbols
        
    def test_spin_dimensions(self):
        """Test that spin returns grid with correct dimensions"""
        result = self.slot_machine.spin()
        # Check number of columns
        self.assertEqual(len(result), self.slot_machine.cols)
        # Check number of rows in each column
        for column in result:
            self.assertEqual(len(column), self.slot_machine.rows)
    
    def test_spin_randomness(self):
        """Test that spin produces somewhat random results"""
        # This is a simple test - in a real scenario you might want more comprehensive randomness testing
        results = []
        for _ in range(10):
            results.append(self.slot_machine.spin())
        
        # Check that not all spins are identical
        # This is a probabilistic test, but very unlikely to fail
        all_same = True
        first_spin = results[0]
        for spin in results[1:]:
            if spin != first_spin:
                all_same = False
                break
        self.assertFalse(all_same)
    
    def test_check_winnings_no_wins(self):
        """Test check_winnings with no winning lines"""
        # Create a grid with no winning lines
        columns = [
            ["🍒", "🍉", "🍀"],
            ["🍒", "🍋", "🍀"],
            ["🍒", "🍉", "🍀"]
        ]
        winnings, winning_lines = self.slot_machine.check_winnings(columns, 3, 10)
        self.assertEqual(winnings, 0)
        self.assertEqual(winning_lines, [])
    
    def test_check_winnings_with_wins(self):
        """Test check_winnings with winning lines"""
        # Create a grid with winning lines (first line is all A, third line is all C)
        columns = [
            ["A", "B", "C"],
            ["A", "D", "C"],
            ["A", "B", "C"]
        ]
        winnings, winning_lines = self.slot_machine.check_winnings(columns, 3, 10)
        # A has value 5, C has value 3, bet is 10
        # So winnings should be 5*10 + 3*10 = 80
        self.assertEqual(winnings, 80)
        self.assertEqual(set(winning_lines), {1, 3})  # Lines 1 and 3 should win

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()
    
    def test_init(self):
        """Test player initialization"""
        self.assertEqual(self.player.balance, 0)
    
    @patch('builtins.input', return_value="100")
    def test_deposit_valid(self, mock_input):
        """Test deposit with valid input"""
        amount = self.player.deposit()
        self.assertEqual(amount, 100)
        self.assertEqual(self.player.balance, 100)
    
    @patch('builtins.input', side_effect=["abc", "-50", "0", "100"])
    @patch('builtins.print')
    def test_deposit_invalid_then_valid(self, mock_print, mock_input):
        """Test deposit with invalid inputs followed by valid input"""
        amount = self.player.deposit()
        self.assertEqual(amount, 100)
        self.assertEqual(self.player.balance, 100)
        # Check that print was called for error messages
        self.assertTrue(mock_print.call_count >= 3)  

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
    
    def test_init(self):
        """Test game initialization"""
        self.assertIsInstance(self.game.slot_machine, SlotMachine)
        self.assertIsInstance(self.game.player, Player)
        self.assertEqual(self.game.max_lines, 3)
        self.assertEqual(self.game.min_bet, 1)
        self.assertEqual(self.game.max_bet, 100)
    
    @patch('builtins.input', side_effect=["2"])
    def test_get_number_of_lines_valid(self, mock_input):
        """Test get_number_of_lines with valid input"""
        lines = self.game.get_number_of_lines()
        self.assertEqual(lines, 2)
    
    @patch('builtins.input', side_effect=["abc", "0", "4", "2"])
    @patch('builtins.print')
    def test_get_number_of_lines_invalid_then_valid(self, mock_print, mock_input):
        """Test get_number_of_lines with invalid inputs followed by valid input"""
        lines = self.game.get_number_of_lines()
        self.assertEqual(lines, 2)
        # Check that print was called for error messages
        self.assertTrue(mock_print.call_count >= 3)
    
    @patch('builtins.input', side_effect=["50"])
    def test_get_bet_valid(self, mock_input):
        """Test get_bet with valid input"""
        bet = self.game.get_bet()
        self.assertEqual(bet, 50)
    
    @patch('builtins.input', side_effect=["abc", "0", "150", "50"])
    @patch('builtins.print')
    def test_get_bet_invalid_then_valid(self, mock_print, mock_input):
        """Test get_bet with invalid inputs followed by valid input"""
        bet = self.game.get_bet()
        self.assertEqual(bet, 50)
        # Check that print was called for error messages
        self.assertTrue(mock_print.call_count >= 3)
    
    @patch('builtins.input', side_effect=["2", "25"])
    @patch('builtins.print')
    def test_play_round_insufficient_balance(self, mock_print, mock_input):
        """Test play_round with insufficient balance"""
        self.game.player.balance = 40  # Not enough for 2 lines at $25 each
        
        # We need to mock the get_bet method to return a smaller value after first attempt
        original_get_bet = self.game.get_bet
        mock_returns = [25, 10]  # First try $25, then $10
        
        def mock_get_bet():
            return mock_returns.pop(0)
            
        self.game.get_bet = mock_get_bet
        
        # Mock spin method to return predictable results
        def mock_spin():
            return [["A", "B", "C"], ["A", "B", "C"], ["A", "B", "C"]]
            
        self.game.slot_machine.spin = mock_spin
        
        # Let's reset the inputs for the test
        mock_input.side_effect = ["2"]
        
        # Run the method
        with patch.object(self.game, 'get_bet', side_effect=[25, 10]):
            with patch.object(self.game.slot_machine, 'spin', return_value=[["A", "B", "C"], ["A", "B", "C"], ["A", "B", "C"]]):
                with patch.object(self.game.slot_machine, 'display'):
                    self.game.play_round()
        
        # Check that an error message was printed
        for call in mock_print.call_args_list:
            args, _ = call
            if "You do not have enough" in ''.join(str(arg) for arg in args):
                break
        else:
            self.fail("Did not print insufficient balance message")

if __name__ == '__main__':
    unittest.main()