from owlready2 import *
import processing
import pathlib
import cae_log_utils
import deviation


parameter_ont2xplane_scaling = {
               'SideStickPositionX': '(x-50.0)/50.0', # Units may be wrong
               'SideStickPositionY': '', # Units may be wrong
               'Engine1FireSwitch': '',
               'Engine2FireSwitch': '',
               'Engine2MasterSwitchPosition': '',
               'Engine1MasterSwitchPosition': '',
               'EGT': '',
               'AutoThrustMode': '',
               'AutoPilotMasterSwitch': '',
               'AltitudeMode': '',
               'Agent2Switch': '',
               'Agent1Switch': '',
               'ParkBrakePosition': '',
               'SpeedBrakeLeverPosition': '',
               'BrakeLeft': '', # There is left and right brake. I'll make a modification in the reference model
               'BrakeRight': '', # There is left and right brake. I'll make a modification in the reference model
               'LandingGearLeverPosition': '',
               'Speed': '',
               'SpeedTrend': '',
               'VSIIndicator': '',
               'VSIIndication': '',
               'RadioAltitude': '',
               'SpoilerMode': '',
               'TCASMode': '',
               'VisualIndication': '',
               'trimDirection': '',
               'MasterSwitchWarningSwitchPress': '',  # This is probably wrong
               'RadioTransmitting': '',
               'TailWind':'',
               'CrossWind':'',
               'VerballyAnnounce': '',
               'Engine1Failure': '',# this might not be accurate
               'Engine2Failure': '',# this might not be accurate
               'LandingGearPosition':'',
               'Airspeed':'',
               'LeftThrustLever':'', # This should be Engine1ThrustLever
               'RightThrustLever':'', # This should be Engine2ThrustLever
               'TimeInterval': '', # What is this!
               'FMAIndication': '',
               'FMSDirection': '',
               'Altitude':'',
               'FlapLever':'',
               'PFD': '',
               'TCASAlert': '',
               'RudderPedals':'', # This label was made up by me (units may also be wrong)
               'Pitch':'',
               'WindShearWarning':''
}

action_ont2xplane_dict = {
               'SideStickPositionX': 'a320/Panel/SidestickTakeoverL_button', # ok Units may be wrong
               'SideStickPositionY': 'a320/Panel/SidestickTakeoverR_button', # ok Units may be wrong
               'Engine1FireSwitch': 'a320/Overhead/FireEngine1_button', # ok
               'Engine2FireSwitch': 'a320/Overhead/FireEngine2_button',# ok
               'Engine2MasterSwitchPosition': 'a320/Pedestal/EngineMaster2_switch+',# ok
               'Engine1MasterSwitchPosition': 'a320/Pedestal/EngineMaster1_switch+',# ok
               'EGT': 'sim/aircraft/engine/acf_EGT_is_C', # ok
               'AutoThrustMode': 'a320/Panel/FCU_AutoThrust_button', # ok
               'AutoPilotMasterSwitch': 'a320/Panel/FCU_AutoPilot1_button', # ok
               'AltitudeMode': 'a320/Panel/FCU_AltitudeMode_switch_push', # ok
               'Agent2Switch': 'a320/Overhead/FireEngine1_Agent2_button', # ok
               'Agent1Switch': 'a320/Overhead/FireEngine1_Agent1_button', # ok
               'ParkBrakePosition': 'sim/flightmodel/controls/parkbrake', # ok
               'SpeedBrakeLeverPosition': 'a320/Panel/BrakeAuto1_button', # ok
               'BrakeLeft': 'sim/cockpit2/controls/left_brake_ratio', # There is left and right brake. I'll make a modification in the reference model # ok
               'BrakeRight': 'sim/cockpit2/controls/right_brake_ratio', # There is left and right brake. I'll make a modification in the reference model # ok
               'LandingGearLeverPosition': 'sim/cockpit2/controls/gear_handle_down', # ok
               'Speed': 'sim/flightmodel/position/indicated_airspeed', # ok
               'SpeedTrend': 'None_4', # Not sure what is that. I'm not using it in the refewrence model # ok
               'VSIIndicator': 'StandardAircraft/RateOfClimb', # What's the difference with the next dataref? # ok
               'VSIIndication': 'sim/cockpit/autopilot/vertical_velocity', # ok
               'RadioAltitude': 'sim/cockpit2/gauges/indicators/radio_altimeter_height_ft_pilot', # ok
               'SpoilerMode': 'None_6', # ok
               'TCASMode': 'sim/cockpit2/EFIS/EFIS_tcas_on', # ok
               'VisualIndication': 'None_7', # ok
               'trimDirection': 'sim/flightmodel2/controls/rudder_trim', # ok
               'MasterSwitchWarningSwitchPress': 'sim/cockpit/warnings/annunciator_test_pressed',  # This is probably wrong. When the alarm is on, this switch is used for stopping the alarm. # ok
               'RadioTransmitting': 'sim/atc/user_aircraft_transmitting', # This dataref is frequently used by the reference model. It detect when the pilot use it but not what he is saying. # ok
               'TailWind':'sim/weather/wind_speed_kt[0]', # ok
               'CrossWind':'sim/weather/wind_speed_kt[1]', # ok
               'VerballyAnnounce': 'None_10', # ok
               'Engine1Failure': 'sim/operation/failures/rel_engfai1',# this might not be accurate # ok
               'Engine2Failure': 'sim/operation/failures/rel_engfai2',# this might not be accurate # ok
               'LandingGearPosition':'sim/aircraft/prop/acf_prop_gear_rat', # ok
               'Airspeed':'sim/flightmodel/position/indicated_airspeed', # ok
               'LeftThrustLever':'sim/cockpit2/engine/actuators/throttle_ratio', # This should be Engine1ThrustLever # ok
               'RightThrustLever':'sim/cockpit2/engine/actuators/throttle_ratio', # This should be Engine2ThrustLever # ok
               'TimeInterval': 'None_11', # What is this! # ok
               'FMAIndication': 'None_12', # ok
               'FMSDirection': 'sim/cockpit/gyros/psi_ind_degm3', #  Not the vaccum. Important! # ok
               'Altitude':'sim/flightmodel/misc/h_ind', # No the ASL always! So it is the pressure altitude # ok
               'FlapLever':'sim/multiplayer/controls/flap_request', # ok
               'PFD': 'None_14', # ok
               'TCASAlert': 'sim/cockpit2/tcas/indicators/tcas_alert', # ok
               'RudderPedals':'sim/flightmodel2/wing/rudder1_deg', # This label was made up by me (units may also be wrong) # ok
               'Pitch':'sim/cockpit/gyros/the_vac_ind_deg', # Vaccum pitch is ok # ok
               'WindShearWarning':'sim/cockpit2/annunciators/windshear_warning' # ok
               }

action_xplane2ont_dict = {}

def load_ontologies(path, domain_ont_name, task_ont_name):
    onto_domain = get_ontology(str(path / domain_ont_name)).load()
    onto_task = get_ontology(str(path / task_ont_name)).load()
    print('Domain ontology loaded : ', onto_domain)
    print('Task ontology loaded : ', onto_task)
    return onto_domain, onto_task

def get_super_tasks(onto_task):
  list_of_individuals = list(onto_task.individuals())

  classes = []
  for i in list_of_individuals:
    try:
      if i.is_a[0] == onto_task.Task:
        classes.append(i.hasSuperTask[0])
    except:
      continue
  custom_set = set(classes)
  return custom_set



def get_task_chain_tasks(onto_task, onto_domain):

    cae_log_data_inputs = cae_log_utils.get_cae_log('1617239081361_R00000117_2.1.parquet', cae_log_utils.cae_log_inputs)
    cae_log_data_context = cae_log_utils.get_cae_log('1617239081361_R00000117_2.1.parquet', cae_log_utils.cae_log_context)
    cae_log_data_aircraft_state = cae_log_utils.get_cae_log('1617239081361_R00000117_2.1.parquet', cae_log_utils.cae_log_aircraft_state)

    length_of_log = len(cae_log_data_inputs)
    row = 2 # We start at 2
    actions_recorded = []
    executed_actions_dict = {}
    executed_tasks_dict = {}

    action_sequence_list = []

    initial_task = onto_task['1001']
    current_task = [initial_task]

    task_sequence_obj = deviation.Task_Sequence(current_task)
    while True:

        if row == length_of_log:
            # End of log
            break

        # Monitor inputs
        changed_input_vals_dict = cae_log_utils.get_changed_vals(row, cae_log_data_inputs, 0.1) # Changed Pilot inputs
        changed_context_vals_dict = cae_log_utils.get_changed_vals(row, cae_log_data_context, 0.1) # Changed Aircraft Context
        changed_aircraft_state = cae_log_utils.get_changed_vals(row, cae_log_data_aircraft_state, 0.1) # Changed Aircraft State

        #expected_next_task = find_tasks_with_pretask(onto_task, current_task.is_a, current_task.name) # Tasks containing current task as pretask
        all_tasks = find_all_tasks(onto_task, onto_task.Task) # Get all Tasks in ontology
        all_actions = find_all_tasks(onto_task, onto_task.Action) # Get all Actions in ontology

        current_data_inputs = cae_log_utils.get_current_data(row, cae_log_data_inputs)
        current_data_context = cae_log_utils.get_current_data(row, cae_log_data_context)
        current_data_aircraft_state = cae_log_utils.get_current_data(row, cae_log_data_aircraft_state)
        current_data_list = [current_data_inputs, current_data_context, current_data_aircraft_state]


        # Check which tasks are currently acceptable to be executed
        task_validation_dict = {}
        constraint_validation_dict = {}
        params_validation_dict = {}
        for task in all_tasks:
            result, constraints_evaluated_dict, tasks_evaluated_dict, params_evaluated_dict = get_task_validation(task, current_data_list, task_validation_dict, constraint_validation_dict, onto_task)
            task_validation_dict[task.name] = result
            task_validation_dict = {**task_validation_dict, **tasks_evaluated_dict}
            constraint_validation_dict = {**constraint_validation_dict, **constraints_evaluated_dict}
            params_validation_dict = {**params_validation_dict, **params_evaluated_dict}


        # If input action found, store it
        if len(changed_input_vals_dict) > 0:
            print("Input change detected")
            for changed_input, value in changed_input_vals_dict.items():
                # Map the action to an ontology action
                if changed_input in cae_log_utils.action_cae2ont_dict:
                    mapped_action = cae_log_utils.action_cae2ont_dict[changed_input]
                    action_combo = [mapped_action, value, row]
                    actions_recorded.append(action_combo)


        # Validate which actions have been executed up until this point in sequence (list of all possible actions)
        actions_this_sequence_dict = {}
        for action in all_actions:
            if action.name == 'Action':
                continue
            result = validate_action_execution(action, current_data_list, onto_task)
            actions_this_sequence_dict[action.name] = result

        # Loop through all actions
        # Add all executed actions into the chain at their given timestamp and add them to the  "Already_Executed"
        # Actions dict so that they don't get executed a second time
        # We only add actions that are not already executed
        for action, value in actions_this_sequence_dict.items():
            if value == True and not action in executed_actions_dict:
                action_sequence_list.append([action, value, row]) # Add task to sequence
                executed_actions_dict[action] = value



        # Process the Task Chain based on current execution of actions
        # Pilot Tasks Executed
        # 1) Annotate
        # 2) Align

        task_sequence_obj.update(current_task, task_validation_dict, actions_recorded, params_validation_dict, onto_task, onto_domain, row)


        # Process the expected Task Chain and expected actions
        # This is based on:
        # 1) the tasks that the ontology is expecting next
        # 2) Which task is approved to proceed next
        # 3) dump the actions of that of that task when either one of those tasks becomes true


        # Process the correlation between the two task chains or action chains based on ProM algorithm

        # Update live diagrams

        print(row)

        row += 1

    return task_sequence_obj.task_sequence, actions_recorded
    # Terminated the Log Processing


    


def validate_action_execution(action, current_data_list, onto_task):

    error_code = 0

    # If it is not an action skip it
    if action.is_a[0] != onto_task.Action:
        return True

    # Check for the action parameter
    action_param = action.hasActionParameter[0]
    if len(action.hasActionValue) == 0:
        return True
    else:
        action_value = action.hasActionValue[0]

    error_code, cae_val = cae_log_utils.get_cae_val_from_data(action_param.name, current_data_list)
    if error_code == 1:
        return False, None, None
    elif error_code == 2:
        print(f"Error occured in validate_action_execution cae_label for {action_param.name} "
              f"was not found in log columns")
        return False, None, None

    # Apply Scaling here
    scaling = eval(cae_log_utils.parameter_ont2cae_scaling[action_param.name])


    # We most likely need a delta value here to have an acceptable range (maybe another dict for this)
    scaled_action_value = (action_value * scaling)
    if cae_val != scaled_action_value: # This logic is temporary as it is not applicable for all actions
        return False, scaled_action_value, cae_val
    else:
        return True, scaled_action_value, cae_val

    # Returns if action was executed correctly

def find_all_tasks(onto_task, type):
    values = onto_task.search(is_a = type)
    #print(values)
    return values


def find_tasks_with_pretask(onto_task, type, pre_task_value):
    values = onto_task.search(is_a = type, hasPreCondition = onto_task[pre_task_value])
    return values


def find_tasks_with_constraint(onto_task, type, pre_task_value):
    values = onto_task.search(is_a=type, hasPreCondition=onto_task[pre_task_value])
    return values


class TaskObj:
    def __init__(self):
        self.id = None
        self.name = None
        self.number_of_actions = None
        self.number_of_constraints = None
        self.super_tasks = {}
        self.sub_tasks = {}
        self.constraints = {}
        self.actions = {}
        self.pre_condition = {}

class ConstraintObj:
    def __init__(self):
        self.id = None
        self.type = None
        self.constr_eval_criteria = {}
        self.task_eval_criteria = {}

class ActionObj:
    def __init__(self):
        self.id = None
        self.type = None
        self.eval_criteria = {}

class EvalCriteriaObj:
    def __init__(self):
        self.name = None
        self.exact_value = None
        self.min_value = None
        self.max_value = None

class ActionObj:
    def __init__(self):
        self.id = None
        self.name = None
        self.parameters = None
        self.exact_value = None
        self.min_value = None
        self.max_value = None
        self.comment = None


class OntoObj:
    def __init__(self, task_list):
        self.task_list = task_list
        self.forward_condition_task_list = {}  # Contains key:task, value:next task
        self.backward_condition_task_list = {} # Contains key:task, value:precondition task
        self.event_list = {}                   # Contains key:event, value:start task for event chain

        OntoObj.convert_task_constraints_to_preconditions(self)
        OntoObj.decompose_task_list(self)
        OntoObj.get_events_task_list(self)

        print("done")

    def decompose_task_list(self):
        # Build forward condition task
        for task, task_obj in self.task_list.items():
            if len(list(task_obj.pre_condition.keys())) != 0:
                self.backward_condition_task_list[task] = list(task_obj.pre_condition.keys())
            for precondition, precon_value in task_obj.pre_condition.items():
                if not precondition in self.forward_condition_task_list.keys():
                    tmp_array = [task]
                    self.forward_condition_task_list[precondition] = tmp_array
                else:
                    tmp_array = self.forward_condition_task_list[precondition]
                    tmp_array.append(task)
                    self.forward_condition_task_list[precondition] = tmp_array.copy()

    def get_events_task_list(self):
        for task, task_obj in self.task_list.items():
            if isinstance(task, str):
                self.event_list[task] = OntoObj.get_start_of_chain(self, task)


    def get_start_of_chain(self, task):
        cyclic_dict = {} # Use this to avoid cycles
        if isinstance(task, str):
            current_task = task
        else:
            current_task = task
        while(True):
            cyclic_dict[current_task] = 1
            if current_task in self.backward_condition_task_list:
                previous_task = current_task
                current_task = self.backward_condition_task_list[current_task]
            else:
                return current_task

            if isinstance(current_task, list) and len(current_task) != 0:
                current_task = current_task[0]

            if current_task in cyclic_dict:
                return previous_task

    def convert_task_constraints_to_preconditions(self):
        for task_id, task_obj in self.task_list.items():
            for constraint_id, constraint_obj in task_obj.constraints.items():
                if len(list(constraint_obj.task_eval_criteria.keys())) != 0:
                    for key in constraint_obj.task_eval_criteria.keys():
                        task_obj.pre_condition[key] = 1
                    self.task_list[task_id] = task_obj # Update the object


def build_ontology_hierarchy(onto_task):
    print("Building Ontology Hierarchy: Started...")
    start = time.time()
    all_tasks = find_all_tasks(onto_task, onto_task.Task) # Get all Tasks in ontology
    #all_actions = find_all_tasks(onto_task, onto_task.Action) # Get all Actions in ontology

    tasks_dict = {}
    for task in all_tasks: # Loop through all tasks
        task_obj = get_task_object(task, onto_task)
        if task_obj != None:
            tasks_dict[task_obj.id] = task_obj

    onto_obj = OntoObj(tasks_dict)
    end = time.time()
    print(f"Building Ontology Hierarchy: Complete : {end - start} seconds")
    return onto_obj
def get_task_object(task, onto_task):

    # if task.name =="1003":
    #     print("hello")

    if task.name == "Task" or not hasattr(task,'hasConstraint'):
        return None # Return, we dont want to process these

    task_obj = TaskObj() # Create the empty task object
    if len(task.hasTaskID) != 0:
        task_obj.id = task.hasTaskID[0]
    else:
        task_obj.id = task.name

    if len(task.hasNbAction) != 0:
        task_obj.number_of_actions = task.hasNbAction[0]
    if len(task.hasNbConstraint) != 0:
        task_obj.number_of_constraints = task.hasNbConstraint[0]

    subtask = task.hasSubtask
    subtask_dict = {}
    for _task in subtask:
        subtask_dict[_task.hasTaskID[0]] = 1

    supertask = task.hasSuperTask
    supertask_dict = {}
    for _task in supertask:
        supertask_dict[_task.name] = 1

    precond = task.hasPreCondition
    precond_dict = {}
    for _task in precond:
        if len(_task.hasTaskID) != 0:
            precond_dict[_task.hasTaskID[0]] = 1
        elif len(_task.hasConstraintID) != 0:
            precond_dict[_task.hasConstraintID[0]] = 1


    task_obj.sub_tasks = subtask_dict
    task_obj.super_tasks = supertask_dict
    task_obj.pre_condition = precond_dict

    task_obj.actions = get_task_actions(task, onto_task)
    task_obj.constraints = get_task_constraints(task, onto_task)

    return task_obj


def get_task_actions(task, onto_task):
    actions_dict = {}

    actions = task.hasAction

    if len(task.hasAction) == 0:
        return actions_dict

    for action in actions:
        action_obj = ActionObj()
        if len(action.hasActionID) != 0:
            action_obj.id = action.hasActionID[0]
        if len(action.hasActionValue) != 0:
            action_obj.exact_value = action.hasActionValue[0]
        if len(action.comment) != 0:
            action_obj.comment = action.comment[0]

        action_params = action.hasActionParameter
        for param in action_params:
            action_obj.parameters = param.name

        actions_dict[action_obj.id] = action_obj

    return actions_dict

def get_task_constraints(task, onto_task):

    constraints_dict = {}
    constraints = task.hasConstraint

    if len(task.hasConstraint) == 0:
        return constraints_dict

    for constraint in constraints:
        # Create Objects
        eval_dict = {}
        task_dict = {}
        # if constraint.is_a[0] == onto_task.Constraint:
        #     constraint_obj = ConstraintObj(constraint.hasConstraintID[0], constraint.hasConstraintType[0])
        if constraint.is_a[0] == onto_task.Task:
            task_obj = get_task_object(constraint, onto_task)
            task_dict[task_obj.id] = task_obj
            continue

        constraint_obj = ConstraintObj()
        if len(constraint.hasConstraintID) != 0:
            constraint_obj.id = constraint.hasConstraintID[0]
        if len(constraint.hasConstraintType) != 0:
            constraint_obj.type = constraint.hasConstraintType[0]

        # Find the Evaluation criteria list
        constraint_eval = constraint.hasEvaluationCriteria

        # Loop through each evaluation Criteria
        sub_constraints_dict = {}
        for eval in constraint_eval:

            if eval.is_a[0] != onto_task.Constraint and eval.is_a[0] != onto_task.Task:
                eval_constraint_obj = EvalCriteriaObj()

                if len(constraint.hasMinValue) != 0 and len(constraint.hasMaxValue) != 0:
                    eval_constraint_obj.min_value = constraint.hasMinValue[0]
                    eval_constraint_obj.max_value = constraint.hasMaxValue[0]
                elif len(constraint.hasMinValue) != 0 and len(constraint.hasMaxValue) == 0:
                    eval_constraint_obj.min_value = constraint.hasMinValue[0]
                elif len(constraint.hasExactValue) != 0:
                    eval_constraint_obj.exact_value = constraint.hasExactValue[0]

                eval_constraint_obj.name = eval.name
                eval_dict[eval_constraint_obj.name] = eval_constraint_obj # Add it to the dict

            # constraint could also be a list of tasks, if so we need to recursively call this function
            if eval.is_a[0] == onto_task.Task:
                task_dict[eval.hasTaskID[0]] = 1

            if eval.is_a[0] == onto_task.Constraint:
                tmp_constraints_dict = get_task_constraints(eval, onto_task)
                sub_constraints_dict = {**sub_constraints_dict, **tmp_constraints_dict} # Merge both dicts together

        constraint_obj.constr_eval_criteria = eval_dict
        constraint_obj.task_eval_criteria = task_dict
        constraints_dict[constraint_obj.id] = constraint_obj

        constraints_dict = {**constraints_dict, **sub_constraints_dict} # Merge both dicts together

    return constraints_dict


def get_task_validation(task, current_data_list, all_task_validation_dict, all_constraint_validation_dict, onto_task):
    # Get list of all constraints for next task
    constraints_evaluated_dict = {}
    tasks_evaluated_dict = {}
    params_evaluated_dict = {}

    if task.name in all_task_validation_dict or task.name == "Task" or not hasattr(task,'hasConstraint'):
        return True, constraints_evaluated_dict, tasks_evaluated_dict, params_evaluated_dict # Return, we dont want to process these

    if len(task.hasConstraint) != 0: # if no constraints, we make it true and exit

        error_code, constraints_evaluated_dict, tasks_evaluated_dict, params_evaluated_dict, labels_missing =  get_constraint_validation(task.hasConstraint, current_data_list, all_task_validation_dict, all_constraint_validation_dict, onto_task)
        if error_code == 1: # they are Tasks not constraints
            print(f"Error in get_constraint_validation with task {task.name}. Label not found or is mapped to 'None' in action_ont2cae_dict: {labels_missing.keys()}")
    else:
        return True, constraints_evaluated_dict, tasks_evaluated_dict, params_evaluated_dict
        
    # Validate if the task can be executed
    # If all evaluated constraints and tasks passed then we return true
    constraint_result = check_task_valid(constraints_evaluated_dict)
    task_result = check_task_valid(tasks_evaluated_dict)
    if constraint_result and task_result:
        result = True
    else:
        result = False

    return result, tasks_evaluated_dict, constraints_evaluated_dict, params_evaluated_dict

def get_constraint_validation(constraints, current_data_list, all_task_validation_dict, all_constraint_validation_dict, onto_task):
    
    error_code = 0
    constraints_evaluated_dict = {}
    tasks_evaluated_dict = {}
    params_evaluated_dict = {}
    labels_missing = {}

    for constraint in constraints:
        
        # Get Evaluation criteria
        constraint_eval = constraint.hasEvaluationCriteria

        # Loop through each evaluation Criteria
        for eval in constraint_eval:

            # constraint could also be a list of tasks, if so we need to recursively call this function
            if eval.is_a[0] == onto_task.Task:
                
                result, constraints_evaluated_dict_tmp, tasks_evaluated_dict_tmp, params_evaluated_dict_tmp = get_task_validation(eval, current_data_list, all_task_validation_dict, all_constraint_validation_dict, onto_task)
                tasks_evaluated_dict[eval.name] = result # add the task to the evaluated task dictionary
                tasks_evaluated_dict = {**tasks_evaluated_dict, **tasks_evaluated_dict_tmp}
                constraints_evaluated_dict = {**constraints_evaluated_dict, **constraints_evaluated_dict_tmp}
                params_evaluated_dict = {**params_evaluated_dict, **params_evaluated_dict_tmp}
                continue
                
            # Constraint could also have a list of more Constraints, if so we need to recursively call this function
            if isinstance(eval, list) and eval[0].is_a[0] == onto_task.Constraint:
                result, constraints_evaluated_dict_tmp, tasks_evaluated_dict_tmp, params_evaluated_dict_tmp = get_constraint_validation(eval, current_data_list, all_task_validation_dict, all_constraint_validation_dict, onto_task)
                constraints_evaluated_dict[constraint.name] = result # add the task to the evaluated task dictionary
                tasks_evaluated_dict = {**tasks_evaluated_dict, **tasks_evaluated_dict_tmp}
                constraints_evaluated_dict = {**constraints_evaluated_dict, **constraints_evaluated_dict_tmp}
                params_evaluated_dict = {**params_evaluated_dict, **params_evaluated_dict_tmp}
                continue

            # # This is a temporary bug fix
            if eval.is_a[0] == onto_task.Constraint:
                result, params_evaluated_dict_tmp, labels_missing_tmp = check_eval_valid(eval.hasEvaluationCriteria[0], eval, constraints_evaluated_dict,
                                                              all_constraint_validation_dict, current_data_list)
                constraints_evaluated_dict[constraint.name] = result
                labels_missing = {**labels_missing, **labels_missing_tmp}
                params_evaluated_dict = {**params_evaluated_dict, **params_evaluated_dict_tmp}

            else:
                result, params_evaluated_dict_tmp, labels_missing_tmp = check_eval_valid(eval, constraint, constraints_evaluated_dict,
                                                              all_constraint_validation_dict, current_data_list)
                constraints_evaluated_dict[constraint.name] = result
                labels_missing = {**labels_missing, **labels_missing_tmp}
                params_evaluated_dict = {**params_evaluated_dict, **params_evaluated_dict_tmp}

    
    return error_code, constraints_evaluated_dict, tasks_evaluated_dict, params_evaluated_dict, labels_missing


def check_eval_valid(eval, constraint, constraints_evaluated_dict, all_constraint_validation_dict, current_data_list):

    labels_missing = {}
    params_evaluated_dict = {}
    constraint_eval_name = eval.name

    # Check if constrain already in constraint_validation
    if constraint_eval_name in all_constraint_validation_dict:
        return all_constraint_validation_dict[constraint_eval_name], labels_missing
    # If we already processed it this run then we proceed
    if constraint_eval_name in constraints_evaluated_dict:
        return constraints_evaluated_dict[constraint_eval_name], labels_missing

    # Begin Processing the constraint
    # Get CAE Value from data slice
    error_code, cae_value = cae_log_utils.get_cae_val_from_data(constraint_eval_name, current_data_list)
    if error_code == 1:
        params_evaluated_dict[constraint_eval_name + "_" + constraint.name] = get_constraint_min_max_exact_values(constraint)
        return True, params_evaluated_dict, labels_missing
    elif error_code == 2:
        params_evaluated_dict[constraint_eval_name + "_" + constraint.name] = get_constraint_min_max_exact_values(constraint)
        labels_missing[constraint_eval_name] = True
        print(f"Error occured in get_cae_val_from_data cae_label for {constraint_eval_name} "
              f"was not found in log columns")
        return True, params_evaluated_dict, labels_missing

    # Check constraint validation
    error_code, result = check_constraint_valid(constraint, cae_value)
    if error_code == 1:
        print(f"Error in check_constraint_valid with constraint {constraint.name}")
        params_evaluated_dict[constraint_eval_name + "_" + constraint.name] = get_constraint_min_max_exact_values(constraint)
        return result, params_evaluated_dict, labels_missing
    else:
        params_evaluated_dict[constraint_eval_name + "_" + constraint.name] = get_constraint_min_max_exact_values(constraint)
        return result, params_evaluated_dict, labels_missing


def check_task_valid(validation_dict):

    # If validation_dict is empty then it is true
    if len(validation_dict) == 0:
        return True

    # Validate if the task can be executed
    first_value = list(validation_dict.values())[0]
    all_equal = list(validation_dict.values()).count(first_value) == len(validation_dict)
    if (first_value == True and all_equal == True):
        return True
    else:
        return False

def check_constraint_valid(constraint, value):

    error_code = 0 # 0 = no error; 1 = error occured
    constraint_name = constraint.name
    # Validate Value from constraints
    if len(constraint.hasMinValue) != 0 and len(constraint.hasMaxValue) != 0:
        constraint_min = constraint.hasMinValue[0]
        constraint_max = constraint.hasMaxValue[0]
        if value >= constraint_min and value < constraint_max:
            return error_code, True
        else:
            return error_code, False
    elif len(constraint.hasMinValue) != 0 and len(constraint.hasMaxValue) == 0:
        constraint_min = constraint.hasMinValue[0]
        try:
            if value >= constraint_min:
                return error_code, True
            else:
                return error_code, False
        except:
            return False
    elif len(constraint.hasExactValue) != 0:
        constraint_val = constraint.hasExactValue[0]
        if value == constraint_val:
            return error_code, True
        else:
            return error_code, False
    else:
        return error_code, False

def get_constraint_min_max_exact_values(constraint):
    
    error_code = 0 # 0 = no error; 1 = error occured
    constraint_name = constraint.name
    # Validate Value from constraints
    if len(constraint.hasMinValue) != 0 and len(constraint.hasMaxValue) != 0:
        constraint_min = constraint.hasMinValue[0]
        constraint_max = constraint.hasMaxValue[0]

        return [constraint_name, constraint_min, constraint_max, None]
    elif len(constraint.hasMinValue) != 0 and len(constraint.hasMaxValue) == 0:
        constraint_min = constraint.hasMinValue[0]
        return [constraint_name, constraint_min, None, None]
    elif len(constraint.hasExactValue) != 0:
        constraint_val = constraint.hasExactValue[0]
        return [constraint_name, None, None, constraint_val]
    else:
        return [constraint_name, None, None, None]


    # First we grab all the tasks from the super tasks
    # There are currently 5 superclasses
    # 1) Takeoff
    # 2) TCAS_event
    # 3) Rejected_takeoff
    # 4) Reactive_windshear
    # 5) Engine_failure_after_V1

    # superclass_Takeoff = onto_task.Takeoff
    # superclass_TCAS_event = onto_task.TCAS_event
    # superclass_Rejected_takeoff = onto_task.Rejected_takeoff
    # superclass_Reactive_windshear = onto_task.Reactive_windshear
    # superclass_Engine_failure_after_V1 = onto_task.Engine_failure_after_V1
    #
    # # We will work our way backwards, find all actions with
    #
    # actions_Takeoff =  superclass_Takeoff.hasSubtask
    # actions_TCAS_event =  superclass_TCAS_event.hasSubtask
    # actions_Rejected_takeoff =  superclass_Rejected_takeoff.hasSubtask
    # actions_Reactive_windshear =  superclass_Reactive_windshear.hasSubtask
    # actions_Engine_failure_after_V1 =  superclass_Engine_failure_after_V1.hasSubtask
    #
    #
    # superclass_list = [actions_Takeoff,
    #                    actions_TCAS_event,
    #                    actions_Rejected_takeoff,
    #                    actions_Reactive_windshear,
    #                    actions_Engine_failure_after_V1]
    #
    #
    # list_actions = []
    # for superclass in superclass_list:
    #   for action in superclass:
    #     for item in action.hasPreCondition:
    #       list_actions.append(item)

    # custom_set = set(list_actions)
    # custom_set = list(custom_set)
    # custom_set = sorted(custom_set)