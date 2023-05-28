
import networkx as nx

import GA1
from JudgeResource.fitness import recordBestAndBad
from Mythread.parallelSGS import allboci
from Simulator import QLGA
from conM import FixedMess
from draw.people import Draw1
from Mythread import myInit
from conM.FixedMess import FixedMes
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

class BigSim():
    def __init__(self,dis_file):
        self.dis_file = dis_file
        self.Ns = 20
        self.Cmax = 90
        FixedMes.lowTime = self.Cmax
        # print()
        self.Init = myInit.MyInit(self.dis_file)
        self.Algorithm = GA1.Ga()
        self.adj = []
        for _, activity in FixedMess.FixedMes.act_info.items():
            id = activity.id
            for toid in activity.successor:
                self.adj.append((id, toid))

        self.G = nx.DiGraph()#Create a networkx graph object
        self.G_T = nx.DiGraph()#Create a networkx graph object
        for i in range(0,len(self.adj)):
            for j in self.adj[i]:
                self.G.add_edge(i, j)
                self.G_T.add_edge(j, i)

    def RUN(self):
        FixedMes.my()
        self.Init.InitPopulation()
        self.pa = FixedMes
        print("各类型人员组成: ", self.pa.total_Huamn_resource)
        allCount = 0
        g = 0
        recordBestAndBad(g, FixedMes.AllFit)
        while g < FixedMes.ge:
            g += 1
            allCount += 1
            self.Algorithm.RUN(g, FixedMes.AllFit,0,0)

            print("--{}-------Emax: {}---best: {}-----".format(g,FixedMes.Avufit[g], FixedMes.BestCmax[g]))

        sortFit = sorted(FixedMes.AllFit, key=lambda x: x.WorkTime)
        pop = sortFit[0]
        Human, Station, space, workTime, act_info = self.Init.fitness(pop)

        for i in range(len(pop.codes)):
            id = pop.codes[i][0]
            act_info[id].priority = i
        pop.WorkTime = workTime
        Draw1(Human)
        # Draw1(Station)
        print(pop.WorkTime)
        return Human,act_info

if __name__ == '__main__':
    JZJsim = BigSim("../dis.csv")
    Humans , act_info=  JZJsim.RUN()
    bociNums = 7
    allboci(act_info, Humans, bociNums)
    print("")