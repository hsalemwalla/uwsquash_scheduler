import csv
import random
import pprint
import copy
import os.path

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
courts = ["court8", "court9"]
info_file = "player_info.csv"

# Hold the times parsed from the doodle
keys = []
# Hold all person objects
persons = []

# Init some helper stuff
pp = pprint.PrettyPrinter(indent=4)
random.seed()

class Person:
    def __init__(self, name=""):
        self.name = name
        self.times = {"Monday":{}, "Tuesday":{}, "Wednesday":{}, "Thursday":{}, "Friday":{}}
        self.level = -1
        self.team = "Men"
        self.scheduled = False

# Parse the schedule from the csv files into Person objects
# TODO: Pass in the day to parse
def parse_doodle(day):
    # TODO: Cheeck if file exists - move it out of main()
    with open(day+".csv", 'rb') as csvfile:
        doodle = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in doodle:
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
                # We might be parsing a new day, and have the person already there, let's just get that person
                p = Person(row[0])
                for p_temp in persons:
                    if p_temp.name == row[0]:
                        p = p_temp
                        break
                i = 1
                for val in row[1:]:
                    # Create the times dict entry, based on the doodle response
                    if val == "OK":
                        p.times[day][keys[i]] = True
                    else:
                        p.times[day][keys[i]] = False
                    # print keys[i-1], p.name, p.times[keys[i-1]], val
                    i = i + 1
                if p: # TODO: I don't think we need this check
                    persons.append(p)

# Player info contains team and ranking info
# Parse this into the person objects
def parse_player_info_into_persons():
    # TODO: Cheeck if file exists
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

def print_player_info():
    for p in persons:
        print p.name, ",", p.level, ",", p.team

# def generate_schedule(court):
def generate_schedule(day):
    generated_schedule = {}
    for time in keys[1:]: # 'Times' is the first key - ignore this key
        for court in courts:
        # Look for a person at the time
            get_player_at_time(generated_schedule, day, time, court)
    return generated_schedule

def get_player_at_time(generated_schedule, d, t, c):
    for p in persons:
        if not p.scheduled:
            if p.times[d][t] == True:
                # Found a person available at the time
                # Look for an opponent
                if get_opponent(generated_schedule, p, d, t, c):
                    return True
                else:
                    continue
    return False

def get_opponent(generated_schedule, p, d, t, c):
    curr_player_lvl = p.level
    for p_temp in persons:
        if not p_temp.scheduled:
            if p_temp.name != p.name:
                if abs(int(p_temp.level) - int(curr_player_lvl)) < 3:
                    # print p_temp.times[d]
                    # print p.name
                    # print p_temp.name
                    # print d
                    # print t
                    # print c
                    if p_temp.times[d][t] == True:
                        # Final check - add some randomness
                        r = random.randint(1,2)
                        if r == 1:
                            # Found another player for the time
                            # Set the scheduled flag to true for both players
                            p.scheduled = True
                            p_temp.scheduled = True
                            # Add them to the generated_schedule
                            if d not in generated_schedule:
                                generated_schedule[d] = {}
                            if c not in generated_schedule[d]:
                                generated_schedule[d][c] = {}
                            generated_schedule[d][c][t] = [p.name, p_temp.name]
                            return True
    return False

def get_persons_not_scheduled():
    for p in persons:
        if not p.scheduled:
            yield p

def reset_players_scheduled():
    for p in persons:
        p.scheduled = False;

def main():
    # parse_doodle("Tuesday")
    # for day in days:
        # # Check if the file exists - then parse
        # if os.path.isfile(day+".csv"):
            # print day
            # parse_doodle(day)
    parse_doodle("Monday")
    parse_player_info_into_persons()
    print_player_info()

    lowest_people_not_scheduled = []
    lowest_not_scheduled_num = 10000
    best_schedule = {}

    people_not_scheduled = []
    not_scheduled_num = 0
    new_schedule = {}

    # Generate schedule for all days that have times
    for day in days:
        if "3:00" in persons[0].times[day]:
            print day
            for i in range(1,100):
                reset_players_scheduled()

                new_schedule = generate_schedule(day)
                # new_schedule = generate_schedule("Wednesday")
                people_not_scheduled = list(get_persons_not_scheduled())
                not_scheduled_num = len(people_not_scheduled)

                if not_scheduled_num < lowest_not_scheduled_num:
                    lowest_not_scheduled_num = not_scheduled_num
                    lowest_people_not_scheduled = people_not_scheduled
                    best_schedule = copy.deepcopy(new_schedule)

            schedule = copy.deepcopy(best_schedule)

    pp.pprint(schedule)
    print "Num not scheduled: %s" % lowest_not_scheduled_num
    for p in lowest_people_not_scheduled:
        print p.name


if __name__ == "__main__":
    main()
