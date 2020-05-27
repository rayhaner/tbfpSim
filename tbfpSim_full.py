# 0 2300
# 1 2330
# 2 0000
# 3 0030
# 4 0100
# 5 0130
# 6 0200
# 7 0230
# 8 0300
# 9 0330
# 10 0400
# 11 0430
# 12 0500
# 13 0530 
# 14 0600
# 15 0630
# 16 0700
# 17 0730

import random
import queue
import numpy as np
import matplotlib.pyplot as plt

class Medic:
    def __init__(self, name):
        self.status = 0 # 0=idle, 1=manning, 2=on call
        self.time_asleep = 0
        self.time_manned = 0
        self.time_to_return = 0
        self.name = name
        self.consec_sleep = 0
        self.longest_consec = 0

    # respond to a call, sets own time to return
    def respond_call(self, call, t):
        self.status = 2
        self.time_to_return = t + call.call_duration
        
    # return from call, adding self to the call queue
    def return_call(self, q):
        q.put(self)
        self.status = 0
        self.time_to_return = 0

class Call:
    def __init__(self):
        self.call_duration = random.randint(60, 120) # 1 - 2 hours call

# calculates the average and standard deviation of values in an array to 2dp
def avg_stdev(arr):
    
    avg = sum(arr) / len(arr) / 60
    stdev = np.std(arr) / 60
    rd = lambda x: round(x, 2)
    
    return (rd(avg), rd(stdev))

# package the results
def package_results(m1_arr, m2_arr, m1_c_arr, m2_c_arr, num_calls_arr):
    m1_result = (avg_stdev(m1_arr), avg_stdev(m1_c_arr))
    m2_result = (avg_stdev(m2_arr), avg_stdev(m2_c_arr))

    return (m1_result, m2_result)
    
def get_sleep_data(result, index):
    return result[index-1][0]

def get_consec_data(result, index):
    return result[index-1][1]

def print_results(data_1, data_2, n):
    print("SIMULATION RESULTS FOR " + str(n) + " RUNS")
    print("\nSCENARIO 1: 1ST CALL (M1) MANS DESK 2300 - 0100, 2ND CALL (M2) MANS DESK 0530 - 0730")

    print("\nM1 TIME ASLEEP: (" + str(get_sleep_data(data_1, 1)[0])
          + " +- " + str(get_sleep_data(data_1, 1)[1]) + ") HOURS")
    print("M1 CONSEC. ASLEEP: (" + str(get_consec_data(data_1, 1)[0])
          + " +- " + str(get_consec_data(data_1, 1)[1]) + ") HOURS")

    print("\nM2 TIME ASLEEP: (" + str(get_sleep_data(data_1, 2)[0])
          + " +- " + str(get_sleep_data(data_1, 2)[1]) + ") HOURS")
    print("M2 CONSEC. ASLEEP: (" + str(get_consec_data(data_1, 2)[0])
          + " +- " + str(get_consec_data(data_1, 2)[1]) + ") HOURS")

    print("\n\nSCENARIO 2: 2ND CALL (M2) MANS DESK 2300 - 0100, 1ST CALL (M1) MANS DESK 0530 - 0730")

    print("\nM1 TIME ASLEEP: (" + str(get_sleep_data(data_2, 1)[0])
          + " +- " + str(get_sleep_data(data_2, 1)[1]) + ") HOURS")
    print("M1 CONSEC. ASLEEP: (" + str(get_consec_data(data_2, 1)[0])
          + " +- " + str(get_consec_data(data_2, 1)[1]) + ") HOURS")

    print("\nM2 TIME ASLEEP: (" + str(get_sleep_data(data_2, 2)[0])
          + " +- " + str(get_sleep_data(data_2, 2)[1]) + ") HOURS")
    print("M2 CONSEC. ASLEEP: (" + str(get_consec_data(data_2, 2)[0])
          + " +- " + str(get_consec_data(data_2, 2)[1]) + ") HOURS")

def compare_results(data_1, data_2, mode):
    
    # get all the data
    m1_run1_sleep_data = get_sleep_data(data_1, 1)[0]
    m1_run1_consec_data = get_consec_data(data_1, 1)[0]

    m2_run1_sleep_data = get_sleep_data(data_1, 2)[0]
    m2_run1_consec_data = get_consec_data(data_1, 2)[0]

    m1_run2_sleep_data = get_sleep_data(data_2, 1)[0]
    m1_run2_consec_data = get_consec_data(data_2, 1)[0]

    m2_run2_sleep_data = get_sleep_data(data_2, 2)[0]
    m2_run2_consec_data = get_consec_data(data_2, 2)[0]

    versus = lambda x, y: "(" + str(x) + "h VS " + str(y) + "h)"

    print("\n\nCONCLUSION\n")

    foo = 0
    bah = 0
    
    if mode == 1:
        res_str_1 = "IF YOU ARE 1ST CALL: THE OPTIMAL FRONT DESK SHIFT FOR AVERAGE SLEEP TIME IS "
        res_str_2 = "IF YOU ARE 2ND CALL: THE OPTIMAL FRONT DESK SHIFT FOR AVERAGE SLEEP TIME IS "

        if m1_run1_sleep_data > m1_run2_sleep_data:
            foo = 1
            comp_str_1 = "1ST, 2300 - 0100 "
        else:
            foo = 2
            comp_str_1 = "2ND, 0530 - 0730 "
        if m2_run1_sleep_data < m2_run2_sleep_data:
            bah = 1
            comp_str_2 = "1ST, 2300 - 0100 "
        else:
            bah = 2
            comp_str_2 = "2ND, 0530 - 0730 "

        if foo == 1 and bah == 1:
            print("FOR AVERAGE SLEEP TIME, OPTIMUM IS TO ALWAYS TAKE THE 1ST SHIFT")
            print("DATA FOR 1ST CALL: " + versus(m1_run1_sleep_data, m1_run2_sleep_data))
            print("DATA FOR 2ND CALL: " + versus(m2_run2_sleep_data, m2_run1_sleep_data))
        elif foo == 2 and bah == 2:
            print("FOR AVERAGE SLEEP TIME, OPTIMUM IS TO ALWAYS TAKE THE 2ND SHIFT")
            print("DATA FOR 1ST CALL: " + versus(m1_run1_sleep_data, m1_run2_sleep_data))
            print("DATA FOR 2ND CALL: " + versus(m2_run2_sleep_data, m2_run1_sleep_data))
        else:
            print(res_str_1 + comp_str_1 + versus(m1_run1_sleep_data, m1_run2_sleep_data))
            print(res_str_2 + comp_str_2 + versus(m2_run2_sleep_data, m2_run1_sleep_data))

    elif mode == 2:
        res_str_1 = "IF YOU ARE 1ST CALL: THE OPTIMAL FRONT DESK SHIFT FOR UNINTERRUPTED SLEEP TIME IS "
        res_str_2 = "IF YOU ARE 2ND CALL: THE OPTIMAL FRONT DESK SHIFT FOR UNINTERRUPTED SLEEP TIME IS "

        if m1_run1_consec_data > m1_run2_consec_data:
            foo = 1
            comp_str_1 = "1ST, 2300 - 0100 "
        else:
            foo = 2
            comp_str_1 = "2ND, 0530 - 0730 "
        if m2_run1_consec_data < m2_run2_consec_data:
            bah = 1
            comp_str_2 = "1ST, 2300 - 0100 "
        else:
            bah = 2
            comp_str_2 = "2ND, 0530 - 0730 "

        if foo == 1 and bah == 1:
            print("FOR UNINTERRUPTED SLEEP TIME, OPTIMUM IS TO ALWAYS TAKE THE 1ST SHIFT")
            print("DATA FOR 1ST CALL: " + versus(m1_run1_consec_data, m1_run2_consec_data))
            print("DATA FOR 2ND CALL: " + versus(m2_run2_consec_data, m2_run1_consec_data))
        elif foo == 2 and bah == 2:
            print("FOR UNINTERRUPTED SLEEP TIME, OPTIMUM IS TO ALWAYS TAKE THE 2ND SHIFT")
            print("DATA FOR 1ST CALL: " + versus(m1_run1_consec_data, m1_run2_consec_data))
            print("DATA FOR 2ND CALL: " + versus(m2_run2_consec_data, m2_run1_consec_data))
        else:
            print(res_str_1 + comp_str_1 + versus(m1_run1_consec_data, m1_run2_consec_data))
            print(res_str_2 + comp_str_2 + versus(m2_run2_consec_data, m2_run1_consec_data))
    else:
        print("MODE NOT FOUND")

# MANNING DESK DETERMINATION
def man_desk(m1, m2, mod_arr, medic_q, t): 

    if m1.status != 1 and m2.status != 1: # if nobody is manning the desk
        if m1.status == 0 and m2.status == 0: # and both are sleeping, activate the original arrangement
            
            if t >= 0 and t < 120:
                m1.status = 1
            elif t >= 390 and t < 510:
                if mod_arr[0] and t < 450:
                    m1.status = 1
                    if m2.status == 1: m2.status = 0
                elif mod_arr[0] and t >= 450:
                    m2.status = 1
                    if m1.status == 1: m1.status = 0
                elif mod_arr[1]:
                    m1.status = 1
                    if m2.status == 1: m2.status = 0
                else:
                    m2.status = 1
                
        else: # else, if one person is on call, get the other to man
            if not medic_q.empty():
                if t >= 0 and t < 120 or t >= 390 and t < 510:
                    scan = medic_q.queue
                    man_medic = scan[0] # get whoever is available at FP
                    if man_medic != 0:
                        man_medic.status = 1 # if there is a medic at FP, he will man the desk

    else: # if there is a person manning the desk already
        
        # mercy system
        # if m1 turnout while manning desk and m2 mans for >=2u
        # if timing 1:1, split each shift in half
        # if timing 0.5:1.5/0.5:1, too bad
        # if timing 1.5:0.5, let the 1.5 finish first

        # range += 15mins

        within_ten = lambda x, y: x <= y + 15 and x >= y - 15
        
        if t == 120 and within_ten(m1.time_manned, m2.time_manned):
            mod_arr[0] = True
        elif t == 90 and m2.time_manned / 2 >= m1.time_manned:
            mod_arr[1] = True
        elif t == 120 and m2.time_manned / 3 >= m1.time_manned:
            mod_arr[1] = True

        if t >= 0 and t < 120:
            if mod_arr[0]:
                m1.status = 1
                if m2.status == 1: m2.status = 0
            elif mod_arr[1]:
                m2.status = 1
                if m1.status == 1: m1.status = 0
        elif t >= 390 and t < 510:
            if mod_arr[0] and t < 450:
                m1.status = 1
                if m2.status == 1: m2.status = 0
            elif mod_arr[0] and t >= 450:
                m2.status = 1
                if m1.status == 1: m1.status = 0
            elif mod_arr[1]:
                m1.status = 1
                if m2.status == 1: m2.status = 0
                
    if t == 120:
        if m1.status == 1: m1.status = 0
        if m2.status == 1: m2.status = 0

    if m1.status == 1: m1.time_manned += 1
    if m2.status == 1: m2.time_manned += 1

    return mod_arr

def tbfp_sim(n, mode, p):

    # initialize result arrays
    m1_arr = []
    m2_arr = []
    m1_c_arr = []
    m2_c_arr = []
    num_calls_arr = []
    
    for i in range(n):

        # initialize variables
        m1 = Medic("m1")
        m2 = Medic("m2")

        medic_q = queue.Queue()
        medic_q.put(m1)
        medic_q.put(m2)

        mod_arr = [False, False]

        next_call = 0
        num_of_calls = 0
        split = False
        swap = False

        # 1 unit = 30 mins
        # 11pm - 7.30am
        # 1st watch 11pm - 1am (t=0 to 3), 2nd watch 5.30am - 7.30am (t=13 to 16)

        for t in range(510):

            # dispatch
            if next_call == 0:
                time_to_next_call = random.expovariate(p/510)
                next_call += round(time_to_next_call)
            elif t == next_call and not medic_q.empty(): # 3 in 17 chance for call
                turnout_medic = medic_q.get() # choose which medic to turnout based on order
                call = Call()
                turnout_medic.respond_call(call, t)
                time_next_call = random.expovariate(p/510)
                next_call += round(time_to_next_call)
                num_of_calls += 1

            # return all medics if respective time is up
            medic_arr = [m1, m2]
            for medic in medic_arr:
                if medic.time_to_return == t and medic.time_to_return != 0:
                    medic.return_call(medic_q)

            # two modes for the two cases
            if mode == 1:
                mod_arr = man_desk(m1, m2, mod_arr, medic_q, t)
            elif mode == 2:
                mod_arr = man_desk(m2, m1, mod_arr, medic_q, t)

            # update sleep timer
            for medic in medic_arr:
                if medic.status == 0:
                    medic.time_asleep += 1
                    medic.consec_sleep += 1
                    # determine the longest time spent asleep consecutively
                    if medic.consec_sleep > medic.longest_consec: 
                        medic.longest_consec = medic.consec_sleep
                else:
                    medic.consec_sleep = 0

        # compile all results in an array
        m1_arr.append(m1.time_asleep)
        m2_arr.append(m2.time_asleep)

        m1_c_arr.append(m1.longest_consec)
        m2_c_arr.append(m2.longest_consec)

        num_calls_arr.append(num_of_calls)
    
    return (m1_arr, m2_arr, m1_c_arr, m2_c_arr, num_calls_arr)
            
def graph_data_per_num_calls(m1_arr, m2_arr, num_calls_arr):
    graph_data_m1 = [0,0,0,0,0,0,0,0,0,0]
    tracker_data_m1 = [0,0,0,0,0,0,0,0,0,0]
    graph_data_m2 = [0,0,0,0,0,0,0,0,0,0]
    tracker_data_m2 = [0,0,0,0,0,0,0,0,0,0]
    
    for i in range(len(num_calls_arr)):
        if num_calls_arr[i] <= 9:
            graph_data_m1[num_calls_arr[i]] += m1_arr[i]
            tracker_data_m1[num_calls_arr[i]] += 1
            graph_data_m2[num_calls_arr[i]] += m2_arr[i]
            tracker_data_m2[num_calls_arr[i]] += 1

    for i in range(10):
        graph_data_m1[i] /= tracker_data_m1[i] if tracker_data_m1[i] != 0 else False
        graph_data_m1[i] = round(graph_data_m1[i] / 60, 2)
        graph_data_m2[i] /= tracker_data_m2[i] if tracker_data_m2[i] != 0 else False
        graph_data_m2[i] = round(graph_data_m2[i] / 60, 2)

    return (graph_data_m1, graph_data_m2)

def plot_graph(data_1, data_2):

    plt.suptitle("Sleep time per number of calls")
                 
    # Plot the data
    plt.subplot(121)
    plt.plot([0,1,2,3,4,5,6,7,8,9], data_1[0], label='Medic 1')
    plt.plot([0,1,2,3,4,5,6,7,8,9], data_1[1], label='Medic 2')

    # Add a legend
    plt.legend()
    plt.xlim(0, 9)
    plt.xlabel("Number of Calls")
    plt.ylim(0, 7)
    plt.ylabel("Sleep Time")
    plt.title("Medic 1 first shift")

    plt.subplot(122)
    plt.plot([0,1,2,3,4,5,6,7,8,9], data_2[0], label='Medic 1')
    plt.plot([0,1,2,3,4,5,6,7,8,9], data_2[1], label='Medic 2')

    # Add a legend
    plt.legend()
    plt.xlim(0, 9)
    plt.xlabel("Number of Calls")
    plt.ylim(0, 7)
    plt.ylabel("Sleep Time")
    plt.title("Medic 2 first shift")

    # Show the plot
    plt.show()

def run_sim(n, p):
    
    run_1 = tbfp_sim(n, 1, p)
    run_2 = tbfp_sim(n, 2, p)

    data_1 = package_results(*run_1)
    data_2 = package_results(*run_2)

    print_results(data_1, data_2, n)
    compare_results(data_1, data_2, 1)
    compare_results(data_1, data_2, 2)

    graph_data = graph_data_per_num_calls(run_1[0], run_1[1], run_1[4])
    graph_c_data = graph_data_per_num_calls(run_1[2], run_1[3], run_1[4])

    plot_graph(graph_data, graph_c_data)

run_sim(1000, 2)

        
        
