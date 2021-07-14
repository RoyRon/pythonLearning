# -- coding:UTF-8 --
import datetime
import os
import random
import re
import subprocess
import sys
import time

import pymysql

from MonkeyConfigUtil import get_property_byname

package_name = get_property_byname("Bussiness", "package")
mainactivty = get_property_byname("Bussiness", "mainact")
logpath = get_property_byname("Bussiness", "logpath")
deviceid = get_property_byname("Bussiness", "deviceid")
run_times = int(get_property_byname("Bussiness", "runtimes"))  # 事件的个数
throttle = int(get_property_byname("Bussiness", "throttle"))  # 操作（即事件）间的时延，单位是毫秒
# 以下设置事件类型的百分比
pct_touch = int(get_property_byname("Bussiness", "pct_touch"))  # 触摸事件的百分比(触摸事件是一个down-up事件，它发生在屏幕上的某单一位置)
pct_motion = int(get_property_byname("Bussiness", "pct_motion"))  # 动作事件的百分比(动作事件由屏幕上某处的一个down事件、一系列的伪随机事件和一个up事件组成)
pct_trackball = int(get_property_byname("Bussiness", "pct_trackball"))  # 轨迹事件的百分比(轨迹事件由一个或几个随机的移动组成，有时还伴随有点击)
pct_nav = int(get_property_byname("Bussiness", "pct_nav"))  # “基本”导航事件的百分比(导航事件由来自方向输入设备的up/down/left/right组成)
pct_majornav = int(get_property_byname("Bussiness", "pct_majornav"))  # “主要”导航事件的百分比(这些导航事件通常引发图形界面中的动作，如：5-way键盘的中间按键、回退按键、菜单按键)
pct_syskeys = int(get_property_byname("Bussiness", "pct_syskeys"))  # “系统”按键事件的百分比(这些按键通常被保留，由系统使用，如Home、Back、Start Call、End Call及音量控制键)
pct_appswitch = int(get_property_byname("Bussiness", "pct_appswitch"))  # 启动Activity的百分比。在随机间隔里，Monkey将执行一个startActivity()调用，作为最大程度覆盖包中全部Activity的一种方法
pct_anyevent = int(get_property_byname("Bussiness", "pct_anyevent"))  # 其它类型事件的百分比。它包罗了所有其它类型的事件，如：按键、其它不常用的设备按钮、等等


def uninstallAndInstall(apkUrl):
    logger("apkurl---------------->" + apkUrl)
    if apkUrl == '0':
        logger("无apk下载链接，使用本地荔枝APP安装包进行monkey测试")
    else:
        utils_exec_shell('adb -s ' + deviceid + ' uninstall ' + package_name)
        logger("卸载本地荔枝apk成功")
        utils_exec_shell('rm -rf *.apk')
        logger("删除Jenkins项目下历史荔枝apk安装包成功")
        utils_exec_shell('wget -q $apk_url')
        logger("下载荔枝安装包成功")
        log = utils_exec_shell('adb -s ' + deviceid + ' install ./*.apk')
        if 'Failure' in log:
            logger("下载或者安装荔枝APP失败")
            exit()
        elif 'error' in log:
            logger("下载或者安装荔枝APP失败")
            exit()
        else:
            logger("安装荔枝APP成功")


def logger(msg):
    currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('%s  %s' % (currentTime, msg))


def get_devices_list():
    command = 'adb devices'
    devices_list = utils_exec_shell(command).replace('\n', '').replace('\t', '').split('List of devices attached')[
        1].strip().split('device')
    for index in range(len(devices_list)):
        if devices_list[index] == '':
            del devices_list[index]
    logger("检测到连接了(%d)台设备:%s" % (len(devices_list), devices_list))
    return devices_list


'''用于执行shell命令并返回执行的结果，用subprocess.Popen实现'''


def utils_exec_shell(command):
    logger('utils_exec_shell: ' + command + '\n')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    logger("终端执行命令结果： " + out[0].decode())
    return out[0].decode()


def get_monkey_command_with_seed(seed=7):
    monkey_command_raw = 'shell monkey -p %s %d --ignore-crashes --ignore-timeouts -ignore-security-exceptions --kill-process-after-error --throttle %d --pct-touch %d --pct-motion %d ' \
                         '--pct-appswitch %d  --pct-syskeys %d --pct-anyevent %d --pct-majornav %d --pct-nav %d --pct-trackball %d -s %d' % (
                             package_name, run_times, throttle, pct_touch, pct_motion, pct_appswitch, pct_syskeys,
                             pct_anyevent, pct_majornav, pct_nav, pct_trackball, seed)
    return monkey_command_raw


def run_monkey_by_serialno(rounds=1):
    devices_list = get_devices_list()
    if len(devices_list) == 0:
        logger("没有连上安卓设备，请检查！")
        exit()
    for round in range(rounds):
        seed = int(random.random() * 1000)
        logger('已经开始执行第%d/%d次，seed=%d' % (round + 1, rounds, seed))
        utils_exec_shell('adb -s ' + deviceid + ' shell am start -n ' + mainactivty)
        time.sleep(6)
        utils_exec_shell('adb -s ' + deviceid + ' ' + get_monkey_command_with_seed(seed))
        logger('执行完第%d/%d次' % (round + 1, rounds))
        time.sleep(5)
        utils_exec_shell('adb -s ' + deviceid + ' shell am force-stop ' + package_name)
        time.sleep(2)
        utils_exec_shell('adb -s ' + deviceid + ' shell am force-stop ' + package_name)
        time.sleep(2)
        utils_exec_shell('adb -s ' + deviceid + ' shell am force-stop ' + package_name)


def pull_parser_logan():
    """复制手机中日志文件到电脑指定目录，并删除手机中的日志"""
    logger("------------------>开始解析monkey日志~")
    devices_list = get_devices_list()
    if len(devices_list) == 0:
        logger("没有连上安卓设备，请检查！")
        exit()

    """创建当前日期时间的文件夹存放从手机中辅助过来的日志文件"""
    now_date = datetime.datetime.now().strftime('%Y%m')
    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M')
    currentpath = utils_exec_shell("pwd")
    rootPath = currentpath.replace("\n", "") + "/"
    storeFilePath = rootPath + now_date + "/" + now_time
    utils_exec_shell("mkdir " + rootPath + now_date)
    utils_exec_shell("mkdir " + storeFilePath)
    data = utils_exec_shell("adb -s " + deviceid + " pull  " + logpath + ' ' + rootPath + now_date + "/" + now_time)
    if "pulled" in data:
        logger("成功复制手机日志到指定目录~")
    else:
        logger("拉取手机日志失败或者该手机中没有荔枝日志文件~")
        exit()

    """遍历出日志文件夹下面所有的文件，并进行解密"""
    files = []
    for file in os.walk(storeFilePath + "/log"):
        for childFile in file[2]:
            files.append(file[0] + "/" + childFile)
    logger("本次monkey日志文件总数为：" + str(len(files)))
    logger("开始解密日志：")
    for filePath in files:
        data1 = utils_exec_shell("java -jar " + rootPath + "LogzParsernew.jar " + filePath)
        logger("解密工具内部错误，不影响解密日志~")
        logger(data1)
    logFiles = []
    for file in os.walk(storeFilePath):
        for childFile in file[2]:
            if "dec" in childFile:
                logFiles.append(file[0] + "/" + childFile)
    return logFiles


def write_run_info_in_mysql(conn, cursor, totalCount, version, buildVersion, branchName):
    """把monkey运行信息存入数据库"""
    cursor.executemany("INSERT INTO android_run_number VALUES(null,%s,%s,%s,%s,CURRENT_TIME,CURRENT_TIME,'荔枝')",
                       [(totalCount, buildVersion, version, branchName)])
    conn.commit()
    cursor.execute(" select id FROM android_run_number ORDER BY id DESC LIMIT 0,1")
    runNumberId = cursor.fetchall()
    return runNumberId[0][0]


def write_error_info_in_mysql(runNumberId, count, version, buildVersion, errorName, errorDetail, branchName):
    """把解析后的异常信息存入数据库"""
    conn = pymysql.connect(host='172.17.6.232', port=3306, user='fmuser', passwd='fmpass', db='monkeytest')
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO android_monkey_result VALUES(null,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIME,CURRENT_TIME,DEFAULT)",
        [(runNumberId, count, buildVersion, version, branchName, errorName, errorDetail)])
    conn.commit()
    cursor.close()
    conn.close()


def analysis_log(logFiles, branchName):
    """循环读取每个文件，并按行读取文件内容"""
    exceptionList = []
    version = ''
    buildVersion = ''
    for logFile in logFiles:
        logger("当前解析的日志文件为：" + logFile)
        with open(logFile) as f:
            lines = f.readlines()
        """逐行解析日志文件，获取对应的值"""
        msg = ''
        next = False
        num = 1
        for each_line in lines:
            if version == '':
                if '"clientVersion":' in each_line:
                    version = re.findall(r'"clientVersion":"(.*?)",', each_line)[0]
            if buildVersion == '':
                if 'buildVersion' in each_line:
                    buildVersion = re.findall(r'"buildVersion":(.*?),', each_line)[0]
            """排除一些不需要查看的异常"""
            if 'java.lang.' in each_line:
                if 'Exception' in each_line:
                    if 'SocketException' not in each_line:
                        if 'DeadObjectException' not in each_line:
                            if 'ConnectException' not in each_line:
                                if 'ConnectException' not in each_line:
                                    if 'UnknownHostException' not in each_line:
                                        if 'SocketTimeoutException' not in each_line:
                                            if 'kotlinx' not in each_line:
                                                if 'OnlineTempFileUtils' not in each_line:
                                                    if msg == '' and 'Caused by' not in each_line:
                                                        # logger(each_line)
                                                        msg += '<p>' + each_line
                                                        next = True
            elif next:
                """查看异常日志有没有堆栈at符号"""
                matchObj = re.match("\\s+at", each_line)
                if num == 1:
                    if matchObj:
                        msg += '<br>' + each_line
                        num = 5
                    else:
                        num += 1
                elif num == 2:
                    if matchObj:
                        msg += '<br>' + each_line
                        num = 5
                    else:
                        num += 1
                elif num == 3:
                    if matchObj:
                        msg += '<br>' + each_line
                        num = 5
                    else:
                        num += 1
                elif num == 4:
                    if matchObj:
                        msg += '<br>' + each_line
                        num += 1
                    else:
                        num = 1
                        msg = ''
                        next = False
                elif num == 5:
                    if each_line == '\n':
                        msg += '<p>'
                        exceptionList.append(msg)
                        msg = ''
                        next = False
                        num = 1
                    else:
                        msg += '<br>' + each_line

    if len(exceptionList) == 0:
        logger("----------> monkey的运行日志，没有异常堆栈信息，程序结束~")
        exit()

    """第一次去除重复堆栈信息"""
    num = 1
    number = 1
    tempExceptionList = []
    newTempExceptions = ''
    tempExceptions = ''
    newExceptionList = []
    newExceptionDict = {}
    for exception in exceptionList:
        if exception not in tempExceptionList:
            tempExceptionList.append(exception)
        else:
            logger("第一次堆栈信息去重第 " + str(number) + " 条中...")
            number += 1

    """第二次排除时间影响精确去除重复堆栈信息"""
    for exception in tempExceptionList:
        exceptionBody = exception.split('\n', 1)[1]
        tempExceptions += exception
        if exceptionBody not in newTempExceptions:
            newExceptionList.append(exception)
            newTempExceptions += exceptionBody
        else:
            num += 1
            logger("第二次精确堆栈信息去重第 " + str(num) + " 条中...")

    """最后统计每个堆栈出现的相同次数"""
    for exception in newExceptionList:
        exceptionBody = exception.split('\n', 1)[1]
        count = tempExceptions.count(exceptionBody)
        newExceptionDict[exception] = count
    logger("monkey日志解析完成~")

    logger("将解析后的日志存入数据库中")
    totalCount = len(tempExceptionList)
    conn = pymysql.connect(host='172.17.6.232', port=3306, user='fmuser', passwd='fmpass', db='monkeytest')
    cursor = conn.cursor()
    runNumberId = write_run_info_in_mysql(conn, cursor, totalCount, version, buildVersion, branchName)

    """向数据库写入数据"""
    for item, countNum in newExceptionDict.items():
        count = countNum
        logger("正在写入数据库中...")
        # errorName = re.findall(r'lang.(.*?)Exception', item.split('\n', 1)[0])[0] + 'Exception'
        errorName = item.split('\n', 1)[0].replace('<p>', '')
        errorDetail = item
        write_error_info_in_mysql(runNumberId, count, version, buildVersion, errorName, errorDetail, branchName)
        conn.commit()
    cursor.close()
    conn.close()
    logger("monkey日志异常信息存入数据库成功~")
    utils_exec_shell("adb -s " + deviceid + " shell rm -rf " + logpath)
    logger("monkey日志解析完成，并删除手机日志文件成功~")


if __name__ == '__main__':
    branchName = sys.argv[2]
    apkUrl = sys.argv[3]
    uninstallAndInstall(apkUrl)
    run_monkey_by_serialno(int(sys.argv[1]))
    logFiles = pull_parser_logan()
    analysis_log(logFiles, branchName)
