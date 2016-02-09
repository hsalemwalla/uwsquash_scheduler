import csv
import random
import pprint
import copy

doodle_file = "Tuesday.csv"
info_file = "player_info.csv"
keys = []
persons = []
schedule = {}
pp = pprint.PrettyPrinter(indent=4)
random.seed()

class Person:
    def __init__(self, name=""):
        self.name = name
        self.times = {}
        self.level = -1
        self.team = "Men"
        self.scheduled = False


def parse_doodle():
    with open(doodle_file, 'rb') as csvfile:
        # Open file
        schedule = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in schedule:
            # First row
            if row[0] == "Times":
                # Generate keys
                for time in row:
                    keys.append(time.split()[0])
                continue
            else:
                # iterate through keys, add dictionary for each entry based on csv
                # for i in range(1,len(keys)):
                # Get name, create person
                p = Person(row[0])
                i = 1
                for val in row[1:]:
                    # Create the times dict entry, based on the doodle response
                    if val == "OK":
                        p.times[keys[i]] = True
                    else:
                        p.times[keys[i]] = False
                    # print keys[i-1], p.name, p.times[keys[i-1]], val
                    i = i + 1
            if p:
                persons.append(p)

def parse_player_info_into_persons():
    with open(info_file,'rb') as csvfile:
        info = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in info:
            # First row
            if row[0] == "Name":
                continue
            else:
                # Find the person
                for p in persons:
                    if p.name == row[0]:
                        p.team = row[1]
                        p.level = row[2]

def generate_schedule(court):
    for time in keys[1:]: # 'Times' is the first key - ignore this key
        # Look for a person at the time
        get_player_at_time(time, court)

def get_player_at_time(t, c):
    for p in persons:
        if not p.scheduled:
            if p.times[t] == True:
                # Found a person available at the time
                # Look for an opponent
                if get_opponent(t, p, c):
                    return True
                else:
                    continue
    return False


def get_opponent(t, p, c):
    curr_player_lvl = p.level
    for p_temp in persons:
        if not p_temp.scheduled:
            if p_temp.name != p.name:
                if abs(int(p_temp.level) - int(curr_player_lvl)) < 3:
                    if p_temp.times[t] == True:
                        # Final check - add some randomness
                        if random.randint(1,2) == 1:
                            # Found another player for the time
                            # Set the scheduled flag to true for both players
                            p.scheduled = True
                            p_temp.scheduled = True
                            # Add them to the schedule
                            if c not in schedule:
                                schedule[c] = {}
                            schedule[c][t] = [p.name, p_temp.name]
                            return True
    return False

def get_persons_not_scheduled():
    for p in persons:
        if not p.scheduled:
            yield p

def main():
    parse_doodle()
    parse_player_info_into_persons()
    # pp.pprint(schedule)
    # s = {}

    num_not_scheduled = 42
    ctr = 0
    n = 0
    while num_not_scheduled >= n:
        generate_schedule("court8")
        generate_schedule("court9")
        num_not_scheduled = len(list(get_persons_not_scheduled()))
        # s[num_not_scheduled] = copy.deepcopy(schedule)
        ctr = ctr + 1
        if ctr > 100:
            n = n + 1
            ctr = 0

    # pp.pprint(s[num_not_scheduled])
    pp.pprint(schedule)
    print "Num not scheduled: %s" % num_not_scheduled
    for p in get_persons_not_scheduled():
        print p.name





if __name__ == "__main__":
    main()
