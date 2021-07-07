from random import shuffle

suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
         'Jack', 'Queen', 'King', 'Ace']
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:

    def __init__(self, suit, rank):
        # card attributes
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):

        self.all_cards = []

        # generate the deck (each card is a Card class object)
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck (all cards)
        shuffle(self.all_cards)

    def draw_one(self):
        # draw one card and return it
        return self.all_cards.pop()


class Credit:
    # navigating user's balance
    def __init__(self):

        self.balance = 0

    def add_balance(self):
        # adding money to the current balance
        while True:
            try:
                cash_in = int(input("How much would you like to add to your balance? $"))
            except ValueError:
                print("Please provide an integer.")
                continue
            else:
                self.balance += cash_in
                print(f'Your current balance is ${self.balance}')
                break

    def put_bet(self):
        # betting system
        while True:
            try:
                bet = int(input("How much would you like to bet? $"))
            except ValueError:
                print("Please provide an integer.")
                continue
            else:
                if bet > self.balance:
                    while bet > self.balance:
                        no_money = input("You do not have enough credit. Would you like to add "
                                         "to your current balance? ").lower()
                        if no_money == "yes":
                            self.add_balance()
                            bet = 0
                        elif no_money == "no":
                            break
                        else:
                            print("Please type 'Yes' or 'No'")
                            continue
                else:
                    self.balance -= bet
                    return bet


class Table:
    """
    Takes in an instance of the Deck class
    Takes in the bet from Credit.bet()
    """

    def __init__(self, new_deck, bet_value):

        # new deck, player cards, dealer cards
        self.new_deck = new_deck
        self.player_cards = []
        self.dealer_cards = []
        # second hand after split:
        self.split_hand_two = []
        self.bet_value = bet_value
        # if player stands, turns true:
        self.stand = False
        # insurance bet:
        self.insurance = bet_value/2
        # second stake:
        self.split_bet = bet_value
        # on/off hand while split:
        self.hand_one_on = False
        self.hand_two_on = False
        # variables for final value and bust check:
        self.player_sum = 0
        self.hand_two_sum = 0
        self.dealer_sum = 0
        # win/loose
        self.player_win = None
        self.hand_two_win = None
        self.dealer_win = None
        self.dealer_win_hand_two = None
        self.tie = None
        self.tie_hand_two = None

    #  move:

    def first_deal(self):

        # deal two to the player and two to the dealer
        self.player_cards.append(self.new_deck.pop(0))
        self.dealer_cards.append(self.new_deck.pop(0))
        self.player_cards.append(self.new_deck.pop(11))
        self.dealer_cards.append(self.new_deck.pop(0))

    # Adding one card:

    def hit_player(self):

        self.player_cards.append(self.new_deck.pop(0))

    def split_hit_two(self):

        self.split_hand_two.append(self.new_deck.pop(0))

    def hit_dealer(self):

        self.dealer_cards.append(self.new_deck.pop(0))

    def split_table(self):
        self.split_hand_two.append(self.player_cards.pop(-1))
        self.player_cards.append(self.new_deck.pop(0))
        self.split_hand_two.append(self.new_deck.pop(0))

    # Displaying the cards:

    def print_player_cards(self):
        print("Player cards:")
        for x in range(0, len(self.player_cards)):
            print(self.player_cards[x])

    def print_split_hand_two(self):
        print("Hand two:")
        for x in range(0, len(self.split_hand_two)):
            print(self.split_hand_two[x])

    def print_dealer_cards(self):
        print("Dealer cards:")
        for x in range(0, len(self.dealer_cards)):
            print(self.dealer_cards[x])

    # Sums of the cards' values:

    def sum_player_cards(self):
        for i in range(0, len(self.player_cards)):
            self.player_sum += self.player_cards[i].value

    def sum_split_hand_two(self):
        for i in range(0, len(self.split_hand_two)):
            self.hand_two_sum += self.split_hand_two[i].value

    def sum_dealer_cards(self):
        for i in range(0, len(self.dealer_cards)):
            self.dealer_sum += self.dealer_cards[i].value


# Take user move:
def take_input(message):

    while True:
        player_input = input(f"{message}: ").lower()
        if player_input not in ["hit", "stand", "insure", "dd", "split"]:
            print("Please enter a proper command.")
        else:
            break
    return player_input


# Check if a hand contains Ace and change its value to 1 in case the hand is bust:
def bust_hand_has_ace(card_list):
    for i in range(0, len(card_list)):
        if card_list[i].rank == "Ace":
            if card_list[i].value == 11:
                card_list[i].value = 1
                break
            else:
                pass
        elif i == len(card_list) - 1:
            break
        else:
            pass
