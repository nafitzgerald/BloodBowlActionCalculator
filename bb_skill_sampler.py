from enum import Enum
import random

ActionType = Enum('dodge', 'gfi', 'pro', 'pickup', 'loner')
TeamRerollStrategy = Enum('always', 'never', 'after_pro')
Skill = Enum('dodge', 'pro', 'loner', 'sure_hands', 'sure_feet')

class Action:
    def __init__(self, action_type, roll_required, trr_strat = TeamRerollStrategy.always):
        self.action_type = action_type
        self.roll_required = roll_required
        self.trr_strat = trr_strat

    def __str__(self):
        return "(%s, %s, %s)"%(self.action_type, self.roll_required, self.trr_strat)

    def __repr__(self):
        return self.__str__()

# Do one sample of a sequence of actions, given a player with a certain set of skills. Returns true if we
# successfully reach the end of the sequence, return false if we fail somewhere along the way.
def do_sequence(sequence, skills, has_trr, can_use_trr_next = True):
    sequence = list(sequence)
    skills = set(skills)
    if sequence == []:
        # We have successfully reached the end of the sequence
        return 1.0

    curr_action = sequence.pop(0)

    if not isinstance(curr_action, Action):
        raise Exception("Next action is not of type Action: " + curr_action)

    #Do a die roll for hte currect action. If sucessful, we can continue with the sequence.
    chance_of_success = float(6 - curr_action.roll_required + 1) / 6

    chance_after_success = do_sequence(sequence, skills, has_trr)

    # Use skills if we have them. Remove the skill from the set of skills (since it can no longer be used)
    # and repeat the sequence.
    if curr_action.action_type == ActionType.dodge and Skill.dodge in skills:
        chance_after_failure = resolve_skill(Skill.dodge, skills, sequence, curr_action, has_trr)
    elif curr_action.action_type == ActionType.gfi and Skill.sure_feet in skills:
        chance_after_failure = resolve_skill(Skill.sure_feet, skills, sequence, curr_action, has_trr)
    elif curr_action.action_type == ActionType.pickup and Skill.sure_hands in skills:
        chance_after_failure = resolve_skill(Skill.sure_hands, skills, sequence, curr_action, has_trr)

    # If we reach here we have failed the roll
    elif has_trr and can_use_trr_next and (curr_action.trr_strat == TeamRerollStrategy.always or (curr_action.trr_strat == TeamRerollStrategy.after_pro and not Skill.pro in skills)):
        # Attempting to use team reroll.
        sequence.insert(0, curr_action)

        # If the player is a Loner, add the loner check.
        if Skill.loner in skills:
            sequence.insert(0, Action(ActionType.loner, 4, TeamRerollStrategy.never))

        # Redo the sequence, minus the used team reroll.
        chance_after_failure = do_sequence(sequence, skills, False, can_use_trr_next = False)
    elif Skill.pro in skills and can_use_trr_next:
        # Add a pro-check before redoing the action check.
        sequence.insert(0, curr_action)
        sequence.insert(0, Action(ActionType.pro, 4, TeamRerollStrategy.always))
        skills.remove(Skill.pro)
        chance_after_failure = do_sequence(sequence, skills, has_trr, True)
    else:
        chance_after_failure = 0.0

    # If we reach here, we have failed the action with no additional recourse.
    return (chance_of_success * chance_after_success) + ((1 - chance_of_success) * chance_after_failure)

# Apply the free skill reroll by removing the skill (so it can't be used again),
# and adding the current action back to the start of the sequence. If there is a
# team reroll, it cannot be used on this next action.
def resolve_skill(skill, skills, sequence, curr_action, has_trr):
    skills.remove(skill)
    sequence.insert(0, curr_action)
    return do_sequence(sequence, skills, has_trr, False)

# Do N samples of a sequence, and return the percentage of success.
def sample_sequence(sequence, skills = set(), has_trr = False, N = 100000):


    successes = 0.0
    for i in xrange(N):
        curr_seq = list(sequence)
        if do_sequence(curr_seq, skills, has_trr):
            successes += 1
    return (successes / N) * 100
