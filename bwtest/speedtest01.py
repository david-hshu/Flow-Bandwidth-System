import speedtest   # 导入speedtest_cli

print("准备测试ing...")

# 创建实例对象
test = speedtest.Speedtest()
# 获取可用于测试的服务器列表
test.get_servers()
# 筛选出最佳服务器
best = test.get_best_server()

print("正在测试ing...")

# 下载速度
download_speed = int(test.download() / 1024 / 1024)
# 上传速度
upload_speed = int(test.upload() / 1024 / 1024)

# 输出结果
print("下载速度：" + str(download_speed) + " Mbits")
print("上传速度：" + str(upload_speed) + " Mbits")

test.results.share()