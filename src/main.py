import cae_log_utils
from sequence_generation import sequence_generator

import ontology_utils
from pathlib import Path
from owlready2 import *

import deviation
ROOT_DIR = Path(__file__).parent.resolve()
ONT_DIR = ROOT_DIR / "ontology"



seq1 = [1, 2, 3, 4, 5]
seq2 = [2, 3, 4, 5, 6]
#
deviation.deviation_analysis(seq1, seq2)

onto_domain, onto_task = ontology_utils.load_ontologies(ONT_DIR) # Load the ontologies


cae_log_utils.generate_cae_log_dictionaries() # To generate the inverted ont2cae table
task_sequence, action_sequence = ontology_utils.get_task_chain_tasks(onto_task, onto_domain)

# list_of_actions = superclass.


print("Terminated.")


