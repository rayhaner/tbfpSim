import random
import queue
import numpy as np

class Man:
    def __init__(self, name):
        self.name = name
        self.status = 0 # 0=idle, 1=manning, 2=busy
        self.time_manned = 0
        self.time_to_return = 0

        # tracking metrics
        self.time_asleep = 0
        self.consec_sleep = 0
        self.longest_consec = 0

    # respond to boss' call, sets own time to return
    def respond_call(self, call, t):
        self.status = 2
        self.time_to_return = t + call.call_duration
        
    # return from boss' call, adding self to the call queue
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
def package_results(m1_arr, m2_arr, m1_c_arr, m2_c_arr):
    m1_result = (avg_stdev(m1_arr), avg_stdev(m1_c_arr))
    m2_result = (avg_stdev(m2_arr), avg_stdev(m2_c_arr))

    return (m1_result, m2_result)
    
def get_sleep_data(result, index):
    return result[index-1][0]

def get_consec_data(result, index):
    return result[index-1][1]

def print_results(data_1, data_2, n, p):
    print("SIMULATION RESULTS FOR " + str(n) + " RUNS, p = "+ str(p))
    print("\nSCENARIO 1: 1ST IN QUEUE (M1) MANS DESK 1100 - 1300, 2ND IN QUEUE (M2) MANS DESK 1730 - 1930")

    print("\nM1 TIME ASLEEP: (" + str(get_sleep_data(data_1, 1)[0])
          + " +- " + str(get_sleep_data(data_1, 1)[1]) + ") HOURS")
    print("M1 CONSEC. ASLEEP: (" + str(get_consec_data(data_1, 1)[0])
          + " +- " + str(get_consec_data(data_1, 1)[1]) + ") HOURS")

    print("\nM2 TIME ASLEEP: (" + str(get_sleep_data(data_1, 2)[0])
          + " +- " + str(get_sleep_data(data_1, 2)[1]) + ") HOURS")
    print("M2 CONSEC. ASLEEP: (" + str(get_consec_data(data_1, 2)[0])
          + " +- " + str(get_consec_data(data_1, 2)[1]) + ") HOURS")

    print("\n\nSCENARIO 2: 2ND IN QUEUE (M2) MANS DESK 1100 - 1300, 1ST CALL (M1) MANS DESK 1730 - 1930")

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
        res_str_1 = "IF YOU ARE 1ST IN QUEUE: THE OPTIMAL FRONT DESK SHIFT FOR AVERAGE SLEEP TIME IS "
        res_str_2 = "IF YOU ARE 2ND IN QUEUE: THE OPTIMAL FRONT DESK SHIFT FOR AVERAGE SLEEP TIME IS "

        if m1_run1_sleep_data > m1_run2_sleep_data:
            foo = 1
            comp_str_1 = "1ST, 1100 - 1300 "
        else:
            foo = 2
            comp_str_1 = "2ND, 1730 - 1900 "
        if m2_run1_sleep_data < m2_run2_sleep_data:
            bah = 1
            comp_str_2 = "1ST, 1100 - 1300 "
        else:
            bah = 2
            comp_str_2 = "2ND, 1730 - 1900 "

        if foo == 1 and bah == 1:
            print("FOR AVERAGE SLEEP TIME, OPTIMUM IS TO ALWAYS TAKE THE 1ST SHIFT 1100 - 1300")
            print("DATA FOR 1ST IN QUEUE: " + versus(m1_run1_sleep_data, m1_run2_sleep_data))
            print("DATA FOR 2ND IN QUEUE: " + versus(m2_run2_sleep_data, m2_run1_sleep_data))
        elif foo == 2 and bah == 2:
            print("FOR AVERAGE SLEEP TIME, OPTIMUM IS TO ALWAYS TAKE THE 2ND SHIFT 1730 - 1900")
            print("DATA FOR 1ST IN QUEUE: " + versus(m1_run1_sleep_data, m1_run2_sleep_data))
            print("DATA FOR 2ND IN QUEUE: " + versus(m2_run2_sleep_data, m2_run1_sleep_data))
        else:
            print(res_str_1 + comp_str_1 + versus(m1_run1_sleep_data, m1_run2_sleep_data))
            print(res_str_2 + comp_str_2 + versus(m2_run2_sleep_data, m2_run1_sleep_data))

    elif mode == 2:
        res_str_1 = "IF YOU ARE 1ST IN QUEUE: THE OPTIMAL FRONT DESK SHIFT FOR UNINTERRUPTED SLEEP TIME IS "
        res_str_2 = "IF YOU ARE 2ND IN QUEUE: THE OPTIMAL FRONT DESK SHIFT FOR UNINTERRUPTED SLEEP TIME IS "

        if m1_run1_consec_data > m1_run2_consec_data:
            foo = 1
            comp_str_1 = "1ST, 1100 - 1300 "
        else:
            foo = 2
            comp_str_1 = "2ND, 1730 - 1900 "
        if m2_run1_consec_data < m2_run2_consec_data:
            bah = 1
            comp_str_2 = "1ST, 1100 - 1300 "
        else:
            bah = 2
            comp_str_2 = "2ND, 1730 - 1900 "

        if foo == 1 and bah == 1:
            print("FOR UNINTERRUPTED SLEEP TIME, OPTIMUM IS TO ALWAYS TAKE THE 1ST SHIFT 1100 - 1300")
            print("DATA FOR 1ST IN QUEUE: " + versus(m1_run1_consec_data, m1_run2_consec_data))
            print("DATA FOR 2ND IN QUEUE: " + versus(m2_run2_consec_data, m2_run1_consec_data))
        elif foo == 2 and bah == 2:
            print("FOR UNINTERRUPTED SLEEP TIME, OPTIMUM IS TO ALWAYS TAKE THE 2ND SHIFT 1730 - 1900")
            print("DATA FOR 1ST IN QUEUE: " + versus(m1_run1_consec_data, m1_run2_consec_data))
            print("DATA FOR 2ND IN QUEUE: " + versus(m2_run2_consec_data, m2_run1_consec_data))
        else:
            print(res_str_1 + comp_str_1 + versus(m1_run1_consec_data, m1_run2_consec_data))
            print(res_str_2 + comp_str_2 + versus(m2_run2_consec_data, m2_run1_consec_data))
    else:
        print("MODE NOT FOUND")

# FRONT DESK DETERMINATION
def front_desk(m1, m2, mod_arr, m_q, t): 

    # if nobody is manning the desk
    if m1.status != 1 and m2.status != 1:
        
        # and both are sleeping, activate the original arrangement
        if m1.status == 0 and m2.status == 0: 
            
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

        # else, if one person is on call, get the other to sit at the front desk
        else:
            
            if not m_q.empty():
                if t >= 0 and t < 120 or t >= 390 and t < 510:
                    scan = m_q.queue
                    
                    # get whoever is available
                    sit_desk = scan[0]
                    
                    # if there is a receptionist available, he will sit at the desk
                    if sit_desk != 0:
                        sit_desk.status = 1 

    # if there is a person at the desk already
    else: 
        
        # mercy system
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

    # go back to sleep at the end of the first shift if anyone is at the desk
    if t == 120:
        if m1.status == 1: m1.status = 0
        if m2.status == 1: m2.status = 0

    # tracking
    if m1.status == 1: m1.time_manned += 1
    if m2.status == 1: m2.time_manned += 1

    return mod_arr

def reception_sim(n, mode, p):

    # initialize result arrays
    m1_arr = []
    m2_arr = []
    m1_c_arr = []
    m2_c_arr = []
    
    for i in range(n):

        # initialize variables
        m1 = Man("m1")
        m2 = Man("m2")

        m_q = queue.Queue()
        m_q.put(m1)
        m_q.put(m2)

        mod_arr = [False, False]

        for t in range(510):

            # determining if boss calls
            call_chance = random.randint(1, 510)
            
            # assuming every 510mins, boss calls p times on average
            if call_chance <= p and not m_q.empty(): 
                call = Call()
                
                # get the first person in the queue to respond to the boss
                m_q.get().respond_call(call, t) 

            # return all receptionists if their respective times are up
            m_arr = [m1, m2]
            for m in m_arr:
                if m.time_to_return == t and m.time_to_return != 0:
                    m.return_call(m_q)

            # two modes for the two cases
            if mode == 1:
                mod_arr = front_desk(m1, m2, mod_arr, m_q, t)
            elif mode == 2:
                mod_arr = front_desk(m2, m1, mod_arr, m_q, t)

            # update sleep timer
            for m in m_arr:
                if m.status == 0:
                    m.time_asleep += 1
                    m.consec_sleep += 1
                    
                    # determine the longest time spent asleep consecutively
                    if m.consec_sleep > m.longest_consec: 
                        m.longest_consec = m.consec_sleep
                else:
                    m.consec_sleep = 0

        # compile all results in an array
        m1_arr.append(m1.time_asleep)
        m2_arr.append(m2.time_asleep)

        m1_c_arr.append(m1.longest_consec)
        m2_c_arr.append(m2.longest_consec)
    
    return (m1_arr, m2_arr, m1_c_arr, m2_c_arr)
            
def run_sim(n, p):
    
    run_1 = reception_sim(n, 1, p)
    run_2 = reception_sim(n, 2, p)

    data_1 = package_results(*run_1)
    data_2 = package_results(*run_2)

    print_results(data_1, data_2, n, p)
    compare_results(data_1, data_2, 1)
    compare_results(data_1, data_2, 2)

run_sim(1000, 2)
        
        
