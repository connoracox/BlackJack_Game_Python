from random import shuffle

#set up card deck using suits and ranks
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

# create dictionary to give ranks an int value so we can add up to 21
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True

# CLASSES

class Card:  # create cards

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:  # create deck with the cards

    def __init__(self):
        self.deck = []  
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):  # using shuffle from Random
        shuffle(self.deck)
    

    def deal(self):  # .pop takes first card off top
        single_card = self.deck.pop()
        return single_card


class Hand:   # show all the cards that the dealer and player have

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # keep track of aces

    def add_card(self, card):  # deal a card to player or dealer
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self): # makes ace value of 1 if it will cause bust
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Poker_Chips:   # chip bank with funcs for win and lose

    def __init__(self):
        self.total = 100 #bank defaults to 100
        self.bet = 0

    def win(self):
        self.total += self.bet

    def lose(self):
        self.total -= self.bet


# FUNCTIONS

def decorate_print(func):
    def inner(*args, **kwargs):
        print("\n=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~")
        func(*args, **kwargs)
        print("\n=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~")
        
    return inner

def betting(chips):  # ask for user's bet

    while True:
        try:
            chips.bet = int(input("\nPlease enter the number of chips you want to bet: "))
        except ValueError:
            print("\nWoah there, City Slicker! You gotta enter a number.")
        else:
            if chips.bet > chips.total:
                print("\nHold your horses! The maximum bet is 100 chips!")
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stay(deck, hand):   # hit or stay
    global playing

    while True:
        h_or_s = input("\nDo you want to hit or stay? ('h' or 's'): ")

        if h_or_s.lower() == 'h':
            hit(deck, hand)
        elif h_or_s.lower() == 's':
            print(f"\n{player_name} chose to stay, The Dealer is now playing....")
            print("\nPlease wait...")
            playing = False
        else:
            print("\nSorry! Please try again!")
            continue
        break


def show_1(player, dealer):
    print("\nDealer's Hand: ")
    print(" [~ HIDDEN CARD ~]")
    print("", dealer.cards[1])
    print("\nYour Hand: ", *player.cards, sep='\n ')
    print(f"\n{player_name}'s Current Total: ", player.value)


def show_hands(player, dealer):
    print("\nDealer's Hand: ", *dealer.cards, sep='\n ')
    print("\nDealer's Score: ", dealer.value)
    print("\nYour Hand: ", *player.cards, sep='\n ')
    print(f"\n{player_name}'s Score: ", player.value)


# OUTCOMES:

@decorate_print
def player_busts(player, dealer, chips):
    print(f"\n{player_name.upper()} BUSTS!")
    chips.lose()

@decorate_print
def player_wins(player, dealer, chips):
    print(f"\n{player_name.upper()} WINS!")
    chips.win()

@decorate_print
def dealer_busts(player, dealer, chips):
    print("\nDEALER BUSTS!")
    print(f"\n{player_name.upper()} WINS!")
    chips.win()

@decorate_print
def dealer_wins(player, dealer, chips):
    print("\nDEALER WINS!")
    chips.lose()

@decorate_print
def tie(player, dealer):
    print(f"\n{player_name} tied with the dealer!")


# PLAY:

while True:
    print("\n=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~")
    print("\nWelcome to Wild West Casino!")
    print("\nLet's play Blackjack!")
    print("\nYou have 100 poker chips.")
    print("\n=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~")
    player_name = input("\nPlease enter your outlaw name: ")

    # create and shuffle the deck
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # player's bank of chips
    player_chips = Poker_Chips()

    #betting time
    betting(player_chips)

    # show cards
    show_1(player_hand, dealer_hand)

    while playing:
        if player_hand.value == 21: # if 1st deal is 21 => BLACKJACK!!!!
            player_wins(player_hand, dealer_hand, player_chips)
            break

        hit_or_stay(deck, player_hand)
        show_1(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    if player_hand.value <= 21: # game play if not 21 at 1st deal

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        show_hands(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        
        elif dealer_hand.value == player_hand.value:
            tie(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)

    print(f"\n{player_name}'s total chips:", player_chips.total)

    new_game = input("\nDo you want to play again? Enter 'y' or 'n': ")

    if new_game.lower() == 'y':
        playing = True
        continue

    else:
        print("\n=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~")
        print("\nThanks for visiting Wild West Casino!")
        print("\nCome back anytime now, ya hear!")
        print("\n=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~")
        break






