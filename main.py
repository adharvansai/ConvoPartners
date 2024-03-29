import pandas as pd
import numpy as np
from Configure import icols,acols, int_filepath, amc_filepath, week, time_col_start, time_col_end, meeting_preference
import xlwt
from xlwt import Workbook

def data_preprocessing(conv_data, filetype):

    if(filetype == 'i'):
        dcols = icols
    else:
        dcols = acols

    # Removing NAN rows from Training Time
    #conv_data = conv_data[conv_data[dcols[0]] != 'None']

    # Replacing Meeting Preferences with quantitative Values
    # 1 - No Preference
    # 2 - In person
    # 3 - Zoom
    conv_data[dcols[5]] = conv_data[dcols[5]].replace(to_replace ='.*No [pP]reference.*', value = 1, regex = True)
    conv_data[dcols[5]] = conv_data[dcols[5]].replace(to_replace ='.*In-person.*', value = 2, regex = True)
    conv_data[dcols[5]] = conv_data[dcols[5]].replace(to_replace ='.*[zZ]oom.*', value = 3, regex = True)
    filtered_data = conv_data[conv_data[dcols[5]].isin([1, 2, 3])]

    # Seperating Time data and Individual information
    time_data = np.array(filtered_data[dcols[time_col_start:time_col_end]])
    ind_data = filtered_data[dcols[:time_col_start]]

    #Adding a new column to individual data to store timings

    time_slots = []

    total_records = ind_data.shape[0]
    for record in range(total_records):
        slots = []
        time_index = 0
        for time in range(time_col_end - time_col_start):
            time_index += 1
            days = str(time_data[record][time]).replace(";", ",").split(",")
            if(days[0] != "nan"):
                for d in days:
                    d = d.strip()
                    try:
                        slot_value = 12 * (week[d] - 1) + time_index
                    except KeyError as e:
                        print(f"Debug Info: {time_data[record]} KeyError triggered. {days} Value of d: {d}, Value of time_index: {time_index}")
                        raise e
                    slots.append(slot_value)
        time_slots.append(slots)
    time_slots_df = pd.DataFrame({'Time Slots': time_slots})
    combined_data = pd.concat([ind_data.reset_index(drop=True), time_slots_df.reset_index(drop=True)], axis=1)
    return combined_data

class GFG:
    def __init__(self, graph):
        self.graph = graph
        self.rows = len(graph)
        self.cols = len(graph[0])
        #can write like graph.shape

    def bpm(self, u, matchR, seen):

        for v in range(self.cols):

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
        print(len(matchR))
        return matchR





def main():
    int_data = pd.read_excel(int_filepath)
    amc_data = pd.read_excel(amc_filepath)
    non_native = data_preprocessing(int_data,"i")
    native = data_preprocessing(amc_data,"a")

    # ns = open("/Users/adharvan/PycharmProjects/ConvoPartners/ns.txt", 'w+')
    # nns = open("/Users/adharvan/PycharmProjects/ConvoPartners/nns.txt", 'w+')

    ns_em = np.array(native[acols[2]])
    ns_fn = np.array(native[acols[3]])
    ns_uin = np.array(native[acols[4]])
    ns_md = np.array(native[acols[5]])
    ns_ts = np.array(native["Time Slots"])
    nns_em = np.array(non_native[icols[2]])
    nns_fn = np.array(non_native[icols[3]])
    nns_uin = np.array(non_native[icols[4]])
    nns_md = np.array(non_native[icols[5]])
    nns_ts = np.array(non_native["Time Slots"])
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
    # possibility = np.array(possibility)

    # Edmond Matrix with Non-Native speakers are rows and Native speakers as column
    bp_graph = np.array([[0]*native_count]*non_native_count)
    for i in range(non_native_count):
        for a in possibility[i]:
            bp_graph[i][int(a)] = 1

    g = GFG(bp_graph)
    res = np.array(g.maxBPM())

    results = open("results.txt", 'w+')
    wb = Workbook()
    sheet = wb.add_sheet('Matches')

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Georgia'
    font.bold = True
    font.color_index = 4
    font.height = 280
    style.font = font
    sheet.write(0, 0,'NNS - First and Last Name',style)
    sheet.write(0, 1, 'NNS - Email',style)
    sheet.write(0, 2, 'NNS - UIN',style)
    sheet.write(0, 3, 'NNS - Modality', style)
    sheet.write(0, 4, 'NS - First and Last Name',style)
    sheet.write(0, 5, 'NS - Email',style)
    sheet.write(0, 6, 'NS - UIN',style)
    sheet.write(0, 7, 'NS - Modality', style)
    sheet.write(0, 8, 'Modality', style)
    sheet.write(0, 9, 'Available Meeting Times',style)

    sheet.col(0).width = 256 * 40
    sheet.col(1).width = 256 * 30
    sheet.col(2).width = 256 * 15
    sheet.col(3).width = 256 * 30
    sheet.col(4).width = 256 * 40
    sheet.col(5).width = 256 * 30
    sheet.col(6).width = 256 * 15
    sheet.col(7).width = 256 * 30
    sheet.col(8).width = 256 * 30
    sheet.col(9).width = 256 * 150


    sheet.row(0).height = 256*40
    style1 = xlwt.XFStyle()
    font1 = xlwt.Font()
    font1.name = 'Georgia'
    font1.bold = False
    font1.color_index = 4
    font1.height = 230
    style1.font = font1
    rownum = 1
    matched_nns = []
    matched_ns = []
    for i in range(len(ns_em)):
        if(res[i] != -1):
            sheet.write(rownum, 0, nns_fn[res[i]],style1)
            sheet.write(rownum, 1, nns_em[res[i]],style1)
            sheet.write(rownum, 2, str(nns_uin[res[i]]),style1)
            sheet.write(rownum, 3,
                        {1: 'No Preference', 2: 'In person', 3: 'Zoom'}.get(nns_md[res[i]], str(nns_md[res[i]])),
                        style1)
            sheet.write(rownum, 4, ns_fn[i],style1)
            sheet.write(rownum, 5, ns_em[i],style1)
            sheet.write(rownum, 6, str(ns_uin[i]),style1)
            sheet.write(rownum, 7, {1: 'No Preference', 2: 'In person', 3: 'Zoom'}.get(ns_md[i], str(ns_md[i])), style1)
            if(nns_md[res[i]] == 1 and ns_md[i] == 1):
                sheet.write(rownum, 8, "No Meeting Preference",style1)
            elif((nns_md[res[i]] == 2 and ns_md[i] == 2) or (nns_md[res[i]] == 2 and ns_md[i] == 1) or (nns_md[res[i]] == 1 and ns_md[i] == 2)):
                sheet.write(rownum, 8, "In-person Meeting Preferred",style1)
            elif ((nns_md[res[i]] == 3 and ns_md[i] == 3) or (nns_md[res[i]] == 1 and ns_md[i] == 3) or (nns_md[res[i]] == 3 and ns_md[i] == 1)):
                sheet.write(rownum, 8, "Zoom Meeting Preferred",style1)

            times = set(ns_ts[i]).intersection(set(nns_ts[res[i]]))
            time_slots = ""
            times = sorted(times)
            for t in times:
                t = t -1
                quo = t//12 + 1
                day = week[quo]
                rem = t%12 + 9
                if(rem > 12):
                    time = str(rem - 12) + " PM" + " - " + str(rem - 11) + " PM    "
                else:
                    time = str(rem) + " AM" + ' - ' + str(rem) + " AM    "
                time_slots += str(day) + " " + str(time) + "\n"

            sheet.write(rownum, 9, str(time_slots),style1)
            sheet.row(rownum).height = 256 * 30
            matched_ns.append(ns_em[i])
            matched_nns.append(nns_em[res[i]])
            rownum += 1

    sheet2 = wb.add_sheet('Not Matched')

    sheet2.write(0, 0, 'Non Native Speakers', style)
    sheet2.write(0, 1, 'Native Speakers', style)

    nns_dif = set(nns_em) - set(matched_nns)
    ns_dif = set(ns_em) - set(matched_ns)
    rownum = 1
    for i in nns_dif:
        sheet2.write(rownum, 0, str(i), style1)
        rownum += 1
    rownum = 1
    for i in ns_dif:
        sheet2.write(rownum, 1, str(i), style1)
        rownum += 1


    wb.save('/Users/adharvan/PycharmProjects/ConvoPartners/ConvoPartner_Matches_Fall_2023.xls')


    results.close()
    print(sorted(res))
    print(set(nns_em) - set(matched_nns))





if __name__ == "__main__":
    main()