import random
import statistics
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
from os import system

system('clear')

simulations = 10000

attack = input('Attack? (y/n): ')
if attack.lower() == 'y':
    attack = True
else:
    attack = False

my_sides = int(input('Your #sides (6 or 8): '))
my_mods_initial = int(input('Your #mods: '))

their_sides = int(input('Their #sides (6 or 8): '))
their_mods_initial = int(input('Their #mods: '))





def play_risk(attack, my_sides, their_sides, my_mods, their_mods):

    # randomise rolls depending on number of mods
    my_rolls = []
    if my_mods > 2 and attack:
        for i in range(3):
            my_rolls.append(random.choice((range(1, my_sides + 1 ))))  # the random dice throws I throw, length 1 to 3
    elif my_mods < 3 and attack:
        for i in range(my_mods):
            my_rolls.append(random.choice((range(1, my_sides + 1 ))))  # the random dice throws I throw, length 1 to 3
    elif my_mods > 2 and not attack:
        for i in range(2):
            my_rolls.append(random.choice((range(1, my_sides + 1 ))))  # the random dice throws I throw, length 1 to 3
    elif my_mods < 3 and not attack:
        for i in range(my_mods):
            my_rolls.append(random.choice((range(1, my_sides + 1 ))))  # the random dice throws I throw, length 1 to 3


    # randomise rolls depending on number of mods
    their_rolls = []
    if their_mods > 2 and not attack:
        for i in range(3):
            their_rolls.append(random.choice((range(1, their_sides + 1 ))))  # the random dice throws they throw, length 1 to 3
    elif their_mods < 3 and not attack:
        for i in range(their_mods):
            their_rolls.append(random.choice((range(1, their_sides + 1 ))))  # the random dice throws they throw, length 1 to 3
    elif their_mods > 2 and attack:
        for i in range(2):
            their_rolls.append(random.choice((range(1, their_sides + 1 ))))  # the random dice throws they throw, length 1 to 3
    elif their_mods < 3 and attack:
        for i in range(their_mods):
            their_rolls.append(random.choice((range(1, their_sides + 1 ))))  # the random dice throws they throw, length 1 to 3


    # order the rolls in ascending order
    my_rolls.sort()
    their_rolls.sort()

    #print(my_rolls, their_rolls)

    record = []  # to keep track of who wins
    for i in list(min([my_rolls, their_rolls], key=len)):  # loop for whoever has the smaller number of dice
        record.append(who_higher(my_rolls, their_rolls, attack))   # function to compare 2 die
        del my_rolls[-1]   # remove that compared dice
        del their_rolls[-1]# remove that compared dice

    #print(my_rolls, their_rolls, record)

    #print(record)
    # whoever wins each toss, remove a mod from their army
    for i in range(len(record)):

        if record[i] == 1:
            their_mods -= 1
        if record[i] == 0:
            my_mods -= 1

    # the round finishes
    # record is a list showing who wins that particular set of rolls (so either length 1 or length 2)

    if my_mods <= 0:
        my_mods = 0
    if their_mods <= 0:
        their_mods = 0

    return record, my_mods, their_mods





# for set of rolls, decide the winnder
def who_higher(my_rolls, their_rolls, attack):

    if attack:
        if my_rolls[-1] > their_rolls[-1]:
            return 1
        else:
            return 0

    if not attack:
        if my_rolls[-1] >= their_rolls[-1]:
            return 1
        else:
            return 0






def simulate(simulations, my_mods_initial, their_mods_initial, attack, my_sides, their_sides):
    # play risk as many times as we wanto simulate. Hgher simulations = more accurate results
    ls = []
    for _ in range(simulations):
        #reinitialise original number of mods
        my_mods = my_mods_initial
        their_mods = their_mods_initial

        while my_mods > 0 and their_mods > 0:
            record, my_mods, their_mods = play_risk(attack, my_sides, their_sides, my_mods, their_mods)
            #the final record will be a singe [1] or [0], indicating a final win or loss
        ls.append(record)

    ls = sum(ls,[]) # add together all recorded wins / losses

    return 100 * ls.count(1) / len(ls)






chance = simulate(simulations, my_mods_initial, their_mods_initial, attack, my_sides, their_sides)   # overall chance of success 0 - 100

print( "\nThe chance of you winning is " + str(round( chance, 1 )) + "% based on " + str(simulations) + " games. Continuing...")


# Plotting the results
fig, ax = plt.subplots(1, 1, figsize=(12, 10))
x = list(range(1,30))  # attacking with up to 25 mods
y = []
for my_mods_initial in x:
    y.append(simulate(simulations, my_mods_initial, their_mods_initial, attack, my_sides, their_sides))

xnew = np.linspace(min(x), max(x), 300)
spl = make_interp_spline(x, y, k=3)  # type: BSpline
y_smooth = spl(xnew)

for i,x_val in enumerate(list(xnew)):

    if list(y_smooth)[i] > 50:
        print("The number of initial mods to have a > 50% chance winning = " + str(int(x_val)))
        break

for i,x_val in enumerate(list(xnew)):

    if list(y_smooth)[i] > 90:
        print("The number of initial mods to have a > 90% chance winning = " + str(int(x_val)) + "\n" )
        break


ax.plot(x, y, lw=2)
ax.set_xlabel("Number of Initial Mods", fontsize=16)
ax.set_ylabel("Probability of Success, %", fontsize=16)
ax.set_title("%i initial MODs" % their_mods_initial, fontsize=18)

plt.show()
