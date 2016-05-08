from bb_skill_sampler import *

def main():
    sequence = []
    sequence.append(Action(ActionType.dodge, 2))
    sequence.append(Action(ActionType.pickup, 4))
    sequence.append(Action(ActionType.dodge, 2))
    sequence.append(Action(ActionType.gfi, 2))

    skills = set()

    has_trr = True

    print sample_sequence(sequence, skills = skills, has_trr = has_trr)

if __name__ == '__main__':
    main()
