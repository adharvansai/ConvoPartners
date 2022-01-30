import pandas as pd
import numpy as np
from Configure import icols,acols, int_filepath, amc_filepath, week, time_col_start, time_col_end, meeting_preference



def data_preprocessing(conv_data, filetype):

    if(filetype == 'i'):
        dcols = icols
    else:
        dcols = acols

    # Removing NAN rows from Training Time
    conv_data = conv_data[conv_data[dcols[0]] != 'None']

    # Replacing Meeting Preferences with quantitative Values
    # 1 - No Preference
    # 2 - In person
    # 3 - Zoom
    conv_data[dcols[5]] = conv_data[dcols[5]].replace(to_replace ='.*No [pP]reference.*', value = 1, regex = True)
    conv_data[dcols[5]] = conv_data[dcols[5]].replace(to_replace ='.*In-person.*', value = 2, regex = True)
    conv_data[dcols[5]] = conv_data[dcols[5]].replace(to_replace ='.*[zZ]oom.*', value = 3, regex = True)

    # Seperating Time data and Individual information
    time_data = np.array(conv_data[dcols[time_col_start:time_col_end]])
    ind_data = conv_data[dcols[:time_col_start]]

    #Adding a new column to individual data to store timings

    time_slots = []

    total_records = ind_data.shape[0]
    for record in range(total_records):
        #print(record)
        slots = []
        time_index = 0
        for time in range(time_col_end - time_col_start):
            #print(time)
            time_index += 1
            days = str(time_data[record][time]).split(",")

            if(days[0] != "nan"):
                #print("one11")
                for d in days:
                    d = d.strip()
                    slot_value = 12*(week[d] -1) + time_index
                    slots.append(slot_value)
        #print(slots)
        time_slots.append(slots)
    ind_data["Time Slots"] = time_slots

    return ind_data

class GFG:
    def __init__(self, graph):
        self.graph = graph
        self.rows = len(graph)
        self.cols = len(graph[0])
        #can write like graph.shape

    def bpm(self, u, matchR, seen):

        for v in range(self.rows):

            if self.graph[u][v] and seen[v] == False:
                seen[v] = True

                if(matchR[v] == -1 or self.bpm(matchR[v], matchR, seen)):
                    matchR[v] = u
                    return True
        return False

    def maxBPM(self):

        matchR = [-1] * self.cols

        result = 0
        for i in range(self.rows):

            seen = [False] * self.cols

            if self.bpm(i,matchR, seen):
                result += 1
        return result





def main():
    int_data = pd.read_excel(int_filepath)
    amc_data = pd.read_excel(amc_filepath)
    non_native = data_preprocessing(int_data,"i")
    native = data_preprocessing(amc_data,"a")

    non_native_count = non_native.shape[0]
    native_count = native.shape[0]


    # Each row is set of americans compatible with foreigners. Rows = International Columns = Americans
    possibility = []
    for i in range(non_native_count):
        int_mp = non_native[icols[meeting_preference]].tolist()[i]
        int_ts = np.array(non_native["Time Slots"])[i]
        int_ts = set(int_ts)
        matches = []
        for j in range(native_count):
            amc_mp = native[acols[meeting_preference]].tolist()[j]
            amc_ts = set(np.array(native["Time Slots"])[j])
            if(int_mp == 1 or amc_mp == 1 or int_mp == amc_mp):
                if(len(int_ts.intersection(amc_ts)) != 0):
                    matches.append(j)

        possibility.append(sorted(matches))
    possibility = np.array(possibility)

    # Edmond Matrix with Non-Native speakers are rows and Native speakers as column
    bp_graph = np.array([[0]*native_count]*non_native_count)
    for i in range(non_native_count):
        for a in possibility[i]:
            bp_graph[i][int(a)] = 1

    g = GFG(bp_graph)
    print(g.maxBPM())


if __name__ == "__main__":
    main()