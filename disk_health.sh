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

$SMARTCTL > /dev/null 2> /dev/null
rm -f $TEMP_FILE
echo $SPACER
echo SSD SSD SSD SSD SSD SSD SSD SSD SSD SSD
echo $SPACER



$SMARTCTL /dev/disk/by-uuid/fd99d5cd-705d-410b-8555-6c0930c1df67 | egrep "Model|Temperature|Written|Hour|Capacity" | egrep -v "Warn|Criti" > $TEMP_FILE
cat $TEMP_FILE | grep Model | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "   : " $2}'
cat $TEMP_FILE | grep Tempe | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "    : " $2}'
echo -en "\e[0mCapacity       : $ECHO_GREEN$ECHO_BOLD" && cat $TEMP_FILE | grep Capacity | cut -d'[' -f2 | cut -d']' -f1 && echo -en $ECHO_NOFORMAT
cat $TEMP_FILE | grep Hour  | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 " : \033[1;31m" $2 "\033[0m"}'
echo -ne "\e[0mData Written   : $ECHO_RED$ECHO_BOLD" && cat $TEMP_FILE | grep Writt | cut -d'[' -f2 | cut -d']' -f1 && echo -en $ECHO_NOFORMAT


echo $SPACER


$SMARTCTL /dev/disk/by-uuid/e6167454-2a83-4df4-b3e8-21d78bd4231f | egrep "Model|Temperature|Written|Hour|Capacity" | egrep -v "Warn|Criti|Sensor|Size|Unallocated" > $TEMP_FILE
cat $TEMP_FILE | grep Model | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "   : " $2}'
cat $TEMP_FILE | grep Tempe | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "    : " $2}'
echo -en "\e[0mCapacity       : $ECHO_GREEN$ECHO_BOLD" && cat $TEMP_FILE | grep Capacity | cut -d'[' -f2 | cut -d']' -f1 && echo -en "\e[0m"
cat $TEMP_FILE | grep Hour  | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 " : \033[1;31m" $2 "\033[0m"}'
echo -en "\e[0mData Written   : $ECHO_RED$ECHO_BOLD" && cat $TEMP_FILE | grep Writt | cut -d'[' -f2 | cut -d']' -f1 && echo -en "\e[0m"


echo $SPACER

$SMARTCTL /dev/disk/by-uuid/47c27470-ead0-4810-b5be-0318e0123f38 | egrep "Model|Temperature|Host_Writes|Hour|Capacity" > $TEMP_FILE
cat $TEMP_FILE | grep Model | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "   : " $2}'
echo -en "\e[0mCapacity       : $ECHO_GREEN$ECHO_BOLD" && cat $TEMP_FILE | grep Capacity | cut -d'[' -f2 | cut -d']' -f1 && echo -en "\e[0m"
echo -en "\e[0mTemperature    : " && cat $TEMP_FILE | grep Temp | awk '{print $10 " Celsius"}' && echo -en "\e[0m"
echo -en "\e[0mPower On Hours : " && cat $TEMP_FILE | grep Hour | awk '{print "\033[1;31m" $10 "\033[0m"}' && echo -en "\e[0m"
echo -en "\e[0mData Written   : $ECHO_RED$ECHO_BOLD" && cat $TEMP_FILE | grep Writ | awk '{printf "%.2f TB\n", $10/1024}' && echo -en "\e[0m"


echo
echo $SPACER
echo HDD HDD HDD HDD HDD HDD HDD HDD HDD HDD
echo $SPACER




$SMARTCTL /dev/disk/by-uuid/badfa509-cf21-4f5f-9eb3-bdd4043e1316 | egrep "Model|Temperature|Hour|Capacity" | egrep -v "Fly|194" > $TEMP_FILE
cat $TEMP_FILE | grep Model | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "   : " $2}'
echo -en "\e[0mCapacity       : \e[92m$ECHO_BOLD" && cat $TEMP_FILE | grep Capacity | cut -d'[' -f2 | cut -d']' -f1
echo -en "\e[0mTemperature    : " && cat $TEMP_FILE | grep Temp | awk '{print $10 " Celsius"}'
echo -en "\e[0mPower On Hours : " && cat $TEMP_FILE | grep Hour | awk '{print "\033[1;31m" $10 "\033[0m"}'


echo $SPACER


$SMARTCTL /dev/disk/by-uuid/cc77b748-8011-404b-8120-ee780bb88c1f | egrep "Model|Temperature|Hour|Capacity" | egrep -v "Fly|Loaded" > $TEMP_FILE
cat $TEMP_FILE | grep Model | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "   : " $2}'
echo -en "\e[0mCapacity       : \e[92m$ECHO_BOLD" && cat $TEMP_FILE | grep Capacity | cut -d'[' -f2 | cut -d']' -f1
echo -en "\e[0mTemperature    : " && cat $TEMP_FILE | grep Temp | awk '{print $10 " Celsius"}'
echo -en "\e[0mPower On Hours : " && cat $TEMP_FILE | grep Hour | awk '{print "\033[1;31m" $10 "\033[0m"}'



echo $SPACER

echo "*** USB DRIVE"
$SMARTCTL /dev/sdd | egrep "Model|Temperature|Hour|Capacity" | egrep -v "Fly|Loaded" > $TEMP_FILE
cat $TEMP_FILE | grep Model | awk -F':' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $1 "   : " $2}'
echo -en "\e[0mCapacity       : \e[92m$ECHO_BOLD" && cat $TEMP_FILE | grep Capacity | cut -d'[' -f2 | cut -d']' -f1
echo -en "\e[0mTemperature    : " && cat $TEMP_FILE | grep Temp | awk '{print $10 " Celsius"}'
echo -en "\e[0mPower On Hours : " && cat $TEMP_FILE | grep Hour | awk '{print "\033[1;31m" $10 "\033[0m"}'




rm -f $TEMP_FILE

