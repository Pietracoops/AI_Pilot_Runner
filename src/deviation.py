
import utilities
import time


## Alignment Functions
# Python implementation to Smith-Waterman Algorithm
# zeros() was origianlly from NumPy.
# This version is implemented by alevchuk 2011-04-10
# https://github.com/alevchuk/pairwise-alignment-in-python
def zeros(shape):
    retval = []
    for x in range(shape[0]):
        retval.append([])
        for y in range(shape[1]):
            retval[-1].append(0)
    return retval


match_award = 10
mismatch_penalty = -5
gap_penalty = -5  # both for opening and extanding


def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty


def finalize(align1, align2, verbosity=0):
    align1 = align1[::-1]  # reverse sequence 1
    align2 = align2[::-1]  # reverse sequence 2

    i, j = 0, 0

    # calcuate identity, score and aligned sequeces
    symbol = []
    found = 0
    score = 0
    identity = 0
    for i in range(0, len(align1)):
        # if two AAs are the same, then output the letter
        if align1[i] == align2[i]:
            symbol.append(align1[i])
            identity = identity + 1
            score += match_score(align1[i], align2[i])

        # if they are not identical and none of them is gap
        elif align1[i] != align2[i] and align1[i] != '-' and align2[i] != '-':
            score += match_score(align1[i], align2[i])
            symbol.append(' ')
            found = 0

        # if one of them is a gap, output a space
        elif align1[i] == '-' or align2[i] == '-':
            symbol.append(' ')
            score += gap_penalty

    identity = float(identity) / len(align1) * 100

    if verbosity == 1:
        print('Identity =', "%3.3f" % identity, 'percent')
        print('Score =', score)
        print(align1)
        print(symbol)
        print(align2)

    return align1, align2, symbol, identity


def needle(seq1, seq2):
    m, n = len(seq1), len(seq2)  # length of two sequences

    # Generate DP table and traceback path pointer matrix
    score = zeros((m + 1, n + 1))  # the DP table

    # Calculate DP table
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = score[i - 1][j - 1] + match_score(seq1[i - 1], seq2[j - 1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            score[i][j] = max(match, delete, insert)

    # Traceback and compute the alignment
    align1, align2 = [], []
    i, j = m, n  # start from the bottom right cell
    while i > 0 and j > 0:  # end toching the top or the left edge
        score_current = score[i][j]
        score_diagonal = score[i - 1][j - 1]
        score_up = score[i][j - 1]
        score_left = score[i - 1][j]

        if score_current == score_diagonal + match_score(seq1[i - 1], seq2[j - 1]):
            align1.append(seq1[i - 1])
            align2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1.append(seq1[i - 1])
            align2.append('-')
            i -= 1
        elif score_current == score_up + gap_penalty:
            align1 += '-'
            align2.append(seq2[j - 1])
            j -= 1

    # Finish tracing up to the top left cell
    while i > 0:
        align1.append(seq1[i - 1])
        align2.append('-')
        i -= 1
    while j > 0:
        align1.append('-')
        align2.append(seq2[j - 1])
        j -= 1

    return finalize(align1, align2)

## ========== Alignment Functions End ================



criticality_enum_dict ={0: 'No Gravity',
                        1: 'Minor Gravity',
                        2: 'Major Gravity'}

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


class DeviationModel:
    def __init__(self, task_dict, gravity_dict):
        self.task_dict = task_dict
        self.gravity_dict = gravity_dict
    def annotate_tasks(self, action_sequence):

        annotated_output = []
        for action in action_sequence:
            for key,val in tmp_task_dict.items():
                if action in val:
                    annotated_output.append(key)
                    break

        return annotated_output


    def align_tasks(self, annotated_ref_seq, annotated_pilot_seq):

        alignment1, alignment2, symbol, score = needle(annotated_ref_seq, annotated_pilot_seq)
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

    def deviation_analysis(self, pilot_seq, ref_seq):
        start = time.time()
        # Seq 1 and 2 are going to be action sequences
        #pilot_seq1 = ['1', '2', '3', '5', '6', '13', '7', '14', '8', '16', '17', '15', '18', '19', '20']
        pilot_seq2 = ['1', '13', '14', '6', '2', '7', '3', '8', '16', '17', '15', '18', '19', '20', '21']
        ref_seq = ['1', '2', '3', '4', '5', '6', '7', '8', '13', '14', '15', '16', '17', '18', '19', '20']
        # pilot_seq2 = ['1', '13', '14', '6', '2', '7']
        # ref_seq = ['1', '2', '3', '4', '5', '6']

        pilot_seq = pilot_seq2

        # Annotate Tasks
        annotated_pilot_seq = DeviationModel.annotate_tasks(self, pilot_seq)
        annotated_ref_seq = DeviationModel.annotate_tasks(self, ref_seq)

        alignment1, alignment2, symbol, score, indices_of_problematic_actions, unique_symbols =\
            DeviationModel.align_tasks(self, annotated_ref_seq,annotated_pilot_seq)

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
            if self.gravity_dict[key] > criticality:
                criticality = self.gravity_dict[key]

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


