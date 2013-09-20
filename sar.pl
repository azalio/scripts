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
