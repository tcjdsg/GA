from collections import defaultdict


class Graph():
    def __init__(self, v):
        self.graph = defaultdict(list)
        self.v = v
    def addedge(self, u, v):
        self.graph[u].append(v)

    def findcyc(self, v, visited, recst):
        # visited数组元素为true，标记该元素被findcyc递归调用链处理中，或处理过
        # recStack数组元素为true，表示该元素还在递归函数isCyclicUtil的函数栈中
        visited[v] = True
        recst[v] = True
        # 深度遍历所有节点
        for neighbour in self.graph[v]:
            if visited[neighbour] == False: # 如果该节点没有被处理过，那么继续调用递归
                if self.findcyc(neighbour, visited, recst) == True: # 如果邻接点neighbour的递归发现了环
                    return True
            elif recst[neighbour] == True:  # 如果neighbour被处理中（这里强调了不是处理过），且还在递归栈中，说明发现了环
                return True
        recst[v] = False # 函数开始时，V节点进栈，所以函数结束时，V节点出栈
        return False # v 的所有邻接点的递归都没有发现环，则返回假
    def iscyc(self):
        visited = [False] * self.v
        recst = [False] * self.v
        for node in range(self.v):  # 分别以每个节点作为起点，然后开始深度遍历
            if visited[node] == False: # 这里为真，说明之前的深度遍历已经遍历过该节点了，且那次遍历没有发现环
                if self.findcyc(node, visited, recst) == True:
                    return True
        return False #如果分别以每个节点作为起点的深度遍历都没有发现环，那肯定是整个图没有环


# class Solution {
#     boolean[] visited;  // 记录遍历过的节点，防止走回头路
#     boolean[] onPath;  // 记录一次递归堆栈中的节点
#     boolean hasCycle;
#     public boolean canFinish(int numCourses, int[][] prerequisites) {
#         // 建立有向图，判断有向图中是否存在环
#         List<Integer>[] graph = new LinkedList[numCourses];  // 数组链表，数组中每个元素都是一个链表
#         visited = new boolean[numCourses];
#         onPath = new boolean[numCourses];
#         hasCycle = false;
#         for (int i = 0; i < numCourses; i++) {
#             graph[i] = new LinkedList<>();  // 每一个元素都要初始化，因为成员变量没有默认值
#         }
#         for (int[] edges: prerequisites) {
#             int from = edges[1], to = edges[0];  // 要想修课程edges[0], 必须先修课程edges[1]
#             graph[from].add(to);  // 建立每个元素的链表
#         }
#
#         // 遍历图，判断是否有环——DFS
#         for (int i = 0; i < numCourses; i++) {
#             dfs(graph, i);
#         }
#         return !hasCycle;
#     }
#     public void dfs(List<Integer>[] graph, int s){
#         // visited记录访问过的节点，onPath记录正在访问的路径（用于判断环）
#         if(onPath[s]){
#             hasCycle = true;
#         }
#         if(visited[s] || hasCycle){
#             return;
#         }
#
#         onPath[s] = true;
#         visited[s] = true;
#         for (int t: graph[s]) {
#             dfs(graph, t);
#         }
#         onPath[s] = false;
#     }
# }
# class Solution {
#     public boolean canFinish(int numCourses, int[][] prerequisites) {
#         int[] indegrees = new int[numCourses];
#         List<List<Integer>> adjacency = new ArrayList<>();
#         Queue<Integer> queue = new LinkedList<>();
#         for(int i = 0; i < numCourses; i++)
#             adjacency.add(new ArrayList<>());
#         // Get the indegree and adjacency of every course.
#         for(int[] cp : prerequisites) {
#             indegrees[cp[0]]++;
#             adjacency.get(cp[1]).add(cp[0]);
#         }
#         // Get all the courses with the indegree of 0.
#         for(int i = 0; i < numCourses; i++)
#             if(indegrees[i] == 0) queue.add(i);
#         // BFS TopSort.
#         while(!queue.isEmpty()) {
#             int pre = queue.poll();
#             numCourses--;
#             for(int cur : adjacency.get(pre))
#                 if(--indegrees[cur] == 0) queue.add(cur);
#         }
#         return numCourses == 0;
#     }
# }



if __name__ == '__main__':
    edge=[(1, 2, 0), (1, 4, 0), (1, 6, 0), (1, 8, 0), (1, 11, 0), (1, 12, 0), (1, 13, 0), (2, 3, 3.340780097204418), (3, 10, 6.081099134884689), (4, 5, 2.971435400555104), (5, 10, 4.796190201304635), (6, 3, 3.1088445633349577), (6, 5, 3.1088445633349577), (6, 7, 3.1088445633349577), (6, 9, 3.1088445633349577), (7, 14, 10.434925495777854), (8, 9, 4.959994822533342), (9, 10, 3.3504818747656047), (10, 14, 4.071163137282369), (11, 16, 4.094968088542093), (12, 16, 12.860414892542227), (13, 16, 8.282653755146773), (14, 15, 3.796265542267987), (15, 16, 5.478989897811304), (16, 17, 5.147918023982174), (17, 35, 0), (18, 19, 0), (18, 21, 0), (18, 23, 0), (18, 25, 0), (18, 28, 0), (18, 29, 0), (18, 30, 0), (19, 20, 3.008011417128383), (20, 27, 6.321984360854419), (21, 22, 3.31388339519646), (22, 27, 5.449078731969812), (23, 20, 2.9030845960337177), (23, 22, 2.9030845960337177), (23, 24, 2.9030845960337177), (23, 26, 2.9030845960337177), (24, 31, 9.998532576536409), (25, 26, 4.752189753749503), (26, 27, 2.94112972423779), (27, 31, 4.130433314347584), (28, 33, 3.9352794684574506), (29, 33, 12.650359814676591), (30, 33, 7.974114442245578), (31, 32, 3.777084509969429), (32, 33, 5.288612008683941), (33, 34, 5.420220910023381), (34, 35, 0), (0, 1, 0), (0, 18, 0), (4, 6, 2.971435400555104), (6, 21, 3.1088445633349577), (21, 7, 3.31388339519646), (2, 28, 3.340780097204418), (28, 19, 3.9352794684574506), (19, 7, 3.008011417128383), (12, 32, 12.860414892542227), (25, 28, 4.752189753749503), (28, 9, 3.9352794684574506), (9, 27, 3.3504818747656047), (25, 26, 4.752189753749503), (26, 11, 2.94112972423779), (11, 10, 4.094968088542093), (29, 33, 12.650359814676591), (30, 22, 7.974114442245578), (22, 14, 5.449078731969812), (23, 24, 2.9030845960337177), (24, 15, 9.998532576536409), (23, 24, 2.9030845960337177), (24, 16, 9.998532576536409), (8, 13, 4.959994822533342), (8, 3, 4.959994822533342), (3, 20, 6.081099134884689), (6, 11, 3.1088445633349577), (11, 5, 4.094968088542093), (5, 31, 4.796190201304635), (24, 7, 9.998532576536409), (3, 9, 6.081099134884689), (9, 5, 3.3504818747656047), (26, 22, 2.94112972423779), (22, 20, 5.449078731969812), (23, 6, 2.9030845960337177), (28, 11, 3.9352794684574506), (31, 14, 3.777084509969429), (14, 16, 3.796265542267987), (3, 9, 6.081099134884689), (9, 14, 3.3504818747656047), (14, 16, 3.796265542267987), (26, 20, 2.94112972423779), (20, 31, 6.321984360854419), (31, 33, 3.777084509969429)]

    g =Graph(36)
    for e in edge:
        f = e[0]
        to =e[1]
        g.addedge(f,to)

    if g.iscyc():
        print("Graph has a cycle")
    else:
        print("Graph has no cycle")

    visited = []
    trace = []
    has_circle = False

    def dfs(node_index):
            global has_circle
            if (node_index in visited):
                if (node_index in trace):
                    has_circle = True
                    trace_index = trace.index(node_index)
                    for i in range(trace_index, len(trace)):
                        print(str(trace[i]) + ' ', end='')
                    print('\n', end='')
                    return
                return

            visited.append(node_index)
            trace.append(node_index)

            if (node_index != ''):
                children = g.graph[node_index]
                for child in children:
                    dfs(child)
            trace.pop()


    dfs(0)
