import copy
import random
from collections import defaultdict

from Mythread.myInit import MyInit
from conM.FixedMess import FixedMes
from draw.people import Draw1
from read.preprocess import InitM


#基于遗憾值的随机抽样方法
def calNj(E,alltasks):
    u = [0 for i in range(len(E))]
    y = [0.0 for i in range(len(E))]

    for j in range(len(E)):
        for i in range(len(E)):
            u[j] = max(alltasks(E[i]).lf-alltasks(E[j]).lf)
    sumu=0
    for i in range(len(E)):
        sumu+=(u[i]+1)
    for j in range(len(E)):
        y[j] = (u[j]+1)/sumu
    #基于轮赌盘的选择抽样
    m = random.random()
    cum = 0
    for j in range(len(y)):
        cum += y[j]
        if cum >= m:
            return j

def encoderRule(allTasks):
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

        Ei_0 = calNj(Ei_0,allTasks)

        random_Ei_0 = Ei_0
        chromosome.append([random_Ei_0, cloneA[random_Ei_0].belong_plane_id, cloneA[random_Ei_0].taskid])
        allTasks[random_Ei_0].priority = a
        for key, Ei in cloneA.items():
            prece = cloneA[key].predecessor
            if random_Ei_0 in prece:
                prece.remove(random_Ei_0)
        del cloneA[random_Ei_0]

    return chromosome

def calLFTandMTS(SucOrder):
    dfsLFT(SucOrder, 0)
    dfsMTS(SucOrder, 0)

def dfsLFT(SucOrder, i):
    if len(SucOrder[i].successor) == 0:
        SucOrder[i].lf = FixedMes.lowTime
        return FixedMes.lowTime

    time = 999
    for Orderid in SucOrder[i].successor:
        time = min(time,dfsLFT(SucOrder,Orderid)-SucOrder[Orderid].duration)
    SucOrder[i].lf = time
    return time

def dfsMTS(SucOrder,i):
    if len(SucOrder[i].successor)==0:
        return [SucOrder[i].id]

    record = copy.deepcopy(SucOrder[i].successor)
    for Orderid in SucOrder[i].successor:
        record = list(set(record + dfsMTS(SucOrder,Orderid)))

    SucOrder[i].mts = len(record)
    return record



if __name__ == '__main__':
    from chromosome.Chromo import Chromosome
    m = InitM("C:/Users/29639/Desktop/sim/dis.csv","C:/Users/29639/Desktop/sim/dis.csv")
    m.readDis()
    acts =m.readData()
    calLFTandMTS(acts)

    FixedMes.act_info = acts
    codes = encoderRule(acts)
    iter = Chromosome()
    iter.codes = codes

    initt = MyInit("C:/Users/29639/Desktop/sim/dis.csv","C:/Users/29639/Desktop/sim/dis.csv")
    Human=[]
    Station = []
    Space = []
    initt.fitness(iter, Human, Station,Space)
    Draw1(Human)
    Draw1(Station)

    print()









