############################################################################
# ABSTRACT BASE CLASS FOR PDBOTS
# A PDBot has two methods:
# get_play is called to get the bots next play and display
# make_play is called to tell th bot what the opponent played and displayed 
###########################################################################
from abc import ABCMeta, abstractmethod
from random import random

expected_rounds = 5*30.0  #On an average, against an opponent, we play 150 rounds

class PDBot:
    __metaclass__=ABCMeta

    #this is not necessary, but can be used for additional initialization
    @abstractmethod
    def init(self):
        pass

    #must return the bot's next play (one of "give 2" or "take 1") and
    #your bot's emotional display (an EPA vector as a list)
    @abstractmethod
    def get_play(self):
        pass

    #opponent_play is the opponent's last play ("give 2" or "take 1")
    #opponent_emot is the opponents displayed emotion
    @abstractmethod
    def make_play(self, opponent_play, opponent_emot):
        pass


class SpyChameleonBot(PDBot):
    
    #set up counters
    def __init__(self):
            self.rounds_played = 0
            
            self.other_forgive_count = 0
            self.other_cheat_count = 0
            
            self.other_forgive_ratio = 0.0
            self.other_cheat_ratio = 0.0
            
            self.my_forgive_ratio = 0.0
            self.my_cheat_ratio = 0.0
            
            self.other_last_play="give 2"
            self.other_last_emot="happy"
            self.my_last_play="give 2"
            
    
    #this is not necessary, but can be used for additional initialization
    def init(self):
        pass
    
    
    def observe_opponent_strategy(self):
        if self.other_last_play != self.my_last_play:
            if self.other_last_play == "take 1":
                self.other_cheat_count+=1
            else: 
                self.other_forgive_count+=1
                   
    def play_tit_for_tat(self):
        self.observe_opponent_strategy()
        if self.other_last_play == "give 2":
            my_emo = "happy"
        else:
            my_emo = "disappointed"
            
        return (self.other_last_play, my_emo)
    
    def set_strategic_ratios(self):
        self.other_cheat_ratio = self.other_cheat_count/float(self.rounds_played)
        self.other_forgive_ratio = self.other_forgive_count/float(self.rounds_played)
        
        self.my_cheat_ratio = min(self.other_cheat_ratio + self.other_forgive_ratio, 1.0)
        self.my_forgive_ratio = self.other_forgive_ratio
        
        
        
    def adapt_opponent_strategy(self):
        self.observe_opponent_strategy()
        self.set_strategic_ratios()
        if self.other_last_play == "take 1":
            if random() < self.my_forgive_ratio:
                my_play = "give 2"
                my_emo = "cautious"
                
            else:
                my_play = "take 1"
                my_emo = "disappointed"
        else:
            if random() < self.my_cheat_ratio:
                my_play = "take 1"
                my_emo = "guilty"
            else:
                my_play = "give 2"
                my_emo = "happy"
                
        return (my_play,my_emo)
        

    #must return the bot's next play (one of "give 2" or "take 1") and
    #your bot's emotional display (an EPA vector as a list)
    def get_play(self):
        self.rounds_played+=1
        if self.rounds_played <= expected_rounds/2:
            (play,emo) = self.play_tit_for_tat()
        else:
            (play,emo) = self.adapt_opponent_strategy()
            
        self.my_last_play = self.other_last_play
        
        return (play,emo)

    #opponent_play is the opponent's last play ("give 2" or "take 1")
    #opponent_emot is the opponents displayed emotion
    def make_play(self, opponent_play, opponent_emot):
        self.other_last_play = opponent_play
        self.other_last_emot = opponent_emot



