from bb_skill_sampler import *
import string

def main():

    print "Team Reroll?\tDodge\tSure Hands\tSure Feet\tLoner\tPro\tTwo Heads\tExtra Arms\tPrehensize Tail (defender)\tBlizzard\tRain\tAgi\tBreak Tackle Strength"

    for trr in [True, False]:
        for dodge in [True, False]:
            for sure_hands in [True,False]:
                for sure_feet in [True, False]:
                    for agi in range(1,7):
                        for loner in [True, False]:
                            for pro in [True, False]:
                                for two_heads in [True, False]:
                                    for extra_arms in [True, False]:
                                        for prehensile_tail in [True, False]:
                                            for blizzard in [True, False]:
                                                for rain in [True, False]:
                                                    for break_tackle in xrange(0, 7):
                                                        if break_tackle > 0 and break_tackle <= agi:
                                                            continue
                                                        if rain and blizzard:
                                                            #impossible
                                                            continue

                                                        base_dodge = 7 - agi - 1
                                                        if two_heads:
                                                            base_dodge -= 1
                                                        if prehensile_tail:
                                                            base_dodge += 1

                                                        first_dodge = base_dodge - min(0, break_tackle - agi)

                                                        base_pickup = 7 - agi
                                                        if extra_arms:
                                                            base_pickup -= 1

                                                        if blizzard:
                                                            gfi = 3
                                                        else:
                                                            gfi = 2

                                                        skills = set()
                                                        if dodge:
                                                            skills.add(Skill.dodge)
                                                        if sure_hands:
                                                            skills.add(Skill.sure_hands)
                                                        if sure_feet:
                                                            skills.add(Skill.sure_feet)
                                                        if loner:
                                                            skills.add(Skill.loner)
                                                        if pro:
                                                            skills.add(Skill.pro)

                                                        sequenceA = []
                                                        sequenceA.append(Action(ActionType.dodge, first_dodge + 1))
                                                        sequenceA.append(Action(ActionType.pickup, base_pickup))
                                                        sequenceA.append(Action(ActionType.dodge, base_dodge))
                                                        seqA_chance = do_sequence(sequenceA, skills, trr)

                                                        sequenceB = []
                                                        sequenceB.append(Action(ActionType.dodge, first_dodge))
                                                        sequenceB.append(Action(ActionType.pickup, base_pickup))
                                                        sequenceB.append(Action(ActionType.dodge, base_dodge))
                                                        sequenceB.append(Action(ActionType.gfi, gfi))
                                                        seqB_chance = do_sequence(sequenceB, skills, trr)

                                                        ystrings = map(lambda x: "Y" if x else "N", [trr, dodge, sure_hands, sure_feet, loner, pro, two_heads, extra_arms, prehensile_tail, blizzard, rain])
                                                        print string.join(ystrings, '\t') + "\t%d\t%d\t%f\t%f"%(agi, break_tackle, seqA_chance, seqB_chance)




if __name__ == '__main__':
    main()
