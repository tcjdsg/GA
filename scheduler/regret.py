import util
from conM.FixedMess import FixedMes
from util.utils import choice
from scheduler.scheduler import Scheduler
import random
import copy
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
def calNj(E,alltasks):
    u = [0 for i in range(len(E))]
    y = [0.0 for i in range(len(E))]
    x= alltasks[E[0]]
    for j in range(len(E)):
        for i in range(len(E)):
            u[j] = max(alltasks[E[i]].lf-alltasks[E[j]].lf,u[j])
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
            return E[j]

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

        Ei_number = calNj(Ei_0,allTasks)

        random_Ei_0 = Ei_number
        chromosome.append([random_Ei_0, cloneA[random_Ei_0].belong_plane_id, cloneA[random_Ei_0].taskid])
        allTasks[random_Ei_0].priority = a
        for key, Ei in cloneA.items():
            prece = cloneA[key].predecessor
            if random_Ei_0 in prece:
                prece.remove(random_Ei_0)
        del cloneA[random_Ei_0]

    return chromosome

class RBRS(Scheduler):

    def __init__(self, job):
        super(RBRS, self).__init__(job)

    def _reschedule(self):

        """
        Implementation of the RBRS sampling algorithm. See Lecture 4 - NYU Stern pdf for details.
        """
        new_tasks = []
        while True:
            to_run = super(RBRS,self).get_tasks_eligible_to_run()

            if len(to_run) == 1:
                new_tasks.append(self.allocate_resources(to_run[0]))
                del self.tasks_to_do[to_run[0].id]
                continue

            if len(to_run)  < 1:
                break

            max = 0
            for task in to_run:
                if task.mean > max:
                    max = task.mean
            ws = []
            for task in to_run:
                ws.append(max - task.mean)

            c = 1 / sum(ws)

            ps = []

            for w in ws:
                ps.append(w * c)

            the_task = choice(to_run, ps)
            new_tasks.append(self.allocate_resources(the_task))
            del self.tasks_to_do[the_task.id]
        if len(new_tasks) > 0:
            return new_tasks
