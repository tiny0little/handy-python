#!/bin/bash

SPACER="---------------------------------------"
TEMP_FILE="/tmp/disk_health.tmp"
SMARTCTL="sudo smartctl -a"

AWK_GREENB='\033[0;41m'    #Green Background (Color verde de fondo)
AWK_GREEN='\033[0;32m'     #Green Text (Color verde en el texto
AWK_REDB='\033[0;41m'      #Red Background (Color rojo de fondo)
AWK_RED='\033[0;31m'       #Red text (Color rojo en el texto)
AWK_NORMALB='\033[0;49m'   #Default background (Color por defecto de fondo)
AWK_NORMAL='\033[0m'       #Default foreground (Color por defecto del texto)

ECHO_BOLD='\e[1m'
ECHO_GREEN='\e[92m'
ECHO_RED='\e[91m'
ECHO_NOFORMAT='\e[0m'

rm -f $TEMP_FILE

$SMARTCTL /dev/nvme1n1 | egrep "Model|Temperature|Written|Hour|Capacity" | egrep -v "Warn|Criti" > $TEMP_FILE
cat $TEMP_FILE | grep Model | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "   : " $2}'
cat $TEMP_FILE | grep Tempe | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "    : " $2}'
echo -en "\e[0mCapacity       : $ECHO_GREEN$ECHO_BOLD" && cat $TEMP_FILE | grep Capacity | cut -d'[' -f2 | cut -d']' -f1 && echo -en $ECHO_NOFORMAT
cat $TEMP_FILE | grep Hour  | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 " : \033[1;31m" $2 "\033[0m"}'
echo -ne "\e[0mData Written   : $ECHO_RED$ECHO_BOLD" && cat $TEMP_FILE | grep Writt | cut -d'[' -f2 | cut -d']' -f1 && echo -en $ECHO_NOFORMAT


echo $SPACER


$SMARTCTL /dev/nvme0n1 | egrep "Model|Temperature|Written|Hour|Capacity" | egrep -v "Warn|Criti|Sensor|Size|Unallocated" > $TEMP_FILE
cat $TEMP_FILE | grep Model | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "   : " $2}'
cat $TEMP_FILE | grep Tempe | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "    : " $2}'
echo -en "\e[0mCapacity       : $ECHO_GREEN$ECHO_BOLD" && cat $TEMP_FILE | grep Capacity | cut -d'[' -f2 | cut -d']' -f1 && echo -en "\e[0m"
cat $TEMP_FILE | grep Hour  | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 " : \033[1;31m" $2 "\033[0m"}'
echo -en "\e[0mData Written   : $ECHO_RED$ECHO_BOLD" && cat $TEMP_FILE | grep Writt | cut -d'[' -f2 | cut -d']' -f1 && echo -en "\e[0m"


echo $SPACER


$SMARTCTL /dev/sdb | egrep "Model|Temperature|Host_Writes|Hour|Capacity" > $TEMP_FILE
cat $TEMP_FILE | grep Model | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "   : " $2}'
echo -en "\e[0mCapacity       : $ECHO_GREEN$ECHO_BOLD" && cat $TEMP_FILE | grep Capacity | cut -d'[' -f2 | cut -d']' -f1 && echo -en "\e[0m"
echo -en "\e[0mTemperature    : " && cat $TEMP_FILE | grep Temp | awk '{print $10 " Celsius"}' && echo -en "\e[0m"
echo -en "\e[0mPower On Hours : " && cat $TEMP_FILE | grep Hour | awk '{print "\033[1;31m" $10 "\033[0m"}' && echo -en "\e[0m"
echo -en "\e[0mData Written   : $ECHO_RED$ECHO_BOLD" && cat $TEMP_FILE | grep Writ | awk '{printf "%.2f TB\n", $10/1024}' && echo -en "\e[0m"


echo $SPACER


$SMARTCTL /dev/sda | egrep "Model|Temperature|Hour|Capacity" | egrep -v "Fly|194" > $TEMP_FILE
cat $TEMP_FILE | grep Model | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "   : " $2}'
echo -en "\e[0mCapacity       : \e[92m$ECHO_BOLD" && cat $TEMP_FILE | grep Capacity | cut -d'[' -f2 | cut -d']' -f1
echo -en "\e[0mTemperature    : " && cat $TEMP_FILE | grep Temp | awk '{print $10 " Celsius"}'
echo -en "\e[0mPower On Hours : " && cat $TEMP_FILE | grep Hour | awk '{print "\033[1;31m" $10 "\033[0m"}'


echo $SPACER


$SMARTCTL /dev/sdc | egrep "Model|Temperature|Hour|Capacity" | egrep -v "Fly" > $TEMP_FILE
cat $TEMP_FILE | grep Model | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "   : " $2}'
echo -en "\e[0mCapacity       : \e[92m$ECHO_BOLD" && cat $TEMP_FILE | grep Capacity | cut -d'[' -f2 | cut -d']' -f1
echo -en "\e[0mTemperature    : " && cat $TEMP_FILE | grep Temp | awk '{print $10 " Celsius"}'
echo -en "\e[0mPower On Hours : " && cat $TEMP_FILE | grep Hour | awk '{print "\033[1;31m" $10 "\033[0m"}'



rm -f $TEMP_FILE

