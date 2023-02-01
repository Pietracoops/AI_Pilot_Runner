import src.cae_log_utils as cae_log_utils
import src.ontology_utils as ontology_utils
from src.sequence_generation import sequence_generator
import src.utilities as utilities
import yaml
import time

class Runner:
    nanos_to_sec = (10 ** -9)
    def __init__(self, path_to_ont, ont_names, path_to_yaml, api_client, frequency, verbosity):
        self.sim_env_dict = {}
        self.runner_stats_dict = {}
        self.client = api_client
        self.runner_frequency = 1/ frequency # Input received in hertz
        self.verbosity = verbosity
        self.ont_extracted = None

        Runner.extract_yaml_objs(self, path_to_yaml)
        print("Runner Initialized")
        onto_domain, onto_task = ontology_utils.load_ontologies(path_to_ont, ont_names[0], ont_names[1]) # Load the ontologies
        self.onto_domain = onto_domain
        self.onto_task = onto_task
        # cae_log_utils.generate_cae_log_dictionaries() # To generate the inverted ont2cae table
        # task_sequence, action_sequence = ontology_utils.get_task_chain_tasks(onto_task, onto_domain)

    def __del__(self):
        print("terminating runner")


    def extract_yaml_objs(self, path):
        # Load the YAML file
        with open(path, 'r') as file:
            data = yaml.safe_load(file)

        # Access the variables in the YAML file
        for key, value in data.items():
            self.sim_env_dict[key] = 0.0 # Init the environment dictionary

    def update_environment(self):
        for key in self.sim_env_dict.keys():
            self.sim_env_dict[key] = self.client.getDataRef(key)

    def display_runner_stats_dict(self):
        print(f"{self.runner_stats_dict}")

    def display_high_precision_runner_data(self, current_time, start_time_sec, end_time_sec, next_iter_time):
        print(f"Start time: {current_time - start_time_sec} \
| End time: {end_time_sec - start_time_sec} \
| Next Iter starting at: {next_iter_time - start_time_sec} \
| Sleeping for {next_iter_time - end_time_sec} \
| Percentage of interval used: \
{Runner.check_workframe_percentage(self, current_time, start_time_sec, end_time_sec, next_iter_time)}%")

    def check_workframe_percentage(self, current_time, start_time_sec, end_time_sec, next_iter_time):
        return (100 * ((end_time_sec - start_time_sec) - (current_time - start_time_sec)) / self.runner_frequency)

    def resume_at(self, next_iter_time):
        # We cannot use the time.sleep function because it is very slow and innacurate
        # By doing it this way, we can achieve a 0.001 second accuracy (vs the 0.16 second time.sleep accuracy)
        while(True):
            # Check current time
            current_time_sec = time.time_ns() * Runner.nanos_to_sec
            if current_time_sec > next_iter_time:
                break

    def build_ontology_hierarchy(self):
        self.ont_extracted = ontology_utils.build_ontology_hierarchy(self.onto_task)

    def run_simulation_loop(self):
        start_time_sec = time.time_ns() * Runner.nanos_to_sec
        next_iter_time = start_time_sec + self.runner_frequency
        self.runner_stats_dict["runner_heartbeat"] = 0
        while(True):
            # Start runner loop
            if self.runner_stats_dict["runner_heartbeat"] % 100 == 0:
                Runner.display_runner_stats_dict(self)

            current_time = time.time_ns() * Runner.nanos_to_sec
            self.runner_stats_dict["runner_heartbeat"] += 1
            self.runner_stats_dict["running_time"] = next_iter_time - start_time_sec

            # ============== Start Runner Work ===============
            Runner.update_environment(self) # Update the environment


            # ============== Stop Runner Work ================
            end_time_sec = time.time_ns() * Runner.nanos_to_sec
            self.runner_stats_dict["last_loop_work_time"] = end_time_sec - current_time

            if Runner.check_workframe_percentage(self, current_time, start_time_sec, end_time_sec, next_iter_time) > 100.0:
                print("Overrun Detected!")
                Runner.display_high_precision_runner_data(self, current_time, start_time_sec, end_time_sec,
                                                          next_iter_time)
            if self.verbosity > 0:
                Runner.display_high_precision_runner_data(self, current_time, start_time_sec, end_time_sec, next_iter_time)
            Runner.resume_at(self, next_iter_time)
            next_iter_time += self.runner_frequency
            # End runner loop


