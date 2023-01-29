from random import seed
from random import random

operations = {0: 'out of place', 1: 'removed', 2: 'added'}

class Sequence_Obj:
    def __init__(self, reference_sequence, scrambled_sequence):
        self.ref = reference_sequence
        self.scr = scrambled_sequence

class Mutation:
    def __init__(self, id, index, status):
        self.id = id
        self.index = index
        self.status = status
    def print(self):
        print(f"Mutation at index {self.index}, with id {self.id}, and status of: {operations[self.status]}")


def sequence_generator(sequence_length, number_of_sequences):
    # seed random number generator
    reference_sequence = []
    seed()
    for i in range(sequence_length):
        reference_sequence.append(int(random() * 100))

    scrambled_sequence,mutations = sequence_scrambler(reference_sequence, 0.7)
    print(reference_sequence)
    print(scrambled_sequence)
    for mutation in mutations:
        mutation.print()


def sequence_scrambler(sequence, mutation_ratio):
    # cycle through sequence of numbers and perform a mutation
    mutations = []
    new_sequence = sequence.copy()
    for i in range(len(sequence) - 1, 0, -1):
        if random() < mutation_ratio:
            # perform a mutation
            mutation_option = random()
            if mutation_option < 0.4:
                new_index = int(random() * (len(new_sequence) - 1))
                id = sequence[i]
                operation = 0
                new_sequence.insert(new_index, new_sequence.pop(i))
                mutation = Mutation(id, new_index + 1, operation)
                mutations.append(mutation)
                continue
            elif mutation_option >= 0.4 and mutation_option < 0.6:
                # Remove action from sequence
                id = sequence[i]
                operation = 1
                index = i
                new_sequence.pop(i)
                mutation = Mutation(id, index + 1, operation)
                mutations.append(mutation)
                continue
            elif mutation_option > 0.6:
                # Generate new action and insert it
                id = int(random() * 100)
                operation = 2
                index = i
                new_sequence.insert(i, id)
                mutation = Mutation(id, index + 1, operation)
                mutations.append(mutation)
                continue

    return new_sequence,mutations