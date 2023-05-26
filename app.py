import csv
import speedtest
from flask import Flask, request, render_template, jsonify
from flask_bootstrap import Bootstrap
import pandas as pd
import os
from Net_Detection import test1
from werkzeug.utils import secure_filename
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Line
from datetime import datetime
import psutil
import time

# 初始化
app = Flask(__name__)
bootstrap = Bootstrap(app)

ALLOWED_EXTENSIONS = {'pcap', 'csv', 'xls'}
# 配置选项
app.config['UPLOAD_FOLDER'] = 'static/upload'
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

# 全局变量
pwd_all = 'D:\\flaskProject\\history'
dir = pwd_all + '\\' + datetime.now().strftime('%Y_%m_%d')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def bandwidth_test():
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    download = round(res["download"] / 1000, 2)
    upload = round(res["upload"] / 1000, 2)
    ping = round(res["ping"])
    client = res["client"]["isp"]
    country = res["client"]["country"]
    print(
        "-->Download Speed: {:.2f} Kb/s\n-->Upload Speed: {:.2f} Kb/s\n-->Ping: {}\n-->ISP: {}, {}".format(download,
                                                                                                           upload,
                                                                                                           ping,

                                                                                                           client,
                                                                                                           country))
    download = round(download / 1024, 2)
    upload = round(upload / 1024, 2)

    return download, upload, ping, country


# 带宽检测页面
@app.route('/bwtest', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        download, upload, ping, client = bandwidth_test()

        path = dir + '\\' + 'bw_test.csv'
        if not os.path.exists(dir):
            os.mkdir(dir)

        with open(path, 'a+', newline='') as f:
            csv_writer = csv.writer(f)
            data_row = [download, upload, ping, client]
            csv_writer.writerow(data_row)

        send_list, rcv_list = getNet()

        line_chart = line_base(send_list, rcv_list)

        return render_template('bwtest.html', download=download, upload=upload, ping=ping, client=client,
                               line_chart=line_chart.dump_options())
    else:
        return render_template('bwtest.html', download=0, upload=0, ping=0, client="---")


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    status_code = 0
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            status_code = 1
            # file_url = url_for('upload', filename=filename)
        return table('D:\\flaskProject\\static\\upload' + '\\' + filename)
    else:
        return render_template('upload.html')


@app.route('/history', methods=['GET', 'POST'])
def history():
    file_list_all = os.listdir(pwd_all)
    file_list_all.sort()
    list_len = []

    # 查看一个文件夹下有多少个文件
    for index in file_list_all:
        pwd_index = pwd_all + '\\' + index
        list_i = os.listdir(pwd_index)

        list_len.append(sum([os.path.isdir(pwd_index + '\\' + list_index) for list_index in list_i]))

    # 点击查看
    list_3 = ['详情'] * len(list_len)

    list1 = list(zip(file_list_all, list_len, list_3))
    list1 = [list(i) for i in list1]
    return render_template('history.html', list=list1)


@app.route('/history_detail/<date1>', methods=['GET', 'POST'])
def history_detail(date1):
    path = pwd_all + '\\' + str(date1)

    file_list1 = os.listdir(path)
    file_list2 = []
    for index in file_list1:
        if os.path.isdir(path + '\\' + index):
            file_list2.append(index)

    alllist1 = []
    alllist2 = []
    alllist3 = []
    for file in file_list2:
        num = 0
        data_csv = pd.read_csv(path + '\\' + str(file) + '\\data\\' + 'show_label.csv', sep=',')
        list1 = data_csv.values.tolist()
        # time1 = time.strptime(file, "%Y-%m-%d %H:%M:%S")
        alllist1.append(str(file))
        alllist2.append(str(len(list1)))
        for i in range(len(list1)):
            if list1[i][0] == '1' or list1[i][0] == 1:
                num = num + 1
        alllist3.append(str(num))

    # alllist3[5] = '25'
    #
    # alllist3[8] = '13'

    list3 = []
    list2 = list(zip(alllist1, alllist2, alllist3))
    for item in list2:
        list3.append(list(item))

    print(list3)

    data_csv = pd.read_csv(path + '\\' + 'bw_test.csv', header=None)
    list_bw = data_csv.values.tolist()
    list_bw_download = [i[0] for i in list_bw]
    list_bw_upload = [i[1] for i in list_bw]
    list_bw_ping = [i[2] for i in list_bw]

    line1 = line_base(list_bw_download, list_bw_upload)
    line2 = line_base2(list_bw_ping)
    print("date1" + date1)
    return render_template('history_detail.html', date1=date1, list=list3, line_chart=line1.dump_options(),
                           line_chart2=line2.dump_options())


@app.route('/net_detection', methods=['GET', 'POST'])
def net_detection():
    return render_template('net_detection.html')


# 显示csv信息
@app.route('/table/<tag>', methods=['POST', 'GET'])
def table(tag):
    # 送入模型检测
    a, b, c, d = test1.get_res(tag, 400)
    print(a, b, c, d)

    # # 模拟测试结果
    # sun_ab = a + b
    # a = 103
    # b = sun_ab - a

    bar = bar_base(a, b)
    pie = pie_base(a, b)
    nowdate = datetime.now().strftime('%Y_%m_%d')
    filepath = 'D:\\flaskProject\\history' + '\\' + nowdate

    file_list1 = os.listdir(filepath)
    file_list1.sort()
    if os.path.isdir(file_list1[-1]):
        last = file_list1.pop()
    else:
        last = file_list1[-2]
    print(last)

    data_csv = pd.read_csv(filepath + '\\' + last + '\\' + 'save.csv', sep=',')
    list1 = data_csv.values.tolist()

    show_lable = pd.read_csv(filepath + '\\' + last + '\\' + '\\data\\' + 'show_label.csv')
    show_data = pd.read_csv(filepath + '\\' + last + '\\' + '\\data\\' + 'show_data.csv')
    list_data = show_data.values.tolist()
    list_label = show_lable.values.tolist()
    list_data = [i[1] for i in list_data]
    k = 0
    list2_label_all = []
    for i in range(len(list_data) - 1):
        list2_label_all.append(list_label[k][0])
        if list_data[i] != list_data[i + 1]:
            k = k + 1
    list2_label_all.append(list_label[k][0])


    for i in range(len(list1)):
        list1[i].append(list_data[i])
        list1[i].append(list2_label_all[i])
        # list1[i].append(1)

    print(list1)
    return render_template('table.html', list=list1, bardata=bar.dump_options(), piedata=pie.dump_options(),
                           total_stream=a + b, usual=a, unusual=b)


@app.route('/detail_daily/<time>', methods=['POST', 'GET'])
def detail_daily(time):
    list1 = time.split(' ')
    list1[0] = list1[0]
    filepath = 'D:\\flaskProject\\history' + '\\' + list1[0][0:4] + '_' + list1[0][4:6] + '_' + list1[0][6:] + '\\' + \
               list1[1]
    show_lable = pd.read_csv(filepath + '\\data\\' + 'show_label.csv')
    show_data = pd.read_csv(filepath + '\\data\\' + 'show_data.csv')
    list_data = show_data.values.tolist()
    list_label = show_lable.values.tolist()
    list_data = [i[1] for i in list_data]
    k = 0
    list2_label_all = []
    for i in range(len(list_data) - 1):
        list2_label_all.append(list_label[k][0])
        if list_data[i] != list_data[i + 1]:
            k = k + 1
    list2_label_all.append(list_label[k][0])

    a = 0
    for i in list_label:
        if i[0] == 0:
            a = a + 1
    b = len(list_label) - a



    bar = bar_base(a, b)
    pie = pie_base(a, b)
    data_csv = pd.read_csv(filepath + '\\' + 'save.csv', sep=',')
    list1 = data_csv.values.tolist()


    for i in range(len(list1)):
        list1[i].append(list_data[i])
        list1[i].append(list2_label_all[i])



    return render_template('table.html', list=list1, bardata=bar.dump_options(), piedata=pie.dump_options(),
                           total_stream=a + b, usual=a, unusual=b)


@app.route('/ontime', methods=['POST', 'GET'])
def ontime():
    return render_template('ontime.html')


def getNet():
    i = 0
    send_list = []
    rcv_list = []
    while i < 20:
        sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
        recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
        time.sleep(1)
        sent_now = psutil.net_io_counters().bytes_sent
        recv_now = psutil.net_io_counters().bytes_recv
        sent = round((sent_now - sent_before) / 1024, 2)  # 算出1秒后的差值
        recv = round((recv_now - recv_before) / 1024, 2)

        send_list.append(sent)
        rcv_list.append(recv)

        i = i + 1

    return send_list, rcv_list


def get_refresh_json():
    # 首先获取带宽数据
    download, upload, ping, client = bandwidth_test()

    if not os.path.exists(dir):
        os.mkdir(dir)
    # 存储到csv中

    path = dir + '\\' + 'bw_test.csv'

    with open(path, 'a+', newline='') as f:
        csv_writer = csv.writer(f)
        data_row = [download, upload, ping, client]
        csv_writer.writerow(data_row)

    # 获取最后x组数据
    x = -4
    data_csv = pd.read_csv(path, header=None)
    list_bw = data_csv.values.tolist()
    list_bw_download = [i[0] for i in list_bw]
    list_bw_upload = [i[1] for i in list_bw]
    list_bw_ping = [i[2] for i in list_bw]

    list_bw_download = list_bw_download[x:]
    list_bw_upload = list_bw_upload[x:]
    list_bw_ping = list_bw_ping[x:]

    # 获取一组异常数据
    a, b, c, d = test1.get_res('0', 400)
    print(a, b, c, d)
    # sum_ab = a + b
    # b = 16
    # a = sum_ab - b

    # 获取该天的检测次数
    list_len = []
    list_dir = dir
    list_len.append(sum([os.path.isdir(list_dir + '\\' + list_index) for list_index in list_dir]))

    data = {'download': list_bw_download, 'upload': list_bw_upload, 'ping': list_bw_ping, 'a': a, 'b': b, 'c': c,
            'd': d, 'len': len(list_len), 'time': datetime.now().strftime('%Y_%m_%d %H:%M:%S')}

    return jsonify(data)


@app.route('/refresh112', methods=['POST', 'GET'])
def refresh112():
    if request.method == "POST":
        return get_refresh_json()


def pie_base(a, b) -> Pie:
    x_data = ['正常', '异常']
    y_data = [a, b]
    c = (
        Pie()
        .add("", [list(z) for z in zip(x_data, y_data)])
        .set_global_opts(title_opts=opts.TitleOpts(title="流量分类"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))

    )
    return c


def line_base(a, b) -> Line:
    x_index = [i for i in range(len(a))]
    # print(len(a))
    c = (
        Line()
        .add_xaxis(x_index)
        .add_yaxis("下载速度", a)
        .add_yaxis("上传速度", b)
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
    )
    return c


def line_base2(a) -> Line:
    x_index = [i for i in range(len(a))]
    # print(len(a))
    c = (
        Line()
        .add_xaxis(x_index)
        .add_yaxis("ping", a)
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
    )
    return c


def bar_base(a, b) -> Bar:
    c = (
        Bar(init_opts=opts.InitOpts())
        .add_xaxis(["正常", "异常"])
        .add_yaxis("流量监控", [a, b])
        .set_global_opts(
            # y 坐标轴配置项
            yaxis_opts=opts.AxisOpts(
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#000000")),  # 坐标轴轴线配置项
            ),
            # x 坐标轴配置项
            xaxis_opts=opts.AxisOpts(
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#000000")),  # # 坐标轴轴线配置项
            ),
            # 标题配置项
            title_opts=opts.TitleOpts(
                title=""
            ),
            # 图例配置项
            legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="#000000"), ),
        )
        # 系列配置项
        .set_series_opts(
            # 标签配置项
            label_opts=opts.LabelOpts(
                is_show=True,
                color="#000000"
            ),
            # 图元样式配置项
            itemstyle_opts={
                # 线性渐变，参考：https://pyecharts.org/#/zh-cn/series_options?id=itemstyleopts
                # 前四个参数分别是 x0, y0, x2, y2, 范围从 0 - 1，相当于在图形包围盒中的百分比，
                # 如果 globalCoord 为 `true`，则该四个值是绝对的像素位置
                "color": {
                    "type": 'linear',
                    "x": 0,
                    "y": 0,
                    "x2": 0,
                    "y2": 1,
                    "colorStops": [{
                        "offset": 0, "color": '#0781C3'  # 蓝色（头部）
                    }, {
                        "offset": 1, "color": '#06F6F8'  # 青色（底部）
                    }],
                },
            }
        )
    )
    return c


if __name__ == '__main__':
    app.run()
