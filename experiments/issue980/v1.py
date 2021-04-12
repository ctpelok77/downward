#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

from lab.environments import LocalEnvironment, BaselSlurmEnvironment

import common_setup
from common_setup import IssueConfig, IssueExperiment
#from relativescatter import RelativeScatterPlotReport
from itertools import combinations

DIR = os.path.dirname(os.path.abspath(__file__))
BENCHMARKS_DIR = os.environ["DOWNWARD_BENCHMARKS"]
# These revisions are all tag experimental branches off the same revision.
# we only need different tags so lab creates separate build directories in the build cache.
# We then manually recompile the code in the build cache with the correct settings.
REVISIONS = ["issue980"]
CONFIGS = [
    IssueConfig("blind", ["--search", "astar(blind())"]),
    IssueConfig("shortest-blind", ["--search", "myastar(blind())"]),
    IssueConfig("lmcut", ["--search", "astar(lmcut())"]),
    IssueConfig("shortest-lmcut", ["--search", "myastar(lmcut())"]),
]
SUITE = common_setup.DEFAULT_OPTIMAL_SUITE
ENVIRONMENT = LocalEnvironment(processes=48)

exp = IssueExperiment(
    revisions=REVISIONS,
    configs=CONFIGS,
    environment=ENVIRONMENT,
)
exp.add_suite(BENCHMARKS_DIR, SUITE)

exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(exp.TRANSLATOR_PARSER)
exp.add_parser(exp.SINGLE_SEARCH_PARSER)
exp.add_parser(exp.PLANNER_PARSER)

exp.add_step('build', exp.build)
exp.add_step('start', exp.start_runs)
exp.add_fetcher(name='fetch')

attributes = (
            IssueExperiment.DEFAULT_TABLE_ATTRIBUTES + ["plan_length"])
exp.add_absolute_report_step(attributes=attributes)
#exp.add_comparison_table_step(attributes=attributes)


#exp.add_comparison_table_step()
"""
for r1, r2 in combinations(REVISIONS, 2):
    for nick in ["opcount-seq-lmcut", "diverse-potentials", "optimal-lmcount"]:
        exp.add_report(RelativeScatterPlotReport(
            attributes=["total_time"],
            filter_algorithm=["%s-%s" % (r, nick) for r in [r1, r2]],
            get_category=lambda run1, run2: run1["domain"]),
            outfile="issue925-v1-total-time-%s-%s-%s.png" % (r1, r2, nick))
"""
exp.run_steps()
