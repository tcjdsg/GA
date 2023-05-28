import copy

import networkx as nx

import GA1
from JudgeResource.fitness import recordBestAndBad, encoder, fitness
from Mythread.myInit import MyInit
from ORM.newDAG import newAON
from chromosome.Chromo import Chromosome
from conM import FixedMess
from draw.people import Draw1

from Mythread import myInit
from conM.FixedMess import FixedMes

import os

from Simulator.simulator import simMonte

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
class BigSim():
    def __init__(self,dis_file):
        self.dis_file = dis_file
        self.Ns = 20
        self.Cmax = 80
        self.Q = 100000
        FixedMes.lowTime = self.Cmax
        # print()
        self.Init = myInit.MyInit(self.dis_file)
        self.Algorithm = GA1.Ga()
        self.adj = []
        self.activities = FixedMes.act_info
        for _, activity in self.activities.items():
            id = activity.id
            for toid in activity.successor:
                self.adj.append((id, toid))

        self.G=nx.DiGraph()#Create a networkx graph object
        self.G_T=nx.DiGraph()#Create a networkx graph object
        for i in range(0,len(self.adj)):
            for j in self.adj[i]:
                self.G.add_edge(i,j)
                self.G_T.add_edge(j,i)

        self.Ns = 20
        self.Nmin  = 10
        self.Nmax = 100
        self.r = 10

    def InitPopulation(self):
        num = 0
        print("正在生成种群。。。。")
        while num < FixedMes.populationnumber:

            iter = Chromosome()
            codes = encoder(self.activities)
            iter.setcodes(codes)
            fitness(iter, self.Cmax, self.Ns)
            FixedMes.AllFit[num] = copy.deepcopy(iter)
            num+=1

    def RUN(self):
        FixedMes.my()
        self.InitPopulation()
        self.pa = FixedMes
        print("各类型人员组成: ", self.pa.total_Huamn_resource)
        allCount = 0
        g = 0
        while allCount < self.Q:
            self.Ns = min(self.Nmax, self.Nmin * (1 + int(g / self.r)))
            g += 1
            allCount += 1
            recordBestAndBad(g,FixedMes.AllFit)
            addcount = (self.Algorithm.RUN(g, FixedMes.AllFit,self.Cmax,self.Ns))*self.Ns
            allCount += addcount
            print("---------cmax: {}---bestPr: {}---bestE:{}----bestzonghe:{}------".format(FixedMes.BestCmax[g],
                                                                                             FixedMes.BestPr[g],
                                                                                             FixedMes.BestEcmax[g],
                                                                                             FixedMes.Bestzonghe[g]))

        sortFit = sorted(FixedMes.AllFit,key=lambda x:x.WorkTime)
        pop = sortFit[0]
        Human, Station, space, workTime, act_info = self.Init.fitness(pop)
        pop.WorkTime = workTime

        Draw1(Human)
        Draw1(Station)
        print(pop.WorkTime)
        return workTime


if __name__ == '__main__':
    JZJsim = BigSim("C:/Users/29639/Desktop/sim/dis.csv")
    JZJsim.RUN()
