import unittest
from unittest.mock import patch
from slot_machine import Symbol, SlotMachine, Player, Game

class TestSymbol(unittest.TestCase):
    def test_symbol_initialization(self):
        symbol = Symbol("💎", 1, 10)
        self.assertEqual(symbol.name, "💎")
        self.assertEqual(symbol.frequency, 1)
        self.assertEqual(symbol.value, 10)

class TestSlotMachine(unittest.TestCase):
    def setUp(self):
        self.slot_machine = SlotMachine()
    
    def test_init(self):
        self.assertEqual(self.slot_machine.rows, 3)
        self.assertEqual(self.slot_machine.cols, 3)
        self.assertEqual(len(self.slot_machine.symbols), 6) 
        
    def test_spin_dimensions(self):
        result = self.slot_machine.spin()
        self.assertEqual(len(result), self.slot_machine.cols)
        for column in result:
            self.assertEqual(len(column), self.slot_machine.rows)
    
    def test_spin_randomness(self):
        results = [self.slot_machine.spin() for _ in range(10)]
        all_same = all(spin == results[0] for spin in results[1:])
        self.assertFalse(all_same)
    
    def test_check_winnings_no_wins(self):
        columns = [
            ["🍒", "🍋", "💎"],
            ["🔔", "🍉", "🍋"],
            ["🍀", "💎", "🍉"]
        ]
        winnings, winning_lines = self.slot_machine.check_winnings(columns, 3, 10)
        self.assertEqual(winnings, 0)
        self.assertEqual(winning_lines, [])
    
    def test_check_winnings_with_wins(self):
        columns = [
            ["🍒", "🍉", "🍀"],
            ["🍒", "🍋", "🍀"],
            ["🍒", "🍉", "🍀"]
        ]
        winnings, winning_lines = self.slot_machine.check_winnings(columns, 3, 10)
        self.assertEqual(winnings, 70)
        self.assertEqual(set(winning_lines), {1, 3})

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()
    
    def test_init(self):
        self.assertEqual(self.player.balance, 0)
    
    @patch('builtins.input', return_value="100")
    def test_deposit_valid(self, mock_input):
        amount = self.player.deposit()
        self.assertEqual(amount, 100)
        self.assertEqual(self.player.balance, 100)
    
    @patch('builtins.input', side_effect=["abc", "-50", "0", "100"])
    @patch('builtins.print')
    def test_deposit_invalid_then_valid(self, mock_print, mock_input):
        amount = self.player.deposit()
        self.assertEqual(amount, 100)
        self.assertEqual(self.player.balance, 100)
        self.assertTrue(mock_print.call_count >= 3)  

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
    
    def test_init(self):
        self.assertIsInstance(self.game.slot_machine, SlotMachine)
        self.assertIsInstance(self.game.player, Player)
        self.assertEqual(self.game.max_lines, 3)
        self.assertEqual(self.game.min_bet, 1)
        self.assertEqual(self.game.max_bet, 100)
    
    @patch('builtins.input', side_effect=["2"])
    def test_get_number_of_lines_valid(self, mock_input):
        lines = self.game.get_number_of_lines()
        self.assertEqual(lines, 2)
    
    @patch('builtins.input', side_effect=["abc", "0", "4", "2"])
    @patch('builtins.print')
    def test_get_number_of_lines_invalid_then_valid(self, mock_print, mock_input):
        lines = self.game.get_number_of_lines()
        self.assertEqual(lines, 2)
        self.assertTrue(mock_print.call_count >= 3)
    
    @patch('builtins.input', side_effect=["50"])
    def test_get_bet_valid(self, mock_input):
        bet = self.game.get_bet()
        self.assertEqual(bet, 50)
    
    @patch('builtins.input', side_effect=["abc", "0", "150", "50"])
    @patch('builtins.print')
    def test_get_bet_invalid_then_valid(self, mock_print, mock_input):
        bet = self.game.get_bet()
        self.assertEqual(bet, 50)
        self.assertTrue(mock_print.call_count >= 3)
    
    @patch('builtins.input', side_effect=["2", "25"])
    @patch('builtins.print')
    def test_play_round_insufficient_balance(self, mock_print, mock_input):
        self.game.player.balance = 40  # Not enough for 2 lines at $25 each

        mock_returns = [25, 10]

        def mock_get_bet():
            return mock_returns.pop(0)
        
        self.game.get_bet = mock_get_bet

        emoji_grid = [
            ["🍉", "🍋", "🍀"],
            ["🍉", "🍋", "🍀"],
            ["🍉", "🍋", "🍀"]
        ]

        with patch.object(self.game, 'get_bet', side_effect=[25, 10]):
            with patch.object(self.game.slot_machine, 'spin', return_value=emoji_grid):
                with patch.object(self.game.slot_machine, 'display'):
                    self.game.play_round()

        for call in mock_print.call_args_list:
            args, _ = call
            if "You do not have enough" in ''.join(str(arg) for arg in args):
                break
        else:
            self.fail("Did not print insufficient balance message")

if __name__ == '__main__':
    unittest.main()
