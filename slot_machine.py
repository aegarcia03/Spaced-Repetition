import random

class Symbol():
    '''Represents each symbol of the slot machine
    Each symbol has a name, frequency (how often appears) and
    value (payout multiplier)'''
    def __init__(self, name, frequency, value):
        self.name = name
        self.frequency = frequency
        self.value = value

class SlotMachine():
    '''Represents the slot machine that manage symbols, spinning 
    and calculating wins'''
    def __init__(self, rows=3, cols=3):
        #Set up dimensions of the slot machine grid
        self.rows = rows
        self.cols = cols

        # Define all available symbols with their properties
        self.symbols = {
            "💎": Symbol("💎", 1, 10),     # Very rare, huge payout
            "🍒": Symbol("🍒", 2, 5),      # Rare, good payout
            "🔔": Symbol("🔔", 3, 6),      # Medium rare
            "🍋": Symbol("🍋", 4, 4),      # Uncommon
            "🍉": Symbol("🍉", 6, 3),      # Common
            "🍀": Symbol("🍀", 8, 2)       # Very common
        }

    def spin(self):
        '''Simulates the spinning of the slot machine'''
        #Create a pool of all symbols according to their frequencies
        all_symbols = []
        for symbol_name, symbol in self.symbols.items():
            # Add each symbol to the pool number of times specified by its frequency
            all_symbols.extend([symbol_name] * symbol.frequency)
        
        # Generate the result grid column by column
        columns = []
        for _ in range(self.cols):
            column = []
            for _ in range(self.rows):
                value = random.choice(all_symbols)
                # add the value to the current colum
                column.append(value)
        
            columns.append(column)
        return columns 

    def display(self, columns):
        '''Displays the slot machine grid'''
        for row in range(len(columns[0])):
            for i, column in enumerate(columns): #get the key:value
                #Print each symbol in the row with a separator

                if i != len(columns) - 1: # Is the current column NOT the last column?
                    #gives you the index of the last column (since indices start at 0
                    print(column[row], end=" | ")
                else:
                    print(column[row], end="")# Last symbol in row has no divider
            print() #Move to the next row

    def check_winnings(self, columns, lines, bet):
        '''
        Checks for winning lines and calculates total winning
        '''
        winnings = 0
        winning_lines = []

        for line in range(lines):  # line = 0, 1, 2 depending on how many lines bet on
            symbol = columns[0][line]

            for column in columns:
                if column[line] != symbol:
                    break
            else:
                # This else block only runs if the loop didn't break
                winnings += self.symbols[symbol].value * bet
                winning_lines.append(line + 1)

        return winnings, winning_lines

    def show_payout_table(self):
        print("\n🎰 Symbol Payouts:")
        print("------------------------")
        for symbol in self.symbols.values():
            print(f"{symbol.name}  →  x{symbol.value} payout")

class Player():
    '''Represents a player balance and deposit functionality'''

    def __init__(self):
        self.balance = 0 #Player starts with 0 balance
    
    def deposit(self):
        '''
        Allows player to deposit money into their balance.
        Handles validation of deposit amount.
        Returns the amount deposited.
        '''
        while True:
            amount = input("What would you like to deposit? $")
            if amount.isdigit():
                amount = int(amount)
                if amount > 0:
                    self.balance += amount 
                    return amount
                else:
                    print("Amount must be greater than 0.")
            else:
                print("Please enter a number.")
        
class Game():
    '''
    Contorl the overall game flow and manages interactions between
    the player and slot machine 
    '''
    def __init__(self):
        #Create the slot machine
        self.slot_machine = SlotMachine()

        #Create the player
        self.player = Player()

        #Define game constants
        self.max_lines = 3
        self.max_bet = 100
        self.min_bet = 1
    
    def get_number_of_lines(self):
        """
        Gets and validates player input for number of lines to bet on.
        """
        while True:
            lines = input(
                "Enter the number of lines to bet on (1-" + str(self.max_lines) + ")? ")
            if lines.isdigit():
                lines = int(lines)
                if 1 <= lines <= self.max_lines:
                    return lines
                else:
                    print("Enter a valid number of lines.")
            else:
                print("Please enter a number.")
    
    def get_bet(self):
        """
        Gets and validates player input for bet amount per line.
        """
        while True:
            amount = input("What would you like to bet on each line? $")
            if amount.isdigit():
                amount = int(amount)
                if self.min_bet <= amount <= self.max_bet:
                    return amount
                else:
                    print(f"Amount must be between ${self.min_bet} - ${self.max_bet}.")
            else:
                print("Please enter a number.")
        
    def play_round(self):
        """
        Executes a complete round of gameplay:
        - Getting bet info
        - Spinning the slot machine
        - Calculating and displaying results
        - Updating player balance
        
        Returns the net winnings (positive or negative) from this round.
        """
        #Get the number of lines to bet on
        lines = self.get_number_of_lines()
        #Get bet amount per line (with validation of sufficient balance)
        while True:
            bet = self.get_bet()
            total_bet = bet * lines
            #Check if player has enough balance for this bet
            if total_bet > self.player.balance:
                print(
                    f"You do not have enough to bet that amount, your current balance is: ${self.player.balance}")
            else:
                break
        #Display bet information
        print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")
        #Spin the slot machine
        slots = self.slot_machine.spin()
        #Display the result grid
        self.slot_machine.display(slots)
        #Check for winnings 
        winnings, winning_lines = self.slot_machine.check_winnings(slots, lines, bet)
        #Display winning information
        print(f"You won ${winnings}.")
        if winning_lines:
            print(f"You won on lines:", *winning_lines) ## The * unpacks the list
        #Calculate and update the player balance
        net_winnings = winnings - total_bet
        self.player.balance += net_winnings
        
        return net_winnings

    def run(self):
        """
        Main game loop that runs the entire game:
        - Initial deposit
        - Repeated rounds of play until player quits
        - Final balance display
        """
        self.player.deposit()
        self.slot_machine.show_payout_table()
        #Main game loop
        while True:
            print(f"Current balance is ${self.player.balance}")
            #Ask if player wants to play or quit
            answer = input("🎰Press enter to play (q to quit).")
            if answer.lower() == "q":
                break
            #Play one round of the fame 
            self.play_round()
        #Display the final balance when player quits
        print(f"You left with ${balance}")



# Entry point - only run game if script is executed directly
if __name__ == "__main__":
    game = Game()
    game.run()