import math

from conM.FixedMess import FixedMes

'''
要改一下移动距离，删除吧
'''


def judgeHuman(Human, type, resourceRequestH1, resourceSumH1, recordH1, now_pos, t, dur):
    # 全甲板模式
    if FixedMes.modeflag == 0:
        typeHuman = Human[type]
    else:
        typeHuman = Human[int((now_pos - 1) / FixedMes.modeflag)][type]

    if resourceRequestH1[type] > 0:
        for human in typeHuman:
            if (len(human.OrderOver) == 0):
                resourceSumH1[type] += 1  # 该类资源可用+1
                recordH1[type].append(human)

            if (len(human.OrderOver) == 1):
                Activity1 = human.OrderOver[0]
                from_pos = Activity1.belong_plane_id
                to_pos = Activity1.belong_plane_id
                movetime1 = 0
                movetime2 = 0
                if (Activity1.ef + round(movetime1, 0)) <= t \
                        or (t + dur) <= (Activity1.es - round(movetime2, 0)):
                    resourceSumH1[type] += 1  # 该类资源可用+1
                    recordH1[type].append(human)

            # 遍历船员工序，找到可能可以插入的位置,如果船员没有工作，人力资源可用
            if (len(human.OrderOver) >= 2):
                flag = False
                for taskIndex in range(len(human.OrderOver) - 1):
                    Activity1 = human.OrderOver[taskIndex]
                    Activity2 = human.OrderOver[taskIndex + 1]

                    from_pos = Activity1.belong_plane_id
                    to_pos = Activity2.belong_plane_id
                    movetime1 = 0
                    movetime2 = 0

                    if (Activity1.ef + round(movetime1, 0)) <= t \
                            and (t + dur) <= (Activity2.es - round(movetime2, 0)):
                        flag = True
                        resourceSumH1[type] += 1  # 该类资源可用+1
                        recordH1[type].append(human)
                        break

                if flag == False:
                    Activity1 = human.OrderOver[0]
                    Activity2 = human.OrderOver[-1]
                    from_pos = Activity2.belong_plane_id
                    to_pos = Activity1.belong_plane_id
                    movetime2 = 0
                    movetime1 = 0

                    if (Activity2.ef + round(movetime2, 0)) <= t \
                            or (t + dur) <= (Activity1.es - round(movetime1, 0)):
                        resourceSumH1[type] += 1  # 该类资源可用+1
                        recordH1[type].append(human)

    return resourceSumH1, recordH1

def judgeRenew(allTasks, stations, resourceSumNew, selectTaskID,  t, dur):
    for type in range(len(resourceSumNew)):
        if allTasks[selectTaskID].resourceRequestS[type] > 0:
            renewFlag = True
            for station in stations[type]:
                if (len(station.OrderOver) == 0):
                    resourceSumNew[type] += 1  # 该类资源可用+1
                if (len(station.OrderOver) == 1):
                    Activity1 = station.OrderOver[0]
                    if (Activity1.ef) <= t \
                            or (t + dur) <= (Activity1.es):
                        resourceSumNew[type] += 1  # 该类资源可用+1
                if (len(station.OrderOver) >= 2):
                    flag = False
                    for taskIndex in range(len(station.OrderOver) - 1):
                        Activity1 = station.OrderOver[taskIndex]
                        Activity2 = station.OrderOver[taskIndex + 1]
                        if (Activity1.ef) <= t \
                                and (t + dur) <= (Activity2.es):
                            resourceSumNew[type] += 1  # 该类资源可用+1
                            flag = True

                    if flag == False:
                        Activity1 = station.OrderOver[-1]
                        Activity2 = station.OrderOver[0]
                        if (Activity1.ef) <= t or (t + dur) <= Activity2.es:
                            resourceSumNew[type] += 1
            #可用资源有多少：
            remian = max(FixedMes.total_renew_resource[type]-FixedMes.total_station_resource[type], 0)

            if remian + resourceSumNew[type] < allTasks[selectTaskID].resourceRequestS[type]:
                return False

    return True

def judgeStation(allTasks, Station, type, resourceSumS, recordS, selectTaskID, now_pos, t, dur):

        if allTasks[selectTaskID].resourceRequestS[type] > 0:
            for station in Station[type]:
                # 舰载机在这个加油站的覆盖范围内：
                if now_pos in FixedMes.constraintS_JZJ[type][station.zunumber]:

                    if (len(station.OrderOver) == 0):
                        resourceSumS[type] += 1  # 该类资源可用+1
                        recordS[type].append(station)

                    if (len(station.OrderOver) == 1):
                        Activity1 = station.OrderOver[0]

                        if (Activity1.ef) <= t \
                                or (t + dur) <= (Activity1.es):
                            resourceSumS[type] += 1  # 该类资源可用+1
                            recordS[type].append(station)

                    if (len(station.OrderOver) >= 2):
                        flag = False
                        for taskIndex in range(len(station.OrderOver) - 1):
                            Activity1 = station.OrderOver[taskIndex]
                            Activity2 = station.OrderOver[taskIndex + 1]

                            if (Activity1.ef) <= t \
                                    and (t + dur) <= (Activity2.es):
                                resourceSumS[type] += 1  # 该类资源可用+1
                                recordS[type].append(station)
                                flag = True
                        if flag == False:
                            Activity1 = station.OrderOver[-1]
                            Activity2 = station.OrderOver[0]

                            if (Activity1.ef) <= t or (t + dur) <= Activity2.es:
                                resourceSumS[type] += 1
                                recordS[type].append(station)
        return resourceSumS, recordS

def judgeSpace(allTasks, spaces, resourceSumSpace, selectTaskID, now_pos, t, dur):
    if allTasks[selectTaskID].resourceRequestSpace[now_pos - 1] > 0:
        for space in spaces[now_pos - 1]:
            if (len(space.OrderOver) == 0):
                resourceSumSpace[now_pos - 1] += 1  # 该类资源可用+1
            if (len(space.OrderOver) == 1):
                Activity1 = space.OrderOver[0]
                if (Activity1.ef) <= t \
                        or (t + dur) <= (Activity1.es):
                    resourceSumSpace[now_pos - 1] += 1  # 该类资源可用+1

            # 遍历船员工序，找到可能可以插入的位置,如果船员没有工作，人力资源可用
            if (len(space.OrderOver) >= 2):
                flag = False
                for taskIndex in range(len(space.OrderOver) - 1):
                    Activity1 = space.OrderOver[taskIndex]
                    Activity2 = space.OrderOver[taskIndex + 1]
                    if (Activity1.ef) <= t \
                            and (t + dur) <= (Activity2.es):
                        flag = True
                        resourceSumSpace[now_pos - 1] += 1  # 该类资源可用+1
                        break

                if flag == False:
                    Activity1 = space.OrderOver[0]
                    Activity2 = space.OrderOver[-1]

                    if (Activity2.ef) <= t \
                            or (t + dur) <= (Activity1.es):
                        resourceSumSpace[now_pos - 1] += 1  # 该类资源可用+1
    return resourceSumSpace

def allocationHuman(recordH1, resourceRequestH1,humans1, allTasks, selectTaskID,now_pos):
        for type in range(len(recordH1)):
            need = resourceRequestH1[type]
            while need > 0:
                alreadyWorkTime = 9999999999999
                index = 0
                for nowHuman in recordH1[type]:
                    if nowHuman.alreadyworkTime < alreadyWorkTime:
                        alreadyWorkTime = nowHuman.alreadyworkTime
                        index = nowHuman.zunumber

                for idn in range(len(recordH1[type])):
                    if recordH1[type][idn].zunumber == index:
                        recordH1[type].remove(recordH1[type][idn])
                        break

                # 更新人员
                if FixedMes.modeflag==0:
                    humans1[type][index].update(allTasks[selectTaskID])
                    allTasks[selectTaskID].HumanNums.append([type, index])
                else:
                    humans1[int((now_pos-1)/FixedMes.modeflag)][type][index].update(allTasks[selectTaskID])
                    allTasks[selectTaskID].HumanNums.append([type, index])

                # allTasks[selectTaskID].HumanNums.append(humans[type][index].number)
                need -= 1


def allocationStation(recordS, stations, allTasks, selectTaskID):
        for type in range(len(recordS)):

            need = allTasks[selectTaskID].resourceRequestS[type]
            if need > 0:
                alreadyWorkTime = math.inf
                index = 0
                for nowStaion in recordS[type]:
                    if nowStaion.alreadyworkTime < alreadyWorkTime:
                        alreadyWorkTime = nowStaion.alreadyworkTime
                        index = nowStaion.zunumber

                # 更新
                stations[type][index].update(allTasks[selectTaskID])
                allTasks[selectTaskID].SheiBei.append([type, index])
                # allTasks[selectTaskID].SNums.append(stations[type][index].number)
                need -= 1
