#!/usr/bin/env python
###
# Version 1.0 - ali/28.11.2022
# Monitoring Adva WDM alarm state
###
# Version 1.1 - ali/11.12.2022
# Cleanup
###
# Nagios Exit-Codes:
# 0 = OK
# 1 = WARNING
# 2 = CRITICAL
# 3 = UNKNOWN
###
# Name:    aosCoreAlarmCondDescr
# OID:     1.3.6.1.4.1.2544.1.20.1.1.1.1.1.5
# MIB:     AOS-CORE-ALARM-MIB
# Type:    OctetString
# Descr:   Text that describes the alarm condition.
# Example: Fan filter needs replacement
###


import sys
import re
import subprocess


def main(switchhostname, snmpcommunity):

    regex_string = re.compile(r'=\sSTRING:\s"(.+)"')
    alarmstate_list = []
    alarmstate_str = []

#   gather facts
    p = subprocess.Popen("snmpwalk " + switchhostname + " -v 2c -c " + snmpcommunity + " 1.3.6.1.4.1.2544.1.20.1.1.1.1.1.5",shell=True,stdout=subprocess.PIPE)
#   read output from subprocess and decode bytes to string as utf-8
    alarmstate_proc = p.stdout.read().decode('utf-8')

    try:

#       split new-lines to extract state
        alarmstate_list = alarmstate_proc.splitlines()

#       extract alarms using regex and append to new list
        for line in alarmstate_list:
            alarmstate_str.append(regex_string.search(line).group(1))

    except Exception as e:
        print("UNKNOWN - An error occured | alarm_state=3;1;2;0;3")
        print("%s" % e)
        sys.exit(3)

#   check if there is an alarm present
    if len(alarmstate_str):
        print("CRITICAL - Alarm present")
        for line in alarmstate_str:
            print("%s" % line)
        print("| alarm_state=2;1;2;0;3")
        sys.exit(2)
    else:
        print("OK - No alarms present | alarm_state=0;1;2;0;3")
        sys.exit(0)


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("\n\t[*] check_adva_alarms 1.1 [*]")
        print("\n\tUsage: check_adva_alarms.py HOSTNAME SNMPCOMMUNITY")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
