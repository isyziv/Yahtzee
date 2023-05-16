import random
from itertools import combinations
from itertools import permutations
from queue import Queue
import threading
import asyncio
import time
from flask import Flask, json, request, jsonify
from copy import copy
import traceback
PORT = 54088
ACCO_FILE = 'data/account.json'
ACCOUNTS = []
lock = threading.Lock()
lock_join = threading.Lock()
join_q=Queue()
room=[]
player_inform={} #{uid:[playid,room]}
def find_next_id():
    with open(ACCO_FILE) as fp:
        ACCOUNTS = json.load(fp)
    return max(account["id"] for account in ACCOUNTS) + 1
def find_same_name(target):
    with open(ACCO_FILE) as fp:
        ACCOUNTS = json.load(fp)
    for account in ACCOUNTS:
        if(account["name"]==target):
            return True
    return False
API = Flask(__name__)
@API.post("/accounts")
def register():
    if request.is_json:
        lock.acquire()
        new = request.get_json()
        new["id"] = find_next_id()
        if find_same_name(new["name"])==True:
            print("same name")
            return {"error": "Account is same"}, 415
            #尋找是否相同
        new["dollar"]=1500
        ACCOUNTS.append(new)
        with open(ACCO_FILE, 'w') as wfp:
            json.dump(ACCOUNTS, wfp)
        lock.release()
        return new, 201
    else:
        return {"error": "Request must be JSON"}, 415
@API.get("/accounts")
def get_account():
    param = request.args.get('name')
    print(param)
    with open(ACCO_FILE) as fp:
        ACCOUNTS = json.load(fp)
    if(param == None):                # no parameters
        return jsonify(ACCO_FILE)
    else:
        RET_COMP = []
        for temp in ACCOUNTS:
            if(temp["name"] == param):
                RET_COMP.append(temp)
        return jsonify(RET_COMP)
@API.put("/accounts")
def put_account():
    if request.is_json:
        lock.acquire()
        new = request.get_json()
        uid=new["uid"]
        money =new["money"] 
        with open(ACCO_FILE) as fp:
            ACCOUNTS = json.load(fp)
        for temp in ACCOUNTS:
            if(temp["id"] == uid):
                temp["dollar"]+=money
                break
        with open(ACCO_FILE, 'w') as wfp:
            json.dump(ACCOUNTS, wfp)
        lock.release()
        return new, 201
    else:
        return {"error": "Request must be JSON"}, 415
@API.post("/join")
def join():
    global join_q
    global player_inform
    uid = request.args.get('uid')
    #{uid:[playid,room]}
    if uid in player_inform.keys():
        return {"error": "You are playing"}
    if uid in list(join_q.queue):
        return {"error": "You are waiting"}   
    lock_join.acquire()        
    if(join_q.empty()):
        t = threading.Thread(target=waiting)
        t.start()
    join_q.put(uid)
    lock_join.release()
    print("Player "+uid+" join the Queue")
    while True:
        if player_inform.get(uid)!=None:
            if len(room)-1>=player_inform[uid][1]:
                print(player_inform)
                return jsonify(player_inform)

@API.get("/load")
def get_game():
    global player_inform
    new = request.get_json()
    uid=new["uid"]
    queue=list(room[player_inform[str(uid)][1]].q_out_total.queue)#main_dice
    result=[]
    for i in range(new["font"],len(queue)):
        result.append(queue[i])
    return jsonify(result)


    # new["uid"]
    # new["font"]

@API.put("/gameinput")
def input_game():
    global player_inform
    if request.is_json:
        new = request.get_json()
        uid = new["uid"]
        item =new["input"]
        print(item)
        if '@@' in item:
            item=item.replace('@@','')
            room[player_inform[str(uid)][1]].cpu_player_+=str(player_inform[str(uid)][0])
            if '0'in room[player_inform[str(uid)][1]].cpu_player_ and '1'in room[player_inform[str(uid)][1]].cpu_player_ and '2'in room[player_inform[str(uid)][1]].cpu_player_ and '3'in room[player_inform[str(uid)][1]].cpu_player_:
                kick_list=[]
                print("close room "+str(player_inform[str(uid)][1]))
                room[player_inform[str(uid)][1]]=None
                for player in player_inform:
                    if player_inform[player][1]==player_inform[str(uid)][1]:
                        print("kick "+player)
                        kick_list.append(player)
                for element in kick_list:
                    del player_inform[element]
        elif 'end' in item:
            kick_list=[]
            temp=player_inform[str(uid)][1]
            for player in player_inform:
                if player_inform[player][1]==temp:
                    print("kick "+player)
                    kick_list.append(player)
            for element in kick_list:
                del player_inform[element]
            room[temp]=None
            print("close room "+str(temp))
            print(room)
        else:
            try:
                room[player_inform[str(uid)][1]].q_in.put(item)
            except:
                print(traceback.format_exc())
        return new, 201
    else:
        return {"error": "Request must be JSON"}, 415

class game:
    def __init__(self):
        super(game,self).__init__()
    def roll_dice(self,i,sortting=False):
        num=[]
        for _ in range(i):
            num_tmp= random.randint(1,6)
            num.append(num_tmp)
        if sortting:
            num.sort()
        return num
    def re_roll_dice(self,fnc,dice,sortting=False):
        if fnc.find('#')==-1:
            return 'ERROR'
        for i in range(0,5):
            if fnc.find(str(i))!=-1:
                dice[i]=random.randint(1,6)
        if sortting:
            dice.sort()
        return dice
    def kind_count(self,num,dice):
        return dice.count(num)
    def count_score(self,fnc,dice_in,score):
        dice=dice_in[:]
        dice.sort()
        if score[12]==50 and (self.kind_count(1,dice)==5 or self.kind_count(2,dice)==5 or self.kind_count(3,dice)==5 or self.kind_count(4,dice)==5 or self.kind_count(5,dice)==5 or self.kind_count(6,dice)==5):
            return '+50'
        if fnc=='1':
            if score[1]!=0:
                return'-signed'
            return '+'+str(self.kind_count(1,dice)*1)
        elif fnc=='2':
            if score[2]!=0:
                return'-signed'
            return '+'+str(self.kind_count(2,dice)*2)
        elif fnc=='3':
            if score[3]!=0:
                return'-signed'
            return '+'+str(self.kind_count(3,dice)*3)
        elif fnc=='4':
            if score[4]!=0:
                return'-signed'
            return '+'+str(self.kind_count(4,dice)*4)
        elif fnc=='5':
            if score[5]!=0:
                return'-signed'
            return '+'+str(self.kind_count(5,dice)*5)
        elif fnc=='6':
            if score[6]!=0:
                return'-signed'
            return '+'+str(self.kind_count(6,dice)*6)
        elif fnc=='7':
            if score[7]!=0:
                return'-signed'
            if self.kind_count(dice[2],dice)>=3:
                re=0
                for num in dice:
                    re+=num
                return '+'+str(re)
            return'-'
        elif fnc=='8':
            if score[8]!=0:
                return'-signed'
            if self.kind_count(dice[2],dice)>=4:
                re=0
                for num in dice:
                    re+=num
                return '+'+str(re)
            return'-'
        elif fnc=='9':
            if score[9]!=0:
                return'-signed'
            if self.kind_count(dice[0],dice)+self.kind_count(dice[4],dice)==5:
                return '+25'
            return'-'
        elif fnc=='10':
            if score[10]!=0:
                return'-signed'
            re='+30'
            if 3 in dice  or 4 in dice:
                if 5 in dice:
                    if 2 in dice or 6 in dice:
                        return re
                if 1 in dice and 2 in dice:
                    return re
            return '-'
        elif fnc=='11':
            if score[11]!=0:
                return'-signed'
            re='+40'
            if 2 in dice and 3 in dice and 4 in dice and 5 in dice :
                if 1 in dice:
                    return re
                if 6 in dice:
                    return re
            return '-'
        elif fnc=='12':
            if self.kind_count(1,dice)==5 or self.kind_count(2,dice)==5 or self.kind_count(3,dice)==5 or self.kind_count(4,dice)==5 or self.kind_count(5,dice)==5 or self.kind_count(6,dice)==5:
                return '+50'
            return '-'
        elif fnc=='13':
            if score[13]!=0:
                return'-signed'
            re=0
            for num in dice:
                re+=num
            return '+'+str(re)
        return '--'
    def cpu_count_score(self,ans_tmp,score_table):
        score=0
        add_item=0
        for k in range(1,14):
            re=self.count_score(str(k),ans_tmp,score_table)
            if '+' in re:
                re=int(re.replace('+',''))
                if re>score:
                    score=max(re,score)
                    add_item=k
        return score,add_item
    def cpu_act(self,ans,score_table):
        score=0
        dance_select=[]
        for j in range(6):
            score_c=0
            dance_select_tmp=[]
            for try_re_dance in (list(combinations([i for i in range(5)],j))):
                score_b=0
                if try_re_dance!=():
                    for i in range (0,pow(6,j)):
                        ans_tmp=ans[:]
                        tmp=i
                        n1=tmp%6
                        tmp//=6
                        n2=tmp%6
                        tmp//=6
                        n3=tmp%6
                        tmp//=6
                        n4=tmp%6
                        tmp//=6
                        n5=tmp%6
                        nn=[n1+1,n2+1,n3+1,n4+1,n5+1]
                        for k in range(len(try_re_dance)):
                            ans_tmp[try_re_dance[k]]=nn[k]
                        score_a,_=self.cpu_count_score(ans_tmp,score_table)
                        score_b+=score_a
                    score_b/=pow(6,j)
                else:
                    ans_tmp=ans[:]
                    for k in range(len(try_re_dance)):
                        ans_tmp[try_re_dance[k]]=nn[k]
                    score_a,_=self.cpu_count_score(ans_tmp,score_table)
                    score_b=score_a
                if score_c<score_b:
                    score_c=score_b
                    dance_select_tmp=try_re_dance[:]
            if score<score_c:
                score=score_c
                dance_select=dance_select_tmp[:]
        dance_select_str='#'
        for _,select in enumerate (dance_select):
            dance_select_str+=str(select)
        if dance_select_str=='#':
            _,num=self.cpu_count_score(ans[:],score_table)
            dance_select_str='$'+str(num)
        return(dance_select_str)
class main_dice(threading.Thread):
    def __init__(self,player_,cpu_player_):
        super(main_dice,self).__init__()
        self.q_in = Queue()
        self.q_out = Queue()
        self.q_out_total = Queue()
        self.player_=player_
        self.cpu_player_=cpu_player_
    def get_q(self,stri):
        self.put_q('*in*')
        while self.q_in.qsize() ==0:
            pass
        return self.q_in.get()
    def put_q(self,stri):
        self.q_out.put(str(stri))
        self.q_out_total.put(str(stri))
        return
    def run(self):
        player = self.player_
        player=int(player)
        score=[[0]*14 for i in range(player)]
        dice=game()
        for ___ in range(13):
            for now_play in range(player):
                if str(now_play)in self.cpu_player_:
                    self.put_q('%d player turn(cpu)'%now_play)
                else:
                    self.put_q('%d player turn'%now_play)
                ans=dice.roll_dice(5,sortting=False)
                self.put_q(ans)
                if str(now_play)in self.cpu_player_:
                    ans_tmp=ans[:]
                    score_table_tmp=score[now_play][:]
                    fnc=dice.cpu_act(ans_tmp,score_table_tmp)
                else:
                    fnc = self.get_q('FNC:')
                self.put_q('2'+fnc)
                for __ in range(2):
                    if fnc.find('#')==-1:
                        break
                    ans=dice.re_roll_dice(fnc,ans,sortting=False)
                    self.put_q(ans)
                    if str(now_play)in self.cpu_player_:
                        ans_tmp=ans[:]
                        score_table_tmp=score[now_play][:]
                        fnc=dice.cpu_act(ans_tmp,score_table_tmp)
                        self.put_q(fnc)
                    else:
                        fnc = self.get_q('FNC:')
                        self.put_q(fnc)
                if str(now_play)in self.cpu_player_:
                    ans_tmp=ans[:]
                    score_table_tmp=score[now_play][:]
                    _,num=dice.cpu_count_score(ans_tmp,score_table_tmp)
                    fnc='$'+str(num)
                end=False
                while not end:
                    if fnc.find('$')==-1:
                        self.put_q('ERROR')
                        fnc = self.get_q('FNC:')
                        self.put_q(fnc)
                    self.put_q(fnc)
                    fnc_=fnc.replace('$','')
                    re=dice.count_score(fnc_,ans,score[now_play])
                    self.put_q(re)
                    if fnc=='$0':
                        if str(now_play)in self.cpu_player_:
                            end = True
                    if '-signed'in re:
                        end = False
                    elif '--' not in re:
                        if '-' in re:
                            re='0'
                        re=re.replace('+','')
                        score[now_play][int(fnc_)]=int(re)
                        bones=0
                        for j in range(7):
                            bones+=score[now_play][j]
                        if bones>=63:
                            score[now_play][0]=35
                        end = True
                    if not end:
                        if str(now_play)in self.cpu_player_:
                            ans_tmp=ans[:]
                            score_table_tmp=score[now_play][:]
                            _,num=dice.cpu_count_score(ans_tmp,score_table_tmp)
                            fnc='$'+str(num)
                            self.put_q(fnc)
                        else:
                            fnc = self.get_q('FNC:')
                            self.put_q(fnc)
                self.put_q('score')
                self.put_q(score)
                self.put_q('next roll')
        self.put_q('~~end~~')
# def game_io(q):
#     while True:
#         if q.q_out.qsize()!=0:
#             out=q.q_out.get()
#             if '~~end~~' == str(out):
#                 print('return')
#                 return
#             elif '*in*' == str(out):
#                 if '@@' in in_fnc:
#                     in_fnc=in_fnc.replace('@@','')
#                     self.cpu_player+=in_fnc
#                 else:
#                     q.q_in.put(input('FNC:'))
#             else:
#                 print(out)
#         else:
#             time.sleep(0.1)
def waiting():
    print("startwait")
    time.sleep(20)
    global join_q
    global player_inform
    while not join_q.empty():
        print("in")
        player=[]
        for i in range(4):
            if not join_q.empty():
                #{uid:[playid,room]}
                uid=join_q.get()
                player.append(uid)
                player_inform[uid]=[i,len(room)]
                print("playerid: "+str(i)+"  room number: "+str(len(room)))
            else:
                print("robot")
                continue
            print(len(player))
        if len(player)==1:
            room.append(main_dice('4','#'+'123'))
        elif len(player)==2:
            room.append(main_dice('4','#'+'23'))
        elif len(player)==3:
            room.append(main_dice('4','#'+'3'))
        elif len(player)==4:
            room.append(main_dice('4','#'))
        room[len(room)-1].start()
    print("endwait")
        #main(player)清光Queue 結束waiting lobby  
def main():
    global ACCOUNTS
    global FORUM
    # load JSON file
    with open(ACCO_FILE) as fp:
        ACCOUNTS = json.load(fp)
    print(ACCOUNTS)
    API.run(host='0.0.0.0', port=PORT, debug=True)    


if __name__ == '__main__':
    main()

# player=input('player:')
# cpu_player=input('cpu player id:')
# cpu_player='#'+cpu_player
# q=main_dice(player,cpu_player)
# q.start()
# print('@@')
# game_io(q)

