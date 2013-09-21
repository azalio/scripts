#!/usr/bin/perl

use warnings;
use strict;
use v5.10;
use Data::Dumper;
use List::Util qw(sum);

=count
 - Если 0 виртуалок - то это самая лучшая 
 - free space on lvm
 - memory
 - 
=cut

sub av {
	my $aref = shift;
	@{$aref} = grep defined, @{$aref};
	for(@{$aref}) {
		s/,/./g;
	}
	my $average = sum(@{$aref})/scalar(@{$aref});
	return $average;
}
	
	
my ( @hostname,@interval,@timestamp,@kbmemfree,@kbmemused,
		@memused,@kbbuffers,@kbcached,@kbcommit,@commit,@kbactive,@kbinact );

#mem usage
open(SAR,"sadf -dt /var/log/sysstat/sa19 -- -r | ");
while(<SAR>) {
	next if $. == 1;
## hostname;interval;timestamp;kbmemfree;kbmemused;%memused;kbbuffers;kbcached;kbcommit;%commit;kbactive;kbinact
	( $hostname[$.],$interval[$.],$timestamp[$.],$kbmemfree[$.],$kbmemused[$.],
		$memused[$.],$kbbuffers[$.],$kbcached[$.],$kbcommit[$.],$commit[$.],
		$kbactive[$.],$kbinact[$.] ) = split(/;/);
}

close(SAR);
@kbmemfree  = grep defined, @kbmemfree;
say "Free average mem on " . $hostname[2] ." is " .  sum(@kbmemfree)/scalar(@kbmemfree) . " Kb";

@kbmemused  = grep defined, @kbmemused;
say "Used average mem on " . $hostname[2] ." is " .  sum(@kbmemused)/scalar(@kbmemused) . " Kb";

## hostname;interval;timestamp;tps;rtps;wtps;bread/s;bwrtn/s

my ( @tps,@rtps,@wtps,@bread,@bwrtn );

open(SAR,"sadf -dt /var/log/sysstat/sa19 -- -b | ");
while(<SAR>) {
	next if $. == 1;
	( undef,undef,undef, $tps[$.] ) = split(/;/);
	$tps[$.] =~ s/,/./;
#	say $tps[$.];
}
close(SAR);

say "average transfer per sec " . av(\@tps);

#lvm info
# pvs --options pv_name,pv_size,pv_free,pv_used --nosuffix --units k --noheadings
#  PV         PSize         PFree         Used        
#  /dev/md1   1911324672,00 1701609472,00 209715200,00

my ( @dev_name,@PSize,@PFree,@PUsed );

open(PV,"pvs --options pv_name,pv_size,pv_free,pv_used --nosuffix --units k --noheadings |");
while (<PV>) {
	( $dev_name[$.],$PSize[$.],$PFree[$.],$PUsed[$.] ) = split();
}
close(PV);
say $dev_name[1];

my $rdev = ( stat "$dev_name[1]" )[ 6 ];
my $minor = $rdev % 256;
my $major = int( $rdev / 256 );
my $pv_dev =  "dev$major-$minor";
say $pv_dev;

# sadf -dt /var/log/sysstat/sa19 -- -d | head
# hostname;interval;timestamp;DEV;tps;rd_sec/s;wr_sec/s;avgrq-sz;avgqu-sz;await;svctm;%util
#mail-srv01g;599;2013-09-19 00-45-01;dev8-0;13,89;0,28;766,76;55,24;0,21;15,44;1,59;2,21

my ( @dev,@dev_tps,@await,@util ) = 0;

open (DEV,"sadf -dt /var/log/sysstat/sa19 -- -d | ");
while (<DEV>) {
	next if $. == 1;
	( undef,undef,undef,$dev[$.],$dev_tps[$.],undef,undef,undef,undef,$await[$.],undef,$util[$.] ) = split(/;/);
	( $dev_tps[$.],$await[$.],$util[$.] ) = undef if $dev[$.] ne $pv_dev;
}
close(DEV);

say "average transfer per sec on $pv_dev " . av(\@dev_tps);
say "average await $pv_dev " . av(\@await);
say "average util $pv_dev " . av(\@util);

# sadf -dt -P ALL /var/log/sysstat/sa19 | head -2
# hostname;interval;timestamp;CPU;%user;%nice;%system;%iowait;%steal;%idle
#mail-srv01g;599;2013-09-19 00-45-01;-1;0,27;0,00;0,10;0,02;0,00;99,61

my (@cpu,@cpu_iowait,@idle);
open(CPU,"sadf -dt -P ALL /var/log/sysstat/sa19 | ");

while (<CPU>) {
	next if $. == 1;
	( undef,undef,undef,$cpu[$.],undef,undef,undef,$cpu_iowait[$.],undef,$idle[$.] ) = split(/;/);
	( $cpu[$.],$cpu_iowait[$.],$idle[$.] ) = undef if $cpu[$.] != -1;
}
close(CPU);

say "average cpu_iowait  " . av(\@cpu_iowait);
say "average cpu_idle " . av(\@idle);

# sadf -dt /var/log/sysstat/sa19 -- -q | head -2
# hostname;interval;timestamp;runq-sz;plist-sz;ldavg-1;ldavg-5;ldavg-15;blocked
#mail-srv01g;599;2013-09-19 00-45-01;5;391;0,21;0,11;0,10;0

my (@ldavg15,@blocked);
open(LA,"sadf -dt /var/log/sysstat/sa19 -- -q | ");
while (<LA>) {
	next if $. == 1;
	( undef,undef,undef,undef,undef,undef,undef,$ldavg15[$.],$blocked[$.] ) = split(/;/);
}
close(LA);

say "average la15  " . av(\@ldavg15);
say "average blocked " . av(\@blocked);

# sadf -dt /var/log/sysstat/sa19 -- -S | head -2
# hostname;interval;timestamp;kbswpfree;kbswpused;%swpused;kbswpcad;%swpcad
#mail-srv01g;599;2013-09-19 00-45-01;0;0;0,00;0;0,00

my @swpused;
open(SWAP,"sadf -dt /var/log/sysstat/sa19 -- -S | ");
while (<SWAP>) {
	next if $. == 1;
	(undef,undef,undef,undef,undef,$swpused[$.] ) = split(/;/);
#	say $swpused[$.];
}
close(SWAP);
say "average swap used  " . av(\@swpused);

# sadf -dt /var/log/sysstat/sa19 -- -w | head -2
# hostname;interval;timestamp;proc/s;cswch/s
#mail-srv01g;599;2013-09-19 00-45-01;5,44;1208,76

my ( @proc,@cswch );
open(PROC,"sadf -dt /var/log/sysstat/sa19 -- -w | ");
while (<PROC>) {
	next if $. == 1;
	(undef,undef,undef,$proc[$.],$cswch[$.]) = split(/;/);
}
close(PROC);
say "average number of tasks created per second " . av(\@proc);
say "average number of context switches per second " . av(\@cswch);
