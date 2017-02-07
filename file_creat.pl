#!/usr/bin/perl -w
#use strict;
use warnings;
use Getopt::Long;
use Data::Dumper;
use File::Find;
use Storable;
use File::Basename;
use DateTime;
use List::Util qw/max min sum maxstr minstr shuffle/;

GetOptions(
"name=s"=>\$name,
);

my $usage=<<END;

========================Usage=======================

perl $0

-name	yanghuan
-t		'GXY','YC','Cus','CR'
-p		WES,902
END

my ($filename,$in,@cut,%path,$sam_info,%hash);
my ($input,$output)=@ARGV;
open IN,$input;
while(<IN>){
	chomp;
	/#/ && next;
	@cut=split/\t/,$_;
	$sam_info=join "\t",@cut[1..7];
	my $lujing=(split/\t/,$_)[1];
	$filename=(split/\//,$lujing)[-1];
	my $type=(split/\t/,$_)[0];
	if ($type=~/个人基因组/){
		$path{$type}="/BJPROJ/HEALTH/Project_new/2C";
		$hash{$type}="-t YC,GXY,CR,CS,Fit,Drug,kid -p WES";
		push @{$path{$type}},$sam_info;
	}elsif ($type=~/新华医院/){
		$path{$type}="/BJPROJ/HEALTH/Project/XinHuaYiYuan";
		$hash{$type}="-t XHYY -p 902";
		push @{$path{$type}},$sam_info;
	}elsif ($type=~/儿童医院/){
		$path{$type}="/BJPROJ/HEALTH/Project/ErTongYiYuan";
		$hash{$type}="-t ETYY -p 902";
		push @{$path{$type}},$sam_info;
	}elsif ($type=~/量康/){
		$path{$type}="/BJPROJ/HEALTH/Project_new/LiangKang";
		$hash{$type}="-t YC,GXY,CR,CS,Fit,Drug,kid -p WES";
		push @{$path{$type}},$sam_info;
	}elsif ($type=~/睿持/){
		$path{$type}="/BJPROJ/HEALTH/Project_new/RuiChi";
		$hash{$type}="-t YC,GXY,CR,CS,Fit,Drug,kid -p WES";
		push @{$path{$type}},$sam_info;
	}elsif ($type=~/诺兰德/){
		$path{$type}="/BJPROJ/HEALTH/Project_new/NuoLanDe";
		$hash{$type}="-t YC,GXY,CR,CS,Fit,Drug,kid -p WES";
		push @{$path{$type}},$sam_info;
	}elsif ($type=~/荣之联/){
		$path{$type}="/BJPROJ/HEALTH/Project_new/rongzhilian";
		$hash{$type}="-t YC,GXY,CR,CS,Fit,Drug,kid -p WES";
		push @{$path{$type}},$sam_info;
	}elsif ($type=~/欣盛/){
		$path{$type}="/BJPROJ/HEALTH/Project_new/xinsheng";
		$hash{$type}="-t YC,GXY,CR,CS,Fit,Drug,kid -p WES";
		push @{$path{$type}},$sam_info;
	}elsif ($type=~/爱尚/){
		$path{$type}="/BJPROJ/HEALTH/Project_new/AiShangJia";
		$hash{$type}="-t YC,GXY,CR,CS,Fit,Drug,kid -p WES";
		push @{$path{$type}},$sam_info;
	}elsif ($type=~/高血压/){
		$path{$type}="/BJPROJ/HEALTH/Project/Hypertension";
		$hash{$type}="-t FWGXY";
		push @{$path{$type}},$sam_info;
	}else{print "没有该文件夹，请到Project／Project_new创建文件夹后修改此脚本运行";
	}			
}

	foreach my $n(keys %path){
		if( -e "$path{$n}/$filename"){
			open SAMPLE,">$path{$n}/$filename/sample.ini";
			open WORK,">$path{$n}/$filename/work.sh";
			print SAMPLE (join"\n", @{$path{$n}});
			print WORK "python /ifs/TJPROJ3/HEALTH/zhongying/01script/01QCstat/XML/Produce_shell.1.2.py -s sample.ini -n $name  $hash{$n} > work_shell.sh\n";
		}else{
		`mkdir $path{$n}/$filename`;
		open SAMPLE,">$path{$n}/$filename/sample.ini";
		open WORK,">$path{$n}/$filename/work.sh";
		print SAMPLE (join"\n", @{$path{$n}});
		print WORK "python /ifs/TJPROJ3/HEALTH/zhongying/01script/01QCstat/XML/Produce_shell.1.2.py -s sample.ini -n $name  $hash{$n} > work_shell.sh\n"
		}
	}
close SAMPLE;
close WORK;
