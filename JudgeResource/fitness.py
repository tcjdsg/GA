import copy
import random

import numpy as np

from JudgeResource.judgeH import allocationHuman, allocationStation, judgeStation, judgeHuman, judgeSpace, judgeRenew
from ORM.newDAG import newAON
from conM.FixedMess import FixedMes
from draw.people import Draw1
from human.Human import Human
from Simulator.simulator import simMonte
from space.Space import Space
from station.Station import Station


def encoder(activities):
    numbers = len(activities)
    cloneA = copy.deepcopy(activities)
    chromosome = []
    for a in range(numbers):
        Ei_0 = []  # 紧前任务数为0的任务集编号
        for key, Ei in cloneA.items():
            prece = cloneA[key].predecessor
            if prece is None:
                continue
            Ei_number = len(prece)

            if Ei_number == 0:
                Ei_0.append(key)
        random.shuffle(Ei_0)
        random_Ei_0 = Ei_0[0]

        chromosome.append([random_Ei_0, cloneA[random_Ei_0].belong_plane_id, cloneA[random_Ei_0].taskid])
        activities[random_Ei_0].priority = a
        for key, Ei in cloneA.items():
            prece = cloneA[key].predecessor
            if random_Ei_0 in prece:
                prece.remove(random_Ei_0)
        del cloneA[random_Ei_0]
    return chromosome

def recordBestAndBad(g, Pops):
    temp = 99999
    bad = 0
    for pop in Pops:
        if pop.WorkTime < temp:
            temp = pop.WorkTime
            # 记录最优个体
            FixedMes.recordBest[g] = pop
        if pop.WorkTime > bad:
            bad = pop.WorkTime
            # 记录最优个体
            FixedMes.recordBad[g] = pop

    DVPU = 0
    for pop in Pops:
        pop.setDVPU(FixedMes.recordBest[g].activityEF)
        if pop.DVPC > DVPU:
            DVPU = pop.DVPC
            FixedMes.recordBadD[g] = pop
    # guiyihua(g, Pops)

    SumTime = 0
    BestCmax = 999
    BestPr = 0
    BestE=999
    Bestzonghe = 999999999999
    var=0
    for i in FixedMes.AllFit:
        # if i.Pr > BestPr:
        #     BestPr = i.Pr
        #
        # if i.Ecmax < BestE:
        #     BestE = i.Ecmax

        if i.WorkTime < BestCmax:
            BestCmax = i.WorkTime

        # if i.zonghe < Bestzonghe:
        #     Bestzonghe = i.zonghe

        SumTime += i.WorkTime


    FixedMes.AverPopTime = SumTime / len(FixedMes.AllFit)

    FixedMes.Avufit[g] = FixedMes.AverPopTime
    #
    # FixedMes.BestEcmax[g] = BestE
    FixedMes.BestCmax[g] = BestCmax
    # FixedMes.Bestzonghe[g] = Bestzonghe
    # FixedMes.BestPr[g] = BestPr

    FixedMes.f[g] = FixedMes.Avufit[g]/FixedMes.Avufit[0]
    var = 0
    for i in FixedMes.AllFit:
        var += abs(i.WorkTime - FixedMes.Avufit[g])

    FixedMes.var[g] = var
    FixedMes.d[g] = FixedMes.var[g]/FixedMes.var[0]
    FixedMes.m[g] = FixedMes.BestCmax[g]/FixedMes.BestCmax[0]

'''
归一化
'''
def guiyihua( g, Pops):
    minCmax = FixedMes.recordBest[g].WorkTime
    maxCmax = FixedMes.recordBad[g].WorkTime
    minDVPU = 0
    maxDVPU = FixedMes.recordBadD[g].DVPC

    for pop in Pops:
        pop.ForCluster[0] = (pop.WorkTime - minCmax) / (maxCmax - minCmax)
        pop.ForCluster[1] = (pop.DVPC) / maxDVPU

def serialGenerationScheme(allTasks, codes, humans, stations, spaces, LR):
    # 记录资源转移
    priorityToUse = codes
    resourceAvailH = FixedMes.total_Huamn_resource
    resourceAvailS = FixedMes.total_station_resource

    ps = [0]  # 局部调度计划初始化

    allTasks[0].es = 0  # 活动1的最早开始时间设为0
    allTasks[0].ef = allTasks[0].es + allTasks[0].duration

    for stage in range(0, len(priorityToUse)):
        selectTaskID = priorityToUse[stage][0]
        earliestStartTime = 0

        '''
        需要考虑移动时间
        '''
        now_pos = allTasks[selectTaskID].belong_plane_id
        dur = allTasks[selectTaskID].duration
        for preTaskID in allTasks[selectTaskID].predecessor:
            if allTasks[preTaskID].ef > earliestStartTime:
                earliestStartTime = allTasks[preTaskID].ef

        startTime = earliestStartTime
        # 检查满足资源限量约束的时间点作为活动最早开始时间，即在这一时刻同时满足活动逻辑约束和资源限量约束
        t = startTime

        resourceSumH = np.zeros(len(resourceAvailH))
        recordH = [[] for _ in range(len(resourceAvailH))]
        resourceSumS = np.zeros(len(resourceAvailS))
        recordS = [[] for _ in range(len(resourceAvailS))]
        resourceAvailSpace = FixedMes.total_space_resource

        # 计算t时刻正在进行的活动的资源占用总量,当当前时刻大于活动开始时间小于等于活动结束时间时，说明活动在当前时刻占用资源
        while t >= startTime:

            resourceSumH = np.zeros(len(resourceAvailH))
            recordH = [[] for _ in range(len(resourceAvailH))]
            resourceSumS = np.zeros(len(resourceAvailS))
            recordS = [[] for _ in range(len(resourceAvailS))]
            resourceSumSpace = np.zeros(len(resourceAvailSpace))
            resourceSumNew = np.zeros(len(resourceAvailS))

            flag = judgeRenew(allTasks, stations, resourceSumNew, selectTaskID, t, dur)

            # 第舰载机的座舱资源
            resourceSumSpace = judgeSpace(allTasks, spaces, resourceSumSpace, selectTaskID, now_pos, t, dur)
            for type in range(len(resourceAvailH)):
                resourceSumH, recordH = judgeHuman(humans, type, allTasks[selectTaskID].resourceRequestH,
                                                   resourceSumH, recordH, now_pos, t, dur)
            for type in range(len(resourceAvailS)):
                resourceSumS, recordS = judgeStation(allTasks, stations, type, resourceSumS, recordS,
                                                     selectTaskID, now_pos, t, dur)

            # 若资源不够，则向后推一个单位时间
            if (flag == False) or (resourceSumSpace < allTasks[selectTaskID].resourceRequestSpace).any() or (
                    resourceSumH < allTasks[selectTaskID].resourceRequestH).any() or (
                    resourceSumS < allTasks[selectTaskID].resourceRequestS).any():
                t = round(t + 1, 1)
            else:
                break
        # 若符合资源限量则将当前活动开始时间安排在这一时刻
        allTasks[selectTaskID].es = round(t, 1)
        allTasks[selectTaskID].ef = round(t + dur, 1)

        allocationHuman(recordH, allTasks[selectTaskID].resourceRequestH, humans, allTasks, selectTaskID, now_pos)
        allocationStation(recordS, stations, allTasks, selectTaskID)

        need = allTasks[selectTaskID].resourceRequestSpace[now_pos - 1]
        if need > 0:
            index = 0
            spaces[now_pos - 1][index].update(allTasks[selectTaskID])
            need -= 1

        # 局部调度计划ps
        ps.append(selectTaskID)

    return allTasks


def fitness(iter, Cmax ,Ns):
    Humans = []
    Stations = []
    Spaces = []
    initMess(Humans, Stations, Spaces)
    # initMessOrder(Orders, activities)
    newAct = serialGenerationScheme(copy.deepcopy(FixedMes.act_info), iter.codes, Humans, Stations, Spaces,
                                           "left")
    iter.WorkTime = newAct[FixedMes.Activity_num - 1].ef
    for key, acti in newAct.items():
        iter.activityES[key] = acti.es
        iter.activityEF[key] = acti.ef

    iter.setf()
    return Humans, Stations, Spaces,  newAct

def execution_historyToshow(result,newAct):
    Humans =[]
    initMess(Humans,[],[])

    jobInfo = result.jobs
    for key,job in jobInfo.items():
        id = job.id
        start = job.started
        finished = job.finished
        duration = job.duration
        newAct[id].es = start
        newAct[id].ef = finished
        needHumanNumber = newAct[id].HumanNums
        for everyHuman in needHumanNumber:
            type = everyHuman[0]
            index = everyHuman[1]
            Humans[type][index].OrderOver.append(newAct[id])
    Draw1(Humans)

def initMess(Humans,Stations,Spaces):
        number = 0

        for i in range(FixedMes.Human_resource_type):
            Humans.append([])
            for j in range(FixedMes.total_Huamn_resource[i]):
                # ij都是从0开头 ,number也是

                Humans[i].append(Human([i,j,number]))
                number += 1

        number = 0

        for i in range(FixedMes.station_resource_type):
            Stations.append([])
            for j in range(FixedMes.total_station_resource[i]):
                # ij都是从0开头 ,number也是
                Stations[i].append(Station([i,j,number]))
                number += 1

        for i in range(FixedMes.space_resource_type):
            Spaces.append([])
            for j in range(FixedMes.total_space_resource[i]):
                # ij都是从0开头 ,number也是
                Spaces[i].append(Space(j))
