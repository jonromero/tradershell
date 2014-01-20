"""
An interactive shell to calculate positions in the stock market

Jon Vlachogiannis
darksun4@gmail.com
20/01/2014
"""
import readline
import shlex
from datetime import datetime
import json

def read_config():
    with open("settings.json", "r") as f:
        return json.loads(f.read().strip())

def read_bank():
    with open("current_bank.dat", "r") as f:
        return f.read().strip()

def update_bank(amount):
    with open("current_bank.dat", "w") as f:
        f.write(amount)

def write_position(trade, amount):
    print "Writing transaction..."
    with open("transactions.csv", "a+") as f:
        f.write("%s; %s; %s; %s; %s\n" % (datetime.now(),   
                                     trade['ticker'],  
                                     trade['price'],   
                                     trade['position'],
                                     trade['reason']))
    print "Done"

    print "Updating bank..."
    update_bank(str(float(read_bank())-amount))
    print "Done"

def calculate_position(trade):
    bank = float(read_bank())
    strategy = read_config()
    price = float(trade['price'])
    
    amount = bank * strategy['risk']
    stop_win = price * strategy['stop_win']
    stop_loss = price * strategy['stop_loss']

    stop_win += price if trade['position'] == "BUY" else -price
    stop_loss -= price if trade['position'] == "BUY" else -price
    
    return {'amount': amount,
            'stop_win': stop_win,
            'stop_loss': stop_loss}

def display(trade):
    print trade

def sync_gdocs():
    print "TODO: sync with gdocs"
    return

def next_arg(prompt=""):
    return shlex.split(raw_input(prompt+'> '))[0]

def start_session():
    trade = {}

    while True:
        print("Enter 'new', 'update', 'save' or 'sync'")

        selection = next_arg()

        if selection == "new":
            trade = {}
            trade['ticker'] = next_arg("ticker?")
            trade['price'] = next_arg("price?")
            trade['position'] = next_arg("position? (buy/sell)").upper()
            trade['reason'] = next_arg("reason?")

            proposed_position = calculate_position(trade)
            display(proposed_position)

        elif selection == "save":
            proposed_position = calculate_position(trade)
            write_position(trade, proposed_position['amount'])

        elif selection == "update":
            trade['price'] = next_arg("price?")

            proposed_position = calculate_position(trade)
            display(proposed_position)

        elif selection == "sync":
            sync_gdocs()
            
        else:
            print "Unknown command '%s'" % selection

def main():
    print("Tradershell by Jon Vlachogiannis")

    start_session()


main()
