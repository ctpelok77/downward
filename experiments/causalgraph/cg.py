#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os

from lab.environments import LocalEnvironment, BaselSlurmEnvironment

import common_setup
from common_setup import IssueConfig, IssueExperiment



DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
BENCHMARKS_DIR = os.environ["DOWNWARD_BENCHMARKS"]
REVISIONS = ["causal_graph"]

CONFIGS = [
    IssueConfig("cg", ["--search", 'lazy_greedy([cg(),const(infinity)])'],
                driver_options=[]),
]

SUITE = common_setup.DEFAULT_OPTIMAL_SUITE
SUITE = IssueExperiment.DEFAULT_TEST_SUITE
ENVIRONMENT = LocalEnvironment(processes=48)

exp = common_setup.IssueExperiment(
    revisions=REVISIONS,
    configs=CONFIGS,
    environment=ENVIRONMENT,
)

exp.add_suite(BENCHMARKS_DIR, SUITE)

exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(exp.PLANNER_PARSER)
exp.add_parser(exp.SINGLE_SEARCH_PARSER)
exp.add_parser("cgparser.py")

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_fetcher(name="fetch")

exp.run_steps()

