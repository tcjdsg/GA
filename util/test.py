import numpy as np
import pandas as pd

ACTIONS_Pm = [1,2,3,4,5,6,7,8,9,10]
def build_Pc_q_table(n_states, actions):
    return pd.DataFrame(
        np.zeros((n_states, len(actions)))
        # columns=actions
    )
Pc_q_table= build_Pc_q_table(20,ACTIONS_Pm)
Pc_A = np.random.choice(ACTIONS_Pm)
print(Pc_A)
Pc_q_predict = Pc_q_table.loc[1, Pc_A]
print(Pc_q_predict)
a=np.random.choice(10)
print(a)

indices = np.full(4, np.inf, dtype=int)
indices[0] = 1
indices[1] = 2
indices[2] = 3
indices[3] = 4
successors = [[1,2,3],
              [2,3],
              [3]]
processors = [[1,2,3],
              [2,3],
              [3]]

ll = np.array([np.max(indices[processors[job]], initial=0)
               for job in range(3)])

rl = np.array([np.min(indices[successors[job]],
                      initial=3)
               for job in range(3)])

mobility = np.maximum(rl - ll, 0)


p = mobility / mobility.sum()

l = [1,2,3]
l.insert(1,7)
print(l)
ll=1
rl=3
pop =[0,1,2,3]
x=pop.pop(2)
pop.insert(2,x)
print(pop)
# ll = np.array([np.max(indices[self.pa.act_info[jobIndex].predecessor], initial=0)]) + 1
# rl = np.array([np.min(indices[self.pa.act_info[jobIndex].successor], initial=999)])
# for id in range(len(popi.codes)):
#     if popi.codes[id][0] == jobIndex:
#         record = popi.codes.pop(id)
#         break
# try:
#     choose_Insert = np.random.randint(ll, rl)[0] if ll < rl else ll