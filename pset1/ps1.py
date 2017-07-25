###########################
# 6.00.2x Problem Set 1: Space Cows

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')

    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    #copy cows to not mutate dict, set up a result list, keep track of weight
    cows_on_deck = cows.copy()
    result = []
    total_weight = 0

    #create a variable to use as a list iterator in while loop for indexing list of lists
    trip = 0

    while len(cows_on_deck) != 0:
        #make a new list in the result list for the first trip
        result.append([])

        #calculate the heaviest cow and add it to the total weight for the trip
        heaviest_cow = max(cows_on_deck, key = lambda i: cows_on_deck[i])
        total_weight += cows_on_deck[heaviest_cow]
        result[trip].append(heaviest_cow)
        del cows_on_deck[heaviest_cow]

        #sort the cows by weight
        sorted_cows = sorted(list(cows_on_deck.values()), reverse = True)

        #find the next cows to add to the list based on their sorted weight
        for i in sorted_cows:
            #reverse look up the cows name by weight from cows_on_deck using the next sorted weight
            next_cow = list(cows_on_deck.keys())[list(cows_on_deck.values()).index(i)]
            next_cow_weight = cows_on_deck[str(list(cows_on_deck.keys())[list(cows_on_deck.values()).index(i)])]

            #if the cow is over weight skip it
            #otherwise add it on the trip, tally the weight, remove from cows_on_deck
            if next_cow_weight + total_weight > limit:
                pass
            elif next_cow_weight + total_weight <= limit:
                result[trip].append(next_cow)
                total_weight += next_cow_weight
                del cows_on_deck[next_cow]

        #if there are cows left to transport set our weight back to 0
        #incriment by 1 to add a trip
        total_weight = 0
        trip += 1

    return result


# Problem 2
def brute_force_cow_transport(cows,limit):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    #copy cows to not mutate original dict
    cows_on_deck = cows.copy()

    #get all the possible cow combos, make a new list for only the viable cow combos
    cow_combos = [i for i in get_partitions(cows_on_deck)]
    viable_cow_combos = []

    #loop through each sequence of cows one at a time
    for cows in cow_combos:
        #set up a temp list to perform a check weight before we add to the viable_cow_combos
        temp = []
        #loop through each trip in the list of cows from cow_combos
        #check the total weight of the trip in the sequence against the limit
        for trip in cows:
            if sum(cows_on_deck[i] for i in trip) <= limit:
                temp.append(trip)

        #if the length of the temp list matches the length of the original cow list
        #add it to the viable_cow_combos because it has met the weight requirements
        if len(temp) == len(cows):
            viable_cow_combos.append(cows)

    #return the shortest trip based on length
    return min(viable_cow_combos, key = len)


# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """

    start_greedy = time.time()
    print(greedy_cow_transport(cows, limit))
    end_greedy = time.time()
    print("Greedy run time: %f" % (end_greedy - start_greedy))
    print("*" * 30)
    start_brute = time.time()
    print(brute_force_cow_transport(cows, limit))
    end_brute = time.time()
    print("Brute run time: %f" % (end_brute - start_brute))
    print("*" * 30)

"""
Here is some test data for you to see the results of your algorithms with.
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=10
print(cows)

compare_cow_transport_algorithms()

#print(greedy_cow_transport(cows, limit))
#print(brute_force_cow_transport(cows, limit))
