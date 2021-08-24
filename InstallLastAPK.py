#-- coding:UTF-8 --
import os
import re
import subprocess
import sys
import time
import requests
import json
import datetime
import pymysql

def logger(msg):
    currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('%s  %s' % (currentTime, msg))

def uninstallAndInstall(platform, installUrl):
    if (platform == "Android"):
        utils_exec_shell('rm -rf *.apk')
        logger("删除Jenkins项目下历史荔枝apk安装包成功")
        downloadcommand = 'wget -q ' + installUrl
        utils_exec_shell(downloadcommand)
        logger("下载荔枝安装包成功")
        check_apk_exist=utils_exec_shell('adb -s XPC0220728002697 shell pm list packages | grep package:com.yibasan.lizhifm')
        if('com.yibasan.lizhifm' in check_apk_exist):
            logger("卸载荔枝APP")
            utils_exec_shell('adb -s XPC0220728002697 uninstall com.yibasan.lizhifm')
            logger("安装荔枝APP")
            utils_exec_shell('adb -s XPC0220728002697 install ./*.apk')
        else:
            logger("手机未安装荔枝APP")
            logger("安装荔枝APP")
            utils_exec_shell('adb -s XPC0220728002697 install ./*.apk')
    elif (platform == "iOS"):
        utils_exec_shell('rm -rf *.ipa')
        logger("删除Jenkins项目下历史荔枝ipa安装包成功")
        downloadcommand = 'wget -q ' + installUrl
        utils_exec_shell(downloadcommand)
        logger("下载荔枝安装包成功")
        check_apk_exist=utils_exec_shell('ideviceinstaller -l -u 00008030-000E4DD60EF9802E | grep com.lizhi.lizhifm')
        if('com.lizhi.lizhifm' in check_apk_exist):
            logger("卸载荔枝APP")
            utils_exec_shell('ideviceinstaller -U com.lizhi.lizhifm -u 00008030-000E4DD60EF9802E')
            logger("安装荔枝APP")
            utils_exec_shell('ideviceinstaller -i ./*.ipa -u 00008030-000E4DD60EF9802E')
        else:
            logger("手机未安装荔枝APP")
            logger("安装荔枝APP")
            utils_exec_shell('ideviceinstaller -i ./*.ipa -u 00008030-000E4DD60EF9802E')

def check_devices(platform):
    if (platform == "Android"):
        command = 'adb devices'
        devices_list = utils_exec_shell(command)
        if('XPC0220728002697' in devices_list):
            logger("XPC0220728002697自动化设备已连接")
        else:
            logger("XPC0220728002697自动化设备未连接，请检查")
    elif (platform == "iOS"):
        command = 'idevice_id -l'
        devices_list =utils_exec_shell(command)
        if ('00008030-000E4DD60EF9802E' in devices_list):
            logger("00008030-000E4DD60EF9802E自动化设备已连接")
        else:
            logger("00008030-000E4DD60EF9802E自动化设备未连接，请检查")

'''用于执行shell命令并返回执行的结果，用subprocess.Popen实现'''
def utils_exec_shell(command):
    logger('utils_exec_shell: ' + command + '\n')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    if (p.returncode == 0) :
        logger("终端执行shell命令(" + command + ")成功 " + out[0].decode())
    else:
        logger("终端执行shell命令(" + command + ")失败 " + out[0].decode())
    return out[0].decode()

'''安装完成后的安卓荔枝app，使用adb授权权限'''
def adb_grant_permission():
    utils_exec_shell('adb -s XPC0220728002697 -d shell pm grant com.yibasan.lizhifm android.permission.CAMERA')
    utils_exec_shell('adb -s XPC0220728002697 -d shell pm grant com.yibasan.lizhifm android.permission.READ_PHONE_STATE')
    utils_exec_shell('adb -s XPC0220728002697 -d shell pm grant com.yibasan.lizhifm android.permission.READ_EXTERNAL_STORAGE')
    utils_exec_shell('adb -s XPC0220728002697 -d shell pm grant com.yibasan.lizhifm android.permission.WRITE_EXTERNAL_STORAGE')
    utils_exec_shell('adb -s XPC0220728002697 -d shell pm grant com.yibasan.lizhifm android.permission.ACCESS_COARSE_LOCATION')
    utils_exec_shell('adb -s XPC0220728002697 -d shell pm grant com.yibasan.lizhifm android.permission.RECORD_AUDIO')


if __name__ == '__main__':
    logger(len(sys.argv))
    if(len(sys.argv) == 3):
        installUrl = sys.argv[2]
    else:
        logger("缺少执行Python脚本入参")
        sys.exit(0)
    platform = sys.argv[1]
    check_devices(platform)
    uninstallAndInstall(platform, installUrl)
    if(platform == "Android"):
        adb_grant_permission()
