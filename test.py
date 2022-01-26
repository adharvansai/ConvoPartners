import pandas as pd
from Configure import icols

test = pd.read_excel("/Users/adharvan/PycharmProjects/ConvoPartners/imbp.xlsx")
s = 'Please select your preference for meetings with your conversation partner.'
test[s] = test[s].replace(to_replace ='.*[zZ]oom.*', value = 3, regex = True)
test[s] = test[s].replace(to_replace ='.*In-person.*', value = 2, regex = True)
test[s] = test[s].replace(to_replace ='.*No [pP]reference.*', value = 1, regex = True)
#print(test['Training Timestamp'])
tnp = test.to_numpy()
tnpr= test[icols[6:]]
tnpl = test[icols[:6]]
tnpl["Time Slots"] = ""
#print(tnpr[icols[6]][2])
tnpr.fillna("")
for i in range(10):
    for j in range(6, len(icols)):
        col = icols[j]
        ts = tnpr[col][i]
        #ts = ts.split(",")
        print(ts)

    print("="*30)
#print(tnpl)


