from random import shuffle

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True

# CLASSES


class Card:  # Creates all the cards

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:  # creates a deck of cards

    def __init__(self):
        # self.cards = []
        # self.value = 0
        # self.aces = 0
        self.deck = []  # haven't created a deck yet
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):  # using shuffle from Random
        # print([card.rank for card in self.deck])
        shuffle(self.deck)
        # print([card.rank for card in self.deck])
    

    def deal(self):  # pick out a card from the deck
        self.deck.pop()

    def add_card(self, hand):  # add a card to the player's or dealer's hand

        current_card = self.deck.pop()
        hand.cards.append(current_card)
        hand.value += values[current_card.rank]
        if current_card.rank == 'Ace':
            hand.aces += 1
    
        

class Hand:   # show all the cards that the dealer and player have

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # keep track of aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Poker_Chips:   # keep track of chips

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win(self):
        self.total += self.bet

    def lose(self):
        self.total -= self.bet


class Functions: # game functionality and outcomes

    def __init__(self):
        self.deck = Deck()
        self.chips = Poker_Chips()
        
    def decorate_print(func):
        def inner(*args, **kwargs):
            print("\n=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~")
            func(*args, **kwargs)
            print("\n=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~")
            
        return inner


    def betting(self):  # ask for user's bet

        while True:
            try:
                self.chips.bet = int(input("\nPlease enter the number of chips you want to bet: "))
            except ValueError:
                print("\nWoah there, City Slicker! You gotta enter a number.")
            else:
                if self.chips.bet > 100:
                    print("\nHold your horses! The maximum bet is 100 chips!")
                else:
                    break


    def hit(self):
        self.deck.add_card(self.dealer_hand) # self.deck.deal()
        self.player_hand.adjust_for_ace()


    def hit_or_stay(self):   # hit or stay
        global playing

        while self.player_hand.value < 21:
            h_or_s = input("\nDo you want to hit or stay? ('h' or 's'): ")

            if h_or_s.lower() == 'h':
                
                self.deck.add_card(self.player_hand) # self.deck.deal()
                self.player_hand.adjust_for_ace()
                self.show_1()
            elif h_or_s.lower() == 's':
                print(f"\n{name} chose to stay, The Dealer is now playing....")
                print("\nPlease wait...")
                break
            else:
                print("\nThat ain't a choice, partner! Pick again")
                continue
            


    def show_1(self):
        print("\nDealer's Hand: ")
        print("[~ HIDDEN CARD ~]")
        print("", self.dealer_hand.cards[1])
        print(f"\n{name}'s Hand: ", *self.player_hand.cards, sep='\n ')
        print(f"\n{name}'s Current Total: ", self.player_hand.value)


    def show_hands(self):
        print("\nDealer's Hand: ", *self.dealer_hand.cards, sep='\n ')
        print("\nDealer's Score: ", self.dealer_hand.value)
        print(f"\n{name}'s Hand: ", *self.player_hand.cards, sep='\n ')
        print(f"\n{name}'s Score: ", self.player_hand.value)


    # OUTCOMES:

    @decorate_print
    def player_busts(self):
        print(f"\n{name} BUSTS!")
        self.chips.lose()

    @decorate_print
    def player_wins(self):
        print(f"\n{name} WINS!")
        self.chips.win()

    @decorate_print
    def dealer_busts(self):
        print("\nDEALER BUSTS!")
        print(f"\n{name} WIN!")
        self.chips.win()

    @decorate_print
    def dealer_wins(self):
        print("\nDEALER WINS!")
        self.chips.lose()

    @decorate_print
    def tie(self):
        print(f"\n{name} tied with the dealer!")

 #play the game    

    def run(self):
        playing = True
        while True:
            print("\n=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~")
            print("\nWelcome to Wild West Casino!")
            print("\nLet's play Blackjack!")
            print("\nYou have 100 poker chips.")
            print("\n=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~")
            global name
            name = input("\nPlease enter your outlaw name: ")

            # shuffle the deck
            self.deck.shuffle()

            self.player_hand = Hand()
            self.deck.add_card(self.player_hand) 
            self.deck.add_card(self.player_hand) # (self.deck.deal())

            self.dealer_hand = Hand()
            self.deck.add_card(self.dealer_hand)
            self.deck.add_card(self.dealer_hand)

            # ask player for bet
            self.betting()

            # show cards
            self.show_1()

            while playing:
                if self.player_hand.value == 21: # if 1st deal is 21 => BLACKJACK!!!!
                    self.player_wins()
                    break

                self.hit_or_stay()
                self.show_1()

                if self.player_hand.value > 21:
                    self.player_busts()
                    break

            # playing = False
            
                if self.player_hand.value <= 21:

                    while self.dealer_hand.value < 17:
                        self.hit()

                    self.show_hands()

                    if self.dealer_hand.value > 21:
                        self.dealer_busts()

                    elif self.dealer_hand.value > self.player_hand.value:
                        self.dealer_wins()

                    elif self.dealer_hand.value < self.player_hand.value:
                        self.player_wins()
                    
                    elif self.dealer_hand.value == self.player_hand.value:
                        self.tie()

                    if self.player_hand.value > 21:
                        self.player_busts()
                playing = False
            print(f"\n{name}'s total chips:", self.chips.total)

            new_game = input("\nDo you want to play again? Enter 'y' or 'n': ")

            if new_game.lower() == 'y':
                playing = True
                # print(self.player_hand.value)
                # self.player_hand.value = 0
                # self.dealer_hand.value = 0
                continue

            else:
                print("\n=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~")
                print("\nThanks for visiting Connor's Casino!")
                print("\nCome back anytime!")
                print("\n=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~")
                break


play = Functions()
print(play.run())
