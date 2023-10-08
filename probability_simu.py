import random as rd
import statistics
#aaaaaaa
#aaaafffff
#####
#遊び方
# card_A と card_B に検証したい枚数を入れる。
# draw_numは上から引く枚数を入れる
# trials_numは試行回数
class Probability():
    def __init__(self):
        self.card_A=6
        self.card_B=9
        self.deck_num=40
        self.draw_num=7
        self.first_hands=4
        self.trials_num=100
        self.deck=[0]*(self.deck_num-self.card_A-self.card_B)
        self.count_card_A=0
        self.count_card_B=0
        self.count_card_AB=0
        self.count_mulligan=0
        self.result_A=[]
        self.result_B=[]
        self.result_AB=[]

        self.deck_set()
        
    def deck_set(self):
        for i in range(self.card_A):
            self.deck.append(1)
        for i in range(self.card_B):
            self.deck.append(2)

    def check_probability(self):
        flag_A=False
        flag_B=False
        flag_AB=False
        self.count_card_A=0
        self.count_card_B=0
        self.count_card_AB=0
        for i in range(self.trials_num):
            rd.shuffle(self.deck)
            for j in range(self.draw_num):
                if flag_A==False:
                    if self.deck[j]==1:
                        self.count_card_A+=1
                        flag_A=True
                if flag_B==False:
                    if self.deck[j]==2 :
                        self.count_card_B+=1
                        flag_B=True
                if flag_AB==False:
                    if flag_A==True and flag_B==True:
                        self.count_card_AB+=1
                        flag_AB=True
            flag_A=False
            flag_B=False
            flag_AB=False
        self.result_A.append(self.count_card_A)
        self.result_B.append(self.count_card_B)
        self.result_AB.append(self.count_card_AB)
    
    def mulligan_True_check(self):
        flag_A=False
        flag_B=False
        flag_AB=False
        flag_mulligan=False
        self.count_card_A=0
        self.count_card_B=0
        self.count_card_AB=0
        self.count_mulligan=0
        for i in range(self.trials_num):
            rd.shuffle(self.deck)
            for j in range(self.draw_num):
                if j==3 and flag_A ==False and flag_B ==False :
                    self.count_mulligan+=1
                    if flag_A:
                        self.count_card_A-=1
                    if flag_B:
                        self.count_card_B-=1
                    flag_mulligan=True
                    break
                if flag_A==False:
                    if self.deck[j]==1:
                        self.count_card_A+=1
                        flag_A=True
                if flag_B==False:
                    if self.deck[j]==2 :
                        self.count_card_B+=1
                        flag_B=True
                if flag_AB==False:
                    if flag_A==True and flag_B==True:
                        self.count_card_AB+=1
                        flag_AB=True
            if flag_mulligan:
                self.mulligan()
                flag_mulligan=False
            flag_A=False
            flag_B=False
            flag_AB=False
        self.result_A.append(self.count_card_A)
        self.result_B.append(self.count_card_B)
        self.result_AB.append(self.count_card_AB)
    def mulligan(self):
        flag_A=False
        flag_B=False
        flag_AB=False
        for j in range(self.first_hands-1,self.draw_num+self.first_hands-1):
                if flag_A==False:
                    if self.deck[j]==1:
                        self.count_card_A+=1
                        flag_A=True
                if flag_B==False:
                    if self.deck[j]==2 :
                        self.count_card_B+=1
                        flag_B=True
                if flag_AB==False:
                    if flag_A==True and flag_B==True:
                        self.count_card_AB+=1
                        flag_AB=True
    def show_result(self):
        self.check_probability()
        print(str(self.trials_num)+"回試行")
        print("Aが"+str(self.draw_num)+"枚目までに出た回数 -> "+str(self.count_card_A))
        print("Bが"+str(self.draw_num)+"枚目までに出た回数 -> "+str(self.count_card_B))
        print("AとBが"+str(self.draw_num)+"枚目までに出た回数 -> "+str(self.count_card_AB))
        print("")
    
    def print_result(self):
        print("Aが出た回数")
        print(self.result_A)
        print("Bが出た回数")
        print(self.result_B)
        print("AとBが出た回数")
        print(self.result_AB)
    
    def get_average(self):
        mean_A=statistics.mean(self.result_A)
        mean_B=statistics.mean(self.result_B)
        mean_AB=statistics.mean(self.result_AB)
        print("Aの平均: "+str(mean_A*100 / self.trials_num)+" %")
        print("Bの平均: "+str(mean_B*100 / self.trials_num)+" %")
        print("ABの平均: "+str(mean_AB*100 / self.trials_num)+" %")

check=Probability()
trial_check=5 #ここは上の試行を何回試行したいかを入れる。
print(str(check.trials_num)+" 回試行を"+str(trial_check)+" 回繰り返した時の")
for i in range(trial_check):
    check.check_probability()
check.get_average()
for i in range(trial_check):
    check.mulligan_True_check()
    print("マリガンの回数: "+str(check.count_mulligan))
check.get_average()
#for i in range(1,16):
#    check.draw_num=i
#    check.show_result()