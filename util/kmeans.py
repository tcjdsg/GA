import math

import numpy as np
from matplotlib import pyplot as plt

from chromosome.Chromo import Chromosome
from conM import FixedMess
from conM.FixedMess import FixedMes
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

class kmeans(object):
    def __init__(self):
        # self.Init = myInit.MyInit(dis_file,order_file)

        self.dimension=2

        self.number_of_clusters = 3
        self.number_of_individuals = FixedMes.populationnumberson

        self.clusterCenterIndex=[]
        self.cluster = []
        self.meansList = []



    def clustering(self,POPS):
        self.Pop = POPS
        self.meansList = []
        self.cluster=[]

        for i in range(self.number_of_clusters):
            self.meansList.append(Chromosome())
            self.cluster.append([])

        for i in range(self.number_of_clusters):
            centerIndex = -1
            while True:
                flag = False
                centerIndex = np.random.randint(0,self.number_of_individuals)
                if self.Pop[centerIndex] in self.meansList:
                    continue
                # 如果类中心既未重复也未距离其他类中心太近，跳出循环
                break
            self.meansList[i] = self.Pop[centerIndex]

        for i in range(self.number_of_individuals):
            pop=self.Pop[i]
            label = self.getIndividualOfCluster(pop)
            self.cluster[label].append(i)

        oldVar = -1
        newVar = self.getVar()

        while abs(newVar-oldVar)>1:
            self.getMeans()
            oldVar=newVar

            for i in range(self.number_of_clusters):
                self.cluster[i]=[]

            for i in range(self.number_of_individuals):
                pop1 = self.Pop[i]
                label = self.getIndividualOfCluster(pop1)
                self.cluster[label].append(i)
            newVar = self.getVar()

        return self.cluster


    def getdistance(self,t1,t2):
        res=0.0
        for i in range(self.dimension):
            res+=(t1.ForCluster[i] - t2.ForCluster[i])*(t1.ForCluster[i] - t2.ForCluster[i])

        return math.sqrt(res)
    def getIndividualOfCluster(self,t):
        label =0
        mindistance = self.getdistance(t,self.meansList[0])
        for i in range(self.number_of_clusters):
            anotherDistance = self.getdistance(t,self.meansList[i])
            if anotherDistance < mindistance:
                mindistance =anotherDistance
                label = i

        return label
    def getVar(self):
        var=0.0
        for i in range(self.number_of_clusters):
            l = self.cluster[i]
            for j in range(len(l)):
                var +=self.getdistance(self.meansList[i],self.Pop[l[j]])

        return var
    def getMeans(self):
        # 清空上次聚类的质心残留
        self.meansList.clear()
        for i in range(self.number_of_clusters):
            cindividual = Chromosome()
            cindividual.ForCluster = []
            clusterSize = len(self.cluster[i])
            for k in range(self.dimension):
                means = 0.0
                for j in range(clusterSize):
                    means += self.Pop[self.cluster[i][j]].ForCluster[k]
                means /= clusterSize
                cindividual.ForCluster.append(means)
            self.meansList.append(cindividual)

    def plt(self):
        cluster = self.cluster
        """绘制聚类图，每进行一次计算中心点绘制一次
        Args:
            cluster ([二维数组]): 聚类后的索引下标，[[1,2],[0,3]]表示data[1,2]是一类，data[0,3]是一类
        """
        color_list = ['r', 'k', 'y', 'g', 'c', 'b', 'm', 'teal', 'dodgerblue',
                      'indigo', 'deeppink', 'pink', 'peru', 'brown', 'lime', 'darkorange']

        x1 = [pop.ForCluster[0] for pop in self.Pop]
        x2 = [pop.ForCluster[1] for pop in self.Pop]

        record =[0 for i in range(len(self.Pop))]
        for index in range(len(self.cluster)):
            for j in self.cluster[index]:
                record[j] = index

        for i in range(len(self.Pop)):
                plt.plot(x1[i], x2[i],'o', color=color_list[record[i]])
        for i in range(self.number_of_clusters):
                plt.plot(self.meansList[i].ForCluster[0], self.meansList[i].ForCluster[1], '^', color=color_list[len(color_list) - i - 1], ms=10)
        plt.show()
    #确定类中心
    #下面的实现是基于挑选类中最优个体作为类中心的
    #如果最终算法收敛效果不好，那么可以尝试一下使用质心作为类中心
    # def getCenter(self):
    #     for i in range(self.number_of_clusters):
    #         bestValue = 99999999999999999
    #         centerIndex = -1
    #         l = self.cluster[i]
    #         for j in range(len(l)):
    #             curV = self.Pop[l[j]].WorkTime
    #             if curV<bestValue:
    #                 bestValue =curV
    #                 centerIndex = l[j]
    #
    #         self.clusterCenterIndex[i] = centerIndex
