__author__ = 'jules'

import simpy
import argparse
import sys
import copy
import ORM.ORM as ORM

from scheduler.RBPolicy import RBPolicy

from scheduler.referenceScheduler import ReferenceScheduler

from scheduler.regret import RBRS
from scheduler.ABPolicy import ABPolicy

from simulationResult import *

from simulationEntity import SimulationEntity
import random
import numpy as np
import time

import matplotlib.pylab as plt
import seaborn as sns
import datetime

from util.utils import Logger


def simMonte(activities,adj):

    np.random.seed(int(time.time()))
    random.seed()
    job = ORM.Job()
    job.tasks = copy.deepcopy(activities)

    schedulers = {
        ReferenceScheduler.__name__ : ReferenceScheduler,
        RBRS.__name__ : RBRS,
        ABPolicy.__name__  : ABPolicy,
        RBPolicy.__name__: RBPolicy,
    }


    scheduler = schedulers["RBPolicy"](job, adj)
    start_time = datetime.datetime.now()

    Logger.debug("starting simulation...")
    result = simulate_schedule(scheduler)
    return result

i=1
def simulate_schedule(scheduler, stochastic=True):
    env = simpy.Environment()
    i=0

    def task_finished_callback(env):
        while scheduler.has_next():
                SimulationEntity(env, scheduler.get_next(), task_finished_callback, stochastic)

    while scheduler.has_next():
            SimulationEntity(env, scheduler.get_next(), task_finished_callback, stochastic)

    env.run()
    # Logger.info("Simulation successful. Simulated Time: %s" % env.now)
    result = SimulationResult()
    result.total_time = env.now
    result.set_execution_history(scheduler.get_execution_history())

    return result








