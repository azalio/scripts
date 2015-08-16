#!/usr/bin/env bash
# Description:  Script for iostat monitoring
# Author:       Petrov Mikhail azalio@azalio.net

SECONDS=8
FILE=/tmp/iostat
IOSTAT=`which iostat` ;

if [[ $? -ne 0 ]]; then
	echo "Please, install sysstat"
	exit 1
fi

DISK=$(LC_NUMERIC="C" $IOSTAT -xy 1 $SECONDS | awk 'BEGIN {check=0;} {if(check==1 && $1=="avg-cpu:"){check=0}if(check==1 && $1!=""){print $0}if($1=="Device:"){check=1}}' | tr '\n' '|')
echo $DISK | sed 's/|/\n/g' > $FILE

$IOSTAT -d | tail -n +4 | sed "/^$/d" | awk '{print $1}' | while read line; do 

	grep -w $line $FILE | tr -s ' ' | awk -v disk="$line" 'BEGIN {io[2] = "rrqm";io[3] = "wrqm";io[4] = "r"; io[5] = "w"; io[6] = "rkB"; io[7] = "wKB"; io[8] = "avgrq-sz"; io[9] = "avgqu-sz"; io[10] = "await"; io[11] = "r_await"; io[12] = "w_await"; io[13] = "svctm"; io[14] = "util"} {for (i=1;i<=NF;i++){a[i]+=$i;}} END {for (i=1;i<=NF;i++){printf "%s.%s = %.2f", disk,io[i],a[i]/NR; printf "\n"}}' | tail -n +2

done

rm $FILE
