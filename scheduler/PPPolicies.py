__author__ = 'jules'

from conM.FixedMess import FixedMes
from scheduler.MfssRb import MfssRB
from scheduler.scheduler import Scheduler
from simulator.mysim import BigSim
from util.utils import Logger
from regret import encoderRule

"""
This class is the implementation of the Algorithm Proposed by Ashtiani et al.
"""
# class PPPolicies(Scheduler):
#     def __init__(self, job):
#         super(PPPolicies, self).__init__(job)
#         self.job = job
#         self.activities = job.tasks
#         FixedMes.act_info = job.tasks
#
#     def _reschedule(self):
#         return self.scheduler._reschedule()
#
#     def initialize(self):
#         super(PPPolicies, self)
#         Logger.info("Generating initial Population with RBRS")
#         FixedMes.my()
#         initial_pop = self._generate_RBRS(self.job,FixedMes.populationnumber)
#         FixedMes.AllFit = initial_pop
#         Logger.info("Applying ListGA to initial population")
#
#
#         listGA = BigSim(self.job)
#         # 优先列表
#         task_list = listGA.do_it()[0]
#
#
#         self.scheduler = MfssRB(self.job, task_list, [], ignore_infeasible_schedules=True)
#
#     def has_next(self):
#         return self.scheduler.has_next()
#
#     def get_next(self):
#         self.no_tasks_executed +=1
#         return self.scheduler.get_next()
#
#     def has_work_left(self):
#         return self.scheduler.has_work_left()
#
#     def get_execution_history(self):
#         return self.scheduler.get_execution_history()
#
#     def _generate_RBRS(self, job, n):
#         import simulator.simulator as sim # ugly circular dependency
#         inital_population = []
#         for i in range(n):
#             rbrs_scheduler = encoderRule(job)
#             result = sim.simulate_schedule(rbrs_scheduler)
#             inital_population.append(result.execution_history)
#         return inital_population
#
#     def getListGALog(self):
#         return self.listGALog
#     def getArcGALog(self):
#         return self.arcGALog