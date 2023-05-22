from conM.FixedMess import FixedMes
from util import utils


class SimulationEntity(object):
    def __init__(self, env, task, callback, stochastic):
        self.env = env
        self.task = task
        self.action = env.process(self.run())
        self.callback_proc = callback
        self.stochastic = stochastic

    def run(self):

        self.task.set_started(self.env.now)
        yield self.env.timeout(self.compute_sleep_duration())
        self.task.set_finished(self.env.now)
        self.task.set_completed()
        self.callback_proc(self.env)

    def compute_sleep_duration(self):

        if self.stochastic:
            return utils.get_next_execution_time(self.task.taskid)
        else:
            return FixedMes.OrderTime[self.task.taskid]

