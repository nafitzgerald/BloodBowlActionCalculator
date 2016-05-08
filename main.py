from bb_skill_sampler import *

def main():
    sequence = []
    sequence.append(Action(ActionType.dodge, 3))
    sequence.append(Action(ActionType.pickup, 4))
    sequence.append(Action(ActionType.dodge, 2))

    skills = set()
    skills.add(Skill.dodge)
    skills.add(Skill.pro)

    has_trr = True

    print do_sequence(sequence, skills = skills, has_trr = has_trr)

if __name__ == '__main__':
    main()
