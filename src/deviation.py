
import utilities
import time

class Task_Obj:
    def __init__(self, task):
        self.task_name = task.name
        self.task_start_time = 0
        self.task_end_time = 0
        self.actions_complete_correctly = []
        self.actions_completed_incorrectly = []
        self.actions_remaining = []
        self.completed = False

class Task_Sequence:
    def __init__(self, initial_task):
        self.task_sequence = {}
        self.task_reference_sequence = []
        self.last_updated = 0
        self.action_sequence = []

        self.task_sequence[initial_task[0].name] = Task_Obj(initial_task[0])

    def update(self, current_task, task_validation_dict, action_sequence, params_validation_dict, onto_task, onto_domain, timestep): # This is called every time step

        # Which task does this task belong to?
        # Belongs to the following constraint

        while True:

            next_tasks = []
            task_completed = []
            for task in current_task:

                # Check if task is in the chain
                obj = next((val for key, val in self.task_sequence.items() if val.task_name == task.name), None)
                expected_next_tasks = onto_task.search(is_a=onto_task.Task, hasPreCondition=task)

                # Check the preconditions of the current task by using the task validation dict
                next_tasks_tmp = []
                for n_task in expected_next_tasks:
                    if task_validation_dict[n_task.name]:
                        next_tasks_tmp.append(n_task)
                        self.task_sequence[n_task.name] = Task_Obj(n_task)

                if len(next_tasks_tmp) != 0: # we have next tasks starting
                    task_completed.append(task)
                    # Update current task to be next_tasks
                    current_task_seq_obj = self.task_sequence[task.name]
                    current_task_seq_obj.task_end_time = timestep
                    next_tasks += next_tasks_tmp

            if len(next_tasks) != 0:
                current_task = next_tasks

            else:
                break


        print("we can process the actions now")

        # Check if any actions were performed

        self.last_updated = timestep



criticality_enum_dict ={0: 'No criticality',
                        1: 'Minor criticality',
                        2: 'Major criticality'}

tmp_action_criticality_dict = {'1':0,
                               '2':0,
                               '3':1,
                               '4':1,
                               '5':0,
                               '6':1,
                               '7':2,
                               '8':1,
                               '9':0,
                               '10':1,
                               '11':1,
                               '12':1,
                               '13':2,
                               '14':1,
                               '15':1,
                               '16':1,
                               '17':0,
                               '18':0,
                               '19':1,
                               '20':1,
                               '21':1}

tmp_task_dict = {'1001': ['1','2','3'],
                 '1002': ['4','5','6', '7', '8'],
                 '1003': ['9','10','11', '12'],
                 '1004': ['13','14'],
                 '1005': ['15','16','17'],
                 '1006': ['18','19','20'],
                 '1007': ['21'],}

tmp_task_phase = {'1001': ['1'],
                 '1002': ['2'],
                 '1003': ['2'],
                 '1004': ['3'],
                 '1005': ['3','4'],
                 '1006': ['4']}

tmp_attention_scores = {'1001': 5,
                        '1002': 6,
                        '1003': 4,
                        '1004': 7,
                        '1005': 9,
                        '1006': 5}

number_of_phases = 4

def annotate_tasks(action_sequence):

    annotated_output = []
    for action in action_sequence:
        for key,val in tmp_task_dict.items():
            if action in val:
                annotated_output.append(key)
                break

    return annotated_output


def align_tasks(annotated_ref_seq, annotated_pilot_seq):

    alignment1, alignment2, symbol, score = utilities.needle(annotated_ref_seq, annotated_pilot_seq)
    unique_symbols = list(dict.fromkeys(symbol))
    unique_symbols.remove(' ')

    # For the symbol variable, all the first spaces indicate a left shift of the sequence
    # This typically occurs when there are missing elements.
    # We will count these first in order to accurately compute the problematic indices
    shift_counter = 0
    for element in symbol:
        if element == ' ':
            shift_counter += 1
        else:
            break

    symbol_for_processing = symbol[shift_counter:]

    # We need to remove the spaces at the end too
    shift_counter = 0
    reverse_symbol = symbol.copy()
    reverse_symbol.reverse()
    for element in reverse_symbol:
        if element == ' ':
            shift_counter += 1
        else:
            break

    symbol_for_processing = symbol_for_processing[:len(symbol_for_processing) - shift_counter]

    indices_of_problematic_actions = [i for i, x in enumerate(symbol_for_processing) if x == ' ']



    return alignment1, alignment2, symbol, score, indices_of_problematic_actions, unique_symbols

def deviation_analysis(pilot_seq, ref_seq):
    start = time.time()
    # Seq 1 and 2 are going to be action sequences
    #pilot_seq1 = ['1', '2', '3', '5', '6', '13', '7', '14', '8', '16', '17', '15', '18', '19', '20']
    pilot_seq2 = ['1', '13', '14', '6', '2', '7', '3', '8', '16', '17', '15', '18', '19', '20', '21']
    ref_seq = ['1', '2', '3', '4', '5', '6', '7', '8', '13', '14', '15', '16', '17', '18', '19', '20']
    # pilot_seq2 = ['1', '13', '14', '6', '2', '7']
    # ref_seq = ['1', '2', '3', '4', '5', '6']

    pilot_seq = pilot_seq2

    # Annotate Tasks
    annotated_pilot_seq = annotate_tasks(pilot_seq)
    annotated_ref_seq = annotate_tasks(ref_seq)

    alignment1, alignment2, symbol, score, indices_of_problematic_actions, unique_symbols = align_tasks(annotated_ref_seq,annotated_pilot_seq)

    alignment1_unique = utilities.duplicate_removal(alignment1)
    alignment2_unique = utilities.duplicate_removal(alignment2)

    problematic_tasks1 = list(set(alignment1_unique).difference(unique_symbols))
    problematic_tasks2 = list(set(alignment2_unique).difference(unique_symbols))

    task_reference = list(filter(('-').__ne__, alignment1_unique))
    problematic_tasks1 = list(filter(('-').__ne__, problematic_tasks1))
    problematic_tasks2 = list(filter(('-').__ne__, problematic_tasks2))
    if len(problematic_tasks1) >= len(problematic_tasks2):
        problematic_tasks = problematic_tasks1
    else:
        problematic_tasks = problematic_tasks2

    action_issue_dict = {}
    # 1 = out of place
    # 2 = added
    # 3 = missing - ommission

    added_actions = list(set(pilot_seq).difference(ref_seq)) # Actions that have been added
    omitted_actions = list(set(ref_seq).difference(pilot_seq)) # Actions that have been ommitted
    for index in indices_of_problematic_actions:
        if pilot_seq[index] in ref_seq:
            action_issue_dict[pilot_seq[index]] = 1 # Action not in right place

    # Convert result_1 and result_2 to dictionary
    for action in added_actions:
        action_issue_dict[action] = 2
    for action in omitted_actions:
        action_issue_dict[action] = 3


    # Assess criticality of deviations
    criticality = 0
    for key, val in action_issue_dict.items():
        if tmp_action_criticality_dict[key] > criticality:
            criticality = tmp_action_criticality_dict[key]

    assessment = criticality_enum_dict[criticality]

    # Need to assess Task phase acceptability
    # Actions that are in the same phase can be done in any order in that phase unless otherwise dictated

    stop = time.time()
    print(f"")
    print(f"Reference Action Sequence: {ref_seq}")
    print(f"Pilot Action Sequence: {pilot_seq}")
    print(f"")
    print(f"Deviation Analysis")
    print(f"====================================================================================")
    print(f"Task Reference Alignment output: {task_reference}")
    print(f"Task Alignment output: {unique_symbols}")
    print(f"Problematic tasks found: {problematic_tasks}")
    print(f"Similarity score: {score}%")
    print(f"Process time: {stop - start} seconds")
    print(f"Actions found to be problematic: {[k for k,v in action_issue_dict.items() if v > 0]}")
    print(f"Actions found to be executed out of order in the sequence: {[k for k,v in action_issue_dict.items() if v == 1]}")
    print(f"Actions that have been incorrectly added to the sequence: {[k for k, v in action_issue_dict.items() if v == 2]}")
    print(f"Actions that have been incorrectly omitted from the sequence: {[k for k, v in action_issue_dict.items() if v == 3]}")
    print(f"Assessed Criticality of deviation: {assessment}")
    print(f"====================================================================================")

    return


