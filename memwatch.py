# /usr/bin/python
# encoding:utf-8
import csv
import os
import time

# 监控内存资源信息
class MonitoringMemResources(object):
    def __init__(self, count):
        self.counter = count
        self.alldata = [("timestamp", "memstatus")]
    # 单次执行监控过程
    def monitoring(self):
        result = os.popen("adb shell dumpsys meminfo com.qq.qcloud")
        line = result.readline();
        keyword = "TOTAL";
        while line:
            if (keyword in line):
                memvalue = line.split()[1];
                currenttime = self.getCurrentTime()
                print("mem current time is:" + currenttime + ", mem used is: " + memvalue)
                self.alldata.append([currenttime, memvalue])
                self.SaveDataToCSV()
                break
            else:
                line = result.readline();
    # 多次执行监控过程
    def run(self):
        while self.counter > 0:
            self.monitoring()
            self.counter = self.counter - 1
            time.sleep(3)
    # 获取当前的时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%H:%M:%S", time.localtime())
        return currentTime
    # 数据的存储
    def SaveDataToCSV(self):
        csvfile = open('memstatus.csv', 'w',encoding='utf8',newline='')
        writer = csv.writer(csvfile)
        writer.writerows(self.alldata)
        csvfile.close()
if __name__ == "__main__":
    monitoringMemResources = MonitoringMemResources(100000)
    monitoringMemResources.run()