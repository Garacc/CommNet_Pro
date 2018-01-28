import sys
import os
import random
import csv

#GLOBAL PARAMETER
#initial distribution
TIME_RANGE = 10
#the test range (the max number of successful packets)
SUCCESS_RANGE = 1000
#test range
TEST_RANGE = 1000

#ALOHA PARAMETER
#slot length
SLOT = 2

#MACAW PARAMETER
#Timer parameter
BO_MIN = 2
BO_MAX = 64
#packet length
RTS_len = 1
CTS_len = 1
DS_len = 1
DATA_len = 50
ACK_len = 1
TOTAL_len = RTS_len + CTS_len + DS_len + DATA_len +ACK_len


class Terminal(object):
    def __init__(self, protocol = 'ALOHA', BO = BO_MIN, time = random.randint(0, TIME_RANGE)):
        #the protocol of the network
        self.Prot = protocol
        
        #set of random timer
        if(self.Prot == 'ALOHA'):
            self.Randtime = 1024
            
        elif(self.Prot == 'MACAW'):
            self.BO = max(min(BO, BO_MAX), BO_MIN)
            
        elif(self.Prot == 'TDMA'):
            self.Randtime = 64
        else:
            print('ERROR! No matched Protocol!')
            exit(0)
        
        #set the transmission time
        self.Time = time
    
    def setBO(self, BO):
        self.BO = max(min(BO, BO_MAX), BO_MIN)
    
    def setTime(self, time):
        self.Time = time


class Network(object):
    def __init__(self, terminal_num = 10, protocol = 'ALOHA', BO = BO_MIN):
        #one base station
        self.BaseNum = 1
        #the number of terminal
        self.TermNum = terminal_num
        #the protocol of the network
        self.Prot = protocol
        #the BO value of Timer
        self.BO = BO_MIN
    
    def setTerm(self, terminal_num):
        self.TermNum = terminal_num
        
    def buildNetwork(self):
        #build the initial network cell
        NetCell = []
        for i in range(self.TermNum):
            #append the terminal and random a initial transmission time
            NetCell.append(Terminal(self.Prot, self.BO, random.randint(0, TIME_RANGE)))
        #record the period
        count = 0
        #record the number of packets
        total_pkt = 0
        #record the number of successful packets
        succ_pkt = 0
        
        #the following code is for ALOHA
        if(self.Prot == 'ALOHA'):
            #start the simulation
            while(True):
                #the number and index of collision terminals in one slot
                coll_num = 0
                coll_term = []
                #check every terminal
                for i in range(self.TermNum):
                    if(NetCell[i].Time >= count * SLOT and NetCell[i].Time < (count + 1) * SLOT):
                        coll_num += 1
                        total_pkt += 1
                        coll_term.append(i)
                    else:
                        continue
                #time is going on
                count += 1
                
                if(coll_num == 0): #no pkt call to trans
                    continue
                elif(coll_num == 1): #only one pkt call to trans, no collision
                    succ_pkt += 1
                    NetCell[coll_term[0]].setTime(random.randint(0, NetCell[coll_term[0]].Randtime) + count * SLOT)
                    if(succ_pkt > SUCCESS_RANGE):
                        break
                else: #coll_num > 1 the collision happens
                    for i in range(coll_num):
                        NetCell[coll_term[i]].setTime(random.randint(0, NetCell[coll_term[i]].Randtime) + count * SLOT)
            
            throughput = 1.0 * succ_pkt / count
            load = 1.0 * total_pkt / count
            print('load: ', load)
            print('throughput: ', throughput)
            return load, throughput
        
        elif(self.Prot == 'MACAW'):
            #data sending countdown
            DS_num = 0
            #start the simulation
            while(True):
                #the number and index of collision terminals in one slot
                coll_num = 0
                coll_term = []
                #check network state
                if(DS_num == 0):
                    #check every terminal
                    for i in range(self.TermNum):
                        if(NetCell[i].Time == count):
                            coll_num += 1
                            total_pkt += 1
                            coll_term.append(i)
                        else:
                            continue
                    #time is going on
                    count += 1

                    if(coll_num == 0):
                        continue
                    elif(coll_num == 1):
                        #LD of MILD
                        BO = NetCell[coll_term[0]].BO - 1
                        for i in range(self.TermNum):
                            #copy the BO to each terminal
                            NetCell[i].setBO(BO)
                            #calculate the transmission time for each terminal
                            NetCell[i].setTime(random.randint(0, 2**NetCell[i].BO) + count + TOTAL_len)
                        DS_num = TOTAL_len
                        succ_pkt += 1
                        if(succ_pkt > SUCCESS_RANGE):
                            break
                    else:
                        for i in range(coll_num):
                            #MI of MILD
                            NetCell[coll_term[i]].setBO(int(NetCell[coll_term[i]].BO * 1.5))
                            #calculate the retransmission time for each collision terminal
                            NetCell[coll_term[i]].setTime(random.randint(0, 2**NetCell[coll_term[i]].BO) + count)
                            
                else: #DS_num != 0 means the data is sending
                    for i in range(self.TermNum):
                        if(NetCell[i].Time == count):
                            coll_num += 1
                            total_pkt += 1
                            coll_term.append(i)
                        else:
                            continue
                    #make sure the collision has been avoided
                    if(coll_num != 0):
                        print('ERROR! A COLLISION HAPPENED!')
                        quit(0)
                    #time and countdown is going on
                    count += 1
                    DS_num -= 1
            
            throughput = 1.0 * DATA_len * succ_pkt / count
            load = 1.0 * TOTAL_len * total_pkt / count
            print('load: ', load)
            print('throughput: ', throughput)
            return load, throughput
        
        elif(self.Prot == 'TDMA'):
            #start the simulation
            while(True):
                #check the index of time slot
                index = count % self.TermNum

                #check each terminal
                for i in range(self.TermNum):
                    if(NetCell[i].Time == count and i == index):
                        #success transmission
                        NetCell[i].setTime(random.randint(0, NetCell[i].Randtime) + count + 1)
                        succ_pkt += 1
                        
                    elif(NetCell[i].Time == count and i != index):
                        #push to the next slot
                        NetCell[i].setTime(count + 1)
                        
                    else:
                        continue
                    
                if(succ_pkt > SUCCESS_RANGE):
                    break
                
                #time is going on
                count += 1
            
            throughput = 1.0 * succ_pkt / count
            #load = 1.0 * total_pkt / count
            #print('load: ', load)
            print('Terminal Num: ', self.TermNum)
            print('throughput: ', throughput)
            return self.TermNum, throughput
        
        else:
            print('ERROR! No matched Protocol!')
            exit(0)

def main():
    net_aloha = Network(10, 'ALOHA', BO_MIN)
    net_macaw = Network(10, 'MACAW', BO_MIN)
    net_tdma = Network(10, 'TDMA', BO_MIN)

    aloha_result = []
    macaw_result = []
    tdma_result = []    
    epoch = 0
    
    while(True):
        epoch += 1
        net_aloha.setTerm(epoch)
        aloha_result.append(net_aloha.buildNetwork())        
        if(epoch > TEST_RANGE):
            break
    epoch = 0
    while(True):
        epoch += 1
        net_macaw.setTerm(epoch)
        macaw_result.append(net_macaw.buildNetwork())
        net_tdma.setTerm(epoch)
        tdma_result.append(net_tdma.buildNetwork())
        if(epoch > TEST_RANGE / 5):
            break

    with open('aloha.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(aloha_result) 
    with open('macaw.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(macaw_result)
    with open('tdma.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(tdma_result)

if __name__ == '__main__':
    main()
    
                
        
        