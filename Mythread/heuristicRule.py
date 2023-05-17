import copy
import random
from collections import defaultdict

from Mythread.myInit import MyInit
from conM.FixedMess import FixedMes
from read.preprocess import InitM


def encoder(self):
    numbers = len(self.activities)
    cloneA = copy.deepcopy(self.activities)
    chromosome = []


    for a in range(numbers):
        Ei_0 = []  # 紧前任务数为0的任务集编号
        task = []
        for key, Ei in cloneA.items():
            prece = cloneA[key].predecessor
            if prece is None:
                continue
            Ei_number = len(prece)
            if Ei_number == 0:
                Ei_0.append(key)
                task.append(cloneA[key])

        random.shuffle(Ei_0)
        random_Ei_0 = Ei_0[0]

        chromosome.append([random_Ei_0, cloneA[random_Ei_0].belong_plane_id, cloneA[random_Ei_0].taskid])
        self.activities[random_Ei_0].priority = a
        for key, Ei in cloneA.items():
            prece = cloneA[key].predecessor
            if random_Ei_0 in prece:
                prece.remove(random_Ei_0)
        del cloneA[random_Ei_0]
    return chromosome
def encoderRule(allTasks, task):
    # 设备保障范围约束
    numbers = len(allTasks)
    cloneA = copy.deepcopy(allTasks)
    chromosome = []
    for a in range(numbers):
        Ei_0 = []  # 紧前任务数为0的任务集编号
        task = []
        for key, Ei in cloneA.items():
            prece = cloneA[key].predecessor
            if prece is None:
                continue
            Ei_number = len(prece)
            if Ei_number == 0:
                Ei_0.append(key)
                task.append(cloneA[key])

        sorted(Ei_0,key=lambda x:(-allTasks[x].mts,allTasks[x].lft,allTasks[x].id))
        random_Ei_0 = Ei_0[0]

        chromosome.append([random_Ei_0, cloneA[random_Ei_0].belong_plane_id, cloneA[random_Ei_0].taskid])
        allTasks[random_Ei_0].priority = a
        for key, Ei in cloneA.items():
            prece = cloneA[key].predecessor
            if random_Ei_0 in prece:
                prece.remove(random_Ei_0)
        del cloneA[random_Ei_0]
    return chromosome

def LFT(SucOrder):
    dfsLFT(SucOrder, 0)
    for key,tsak in SucOrder.items():
        print(tsak.id,tsak.lf)

def dfsLFT(SucOrder, i):
    if len(SucOrder[i].successor) == 0:
        SucOrder[i].lf = FixedMes.lowTime
        return FixedMes.lowTime

    time = 999
    for Orderid in SucOrder[i].successor:
        time = min(time,dfsLFT(SucOrder,Orderid)-SucOrder[Orderid].duration)
    SucOrder[i].lf = time
    return time

def MTS(SucOrder):

    dfsMTS(SucOrder,0)
    for key,tsak in SucOrder.items():
        print(tsak.id,tsak.mts)
    # Most total successors


def dfsMTS(SucOrder,i):
    if len(SucOrder[i].successor)==0:
        return [SucOrder[i].id]

    record = copy.deepcopy(SucOrder[i].successor)
    for Orderid in SucOrder[i].successor:
        record = list(set(record + dfsMTS(SucOrder,Orderid)))

    SucOrder[i].mts = len(record)
    return record



if __name__ == '__main__':
    m = InitM("C:/Users/29639/Desktop/sim/dis.csv","C:/Users/29639/Desktop/sim/dis.csv")
    m.readDis()
    acts =m.readData()

    LFT(acts)
    MTS(acts)

    print()









