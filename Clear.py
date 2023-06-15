import pandas as pd

hh = {}

df = pd.read_csv('./url.csv', header = None, engine='python')

le = len(df)

l = ''

for i in range(0, le):
    tmp2 = list(df.iloc[i])
    if (len(tmp2) <= 0):
        continue
    if tmp2[0] in hh:
        continue
    else:
        hh[tmp2[0]] = tmp2[0]
        l += tmp2[0] + ',' + tmp2[1] + ',' + tmp2[2] + ',' + tmp2[3] + ',' + tmp2[4] + '\n'

with open('./url.csv', 'w', encoding='utf-8') as f:
    f.writelines(l)