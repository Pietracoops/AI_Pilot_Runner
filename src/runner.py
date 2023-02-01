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

        self.start_task = 1000
        self.current_task = 1000
        self.task_completion_dict = {} # contains key:task value:[bool started, bool completed]

        Runner.extract_yaml_objs(self, path_to_yaml)
        
        onto_domain, onto_task = ontology_utils.load_ontologies(path_to_ont, ont_names[0], ont_names[1]) # Load the ontologies
        self.onto_domain = onto_domain
        self.onto_task = onto_task
        # cae_log_utils.generate_cae_log_dictionaries() # To generate the inverted ont2cae table
        # task_sequence, action_sequence = ontology_utils.get_task_chain_tasks(onto_task, onto_domain)
        print("Runner Initialized")

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

    def check_task_constraints(self, task):
        # Check constraints
        task_obj = self.ont_extracted.task_list[task]
        return task_obj.validate_eval_criteria(self.sim_env_dict)

    def check_task_action(self, task):
        # Check action
        task_obj = self.ont_extracted.task_list[task]
        return task_obj.validate_action_criteria(self.sim_env_dict)

    def perform_ontology_tasks(self):

        if self.current_task == self.start_task and not self.current_task in self.task_completion_dict: # If current task is start task
            print(f"Starting first task: {self.current_task}")
            self.task_completion_dict[self.current_task] = [True, True] # Update task status to started and finished
            return


        if self.task_completion_dict[self.current_task][1] == True: # Check if current task bool is done
            # Cycle through the next tasks and check constraints
            next_tasks = self.ont_extracted.forward_condition_task_list[self.current_task]
            accepted_tasks = []
            for task in next_tasks:
                if Runner.check_task_constraints(self, task):
                    accepted_tasks.append(task)

            # Return the one and only task that could be executed next
            if len(accepted_tasks) > 1:
                print("more than 1 accepted next task")
            else:
                self.current_task = accepted_tasks[0] # Make it the current task

            print(f"Current task done, proceeding with task: {self.current_task}")
            # Start the task action
            task_obj = self.ont_extracted.task_list[self.current_task]
            task_action_dict = task_obj.actions
            for action, action_obj in task_action_dict.items():
                action_value = action_obj.exact_value
                action_parameter = action_obj.parameters
                print(f"Performing Action: {action_parameter} set to {action_value}")
                if action_parameter in self.ont_extracted.action_exclusion_list:
                    # We can't perform these types of actions like "Verbally Announcing takeoff"
                    self.task_completion_dict[self.current_task] = [True, True]
                else:
                    self.client.setDataRef(action_parameter, str(action_value)) # Perform the action
                    # Update task_completion_dict with task and started bool
                    # Started but not complete (need validation from environment)
                    self.task_completion_dict[self.current_task] = [True, False]

            return
        # Task done bool not updated yet
        if self.task_completion_dict[self.current_task][1] == False:
            # check environment value to see if matches action value
            if Runner.check_task_constraints(self, self.current_task):
                # Matches update done bool and return
                self.task_completion_dict[self.current_task] = [True, True]  # Started but not complete (need validation from environment)
            else:
                return # Does not match - return and wait for next iteration



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
            Runner.perform_ontology_tasks(self) # Perform task actions


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


