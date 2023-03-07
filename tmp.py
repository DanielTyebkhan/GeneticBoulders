
from util import load_pickle
from MapElites.tracking import ExperimentAggregator
from MapElites.ribs_interface import viz_archive

agg: ExperimentAggregator = load_pickle('/home/daniel/Downloads/FinalResults30-20230307T092953Z-001/FinalResults30/V4/aggregator.p')
logger = agg.get_loggers()[1]
last_archive = logger.archives[-1]
viz_archive(last_archive, '')