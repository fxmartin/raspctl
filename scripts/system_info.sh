#! /bin/bash

# This script is meant for recolecting all the information of the system that
# will be displayed in the RaspCTL dashboard. The decision of creating a bash
# script instead of do the same job in Python is the simplicity of it. This
# command will be executed with the STDERR redirected to devnull(2>/dev/null)
# The valueable information must be printed to the STDOUT with the format:
#        NAME_OF_CONSTANT:{value}
# important to note that the colons are required and every metric must be
# expressed # just _ONE_ line. That's why I'm using "echo -n" because when
# printing the key I don't want a \n charater inserted at the end of the
# string. If you want to add more metrics, just take anotherone as example.

# Important note. Is is possible that if you delete some metric from here that
# is used in the dashboard, the dashboard will return a HTTP 500 code because
# it will not find the deleted item. Please when deleting items from this script
# check that you delete it from the dashboard template too. Having metrics that
# are not being used do not harm to anybody, so they can be left here.
# Important note2: In my laptop this command is executed with in 42 milli seconds,
# try to keep this time as lower as you can. This will prevent the dashboard to
# take ages to load. The execution time must be always lower than a second, keep
# this in mind.


# Just in case you have color options for GREP command
export GREP_OPTIONS='--color=none'


echo -n "USER:"
echo $USER

echo -n "HOSTNAME:"
hostname

echo -n "IP_ADDRESS:"
/sbin/ifconfig  | egrep "addr:([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)" -ho | grep -v 127 | head -1 | cut -d":" -f2

echo -n "MEMORY_TOTAL:"
total=`cat /proc/meminfo | grep MemTotal | egrep [0-9]+ -ho`
echo $total

echo -n "USED_MEMORY:"
used=`cat /proc/meminfo | grep "Active:" | egrep [0-9]+ -ho`
echo $used

free=$(($total-$used))
echo -n "FREE_MEMORY:"
echo $free

echo -n "DISK_TOTAL:"
df -h | grep "rootfs.*/$" --color=none  | awk '{print $2}'

echo -n "DISK_USED:"
df -h | grep "rootfs.*/$" --color=none  | awk '{print $3}'


echo -n "DISK_FREE:"
df -h | grep "rootfs.*/$" --color=none  | awk '{print $4}'

echo -n "UPTIME:"
uptime  | awk '{print $3}' | tr -d ','

echo -n "LOAD_AVG:"
uptime  | awk '{print $8, $9, $10}' | tr -d ","

echo -n "PROCESSOR_NAME:"
cat /proc/cpuinfo  | grep "model name" | sort -u | egrep ":.*$" -ho | tr -d ":"

echo -n "PROCESSOR_BOGOMITS:"
cat /proc/cpuinfo  | grep "bogomips" | head -1 | egrep ":.*$" -ho | tr -d ":"

echo -n "PROCESSOR_CURRENT_SPEED:"
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq

echo -n "PROCESSOR_OVERLOCK:"
cat /boot/config.txt | grep arm_freq --color=none | egrep  [0-9]+ -ho
