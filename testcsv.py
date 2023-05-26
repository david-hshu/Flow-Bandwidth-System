import pandas as pd

test1 = pd.read_csv('D:\\flaskProject\\history\\2023_04_26\\11_17_55\\data\\show_label.csv', sep=',')
test2 = test1.values.tolist()
for i in range(len(test2)):
    print(type(test2[i][0]))