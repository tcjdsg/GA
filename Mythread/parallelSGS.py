from JudgeResource.judgeH import allocationHuman1, judgeHuman1
from draw.drawFatigue import  DrawF
from draw.people import Draw1

from util.utils import *

def allboci(allTasks, Humans, bociNums):
    """

    :param allTasks:
    :param Humans:
    :param bociNums: 波次数
    :return:
    """
    zhouqi = FixedMes.lowTime
    for boci in range(bociNums):
        startTime = zhouqi

        # 先更新所有人的 疲劳
        # for humanType in range(len(Humans)):
        #     for human in Humans[humanType]:
        #         human._rest(startTime)
        parallel_sgs(allTasks, Humans,startTime)
        Draw1(Humans)

    maxFatigue = 0
    type = 0
    number = 0
    for humanType in range(len(Humans)):
            for humanNum in range(len(Humans[humanType])):
                print("人员疲劳值是 {}---工种类型是 {}-".format(Humans[humanType][humanNum].fatigue, humanType))
                if Humans[humanType][humanNum].fatigue > maxFatigue:
                    maxFatigue = Humans[humanType][humanNum].fatigue
                    type = humanType
                    number = humanNum


    # DrawF(Humans[type][number])
    print("人员最高疲劳值是 {}---工种类型是 {}-".format(maxFatigue, type))

def parallel_sgs(allTasks, Humans,startTime):
    recordH = [[] for _ in range(len(FixedMes.total_Huamn_resource))]
    resourceSumH = [0 for _ in range(len(FixedMes.total_Huamn_resource))]
    alls = sorted(allTasks.values(),key=lambda x: (x.es, x.priority))
    resourceAvailH = FixedMes.total_Huamn_resource
    nowTime = alls[0].es + startTime
    for task in alls:
        task.es = task.es + startTime
        task.ef = task.ef + startTime

    while len(alls)>0:
        currentTasks = []
        for task in alls:
            if task.es == nowTime:
                currentTasks.append(task)
                alls.remove(task)
        if len(currentTasks) == 0:
            nowTime += 1
        else:
            for nowTask in currentTasks:
                recordH = [[] for _ in range(len(FixedMes.total_Huamn_resource))]
                resourceSumH = [0 for _ in range(len(FixedMes.total_Huamn_resource))]
                for type in range(len(resourceAvailH)):
                    resourceSumH, recordH = judgeHuman1(Humans, type, nowTask.resourceRequestH, resourceSumH,
                                                       recordH, nowTask.belong_plane_id, nowTime, nowTask.duration)

                assert judgeS1S2(resourceSumH, nowTask.resourceRequestH)
                allocationHuman1(recordH, nowTask.resourceRequestH, Humans, allTasks, nowTask.id, nowTime, nowTask.belong_plane_id)
            if len(alls)==0:
                break
            nowTime = alls[0].es






#


