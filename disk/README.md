Script for collect iostat data.  
Add it in cron and send the data to your preferred charting system.  

http://habrahabr.ru/post/220073/  

Disk await — отзывчивость устройства (r_await, w_await);  
Disk merges — операции слияния в очереди (rrqm/s, wrqm/s);  
Disk queue — состояние очереди (avgrq-sz, avgqu-sz);  
Disk read and write — текущие значения чтения/записи на устройство (rkB/s, wkB/s);  
Disk utilization — утилизация диска и значение IOPS (%util, r/s, w/s) — позволяет неплохо отслеживать скачки в утилизации и чем, чтением или записью они были вызваны.  
