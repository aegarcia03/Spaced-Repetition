from flask import Flask, render_template, request
from slot_machine import SlotMachine, Game, Player, Symbol

application = Flask(__name__)


@application.route('/', methods=['GET', 'POST'])
def index():
    #will store the spin results
    result = None
    balance = 0

    if request.method == 'POST':
        initial_balance = int(request.form.get('balance', 0))
        lines = int(request.form.get('lines', 1))
        bet = int(request.form.get('bet', 1))

        print("Form submitted:", request.form)

        # Initialize game with Player
        player = Player(initial_balance)
        game = Game()
        game.player = player
        # Spin the slot machine
        result = game.slot_machine.spin(lines, bet)
        #Check winnings 
        winnings, winning_lines = game.slot_machine.check_winnings(result, lines, bet)
        #Update player balance 
        player.balance += winnings - (bet * lines)
        balance = player.balance
        #store all the result into a dict so i can pass it on HTML template
        result = {
            'columns': result,
            'winnings': winnings,
            'lines': winning_lines
        }
        #Renders the index.html page and gives it the result data
        total_bet = bet * lines 
        balance += winnings - total_bet
    
    return render_template('index.html', result=result, balance=balance)


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=8000)