#!/usr/bin/perl
# Adjust Perl Path

################################################################################
#
# COPYRIGHT NOTICE
# (c)Copyright 2001 SIDE SEVEN. All Rights Reserved.
#
# FlashCGI		: counter_10
# Version		: 1.00
# URL			: http://sideseven.at-mark.tv/
# E-Mail		: info@sideseven.at-mark.tv
#
# Edit			: ¸£¦a¤è
# URL			: http://gs9768.uhome.net/
# E-Mail		: webmaster@gs9768.uhome.net
#
################################################################################


#### ¶}©l³]©w ##################################################################

$file		= "./counter_10.txt";		# ¬ö¿ýÀÉ¦ì¸m
$cookiename	= 'counter_10';			# Cookie ¬ö¿ý«O¥þ¦WºÙ
$dday		= 90;				# Cookie ¬ö¿ý«O¥þ¤é
$uselock	= 0;				# Âê©wÀÉ¨Ï¥Î (0=no 1=yes)

#### µ²§ô³]©w ##################################################################


&lock_open(CNT, "+<$file");

$cnt = <CNT>;
($total_c,$yesterday_c,$today_c,$lastday) = split(/,/, $cnt);

$total_c++;
$today_c++;
$your_c = &get_cookie($cookiename) + 1;

$ENV{'TZ'} = 'CST-8';
( $sec, $min, $hour, $day, $mon, $year )      = localtime(time);
($sec2, $min2, $hour2, $day2, $mon2, $year2 ) = localtime(time-24*60*60);

$mon++;
$year += 1900;
$today = "$year-$mon-$day\n";

$mon2++;
$year2 += 1900;
$yesterday = "$year2-$mon2-$day2\n";

if ($today ne $lastday) {
     
     if ($yesterday ne $lastday) {
         $yesterday_c = 0;
     } else {
         $yesterday_c = $today_c;
     }
     $today_c = 1;
     $lastday = $today;
}

$total_c     = sprintf("%06d", $total_c);
$today_c     = sprintf("%06d", $today_c);
$yesterday_c = sprintf("%06d", $yesterday_c);
$your_c      = sprintf("%06d", $your_c);

seek(CNT, 0, 0);
print CNT "$total_c,$yesterday_c,$today_c,$lastday\n";

&unlock_close(CNT);

print "Content-type: text/plain\n";
&set_cookie($cookiename);
print "\n";
print "cgi=$cgi&total=$total_c&yes=$yesterday_c&today=$today_c&you=$your_c&load=end&";

exit(0);

sub lock_open {
	local(*FILE, $name) = @_;
	if (!open(FILE, $name)) {
		print "content-type: text/plain\n\n";
		print "Can't open $name\n";
		exit(0);
		}
	if ($uselock) {
		eval("flock(FILE, 2)");
		if ($@) {
			print "content-type: text/plain\n\n";
			print "$@ LOCK is BUSY\$uselock = 0\n";
			exit(0);
		}
	}
	seek(FILE, 0, 0);
}

sub unlock_close {
	local(*FILE) = @_;
	if ($uselock) {
		eval("flock(FILE, 8)");
		}
	close(FILE);
}

sub get_cookie_date {
	$ENV{'TZ'} = 'CST-8';
   	my( $csec, $cmin, $chour, $cday, $cmon, $cyear, $cwday )
		= localtime(time + $dday*60*60*24);
	my(@month) = qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
	my(@week) = qw(Sun Mon Tue Wed Thu Fri Sat);
	return sprintf("%s, %d-%s-%04d %02d:%02d:%02d GMT",
				$week[$cwday],$cday,$month[$cmon+1],$cyear+1900,$chour,$cmin,$csec);
}

sub set_cookie {
	local($cookiename2) = @_;
	$cookiedate = &get_cookie_date;

	print "Set-Cookie: $cookiename=$your_c; expires=$cookiedate; \n";
}

sub get_cookie {
	local($cookiename1) = @_;
	@pairs = split(/; /, $ENV{'HTTP_COOKIE'});
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		if ($name eq $cookiename) {
			return $value;
		}
	}
	return '';

}
