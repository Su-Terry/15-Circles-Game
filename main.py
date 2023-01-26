import tkinter as tk
import random
from tkinter import ttk
from database import formula

root = tk.Tk()
root.title('15 circles')
root.minsize(600, 600)
root.maxsize(600, 600) # 視窗大小
root.configure(background='white')
screen = tk.Canvas(root, width=600, height=600, bg='white')
screen.pack(side=tk.TOP)

from picLoad import *

class Game:  #
    def __init__(self):
        ### Frame
        self.title = tk.Label(screen, text='15 circles', font=(None, 96))
        self.title.place(x=85, y=80)

        self.square = tk.Label(screen, image=square, bg='white')
        self.square.place(x=0, y=270)

        self.Select = tk.Button(screen, image=Select, bg='white', command=self.menu) 
        self.Select.place(x=20, y=290)

        self.PK = tk.Button(screen, image=PK, bg='white', command=self.PK_mode)
        self.CHL = tk.Button(screen, image=CHL, bg='white', command=self.CHL_mode)
        self.first = ttk.Button(screen, image=first, command=self.first_mode)
        self.second = ttk.Button(screen, image=second, command=self.second_mode)

        self.mode_list = [self.PK, self.CHL, self.first, self.second]
        self.pos = (20, 290), (210, 290), (210, 360), (400, 290), (400, 450)
        self.push, self.doublepush= False, False

        self.Mode, self.isFirst, self.isClose = None, True, False
    
    def menu(self):
        self.push = not self.push
        if self.push:
            for i, j in zip((self.PK, self.CHL), self.pos[1:3]):
                i.place(x=j[0], y=j[1])
        else:
            self.doublepush = False
            for i in self.mode_list:
                i.place_forget()

    def PK_mode(self):
        global isFrame
        self.Mode = 'PK'
        isFrame = False #
        self.start()

    def CHL_mode(self):
        self.Mode = 'Chl'
        self.doublepush = True
        if self.doublepush:
            for i, j in zip((self.first, self.second), self.pos[3:5]):
                i.place(x=j[0], y=j[1])

    def first_mode(self):
        global isFrame
        isFrame = False
        self.start()

    def second_mode(self):
        global isFrame
        self.isFirst = False
        isFrame = False
        self.start()
    
    def start(self):
        print(self.Mode)
        all_label = self.mode_list
        all_label.extend([self.title, self.square, self.Select])
        for i in all_label:
            i.destroy()
    
    def close(self):
        global isFrame, playing
        root.unbind('<B1-Motion>')
        root.unbind('<Button-1>')
        root.unbind('<ButtonRelease-1>')
        root.unbind('<Control-f>')
        root.unbind('<Control-F>')
        self.isClose = True
        playing = False
        isFrame = False
        tk._exit()


class Circles:  # 內含15個圓圈的顏色, 位置, 狀態
    def __init__(self):
        self.x = 0, 300, 255, 345, 210, 300, 390, 165, 255, 345, 435, 120, 210, 300, 390, 480
        self.y = 0, 210, 290, 290, 370, 370, 370, 450, 450, 450, 450, 530, 530, 530, 530, 530

        self.circle_color = [None]

        for i in range(1, 16):
            self.circle_color.append(screen.create_image(self.x[i], self.y[i], image=Circle_blue))

        self.pressed, self.pressed_now = [], []
        self.rendering, self.legal = False, True

    def isOver(self):
        x, y = root.winfo_pointerx() - root.winfo_rootx(), root.winfo_pointery() - root.winfo_rooty()
        for i in range(1, 16):
            if i in available.one:
                if self.x[i] - 25 < x < self.x[i] + 25 and self.y[i] - 25 < y < self.y[i] + 25:
                    screen.itemconfig(self.circle_color[i], image=Circle_blue2)
                    return
                else:
                    screen.itemconfig(self.circle_color[i], image=Circle_blue)

    def isRender(self, event):
        x, y = root.winfo_pointerx() - root.winfo_rootx(), root.winfo_pointery() - root.winfo_rooty()
        for a in range(1, 16):
            if self.x[a] - 25 < x < self.x[a] + 25 and self.y[a] - 25 < y < self.y[a] + 25:
                self.rendering = True
                if a not in self.pressed_now and a in available.one:
                    self.pressed_now.append(a)
                    screen.itemconfig(self.circle_color[a], image=Circle_blue2)
                    return

    def change_color(self):
        self.pressed_now.sort()
        print("pressed_now =", self.pressed_now)  # 檢查   

        self.rendering = False
        Player_circle_color = Circle_purple if player.player_now else Circle_green  #

        if ((len(self.pressed_now) == 1 and self.pressed_now[0] in available.one) or \
              self.pressed_now in available.two or self.pressed_now in available.three):
            for i in self.pressed_now:
                screen.itemconfig(self.circle_color[i], image=Player_circle_color)  # 

            self.pressed.append(list(self.pressed_now))
            self.legal = True
            print("legally pressed =", self.pressed)  # 檢查
            self.lineDrawing()

        else:
            player.player_now = not player.player_now
            print("illegally pressed!!")  # 檢查
            self.legal = False

    def lineDrawing(self):
        column = ((1,), (2,3), (4,5,6), (7,8,9,10), (11,12,13,14,15)) 
        start, end = self.pressed_now[0], self.pressed_now[-1]
        x1, y1, x2, y2 = self.x[start]-30, self.y[start]-30, self.x[end]-30, self.y[end]-30

        for i in column:
            if start in i and end in i:
                line_pos = (x1-5, y1+30, x2+60+5, y2+30, 7)
                break
        else:
            line_pos = (x1+47, y1, x2+13, y2+60, 8) if x1 > x2 else (x1+13, y1, x2+47, y2+60, 8)

        a, b, c, d, e = line_pos
        line_clr = '#441b83' if player.player_now else '#0a711d'
        screen.create_oval(a-e//2, b-e//2, a+e//2, b+e//2, fill=line_clr, outline='white')
        screen.create_oval(c-e//2, d-e//2, c+e//2, d+e//2, fill=line_clr, outline='white')
        screen.create_line(a, b, c, d, width=e, fill=line_clr)


class Available(formula.Conbine):  # 內含可用的直線列表, 及刪除調整
    def __init__(self):
        super(Available, self).__init__()

    def delete(self):
        print("total pressed =", len(circles.pressed_now))
        
        if circles.legal:
            self.one = list(set(self.one) - set(circles.pressed_now))
            self.one.sort()
            for i in self.two + self.three + self.four + self.five:
                if set(i) - set(circles.pressed_now) != set(i):
                    if len(i) == 2:
                        self.two.remove(i)
                    elif len(i) == 3:
                        self.three.remove(i)
                    elif len(i) == 4:
                        self.four.remove(i)
                    elif len(i) == 5:
                        self.five.remove(i)

            for i in circles.pressed_now:
                self.near[i-1] = []

                for j in self.near:
                    if i in j:
                        j.remove(i)
            
            for i, name in enumerate([self.one, self.two, self.three, self.four, self.five]):
                print("[%d]:"%(i+1), name)
        
        print('Available:', list(map(len, [self.one, self.two, self.three, self.four, self.five])))
        circles.pressed_now = []


class Player:
    def __init__(self):
        self.player_now = True if game.isFirst else False # player one
        self.player_label = tk.Label(screen, image=player_one, bg='white')

        self.ok_button = tk.Label(screen, image=ok_button, bg='white')
        self.regret_button = tk.Label(screen, image=regret_button, bg='white')

        self.player_label_pos = (0, 0)
        self.ok_button_pos = (400, 20)
        self.regret_button_pos = (500, 20)

        self.player_label.place(x=self.player_label_pos[0], y=self.ok_button_pos[1])
        self.ok_button.place(x=self.ok_button_pos[0], y=self.ok_button_pos[1])
        self.regret_button.place(x=self.regret_button_pos[0], y=self.regret_button_pos[1])

    def label_now(self):
        if self.player_now:
            self.player_label.config(image=player_one)
        else:
            self.player_label.config(image=player_two)

    def player_arrange(self):
        global playing
        for i in range(2):
            if game.Mode == "Chl":
                if not self.player_now:
                    computer.calculate()

            circles.change_color()
            available.delete()
            print(self.player_now)
            self.player_now = not self.player_now
            self.label_now()

            if not available.one:
                playing = False  #
                break
        

class Computer(formula.Solution):  # 包含各式必勝條件, 及電腦計算方法
    def __init__(self):
        super(Computer, self).__init__()
        self.good_end.sort(reverse = True, key = lambda i: i[0])

    def dfs(self, i):
        for j in available.near[i-1]:
            if j not in self.need_to_press + self.dfs_picked + self.have:
                self.dfs_picked.append(j)
                self.have.append(j)
                self.dfs(j)

    def near_total(self):  # 檢查相鄰顆數
        self.have, sum_total, self.dfs_picked = [], [], []

        for i in available.one:
            if i not in self.need_to_press + self.dfs_picked + self.have:
                self.dfs_picked.append(i)
                self.have.append(i)
                self.dfs(i)
                sum_total.append(len(self.dfs_picked))

                self.dfs_picked = []

        sum_total.sort()
        return sum_total

    def calculate(self):  # Not yet：電腦要是否判別兩次
        if not circles.legal:
            return

        for i in available.two + available.three + available.one:
            sum1 = 1 if type(i) is int else len(i)
            sum2, sum3, sum4, sum5 = 0, 0, 0, 0
            for j in available.two + available.three + available.four + available.five:
                if type(i) is int and i in j or type(i) is list and set(i) & set(j) != set():
                    if len(j) == 2:
                        sum2 += 1
                    elif len(j) == 3:
                        sum3 += 1
                    elif len(j) == 4:
                        sum4 += 1
                    else:
                        sum5 += 1

            for index, j in enumerate(self.good_end):
                if sum1 == len(available.one) - j[0] \
                  and sum2 == len(available.two) - j[1] and sum3 == len(available.three) - j[2] \
                  and sum4 == len(available.four) - j[3] and sum5 == len(available.five) - j[4]: 
                    self.need_to_press = [i] if type(i) is int else i
                    near_sum = self.near_total()
                    if near_sum == list(self.good_end[index][5]):
                        circles.pressed_now = self.need_to_press
                        print('Found:', j)
                        return

        circles.pressed_now.append(random.choice(available.one))
        
        
class Menu:
    def __init__(self):
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='遊戲', menu=filemenu)
        filemenu.add_command(label='新遊戲')
        filemenu.add_separator()
        filemenu.add_command(label='繼續')
        filemenu.entryconfigure(2, state=tk.DISABLED)
        filemenu.add_command(label='暫停')
        filemenu.add_command(label='重新開始')
        filemenu.add_separator()
        filemenu.add_command(label='離開', command=game.close)
        toolmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='工具', menu=toolmenu)
        toolmenu.add_command(label='指令', command=self.Input)
        helpmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='幫助', menu=helpmenu)
        helpmenu.add_command(label='關於')
        root.config(menu=menubar)

        self.showCmd = False
        self.cmdList = []

    def Input(self):
        self.showCmd = not self.showCmd
        if self.showCmd:
            self.cmdLabel = tk.Entry(root, width=50, bd=5)
            self.cmdLabel.place(x=0, y=0)
            self.cmdLabel.bind('<Return>', self.cmd)
        else:
            self.cmdLabel.place_forget()

    def cmd(self, event):
        try:
            tmp_command = self.cmdLabel.get()
            eval(tmp_command)
        except Exception:
            pass
        else:
            self.cmdList.append(tmp_command)
            print('CMD:', self.cmdList)

    def calculate(self):
        circles.legal = True
        computer.calculate()
        print(circles.pressed_now)
        circles.pressed_now = []
        circles.legal = False


isFrame = True

game = Game()
available = Available()
computer = Computer()

root.protocol('WM_DELETE_WINDOW', game.close)

while isFrame:
    root.update()

circles = Circles()
player = Player()
menu = Menu()

playing = True if not game.isClose else False
player.player_arrange()

root.bind('<B1-Motion>', circles.isRender)
root.bind('<Button-1>', circles.isRender)
root.bind('<ButtonRelease-1>', lambda event: player.player_arrange())
root.bind('<Control-f>', lambda event: menu.Input())
root.bind('<Control-F>', lambda event: menu.Input())

while playing:
    root.update()

    if not circles.rendering:
        circles.isOver()

if not game.isClose:
    with open('train process/process.txt', 'a') as f:
        f.write(str(circles.pressed) + ' ' + str(player.player_now) + '\n')
        
    f.close()


