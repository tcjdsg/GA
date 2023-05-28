
# num_activities,
# num_resource_type,
# total_resource,
# activities
"""
初始化，包括加载数据
初始化编码

"""
import copy
import math
import random
from collections import defaultdict

from JudgeResource.judgeH import judgeHuman, judgeStation, judgeSpace, allocationHuman, allocationStation, judgeRenew
from ORM.newDAG import newAON
from scheduler.regret import encoderRule, calLFTandMTS
from util.utils import *
import numpy as np

from chromosome.Chromo import Chromosome
from conM.FixedMess import FixedMes

from human.Human import Human
from read.preprocess import InitM

from space.Space import Space
from station.Station import Station

#5/11添加优先数标志
class MyInit(object):

    def __init__(self,filenameDis):
        self.geneN = 0
        self.activities = {}
        self.Init = InitM(filenameDis)
        FixedMes.distance = self.Init.readDis()
        self.activities = self.Init.readData()
        self.geneN = FixedMes.Activity_num
        FixedMes.act_info = self.activities

    def InitPopulation(self):
        calLFTandMTS(self.activities)
        num = 0
        print("正在生成种群。。。。")
        while num < FixedMes.populationnumber:

            iter = Chromosome()
            # codes = encoderRule(self.activities)
            codes = self.encoder()
            iter.setcodes(codes)
            Human, Station, space, workTime, act_info = MyInit.fitness(iter)
            edge = newAON(Human, Station, space)
            iter.WorkTime = workTime

            FixedMes.AllFit[num] = copy.deepcopy(iter)
            num+=1

    def encoder(self):
        numbers = len(self.activities)
        cloneA = copy.deepcopy(self.activities)
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

            chromosome.append([random_Ei_0,cloneA[random_Ei_0].belong_plane_id,cloneA[random_Ei_0].taskid])
            self.activities[random_Ei_0].priority = a
            for key, Ei in cloneA.items():
                prece = cloneA[key].predecessor
                if random_Ei_0 in prece:
                    prece.remove(random_Ei_0)
            del cloneA[random_Ei_0]
        return chromosome

    '''
    :param chromosome: 
    :param iter: 
    :param Humans: 
    :param Orders: 
    :return: 
    '''

    @staticmethod
    def fitness(iter):
        Humans=[]
        Stations=[]
        Spaces=[]
        MyInit.initMess(Humans,Stations,Spaces)
        # initMessOrder(Orders, activities)
        newAct = MyInit.serialGenerationScheme(copy.deepcopy(FixedMes.act_info),iter.codes, Humans,Stations,Spaces,"left")
        iter.WorkTime = newAct[FixedMes.Activity_num-1].ef
        for key,acti in newAct.items():
            iter.activityES[key] = acti.es
            iter.activityEF[key] = acti.ef


        iter.setf()
        return Humans,Stations,Spaces ,iter.WorkTime,newAct

    @staticmethod
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


    '''
    串行调度生成机制，传入所有活动，资源限量，优先序列
    :param allTasks:
    :param resourceAvail:
    :param priority:
    :return:
    '''

    @staticmethod
    def serialGenerationScheme(allTasks, codes, humans,stations,spaces,LR):

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
            while t >=startTime :

                resourceSumH = np.zeros(len(resourceAvailH))
                recordH = [[] for _ in range(len(resourceAvailH))]
                resourceSumS = np.zeros(len(resourceAvailS))
                recordS = [[] for _ in range(len(resourceAvailS))]
                resourceSumSpace = np.zeros(len(resourceAvailSpace))
                resourceSumNew = np.zeros(len(resourceAvailS))

                flag = judgeRenew(allTasks, stations, resourceSumNew, selectTaskID,  t, dur)

                #第舰载机的座舱资源
                resourceSumSpace = judgeSpace(allTasks, spaces, resourceSumSpace, selectTaskID, now_pos, t, dur)
                for type in range(len(resourceAvailH)):
                    resourceSumH, recordH = judgeHuman(humans, type, allTasks[selectTaskID].resourceRequestH,
                                                                resourceSumH, recordH, now_pos, t, dur)
                for type in range(len(resourceAvailS)):
                    resourceSumS, recordS = judgeStation(allTasks, stations, type, resourceSumS, recordS,
                                                                selectTaskID, now_pos, t, dur)

                # 若资源不够，则向后推一个单位时间
                if (flag == False) or (resourceSumSpace < allTasks[selectTaskID].resourceRequestSpace).any() or (resourceSumH < allTasks[selectTaskID].resourceRequestH).any() or (resourceSumS < allTasks[selectTaskID].resourceRequestS).any() :
                        t = round(t + 1,1)
                else:
                    break
            # 若符合资源限量则将当前活动开始时间安排在这一时刻
            allTasks[selectTaskID].es = round(t,1)
            allTasks[selectTaskID].ef = round(t+dur,1)

            allocationHuman(recordH, allTasks[selectTaskID].resourceRequestH, humans, allTasks, selectTaskID,now_pos)
            allocationStation(recordS, stations, allTasks, selectTaskID)


            need = allTasks[selectTaskID].resourceRequestSpace[now_pos-1]
            if need > 0:
                index = 0
                spaces[now_pos-1][index].update(allTasks[selectTaskID])
                need -= 1

            # 局部调度计划ps
            ps.append(selectTaskID)

        return allTasks




if __name__ == '__main__':
    m = MyInit("C:/Users/29639/Desktop/sim/dis.csv")
    m.InitPopulation()
    a=[[0,1,2],[[2,3,1]]]
    b=[[1,1,2],[[2,3,1]]]


    print(a==b)












