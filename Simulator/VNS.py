import copy
import math
import random
from collections import defaultdict

import numpy as np

from JudgeResource.fitness import fitness
from Simulator.mysim import BigSim
from conM.FixedMess import FixedMes

'''
子图拓扑排序
'''


def daluan(duan_code):
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

# jzj项目重组
def vns3(pop, Cmax,ns):
        popi = copy.deepcopy(pop)
        a = popi.codes
        duan_code = []
        i = np.random.choice(FixedMes.jzjNumbers, 1, replace=False)
        jzj = i[0]
        poslist = []  # 记录飞机i各工序在a中的位置
        for m in range(FixedMes.Activity_num):
            # print("Varition",a[m])
            if a[m][1] == jzj:
                poslist.append(m)
        try:
            for gongxu in poslist:
                duan_code.append(a[gongxu])
            newcode = daluan(duan_code)
            for q in range(len(poslist)):
                a.pop(poslist[q] - q)

            number = [1]
            x2 = len(popi.codes) - 2
            for i in range(len(poslist) - 1):
                num = np.random.randint(number[-1] + 1, x2 - (len(poslist) - 2 - i))
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
        fitness(popi, Cmax,ns)
        if popi.WorkTime < pop.WorkTime:
            return True, popi
        else:
            # p=exp{-[f（s’）- f（s）]/f（s）}
            # 接受劣解，令s=s’进
            return jieshou(popi, pop)

# 右移
def vns2(pop, Cmax, ns):
    popi = copy.deepcopy(pop)
    jobIndex = np.random.randint(0, FixedMes.planeNum)
    taskIndex = np.random.randint(jobIndex * FixedMes.planeNum + 2, (jobIndex + 1) * FixedMes.planeNum - 1)
    indices = popi.indices()

    rl = np.array([np.min(indices[FixedMes.act_info[taskIndex].successor], initial=FixedMes.Activity_num)])
    for id in range(len(popi.codes)):
        if popi.codes[id][0] == taskIndex:
            record = popi.codes.pop(id)
            break

    choose_Insert = rl[0]-1
    popi.codes.insert(choose_Insert, record)
    fitness(popi, Cmax, ns)
    if popi.WorkTime < pop.WorkTime:
        return True,popi
    else:
        # p=exp{-[f（s’）- f（s）]/f（s）}
        # 接受劣解，令s=s’进
        return jieshou(popi, pop)

# 左移
def vns1( pop,Cmax,ns):
    popi = copy.deepcopy(pop)
    jobIndex = np.random.randint(0, FixedMes.planeNum)
    taskIndex = np.random.randint(jobIndex * FixedMes.planeNum + 2, (jobIndex + 1) * FixedMes.planeNum - 1)
    indices = popi.indices()

    ll = np.array([np.max(indices[FixedMes.act_info[taskIndex].predecessor], initial=-1)]) + 1
    rl = np.array([np.min(indices[FixedMes.act_info[taskIndex].successor], initial=FixedMes.Activity_num)])
    for id in range(len(popi.codes)):
        if popi.codes[id][0] == taskIndex:
            record = popi.codes.pop(id)
            break
    choose_Insert = ll[0]
    popi.codes.insert(choose_Insert, record)
    fitness(popi, Cmax, ns)
    if popi.WorkTime < pop.WorkTime:
        return True,popi
    else:
        # p=exp{-[f（s’）- f（s）]/f（s）}
        # 接受劣解，令s=s’进
        return jieshou(popi,pop)

def jieshou(popi,pop):
    p = math.exp(-(popi.WorkTime - pop.WorkTime)/pop.WorkTime)
    c = random.random()
    if c < p:
        return True, popi
    else:
        return False, pop

def VNS(pops, Cmax, ns , N = 10):
    """
    :param pops:
    :param Cmax:
    :param ns:
    :param N: 变邻域局部搜索的最大迭代次数
    :return:
    """
    pops = sorted(pops,key=lambda x: x.WorkTime)
    #选择前百分之二十的个体
    choosePops = pops[: int(0.2*len(pops))]
    last = pops[int(0.2*len(pops)):]
    record = []
    for choose in choosePops:
        n = 0
        flag = False
        while flag==False:
            n+=1
        # 随机选择三种变邻域
            linyu = np.random.randint(1, 4)
            if linyu == 1:
                flag, choose = vns1(choose, Cmax, ns)
                record.append(choose)
            if linyu == 2:
                flag, choose = vns2(choose, Cmax, ns)
                record.append(choose)
            if linyu == 3:
                flag, choose = vns3(choose, Cmax, ns)
                record.append(choose)
            if n > N:
                break
    pops = last+record
    return pops


if __name__ == '__main__':
    JZJsim = BigSim("C:/Users/29639/Desktop/sim/dis.csv")
    FixedMes.my()
    JZJsim.Init.InitPopulation()
    pops = FixedMes.AllFit

    newpops = VNS(pops,80,10,10)




