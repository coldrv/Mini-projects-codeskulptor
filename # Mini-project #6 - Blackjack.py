# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = { 'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10,'CA':1,'SA':1,'HA':1,'DA':1, 'C2':2,'S2':2,'H2':2,'D2':2, 'C3':3,'S3':3,'H3':3,'D3':3, 'C4':4, 'C5':5, 'C6':6, 'C7':7, 'C8':8, 'C9':9, 'CT':10, 'CJ':10, 'CQ':10, 'CK':10, 'S4':4, 'S5':5, 'S6':6, 'S7':7, 'S8':8, 'S9':9, 'ST':10, 'SJ':10, 'SQ':10, 'SK':10, 'H4':4, 'H5':5, 'H6':6, 'H7':7, 'H8':8, 'H9':9, 'HT':10, 'HJ':10, 'HQ':10, 'HK':10, 'D4':4, 'D5':5, 'D6':6, 'D7':7, 'D8':8, 'D9':9, 'DT':10, 'DJ':10, 'DQ':10, 'DK':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print ("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, in_play):
      
        if in_play and pos[0]==25:
            card_loc = (36,48)
            canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        elif in_play:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

                
        else:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


# define hand class
class Hand:
    
    
    def __init__(self):
        self.card=[]
        
    def add_card(self,c):

        self.card.append(c)
    
    def __str__(self):
        ans=''
        for x in range(len(self.card)):
            c=self.card[x]
            ans += c.__str__() + ' '
            
            
        return 'Hand contains ' + ans

    def get_value(self):
        
        hand_value=0
        c=0
        for i in range(len(self.card)):
            
            if VALUES[self.card[i].__str__()]!=1:
                if c==2:
                    hand_value+=VALUES[self.card[i].__str__()]-10
                    c=1
                else:
                    hand_value+=VALUES[self.card[i].__str__()]
            else:
                if hand_value + 11 <= 21:
                    c+=1
                    hand_value= hand_value+11
                else:
                    c+=1
                    hand_value += 1
                   
        return hand_value

    def drawhand(self, canvas, pos,in_play):
        
        for i in range(len(self.card)):
            self.card[i].draw(canvas,pos,in_play)
            pos[0]+=72
 
        
# define deck class 
class Deck:
    
    def __init__(self):
        self.deck=[]
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s,r))
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        c=self.deck[0]
        self.deck.pop(0)
        return c
    
    def __str__(self): 
        
        ans=''
        
        for i in range(len(self.deck)):
            c= self.deck[i]
            x= c.__str__()
            ans +=x +' '
            
        return 'Deck contains ' + ans


#define event handlers for buttons
def deal():
    global score,outcome,player_hand, dealer_hand, play_deck, in_play
   
    outcome = "Hit or stand?"
    if in_play:
        score-=1
    in_play = True
    player_hand=Hand()
    dealer_hand=Hand()
    play_deck=Deck()
    play_deck.shuffle()

    for i in range(0,4):
        if i==0 or i==1:
            player_hand.add_card(play_deck.deal_card())
            
        else:
            dealer_hand.add_card(play_deck.deal_card())
            
       
                
    
    

def hit():
    global outcome, score, in_play
    
    if player_hand.get_value() <=21 and in_play==True:
        player_hand.add_card(play_deck.deal_card())
        
        if player_hand.get_value() <=21 and in_play==True:
            outcome = 'Hit or Stand?'
        elif in_play:
            
            outcome = "You have busted! For another game, hit deal"
            score-=1
            in_play= False
 
    elif in_play:
        outcome = "You have busted!For another game, hit deal"
        score-=1
        in_play = False
    else:
        outcome ='Hit deal for another game'
        
   
       
def stand():
    global outcome, in_play,score
    in_play=True
    if player_hand.get_value() >21:
        outcome = "You have busted! For another game, hit deal"
        score-=1
        in_play = False
    else:
        while dealer_hand.get_value()<=17:
            dealer_hand.add_card(play_deck.deal_card())
        
        if  dealer_hand.get_value()<=21 and dealer_hand.get_value()>= player_hand.get_value():
            outcome = 'Dealer won! For another game, hit deal'
            score-=1
            in_play = False
        else:
            outcome = 'You Won!! For another game, hit deal'
            score+=1
            in_play = False
            
   

# draw handler    
def draw(canvas):
    
    player_hand.drawhand(canvas,[25,185], False)
    dealer_hand.drawhand(canvas,[25,385], in_play)
    canvas.draw_text('BLACKJACK', (225, 45), 33, 'Yellow')
    canvas.draw_text( str(outcome), (205, 175), 22, 'Red')
    canvas.draw_text('Player', (25, 175), 22, 'Yellow')
    canvas.draw_text('Dealer', (25, 375), 22, 'Yellow')
    canvas.draw_text( 'score: '+str(score), (450, 125), 22, 'Red')



# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Black")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
