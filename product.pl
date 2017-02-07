##################################################################
#																                                 #	
# prod.pl is coded  by yanghuan                                  #
#																                                 #	
# 2017年 1月 15日 星期日 15:16:41 CusT						              	 #
#                                                                #
##################################################################
#!/usr/bin/perl
use strict;
use warnings;
use Getopt::Long;
use Data::Dumper;
use File::Find;
use Storable;
use File::Basename;
use DateTime;
use List::Util qw/max min sum maxstr minstr shuffle/;
my ($name,$t,$p,$shangjidan,$xiajidan);

GetOptions(
"xiajidan=s"	=>\$xiajidan,
"name=s"		=>\$name,
);
my $usage=<<END;

========================Usage=======================

perl $0 

-dir	  required, NOVO1000 home dir , if more one , split by ','
-prefix	  required, product name , must one of 'GXY','YC','Cus','CR'
-date     optional, a data range,fg: 160601,160608
-dup      optional, a file that get rid of dupplication ,

END

#============================MAIN======================================================================
#
open OUT,">step1.sh";
$shangjidan=&judge_lastest_sitedb;
print OUT "
python /BJPROJ/HEALTH/Project/shangjixiajidan/python/prepareAll.py 2B   $xiajidan $shangjidan
python /BJPROJ/HEALTH/Project/shangjixiajidan/python/prepareAll.py 2C   $xiajidan $shangjidan
python /BJPROJ/HEALTH/Project/shangjixiajidan/python/prepareAll.py GXY  $xiajidan $shangjidan
python /BJPROJ/HEALTH/Project/shangjixiajidan/python/prepareAll.py research $xiajidan $shangjidan
cat sample.ini* >sample.info.txt
rm -rf sample.ini*
perl /BJPROJ/HEALTH/Project/shangjixiajidan/bin/file_creat.pl sample.info.txt -name $name";
close OUT;

#======================================================================================================
sub judge_lastest_sitedb{
    my @all_date;
	my $lastest_date;
    my $lastest_sitedb_path;
	my $hutongbiao_path="/BJPROJ/HEALTH/Project/shangjixiajidan/hutongbiao";
    my @all_path=glob "$hutongbiao_path/*";
		foreach(@all_path){
            my $date=(split/\//)[-1];
            if ($date=~/\d+/i){
                push @all_date,$date;
            }
        }
        $lastest_date=max(@all_date);
        $lastest_sitedb_path="$hutongbiao_path/$lastest_date";

		return $lastest_sitedb_path;
}
