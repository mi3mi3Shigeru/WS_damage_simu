import random as rd
import statistics
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from turtle import color
from collections import Counter
import matplotlib.pyplot as plt

FRAME_SIZE =220

class WS_damage_sim:
    def __init__(self):
        self.deck_list=[]
        self.CONST_CARD_CX=1
        self.CONST_CARD_OTHER=0
        self.num_CX=8
        self.num_TOTAL=50
        self.deck_num=50
        self.attack_type=("バーン","みちる","たきな","モカ","ショット","トップ盛り","逆圧縮","山下モカ")
        self.attack_value=[]
        self.attack_situ=[]
        self.damage_count=0
        self.total_damage=[]
        self.log_damage=[]
        self.refresh_damage=0
        self.log_refresh_damage=[]
        self.count=0
        self.deck_index=0
        self.is_canceled=False
        
    def deck_set(self):
        self.deck_list=[]
        for i in range(self.num_CX):
            self.deck_list.append(self.CONST_CARD_CX)
        for i in range(self.num_TOTAL-self.num_CX):
            self.deck_list.append(self.CONST_CARD_OTHER)
        self.deck_index=0

        
    def deck_shuffle(self):
        rd.shuffle(self.deck_list)
    
    def check_refresh(self):
        if self.deck_num <= self.deck_index:
            # print("refresh")
            self.deck_shuffle()
            self.deck_index=0
            self.refresh_damage+=1
            self.deck_num=len(self.deck_list)

        else :
            return
        
    def attack_burn(self,num):
        self.damage_count=0
        self.is_canceled=False
        for i in range(num):
            if self.deck_list[self.deck_index]!=self.CONST_CARD_CX:
                self.damage_count +=1
                self.deck_index +=1
                self.check_refresh()
            else :
                self.damage_count=0
                self.deck_index +=1
                self.check_refresh()
                self.is_canceled=True
                break
    
        self.total_damage.append(self.damage_count)
        
    def attack_michiru(self,num):
        self.burn_count=0
        for i in range(num):
            if self.deck_list[self.deck_num-1]==self.CONST_CARD_CX:
                self.burn_count+=1
            self.deck_num-=1
            self.check_refresh()
        self.attack_burn(self.burn_count)
        
    def attack_takina(self,num):
        self.burn_count=0
        if self.deck_list[self.deck_index]==self.CONST_CARD_OTHER:
            rand=rd.randrange(2)
            if rand==0:
                self.burn_count+=1
                self.check_refresh()
        else:
            self.burn_count+=1
            self.check_refresh()
            
        self.deck_index+=1
        self.attack_burn(self.burn_count)
        
    def attack_moka(self,num):
        num=2
        if self.deck_list[(self.deck_index)+1]==self.CONST_CARD_CX:
            self.deck_list[self.deck_index], self.deck_list[(self.deck_index)+1] = self.deck_list[(self.deck_index)+1],self.deck_list[self.deck_index]
        for i in range(num):
            if self.deck_list[(self.deck_index)]==self.CONST_CARD_CX:
                self.deck_index+=1    
                self.check_refresh()
    
    def attack_shot(self,num,shot_count):
        if self.is_canceled:
            for i in range(shot_count):
                self.attack_burn(num)
            
    def attack_topmori(self,num):
        for i in range(num):
            self.deck_list.insert(self.deck_index,self.CONST_CARD_OTHER)
            self.deck_num+=1
    
    def attack_gyakuassyuku(self,num):
        # print(self.deck_list)
        self.attack_topmori(num)
        # シャッフルしたい範囲を指定
        start_index = self.deck_index
        end_index = self.deck_num  # この範囲までの要素をシャッフル
        # 指定した範囲の要素をランダムにシャッフル
        sublist = self.deck_list[start_index:end_index]
        rd.shuffle(sublist)
        # シャッフルしたサブリストを元のリストに戻す
        self.deck_list[start_index:end_index] = sublist
        # print(self.deck_list)
    def attack_yamashitamoka(self,num):
        for i in range(num):
            if self.deck_list[self.deck_num-1]==self.CONST_CARD_CX:
                break
            else : 
                self.deck_num-=1
                self.check_refresh()

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack()
        self.master.geometry(str(FRAME_SIZE*4)+"x"+str(FRAME_SIZE*3))
        self.master.title("WS_damage_simulator")
        self.deck=WS_damage_sim()
        self.sum_result=0
        self.clear=0
        self.clear_count=0
        self.create_frame()
        self.create_status_input()
        self.create_status_execution()
        self.deck.deck_set()
        
    def label_update(self):
        self.status_deck="山の枚数: "+str(self.value_CX.get())+" / "+str(self.value_TOTAL.get())
        self.status_attack="攻撃の状況 : \n"+str(self.deck.attack_situ)+"\n"+str(self.deck.attack_value)
        self.status_label_deck["text"]=self.status_deck
        self.status_label_attack["text"]=self.status_attack
        self.status_label_deck.update()
        self.status_label_attack.update()
        
    def value_update(self):
        self.deck.num_CX=int(self.value_CX.get())
        self.deck.num_TOTAL=int(self.value_TOTAL.get())
        self.deck.deck_set()
        self.deck.deck_shuffle()
        self.label_update()
        self.label_deck["text"]="山の配置:",self.deck.deck_list
        
    def attack_add(self):
        self.deck.attack_situ.append(self.combobox_attack_situ.get())
        self.deck.attack_value.append(int(self.value_attack_num.get()))
        self.label_update()

    def exe_sim(self):
        count=0
        self.deck.total_damage=[]
        self.deck.refresh_damage=0
        self.value_update()
        self.deck.deck_num=self.deck.num_TOTAL
        self.deck.is_canceled=False
        while count< len(self.deck.attack_situ):
            if self.deck.attack_situ[count] == self.deck.attack_type[0]:
                self.deck.attack_burn(self.deck.attack_value[count])
            elif self.deck.attack_situ[count] == self.deck.attack_type[1]:
                self.deck.attack_michiru(self.deck.attack_value[count])
            elif self.deck.attack_situ[count] == self.deck.attack_type[2]:
                self.deck.attack_takina(self.deck.attack_value[count])
            elif self.deck.attack_situ[count] == self.deck.attack_type[3]:
                self.deck.attack_moka(self.deck.attack_value[count])
            elif self.deck.attack_situ[count] == self.deck.attack_type[4]:
                shot_count=1
                #ショットを数回付与することを想定
                while count+shot_count < len(self.deck.attack_situ):
                    if self.deck.attack_situ[count+shot_count] == self.deck.attack_type[4]:
                        shot_count+=1
                    else :
                        break
                self.deck.attack_shot(self.deck.attack_value[count],shot_count)
                count+=shot_count-1
            elif self.deck.attack_situ[count] == self.deck.attack_type[5]:
                self.deck.attack_topmori(self.deck.attack_value[count])
            elif self.deck.attack_situ[count] == self.deck.attack_type[6]:
                self.deck.attack_gyakuassyuku(self.deck.attack_value[count])
            elif self.deck.attack_situ[count] == self.deck.attack_type[7]:
                self.deck.attack_yamashitamoka(self.deck.attack_value[count])
                
            else:
                continue
            count+=1
        self.label_result["text"]="与えたダメージ："+str(self.deck.total_damage)+"\nリフレッシュダメージ: "+str(self.deck.refresh_damage)+"\n 総ダメージ: "+ str(sum(self.deck.total_damage))
        self.deck.log_damage.append(sum(self.deck.total_damage))
        self.deck.log_refresh_damage.append(self.deck.refresh_damage)
        
        
    def reset(self):
        self.deck.attack_value=[]
        self.deck.attack_situ=[]
        self.value_update()
        
    def exe_trial(self):
        trial_num=1000
        self.sum_result=0
        self.deck.log_damage=[]
        self.deck.log_refresh_damage=[]
        situ=str(self.deck.num_CX)+" / "+str(self.deck.num_TOTAL)
        for i in range(trial_num):
            self.exe_sim()
        self.sum_result = sum(self.deck.log_damage)
        counter = Counter(self.deck.log_damage)
        mode = counter.most_common(1)
        most_common=mode[0][0]
        print("詰めの概要 : "+str(self.entry.get()))
        print("山 : "+situ)
        print(self.deck.attack_situ)
        print(self.deck.attack_value)
        print(str(trial_num)+"回の平均ダメージ : "+str(self.sum_result/trial_num))
        print(str(trial_num)+"回の最頻ダメージ : "+str(most_common))
        print("リフレッシュダメージの平均 : "+str(sum(self.deck.log_refresh_damage)/trial_num))
        for i in range(max(self.deck.log_damage)+1):
            print(str(i)+"点 : " +str(counter[i]))
        
        # グラフ描画のためにデータを抽出
        x_labels = list(counter.keys())
        y_values = list(counter.values())

        # グラフの描画
        plt.bar(x_labels, y_values)
        plt.xlabel("damage")
        plt.xticks(range(min(x_labels), max(x_labels) + 1, 1))
        plt.ylabel("count")
        plt.yticks(range(0, (trial_num//10)*6+1, (trial_num//20) ))
        
        max_x = max(plt.gca().get_xlim())
        max_y = max(plt.gca().get_ylim())
        
        # テキストを右上に配置
        plt.text(max_x, max_y-50,str(trial_num)+"回試行\n" +"山: "+situ+" ",ha='right', va='top',fontname="Meiryo")
        random_color = "#{:02x}{:02x}{:02x}".format(rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))
        plt.axvline(x=(self.sum_result/trial_num), color=random_color, linestyle='--', label=f'Average ({(self.sum_result/trial_num):.2f}) '+situ)
        
        plt.title(self.entry.get() ,fontname="Meiryo")
        plt.legend()
        plt.show()

    
    def create_frame(self):
        #
        self.frame_menu=tk.Frame(self.master,bg="white",relief="sunken",bd=2,width=FRAME_SIZE*3)
        self.frame_status=tk.Frame(self.master,bg="blue",relief="sunken",bd=2,width=FRAME_SIZE)
        self.frame_menu.propagate(False)
        self.frame_status.propagate(False)
        self.frame_menu.pack(side="left",fill="both")
        self.frame_status.pack(side="left",fill="both")

        #
        self.frame_result=tk.Frame(self.frame_menu,bg="green",relief="sunken",bd=2,width=FRAME_SIZE*3,height=FRAME_SIZE*2)
        self.frame_deck=tk.Frame(self.frame_menu,bg="red",relief="sunken",bd=2,width=FRAME_SIZE*3,height=FRAME_SIZE*1)
        self.frame_result.pack(side="top",fill="both",expand="True")
        self.frame_deck.pack(side="top",fill="both",expand="True")
        self.frame_result.propagate(False)
        self.frame_deck.propagate(False)
        
        self.label_deck=tk.Label(self.frame_deck)
        self.label_deck.pack(fill="both")
        #
        self.frame_result_column=tk.Frame(self.frame_result,width=FRAME_SIZE*2,bg="black")
        self.frame_result_damage=tk.Frame(self.frame_result,width=FRAME_SIZE*1)
        self.frame_result_column.pack(side="left",fill="both")
        self.frame_result_damage.pack(side="left",fill="both")
        self.label_result=tk.Label(self.frame_result_column,bg="gray")
        self.label_result.pack(fill="both")
        #
        self.frame_status_input=tk.Frame(self.frame_status,width=FRAME_SIZE*1,height=FRAME_SIZE*2,bg="yellow")
        self.frame_status_execution=tk.Frame(self.frame_status,width=FRAME_SIZE*1,height=FRAME_SIZE*1)
        self.frame_status_input.propagate(False)
        self.frame_status_execution.propagate(False)
        self.frame_status_input.pack(side="top",fill="both")
        self.frame_status_execution.pack(side="top",fill="both")
        
        
    def create_status_input(self):
        #
        self.value_CX=tk.IntVar(self.frame_status_input,value=8)
        self.label_CX=tk.Label(self.frame_status_input,text="CXの枚数",anchor="nw")
        self.spinbox_CX=tk.Spinbox(self.frame_status_input,from_=1,to=8,textvariable=self.value_CX)
        self.label_CX.pack(side="top",fill="both")
        self.spinbox_CX.pack(side="top",fill="both")
        #
        self.value_TOTAL=tk.IntVar(self.frame_status_input,value=50)
        self.label_TOTAL=tk.Label(self.frame_status_input,text="山札の枚数(CXを含む)",anchor="nw")
        self.spinbox_TOTAL=tk.Spinbox(self.frame_status_input,from_=1,to=50,textvariable=self.value_TOTAL)
        self.label_TOTAL.pack(side="top",fill="both")
        self.spinbox_TOTAL.pack(side="top",fill="both")

        self.button_value_update=ttk.Button(self.frame_status_input,text="山札をセット",command=self.value_update)
        self.button_value_update.pack(fill="both")
        
        self.label_attack_situ=tk.Label(self.frame_status_input,text="攻撃の種類 + 枚数 ",anchor="nw")
        self.combobox_attack_situ=ttk.Combobox(self.frame_status_input,values=self.deck.attack_type,state="readonly")
        self.combobox_attack_situ.set(self.deck.attack_type[0])
        self.value_attack_num=tk.IntVar(self.frame_status)
        self.spinbox_attack_num=tk.Spinbox(self.frame_status_input,from_=1,to=10,textvariable=self.value_attack_num)
        self.label_attack_situ.pack(side="top",fill="both")
        self.combobox_attack_situ.pack(side="top",fill="both",pady=10)
        self.spinbox_attack_num.pack(side="top",fill="both",pady=10)
        
        self.button_attack_update=ttk.Button(self.frame_status_input,text="攻撃を追加",command=self.attack_add)
        self.button_attack_update.pack(fill="both",pady=10)

        self.label_entry = tk.Label(self.frame_status_input, text="詰めの概要:")
        self.label_entry.pack()
        self.entry = tk.Entry(self.frame_status_input)
        self.entry.pack()

    def create_status_execution(self):
        self.button_exe=ttk.Button(self.frame_status_execution,text="単発実行",command=self.exe_sim,width="20")
        self.button_exe.pack()
        self.button_trial=ttk.Button(self.frame_status_execution,text="試行",command=self.exe_trial)
        self.button_trial.pack(fill="both")
        self.button_reset=ttk.Button(self.frame_status_execution,text="reset",command=self.reset)
        self.button_reset.pack(side="bottom",fill="both")
        self.status_deck="山の枚数: "+str(self.value_CX.get())+" / "+str(self.value_TOTAL.get())
        self.status_label_deck=tk.Label(self.frame_status_execution,text=self.status_deck,)
        self.status_attack="攻撃の状況 : "+str(self.deck.attack_situ)+str(self.deck.attack_value)
        self.status_label_attack=tk.Label(self.frame_status_execution,text=self.status_attack,wraplength=FRAME_SIZE, justify=tk.LEFT)
        self.status_label_deck.pack(fill="both")
        self.status_label_attack.pack(fill="both",expand="true",anchor="nw")
        
    
def main():
    root = tk.Tk()
    app = Application(master=root)#Inheritクラスの継承！
    app.mainloop()

if __name__ == "__main__":
    main()
