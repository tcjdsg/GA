from conM import FixedMess


def newAON(Humanss,Stations,Spacess):

    edge = []
    for _, activity in FixedMess.FixedMes.act_info.items():
        id = activity.id

        for toid in activity.successor:
            edge.append((id, toid))

    # print("原始边",edge)

    for humans in Humanss:
        for human in humans:
            add(edge,human.OrderOver)
    for stations in Stations:
        for station in stations:
            add(edge,station.OrderOver)

    for spaces in Spacess:
        for space in spaces:
            add(edge, space.OrderOver)

    # 这里面就包含了新的约束，但是燃气等资源约束暂时还未考虑
    return edge

def add(edge, OrderOver):
    Order = sorted(OrderOver, key = lambda x:x.es)

    for activityNum in range(len(Order)):
        frontActivity = Order[activityNum]
        if activityNum < len(Order) - 1:  # 说明这个人后面还有任务要干
                backActivity = Order[activityNum + 1]
                frontId = frontActivity.id
                backId = backActivity.id
                edge.append((frontId,backId))