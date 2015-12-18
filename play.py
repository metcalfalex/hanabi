
# -----------------------------------------------
# References
# -----------------------------------------------

# -----------------------------------------------
# Libraries
# -----------------------------------------------

import random
import os
import time
import sys

# -----------------------------------------------
# Functions
# -----------------------------------------------


###############
### Support Functions
###############


def set_up_table():
   # shuffle deck
   random.shuffle(deck)
   # deal hands
   for deal in range(5):
      for hands in range(len(hand_play)):
         hand_play[hands].append(deck[0])
         hand_play_know[hands].append([[0,0,0,0,0],[0,0,0,0,0]])
         del deck[0]


def build_hand_full(player):
   hand_full[player] = []
   for card in range(len(hand_play[player])):
      hand_full[player].append(hand_play[player][card])
   for card in range(len(hand_keep[player])):
      hand_full[player].append(hand_keep[player][card])
   for card in range(len(hand_throw[player])):
      hand_full[player].append(hand_throw[player][card])
   hand_full_know[player] = []
   for card in range(len(hand_play[player])):
      hand_full_know[player].append(hand_play_know[player][card])
   for card in range(len(hand_keep[player])):
      hand_full_know[player].append(hand_keep_know[player][card])
   for card in range(len(hand_throw[player])):
      hand_full_know[player].append(hand_throw_know[player][card])



def check_hand_number(player,card_number_to_check,hand):
   positions = []
   build_hand_full(player)
   for card in range(len(hand[player])):
      if hand[player][card][card_number] == card_number_to_check:
         positions.append(card)
   return(positions)


def check_card_can_be_played(card_to_check):
   card_playable = False
   if table[card_to_check[card_colour] - 1] + 1 == card_to_check[card_number]:
      card_playable = True
   return card_playable


def check_clue_possible(player,play_position):
   # clue_possible[0] = possible: is the clue possible 1 == True
   # clue_possible[1] = value: what value was the clue
   # clue_possible[2] = type: was the clue number or colour 
   clue_possible = [0,0,-1]
   build_hand_full(player)
   for card in range(len(hand_full[player])):
      if hand_full[player][card][card_number] == play_position + 1:
         clue_possible = [1,hand_full[player][card][card_number],card_number]
      if hand_full[player][card][card_colour] == play_position + 1:
         clue_possible = [1,hand_full[player][card][card_colour],card_colour]
   return clue_possible


def knowledge_clue(player,clue_value,clue_type):
   for card in range(len(hand_keep[player])):
      if clue_type == card_number:
         for card in range(len(hand_keep[player])):
            if hand_keep[player][card][card_number] == clue_value:
               hand_keep_know[player][card][card_number][clue_value - 1] = 1
            else:
               hand_keep_know[player][card][card_number][clue_value - 1] = -1
      if clue_type == card_colour:
         for card in range(len(hand_keep[player])):
            if hand_keep[player][card][card_colour] == clue_value:
               hand_keep_know[player][card][card_colour][clue_value - 1] = 1
            else:
               hand_keep_know[player][card][card_colour][clue_value - 1] = -1
   for card in range(len(hand_play[player])):
      if clue_type == card_number:
         for card in range(len(hand_play[player])):
            if hand_play[player][card][card_number] == clue_value:
               hand_play_know[player][card][card_number][clue_value - 1] = 1
            else:
               hand_play_know[player][card][card_number][clue_value - 1] = -1
      if clue_type == card_colour:
         for card in range(len(hand_play[player])):
            if hand_play[player][card][card_colour] == clue_value:
               hand_play_know[player][card][card_colour][clue_value - 1] = 1
            else:
               hand_play_know[player][card][card_colour][clue_value - 1] = -1


def build_deck_plus_hand():
   deck_deduce = [[1,1],[1,1],[1,1],[2,1],[2,1],[3,1],[3,1],[4,1],[4,1],[5,1],[1,2],[1,2],[1,2],[2,2],[2,2],[3,2],[3,2],[4,2],[4,2],[5,2],[1,3],[1,3],[1,3],[2,3],[2,3],[3,3],[3,3],[4,3],[4,3],[5,3],[1,4],[1,4],[1,4],[2,4],[2,4],[3,4],[3,4],[4,4],[4,4],[5,4],[1,5],[1,5],[1,5],[2,5],[2,5],[3,5],[3,5],[4,5],[4,5],[5,5]]
   # remove discard pile from deck
   for card in range(len(discard_pile)):
      if discard_pile[card] in deck_deduce:
         del deck_deduce[deck_deduce.index(discard_pile[card])]
   # remove played pile from deck
   for card in range(len(played_pile)):
      if played_pile[card] in deck_deduce:
         del deck_deduce[deck_deduce.index(played_pile[card])]
   # remove other hand
   build_hand_full(other_player)
   for card in range(len(hand_full[other_player])):
      if hand_full[other_player][card] in deck_deduce:
         del deck_deduce[deck_deduce.index(hand_full[other_player][card])]
   return deck_deduce


def deduce_card(position):
   card_possibilities = build_deck_plus_hand()
   card_possibilities_cards = []
   card_possibilities_playable = []
   card_possibilities_dontdiscard = []
   build_hand_full(current_player)
   for card in range(len(card_possibilities)):
      # skip cards that don't agree with positive information (number)
      # is the number of the hand card known
      if 1 in hand_full_know[current_player][position][card_number]:
         # is the possible card a number other than the known number
         if hand_full_know[current_player][position][card_number][card_possibilities[card][card_number]-1] != 1:
            continue
      # skip cards that disagree with negative information
      if hand_full_know[current_player][position][card_number][card_possibilities[card][card_number]-1] == -1:
         continue
      # skip cards that don't agree with positive information (colour)
      # is the number of the hand card known
      if 1 in hand_full_know[current_player][position][card_colour]:
         # is the possible card a number other than the known number
         if hand_full_know[current_player][position][card_colour][card_possibilities[card][card_colour]-1] != 1:
            continue
      # skip cards that disagree with negative information
      if hand_full_know[current_player][position][card_colour][card_possibilities[card][card_colour]-1] == -1:
         continue
      # else let card remain
      card_possibilities_cards.append(card_possibilities[card])
      # can this card be played?
      if check_card_can_be_played(card_possibilities[card]):
         card_possibilities_playable.append(1)
      else:
         card_possibilities_playable.append(0)
      # is this the last version of this card?
      if card_possibilities.count(card_possibilities[card]):
         card_possibilities_dontdiscard.append(1)
      else:
         card_possibilities_dontdiscard.append(0)
   return [card_possibilities_cards,card_possibilities_playable,card_possibilities_dontdiscard]



def determine_hand_location(player,card):
   # return[0]: 1 = keep hand; 2 = play hand; 3 = throw hand
   # return[1]: position in sub hand, where position 1 = 0
   position = [0,0]
   if card in hand_keep[player]:
      for card in range(len(hand_keep[player])):
         if hand_keep[player][card] == card:
            position = [1,card]
   else:
      if card in hand_play[player]:
         for card in range(len(hand_play[player])):
            if hand_play[player][card] == card:
               position = [2,card]
      else:
         if card in hand_throw[player]:
            for card in range(len(hand_throw[player])):
               if hand_throw[player][card] == card:
                  position = [3,card]
   return position

def log_table():
   global log
   log += '\n'+'TURN: ' + str(turn_counter) + '   DECK: ' + str(len(deck)) + '   CLUES: ' + str(clues_remaining)
   log += '\n'+str(table)
   log += '\n'+str(discard_pile)
   log += '\n'+str(hand_keep[0])+"     "+str(hand_play[0])+"  "+turn_star_0
   log += '\n'+str(hand_keep_know[0])+"     "+str(hand_play_know[0])+"  "+turn_star_0
   log += '\n'+str(hand_keep[1])+"     "+str(hand_play[1])+"  "+turn_star_1
   log += '\n'+str(hand_keep_know[1])+"     "+str(hand_play_know[1])+"  "+turn_star_1

def check_game_over():
   global end_game
   global game_over
   if len(deck) == 0:
      end_game += 1
      # when deck is 0, allow 2 more turns before finishing the game
      if end_game == 2:
         game_over = True
   return game_over



###############
### Actions
###############



def clue_blue_dont_discard():
   global clues_remaining
   global log
   turn_finished = False
   # are there cards in the play hand
   if len(hand_play[other_player]) > 0:
      # is there a clue token available
      if clues_remaining > 0:
         # if other's first card is in the discard pile
         if hand_play[other_player][0] in discard_pile:
            # don't apply rule to 1s
            if hand_play[other_player][0][card_number] > card_number_1:
               # make sure blue card available
               # build full hand of other player
               build_hand_full(other_player)
               # check blue card available
               for card in range(len(hand_full[other_player])):
                  if hand_full[other_player][card][card_colour] == card_colour_blue:
                     # move first card to keep hand   
                     hand_keep[other_player].append(hand_play[other_player][0])
                     hand_keep_know[other_player].append(hand_play_know[other_player][0])
                     # remove first card from play hand
                     del(hand_play[other_player][0])
                     del(hand_play_know[other_player][0])
                     # update clue knowledge
                     knowledge_clue(other_player,card_colour_blue,card_colour)
                     # finish turn
                     turn_finished = True
                     # log
                     l = 'clue_blue_dont_discard'
                     log += '\n'+l
                     break
   return(turn_finished)


def clue_five_dont_discard():
   global clues_remaining
   global log
   turn_finished = False
   # are there cards in the play hand
   if len(hand_play[other_player]) > 0:
      # is there a clue token available
      if clues_remaining > 0:
         # if other's first card is 5
         if hand_play[other_player][0][card_number] == card_number_5:
            # move to keep hand
            hand_keep[other_player].append(hand_play[other_player][0])
            hand_keep_know[other_player].append(hand_play_know[other_player][0])
            # delete from play hand
            del hand_play[other_player][0]
            del hand_play_know[other_player][0]
            # update clue knowledge
            knowledge_clue(other_player,card_number_5,card_number)
            #check play hand for more fives (once)
            position_of_fives = check_hand_number(other_player,card_number_5,hand_play)
            # check if fives exist
            if len(position_of_fives) > 0:
               # move to keep hand
               hand_keep[other_player].append(hand_play[other_player][position_of_fives[0]])
               hand_keep_know[other_player].append(hand_play_know[other_player][position_of_fives[0]])
               # delete from play hand
               del hand_play[other_player][position_of_fives[0]]
               del hand_play_know[other_player][position_of_fives[0]]
            #check play hand for more fives (twice)
            position_of_fives = check_hand_number(other_player,card_number_5,hand_play)
            # check if fives exist
            if len(position_of_fives) > 0:
               # move to keep hand
               hand_keep[other_player].append(hand_play[other_player][position_of_fives[0]])
               hand_keep_know[other_player].append(hand_play_know[other_player][position_of_fives[0]])
               # delete from play hand
               del hand_play[other_player][position_of_fives[0]]
               del hand_play_know[other_player][position_of_fives[0]]
            # finish turn
            turn_finished = True
            # remove one clue
            clues_remaining -= 1
            # log
            l = 'clue_five_dont_discard'
            log += '\n'+l
   return(turn_finished)


def clue_positive_keep_hand():
   global clues_remaining
   global log
   turn_finished = False
   # is there a clue token available
   if clues_remaining > 0:
      # cycle through each card in hand
      for card in range(len(hand_keep[other_player])):
         # can card be played
         if check_card_can_be_played(hand_keep[other_player][card]):
            # is the number or colour greater than the number of cards in the play hand
            if hand_keep[other_player][card][card_number] > len(hand_play[other_player]): 
               # update clue given
               clue_available_keep[other_player][card] = 1
               # update knowledge based off clue
               knowledge_clue(other_player,hand_keep[other_player][card][card_number],card_number)
               # remove one clue
               clues_remaining -= 1
               # finish turn
               turn_finished = True
               # log
               #print('clue_positive_keep_hand (number)')
               break
            if hand_keep[other_player][card][card_colour] > len(hand_play[other_player]):
               # update clue given
               clue_available_keep[other_player][card] = 1
               # update knowledge based off clue
               knowledge_clue(other_player,hand_keep[other_player][card][card_colour],card_colour)
               # remove one clue
               clues_remaining -= 1
               # finish turn
               turn_finished = True
               # log
               l = 'clue_positive_keep_hand (colour)'
               log += '\n'+l
               break               
   return(turn_finished)


def clue_positive_play_hand():
   global clues_remaining
   global log
   turn_finished = False
   # is there a clue token available
   if clues_remaining > 0:
      # cycle through each card in hand
      for card in range(len(hand_play[other_player])):
         # card not in fifth position
         if card < 5:
            # can card be played
            if check_card_can_be_played(hand_play[other_player][card]):
               # is the required number/colour available to clue
               clue_check = check_clue_possible(other_player,card)
               if clue_check[0] == 1:
                  # update clue given
                  clue_available_play[other_player][card] = 1
                  # update knowledge based off clue
                  knowledge_clue(other_player,clue_check[1],clue_check[2])
                  # remove one clue
                  clues_remaining -= 1
                  # finish turn
                  turn_finished = True
                  # log
                  l = 'clue_positive_play_hand'+' clue_value: '+str(clue_check[1])+' clue_type: '+str(clue_check[2])
                  log += '\n'+l
                  break
   return(turn_finished)


def play_deduced_card():
   global clues_remaining
   global log
   turn_finished = False
   build_hand_full(current_player)
   deduction = []
   for card in range(len(hand_full[current_player])):
      deduction.append(deduce_card(card))
   # try to play any card that all possibilities are playable
   if turn_finished == False:
      for card in range(len(hand_full[current_player])):
         if sum(deduction[card][1]) == len(deduction[card][1]):
            # increase relevent table by 1
            table[hand_full[current_player][card][card_colour] - 1] += 1
            # was card a five
            if hand_full[current_player][card][card_number] == card_number_5:
               # gain one clue
               clues_remaining += 1
            # determine which hand and position of card to be discarded
            location = determine_hand_location(current_player,card)
            # remove played card from hand
            if location[0] == 1:
               # located in keep hand
               del hand_keep[current_player][location[1]]
               del hand_keep_know[current_player][location[1]]
            if location[0] == 2:
               # located in play hand
               del hand_play[current_player][location[1]]
               del hand_play_know[current_player][location[1]]
            if location[0] == 3:
               # located in throw hand
               del hand_throw[current_player][location[1]]
               del hand_throw_know[current_player][location[1]]
            # if cards remaining in deck
            if len(deck) > 0:
               # add card on top of deck to hand
               hand_play[current_player].append(deck[0]) 
               hand_play_know[current_player].append([[0,0,0,0,0],[0,0,0,0,0]])
               # remove that card from the deck
               del deck[0]   
            # finish turn
            turn_finished = True
            # log
            l = 'play_deduced_card: '+str(deduction[card][0])
            log += '\n'+l
            break
   return(turn_finished)



def play_clued_card_keep_hand():
   global clues_remaining
   global log
   turn_finished = False
   if sum(clue_available_keep[current_player]) > 0:
      # increase relevent table by 1
      table[hand_keep[current_player][clue_available_keep[current_player].index(1)][card_colour] - 1] += 1
      # was card a five
      if hand_keep[current_player][clue_available_keep[current_player].index(1)][card_number] == card_number_5:
         # gain one clue
         clues_remaining += 1
      # move card to played pile
      played_pile.append(hand_keep[current_player][clue_available_keep[current_player].index(1)])
      # remove played card from hand
      del hand_keep[current_player][clue_available_keep[current_player].index(1)]
      del hand_keep_know[current_player][clue_available_keep[current_player].index(1)]      
      # if cards remaining in deck
      if len(deck) > 0:
         # add card on top of deck to hand
         hand_play[current_player].append(deck[0]) 
         hand_play_know[current_player].append([[0,0,0,0,0],[0,0,0,0,0]])
         # remove that card from the deck
         del deck[0] 
      # clear clues
      clue_available_keep[current_player] = [0,0,0,0,0]     
      # finish turn
      turn_finished = True
      # log
      l = 'play_clued_card_keep_hand'
      log += '\n'+l
   return(turn_finished)


def play_clued_card_play_hand():
   global clues_remaining
   global log
   turn_finished = False
   if sum(clue_available_play[current_player]) > 0:
      # increase relevent table by 1
      table[hand_play[current_player][clue_available_play[current_player].index(1)][card_colour] - 1] += 1
      # move card to played pile
      played_pile.append(hand_play[current_player][clue_available_play[current_player].index(1)])
      # was card a five
      if hand_play[current_player][clue_available_play[current_player].index(1)][card_number] == card_number_5:
         # gain one clue
         clues_remaining += 1
      # remove played card from hand
      del hand_play[current_player][clue_available_play[current_player].index(1)]
      del hand_play_know[current_player][clue_available_play[current_player].index(1)] 
      # if cards remaining in deck
      if len(deck) > 0:
         # add card on top of deck to hand
         hand_play[current_player].append(deck[0])
         hand_play_know[current_player].append([[0,0,0,0,0],[0,0,0,0,0]]) 
         # remove that card from the deck
         del deck[0] 
      # clear clues
      clue_available_play[current_player] = [0,0,0,0,0]
      # finish turn
      turn_finished = True
      # log
      l = 'play_clued_card_play_hand'
      log += '\n'+l
   return(turn_finished)

def discard_play_hand():
   global clues_remaining
   global log
   turn_finished = False
   # make sure at least one card available in play hand
   if len(hand_play[current_player]) > 0:
      # move card to discard pile
      discard_pile.append(hand_play[current_player][0])
      # remove first card from play hand
      del hand_play[current_player][0]
      del hand_play_know[current_player][0]
      # if cards remaining in deck
      if len(deck) > 0:
         # add card on top of deck to play hand
         hand_play[current_player].append(deck[0])
         hand_play_know[current_player].append([[0,0,0,0,0],[0,0,0,0,0]]) 
         # remove that card from the deck
         del deck[0] 
      # gain one clue
      clues_remaining += 1
      # finish turn
      turn_finished = True
      # log
      l = 'discard_play_hand'
      log += '\n'+l
   return(turn_finished)


def discard_keep_hand():
   global clues_remaining
   global log
   turn_finished = False
   # make sure at least one card available in keep hand
   if len(hand_keep[current_player]) > 0:
      # move card to discard pile
      discard_pile.append(hand_keep[current_player][0])
      # remove first card from play hand
      del hand_keep[current_player][0]
      del hand_keep_know[current_player][0]
      # if cards remaining in deck
      if len(deck) > 0:
         # add card on top of deck to play hand
         hand_play[current_player].append(deck[0])
         hand_play_know[current_player].append([[0,0,0,0,0],[0,0,0,0,0]]) 
         # remove that card from the deck
         del deck[0] 
      # gain one clue
      clues_remaining += 1
      # finish turn
      turn_finished = True
      # log
      l = 'discard_keep_hand'
      log += '\n'+l
   return(turn_finished)

###############
### Play hanabi
###############

def play_hanabi():
   global current_player
   global other_player
   global turn_star_0
   global turn_star_1
   global turn_counter
   global turn
   global log
   # set up table
   set_up_table()
   # loop through turns
   while check_game_over() == False:
      turn_counter += 1
      # reset turn finished flag to False
      turn_finished = False 
      # define current/other player
      if turn == 0:
         current_player = 0
         other_player = 1
         turn_star_0 = "*"
         turn_star_1 = " "
      else:
         current_player = 1
         other_player = 0
         turn_star_0 = " "
         turn_star_1 = "*"
      # log
      log_table()
      # start progression of actions
      if clue_blue_dont_discard() == False:
         if clue_five_dont_discard() == False:
               if play_clued_card_keep_hand() == False:
                  if play_clued_card_play_hand() == False:
                     if play_deduced_card() == False:
                        if clue_positive_keep_hand() == False:
                           if clue_positive_play_hand() == False:
                              if discard_play_hand() == False:
                                 discard_keep_hand()
      # no keep hand
      # if play_clued_card_play_hand() == False:
         # if clue_positive_play_hand() == False:
            # discard_play_hand()
      # Turn finished, swap roles
      if turn == 0:
         turn = 1
      else:
         turn = 0
   # Game finished
   # define current/other player
   if turn == 0:
      current_player = 0
      other_player = 1
      turn_star_0 = "*"
      turn_star_1 = " "
   else:
      current_player = 1
      other_player = 0
      turn_star_0 = " "
      turn_star_1 = "*"
   # log
   log_table()
   # write score
   with open(os.path.expanduser(out_file),'a') as txtfile_out:
      txtfile_out.write(str(sum(table))+'\n')


# -----------------------------------------------
# Parameters
# -----------------------------------------------

###############
### Input Output
###############

out_file = '~/Git/hanabi/output.txt'
log_file = '~/Git/hanabi/log.txt'

###############
### Build table
###############

turn = 0

clues_remaining = 8

turn_counter = 0

game_over = False

end_game = 0

clue_available_play = [[0,0,0,0,0],[0,0,0,0,0]]

clue_available_keep = [[0,0,0,0,0],[0,0,0,0,0]]

lightning_reminaing = 3

# Card = [Number,Colour]
deck = [[1,1],[1,1],[1,1],[2,1],[2,1],[3,1],[3,1],[4,1],[4,1],[5,1],[1,2],[1,2],[1,2],[2,2],[2,2],[3,2],[3,2],[4,2],[4,2],[5,2],[1,3],[1,3],[1,3],[2,3],[2,3],[3,3],[3,3],[4,3],[4,3],[5,3],[1,4],[1,4],[1,4],[2,4],[2,4],[3,4],[3,4],[4,4],[4,4],[5,4],[1,5],[1,5],[1,5],[2,5],[2,5],[3,5],[3,5],[4,5],[4,5],[5,5]]

# [G,W,R,Y,B]
table = [0,0,0,0,0]

card_number = 0

card_colour = 1

card_number_1 = 1
card_number_2 = 2
card_number_3 = 3
card_number_4 = 4
card_number_5 = 5

card_colour_green = 1
card_colour_white = 2
card_colour_red = 3
card_colour_yellow = 4
card_colour_blue = 5

log = ''

discard_pile = []

played_pile = []

###############
### Build Hands
###############

hand_play = [[],[]]

hand_play_know = [[],[]]

hand_keep = [[],[]]

hand_keep_know = [[],[]]

hand_throw = [[],[]]

hand_throw_know = [[],[]]

hand_full = [[],[]]

hand_full_know = [[],[]]


# -----------------------------------------------
# Import
# -----------------------------------------------


# -----------------------------------------------
# Body
# -----------------------------------------------

try:
   play_hanabi()
   print(log)
except Exception as e:
   # print log to console
   print(log)
   print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
   print(e)
   # write log to file
   with open(os.path.expanduser(log_file),'a') as txtfile_out:
      txtfile_out.write(log)
      txtfile_out.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
      txtfile_out.write(e)


# -----------------------------------------------
# Export
# -----------------------------------------------



