import copy
import functools
import math
import numpy as np
import torch

from JudgeResource.fitness import fitness
from Mythread.myInit import MyInit
from util import utils

from chromosome.Chromo import Chromosome

from  collections import defaultdict

from util.utils import *
import random

class Ga(object):
    def __init__(self):
        # self.Init = myInit.MyInit(dis_file,order_file)
        self.pa = FixedMess.FixedMes
        self.acts = FixedMes.Activity_num

        self.DCmin=10
        self.humanNum = self.pa.humanNum

    def RUN(self,i,pop,cmax,ns):
        self.Cmax= cmax
        self.ns = ns
        self.Pop = pop
        self.cur=i
        self.count = 0
        # print("----------- ----",i,"--------------")
        self.select()
        self.Crossover()
        self.Variation()
        self.updata()
        return self.count

    def select(self):

        fitness = []
        for p in self.Pop:
            fitness.append(p.WorkTime)
        fitness = np.array(fitness)
        p = []
        secret_p = 1.5  # 选择压力
        torch_f = torch.from_numpy(fitness)
        sorted, indices = torch.sort(torch_f, dim=0, descending=True)
        sorted = sorted.numpy()
        for i in range(len(fitness)):
            for j in range(len(sorted)):
                if fitness[i] == sorted[j]:
                    p.append([j + 1])
                    break

        p = np.array(p)
        fitness = 2 - secret_p + (2 * (p - 1) * (secret_p - 1)) / (len(self.Pop) - 1)
        s = sum(fitness)
        p = [fitness[i] / s for i in range(len(fitness))]
        index = []
        # 通过赌盘法选择NP个染色体
        for i in range(len(self.Pop)):
            cum = 0
            m = random.random()
            for j in range(len(self.Pop)):
                cum += p[j]
                if cum >= m:
                    index.append(j)
                    break

        for i in range(len(FixedMes.Paternal)):
            two = np.random.choice(index, 2, False)
            FixedMes.Paternal[i] = two
    def Crossover(self):

        num_sonfit = 0
        ge = FixedMes.ge

        for two in FixedMes.Paternal:
            if two[0] == 0 and two[1] == 0:
                break
            k1 = 0.0
            if self.cur <= FixedMes.AgenarationIten:
                k1 = FixedMes.cross
            else:

                k1 = FixedMes.cross * (FixedMes.cross1 - 2 * math.pow(math.e, -(float(self.cur) / float(ge))) / (
                            1 + math.pow(math.e, - (float(self.cur) / float(ge)))))
            num = utils.getRandNum(0, 100)
            if (k1 >= 0.99):
                k1 = 0.99
            if (k1 <= 0.05):
                k1 = 0.05
            k1 = int((k1 * 100) % 100)
            # FixedMes.resver_k1[self.cur] = k1
            if num <= k1:
                # 交叉
                temp1, temp2 = self.cr2(FixedMes.AllFit[two[0]], FixedMes.AllFit[two[1]])

            else:
                temp1, temp2 = copy.deepcopy(FixedMes.AllFit[two[0]]), copy.deepcopy(FixedMes.AllFit[two[1]])
            FixedMes.AllFitSon[num_sonfit] = temp1
            num_sonfit += 1
            FixedMes.AllFitSon[num_sonfit] = temp2
            num_sonfit += 1

    def cr2(self, pop1, pop2):

        a = copy.deepcopy(pop1.codes)
        b = copy.deepcopy(pop2.codes)

        pos = random.randint(1, self.acts - 1)

        temp1 = copy.deepcopy(b[:pos])
        temp2 = copy.deepcopy(a[:pos])
        temp = copy.deepcopy(b[pos:])
        tempx = copy.deepcopy(a[pos:])
        for j in range(self.acts):
            for k in range(len(temp)):
                if a[j][0] == temp[k][0]:
                    temp1 = np.concatenate((temp1, [temp[k]]))
                    break
        # print(i,i+1,len(temp1))

        for j in range(self.acts):
            for k in range(len(tempx)):
                if b[j][0] == tempx[k][0]:
                    temp2 = np.concatenate((temp2, [tempx[k]]))
                    break
        # print(i,i+1,len(temp2))
        pop11 = Chromosome()
        pop11.setcodes(temp1.tolist())

        pop22 = Chromosome()
        pop22.setcodes(temp2.tolist())

        fitness(pop11, self.Cmax, self.ns)
        fitness(pop22, self.Cmax, self.ns)
        self.count += 2

        return pop11, pop22
    def Variation(self):
        ge = FixedMes.ge
        for i in range(len(FixedMes.AllFitSon)):

            k2 = 0
            if self.cur <= FixedMes.AgenarationIten:
                k2 = FixedMes.MutationRate
            else:
                k2 = FixedMes.MutationRate * (2 * math.pow(math.e, -(float(self.cur) / float(ge))) / (
                            1 + math.pow(math.e, - (float(self.cur) / float(ge)))))

            num = utils.getRandNum(0, 100)
            if (k2 >= 0.99):
                k2 = 0.99
            if (k2 <= 0.05):
                k2 = 0.05
            k2 = int((k2 * 100) % 100)
            # FixedMes.resver_k2[self.cur] = k2
            if num <= k2:
                FixedMes.AllFitSon[i] = copy.deepcopy(self.var1(FixedMes.AllFitSon[i]))

    # FixedMes.AllFit = copy.deepcopy(FixedMes.AllFitSon)
    '''
    子图拓扑排序
    '''
    def daluan(self, duan_code):
        newcode = []
        newActs = defaultdict(lambda: [])
        for c in duan_code:
            newActs[c[0]] = []

        for act in duan_code:
            for i in duan_code:
                if act[0] == i[0]:
                    continue
                else:

                    if len(FixedMes.act_info[i[0]].predecessor) > 0:
                        for o in FixedMes.act_info[i[0]].predecessor:
                            if act[0] == o:
                                newActs[i[0]].append(act[0])

        for a in range(len(duan_code)):
            random_Ei_0 = 0
            Ei_0 = []  # 紧前任务数为0的任务集编号
            for key, Ei in newActs.items():
                Ei_number = len(Ei)

                if Ei_number == 0:
                    Ei_0.append(key)
            random.shuffle(Ei_0)
            try:
                random_Ei_0 = Ei_0[0]
            except:
                print("duluan拓扑邻域发生了错误。。。")

            # self.taskid = taskid
            # self.belong_plane_id = jzjId
            newcode.append(
                [random_Ei_0, FixedMes.act_info[random_Ei_0].belong_plane_id, FixedMes.act_info[random_Ei_0].taskid])
            for key, Ei in newActs.items():
                prece = newActs[key]
                if random_Ei_0 in prece:
                    prece.remove(random_Ei_0)
            del newActs[random_Ei_0]
        return newcode
    def insert(self, opt, pop):
        a = copy.deepcopy(pop)
        self.inser(opt, a, FixedMes.act_info)
        # MyInit.fitness(a, [], [], [])
        return a

    def inser(self, opt, pop, activities):

        preorder = activities[opt].predecessor
        success = activities[opt].successor

        ts = 0
        es = 999
        newcode = []
        newcode.append(pop.codes[0][:opt] + pop.codes[0][opt + 1:])
        newcode.append(pop.codes[1][:opt] + pop.codes[1][opt + 1:])

        # 得到了
        for id in preorder:
            if pop[0][id].es > ts:
                ts = activities[id].es

        for id in success:
            if activities[id].es < es:
                es = activities[id].es

        code = []

        for time in newcode[0]:
            if time[1] >= ts and time[1] <= es:
                code.append(time)

        qujian = sorted(code, key=lambda x: x[1])
        optnow = np.random.choice([x for x in range(0, len(qujian) - 1)], 1, replace=False)[0]
        time1 = qujian[optnow][1]
        time2 = qujian[optnow + 1][1]

        a = random.uniform(time1, time2)

        pop.codes[0][opt] = [opt, a]
        pop.codes[1][opt] = [opt, a + activities[opt].duration]

    def exchange1(self, pop):

        newpop = copy.deepcopy(pop)
        a = newpop.codes

        i = np.random.choice(FixedMes.jzjNumbers, 1, replace=False)
        jzj = i[0]

        poslist = []  # 记录飞机i各工序在a中的位置
        for m in range(len(a[0])):
            # print("Varition",a[m])
            if self.acts[a[0][m][0]].belong_plane_id == jzj:
                poslist.append(m)

        dr = np.random.choice([x for x in poslist], 5, replace=False)

        for opt in dr:
            self.inser(opt, newpop, FixedMes.act_info)

        # MyInit.fitness(newpop, [], [], [])
        return newpop

    def exchange2(self, pop):

        newpop = copy.deepcopy(pop)
        a = newpop.codes

        i = np.random.choice(FixedMes.jzjNumbers, 1, replace=False)
        jzj = i[0]

        poslist = []  # 记录飞机i各工序在a中的位置
        for m in range(len(a[0])):
            # print("Varition",a[m])
            if self.acts[a[0][m][0]].belong_plane_id == jzj:
                poslist.append(m)

        for opt in poslist:
            self.inser(opt, newpop, self.acts)

        # MyInit.fitness(newpop, [], [], [])
        return newpop

    def var1(self, pop):

        newpop = copy.deepcopy(pop)
        a = newpop.codes
        duan_code = []
        i = np.random.choice(FixedMes.jzjNumbers, 1, replace=False)
        jzj = i[0]

        poslist = []  # 记录飞机i各工序在a中的位置
        for m in range(self.acts):
            # print("Varition",a[m])
            if a[m][1] == jzj:
                poslist.append(m)
        dr=-1
        TI=[-1]
        Td=[-1]

        try:
            dr = np.random.choice([x for x in range(4, 9)], 1, replace=False)[0]
            TI = np.random.choice([x for x in range(1, FixedMes.planeOrderNum - 3 - dr)], 1, replace=False)

            Td = poslist[TI[0]:TI[0] + dr]

            x1 = Td[0]
            x2 = Td[-1]

            for gongxu in Td:
                duan_code.append(a[gongxu])

            newcode = self.daluan(duan_code)
            for q in range(dr):
                a.pop(Td[q] - q)

            number = [x1 - 1]
            for i in range(dr - 1):
                num = np.random.randint(number[-1] + 1, x2 - (dr - 2 - i))
                number.append(num)
                a.insert(num, newcode[i])

            num = number[-1]
            if (num + 1) < x2:
                number5 = np.random.randint(num + 1, x2 + 1)
                a.insert(number5, newcode[-1])
            if (num + 1) == x2:
                number5 = x2
                a.insert(number5, newcode[-1])
        except:
            print("变异发生了错误。。。。。。")
            print(poslist)
            print(dr)
            print(TI)
            print(Td)
        self.count += 1

        fitness(newpop, self.Cmax, self.ns)
        return newpop

    # def var2(self,pop):
    #
    #     suiji =random.random()*100%len(self.acts)
    #     suijn =
    #     jzj = i[0]
    #
    #     poslist = []  # 记录飞机i各工序在a中的位置
    #     for m in range(self.acts):
    #         # print("Varition",a[m])
    #         if a[m][1] == jzj:
    #             poslist.append(m)
    #
    #     dr = np.random.choice([x for x in range(2, 6)], 1, replace=False)
    #     TI = np.random.choice([x for x in range(1, FixedMes.planeOrderNum - 3 - dr)], 1, replace=False)
    #
    #     Td = poslist[TI[0]:TI[0] + dr]
    #     x1 = Td[0]
    #     x2 = Td[-1]
    #
    #     for gongxu in Td:
    #         duan_code.append(a[gongxu])
    #
    #     newcode = self.daluan(duan_code)
    #     for q in range(dr):
    #         a.pop(Td[q] - q)
    #     number = [x1-1]
    #     for i in range(dr - 1):
    #         num = np.random.randint(number[-1] + 1, x2 - (dr - 2 - i))
    #         number.append(num)
    #         a.insert(num, newcode[i])
    #
    #     num = number[-1]
    #     if (num + 1) < x2:
    #         number5 = np.random.randint(num + 1, x2 + 1)
    #         a.insert(number5, newcode[-1])
    #     if (num + 1) == x2:
    #         number5 = x2
    #         a.insert(number5, newcode[-1])
    #     return a
    '''
     self.WorkTime = 9999

        self.variance = 9999.0

        self.movetime = 9999.0
    '''

    # def pareto_compare(self, arrSlect, pop):
    #     reres = [0, 0]
    #     lenn = len(arrSlect)
    #     arrCh = [copy.deepcopy(pop[i]) for i in arrSlect]
    #
    #     arrCh.sort(key=lambda x: x.zonghe)
    #
    #     for i in range(lenn):
    #         if pop[arrSlect[i]].codes == arrCh[0].codes:
    #             reres[0] = arrSlect[i]
    #         elif pop[arrSlect[i]].codes == arrCh[1].codes:
    #             reres[1] = arrSlect[i]
    #     return reres
    #
    def updata(self):

        FixedMes.AllFit=sorted(FixedMes.AllFit,key=lambda x:x.zonghe)
        best = copy.deepcopy(FixedMes.AllFit[0])
        FixedMes.AllFitSon=sorted(FixedMes.AllFitSon, key=lambda x: -x.zonghe)

        bad = copy.deepcopy(FixedMes.AllFitSon[0])
        FixedMes.AllFit = copy.deepcopy(FixedMes.AllFitSon)
        FixedMes.AllFit[0] = copy.deepcopy(best)

        # dc=self.first(dataEdge)

    def writeArrayList(self,dcNextAll , nowHuman):
        ds = "output/paretoFor0" + nowHuman + ".txt"
        aimValue = 5
        content=[]
        printContent = []

        for i in range(aimValue):
            content.append([])
            printContent.append("")

        for i in range(len(dcNextAll)-1,-1,-1):
            content[0].append(str(nowHuman))
            nowHuman-=1
            content[1].append(str(dcNextAll[i][0]))
            content[2].append(str(dcNextAll[i][1]))
            content[3].append(str(dcNextAll[i][2]))
            content[4].append(str(dcNextAll[i][3]))


        for i in range(len(content)):
            str2 = ''.join(content[i])
            printContent[i]=str2
        writeTxt(ds,printContent)

    def writedataEdge(self,dataEdge,nowHuman):
        ds = "src/output/dataEdge6aim" + nowHuman + ".txt"
        aimValue = 6
        content=[]
        printContent = []

        for i in range(aimValue):
            content.append([])
            printContent.append("")

        for i in range(len(dataEdge.it)-1,-1,-1):
            content[0].append(str(dataEdge.it[i]))
            content[1].append(str(dataEdge.edgeSum[i]))
            content[2].append(str(dataEdge.edgeUp[i]))
            content[3].append(str(dataEdge.worktime[i]))
            content[4].append(str(dataEdge.var[i]))
            content[5].append(str(dataEdge.movetime[i]))


        for i in range(len(content)):
            str2 = ''.join(content[i])
            printContent[i]=str2
        writeTxt(ds,printContent)

        ds = "output/dataEdgegroup" + nowHuman + ".txt"
        aimValue = FixedMes.Human_resource_type
        content = []
        printContent = []
        for i in range(aimValue):
            content.append([])
            printContent.append("")

        for i in range(len(dataEdge.group)):
            for j in range(aimValue):
                content[j].append(dataEdge.group[j])

        for i in range(len(content)):
            str2 = ''.join(content[i])
            printContent[i]=str2
        writeTxt(ds,printContent)

        ds = "output/dataEdgegene" + nowHuman + ".txt"
        aimValue = len(dataEdge.gene)
        content = []
        printContent = []
        for i in range(aimValue):
            content.append([])
            printContent.append("")

        for i in range(aimValue):
                content[i].append(dataEdge.gene[i])
        for i in range(len(content)):
            str2 = ''.join(content[i])
            printContent[i]=str2
        writeTxt(ds,printContent)

    # / **
    # * @ param
    # conPopulation
    # 传入染色体集合
    # * @ return 传出第0层的染色体
    # * /
    def saveFor0Best(self):
        NDset = fast_non_dominated_sort(FixedMes.AllFit)
        FixedMes.bestHumanNumberTarget.append(NDset[0])
        return NDset[0]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   g=Ga("C:/Users/29639/Desktop/sim/dis.csv","C:/Users/29639/Desktop/sim/dis.csv")
   g.RUN(1)