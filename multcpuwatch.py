import csv
import os
import time

# 监控多核cpu资源信息
class MonitoringMultiCpuResources(object):
    def __init__(self, count):
        self.counter = count
        self.alldata = [("timestamp", "cputype ","multicpustatus")]
    # 单次执行监控过程
    def monitoring(self):
        last_idle = last_total = 0
        result = os.popen("adb shell cat /proc/stat")
        line = result.readline();
        keyword = "cpu";
        while line:
            if (keyword in line):
                cputypename = line.split()[0];
                fields = [float(column) for column in line.split()[1:]]
                idle, total = fields[3], sum(fields)
                idle_delta, total_delta = idle - last_idle, total - last_total
                last_idle, last_total = idle, total
                if (total_delta != 0):
                    utilisation = 100.0 * (1.0 - idle_delta / total_delta)
                    currenttime = self.getCurrentTime()
                    print("multicpu current time is: "+ currenttime +", multicpu current cputypename is: "+ cputypename + ' , multicpu used is: %5.1f%%' % utilisation)
                    self.alldata.append([currenttime,cputypename,utilisation])
                    self.SaveDataToCSV()
                line = result.readline();
            else :
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
        csvfile = open('multicpustatus.csv', 'w',encoding='utf8',newline='')
        writer = csv.writer(csvfile)
        writer.writerows(self.alldata)
        csvfile.close()
if __name__ == "__main__":
    monitoringMultiCpuResources = MonitoringMultiCpuResources(100000)
    monitoringMultiCpuResources.run()