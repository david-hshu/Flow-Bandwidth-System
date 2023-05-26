import os

from Net_Detection import datasave
from Net_Detection import predict_c_2 as predict
from Net_Detection.cut_pcap import *
import time
from datetime import datetime


def get_res(filename, num_pacp):
    # 以日期为文件夹名创建文件
    nowdate = datetime.now().strftime('%Y_%m_%d')

    print(nowdate + '\n')

    pwd = 'D:\\flaskProject\\history\\' + nowdate
    if not os.path.exists(pwd):
        os.mkdir(pwd)

    nowtime = datetime.now().strftime('%H_%M_%S')

    pwd = pwd + '\\' + nowtime

    os.mkdir(pwd)

    # 多线程
    num_cores = int(mp.cpu_count())
    print("本地计算机有: " + str(num_cores) + " 核心")
    pool = mp.Pool(num_cores)

    # 开始时间
    start = time.time()

    # 从端口读取数据
    a = pcap_cut()
    data1 = a.read_pcap2(pwd, filename, pool, int(num_pacp))

    # 结束时间
    end = time.time()
    print("截取数据包时间：%.2f" % (end - start))

    # 数据处理
    data_save = datasave.savedata(data1, filename=pwd + '\\' + "test_data")
    data_save.save_excel(pwd)

    path = pwd + '\\' + 'test_data.csv'

    # 预测
    predicted = predict.predict(pwd, path)

    predicted.finalmainmodel1()
    predicted.finalmainmodel2()
    predicted.finalmainmodel3()
    # 返回结果
    return predicted.statistic()


if __name__ == '__main__':
    get_res('0', 400)
