# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 10:58:51 2016

@author: ASUS
"""

from __future__ import division
import sys 
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.stdout = default_stdout
sys.stderr = default_stderr
sys.setdefaultencoding('utf8')
import  xdrlib ,sys,re,os
import xlrd
def open_excel(filename):
    try:
        data = xlrd.open_workbook(filename)
        return data
    except Exception,e:
        print str(e)
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(filename,colnameindex=0,by_index=0):
    data = open_excel(filename)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    for rownum in range(1,nrows):

         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i] 
             list.append(app)
    return list

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，sheet_name：Sheet1名称
def excel_table_byname(filename,targetName,colnameindex=0,sheet_name=u'Sheet1'):
  #  print "Begin to read file '%s'." % filename
    data = open_excel(filename)
    table = data.sheet_by_name(sheet_name)  
    nrows = table.nrows #行数 
    colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    for rownum in range(1,nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                try:
                    for each in targetName:
                        if each==colnames[i]:
                            app[colnames[i]] = number2Unicode(row[i])
                except (Exception),e:
                    print e
            list.append(app)
 #   print "Read file '%s' successfully." % filename
    return list

def RowFilter(data,colname=u"项目名称",filterName=u"遗传委托合同",):
    result=[]
    for row in data:
        if not row[colname]==filterName:
            continue
        result.append(row)
    print "The number of valid sample in XiaJiDan is %s!" % len(result)
    return(result)
def number2Unicode(number):
    tmp=number
    if isinstance(tmp,float) or isinstance(tmp,int):
        sampleID_2=unicode(int(tmp))
    else:sampleID_2=tmp
    sampleID_2=re.sub("\.0$","",sampleID_2)
    return(sampleID_2)
def MatchXJDAndHTB(colname_XJD,colname_HTB,XJD,HTB):
    global type_project
    print "Begin to match the info in XiaJiDan and HuTongBiao_%s." % type_product;
    final=[]
    for row in XJD:
        
        row_info={}     # [u"样本名称",u"文库名",u"LaneID",u"PATH",u"订单编号",u"受检者姓名",u"样本编号",u"样本类型"]
#        print row
        sampleID=row[colname_XJD]
#        print "sampleID: %s" % sampleID
        row_info=row
        for row_HTB in HTB:
            sampleID_2=row_HTB[colname_HTB]
#            print "type of sampleID_2: %s is %s  #####" % (sampleID_2,type(sampleID_2))
            sampleID_2=number2Unicode(sampleID_2)
            if sampleID==sampleID_2:
                row_info.update(row_HTB)
                break
        else:
#            print "sample %s was not found!" % sampleID
            continue
        final.append(row_info)
#    print "Finished to metch the info in XiJiDan and HuTongBiao."
    return(final)
def writefile(data):
    global targetName_XJD,cwd,type_project
#    print "Begin to write the out file sample.ini."
    
    result=[]
    name=[u"#合同名称",u"PATH",u"文库名",u"诺禾编号",u"受检者姓名",u"样本类型",u"LaneID",u"订单编号"]
    name_chr="\t".join(name)+"\n"
    result.append(name_chr)   
    for row in data:
        eachRow=[]
        for each in targetName_XJD:
            if re.search("ane|ANE",each):
                lane_new=unicode("lane")+unicode(re.sub("[^0-9]+","",row[each]))
                row[each]=lane_new
		eachRow.append(row[type_project])
        eachRow.append(row["PATH"])
        eachRow.append(row[u"文库名"])
        eachRow.append(row[u"诺禾编号"])
        eachRow.append(row[u"受检者姓名"])
        eachRow.append(row[u"样本类型"])
        eachRow.append(row[u"LaneID"])
        eachRow.append(row[u"订单编号"])
        eachRow_chr="\t".join(eachRow)+"\n"
        result.append(eachRow_chr)
    with open(cwd+"/sample.ini_" + type_product,"w") as INI:
        INI.writelines(result)
    print "%s samples found in %s !" % (len(result)-1,type_product)
    return

#os.chdir(r"E:\job\20161212\\")

def main():
    global cwd,targetName_XJD,targetName_HTB,type_product,type_project

#    os.chdir(r"C:\Users\ASUS\Desktop\\")
    cwd=os.getcwd()
    if sys.argv[1:]<3:
        print "Your argments were was less then 3, please check!"
        print r"python %s <product type> <file_XiaJiDan> <file_HuTongBiao>" % sys.argv[0]
        print "product type should be one of the 'GXY','research','2C','2B'"
        sys.exit(0)

    file_XiaJiDan=sys.argv[2]    
    file_HuTongBiao=sys.argv[3]
    type_product=sys.argv[1]

    if type_product == "GXY":
        targetName_XJD=[u"项目名称",u"样本名称",u"文库名",u"LaneID",u"PATH",u"诺禾编号"]
        targetName_HTB=[u"订单编号",u"受检者姓名",u"诺禾编号",u"样本类型",u"合同名称"]
        sheetName = u'产品研发'
        type_project =  u"合同名称"
    elif type_product == "research":
        targetName_XJD=[u"项目名称",u"样本名称",u"文库名",u"LaneID",u"PATH",u"诺禾编号"]
        targetName_HTB=[u"订单编号",u"受检者姓名",u"诺禾编号",u"样本类型",u"研发名称"]
        sheetName = u'生产研发'
        type_project = "研发名称" 
    elif type_product == "2C":
        targetName_XJD=[u"项目名称",u"样本名称",u"文库名",u"LaneID",u"PATH",u"诺禾编号"]
        targetName_HTB=[u"订单编号",u"受检者姓名",u"诺禾编号",u"样本类型",u"二级产品名称"]
        sheetName = u'2C样本互通表' 
        type_project =  u"合同名称"
    elif type_product == "2B":
        targetName_XJD=[u"项目名称",u"样本名称",u"文库名",u"LaneID",u"PATH",u"诺禾编号"]
        targetName_HTB=[u"订单编号",u"受检者姓名",u"诺禾编号",u"样本类型",u"合同名称"]
        sheetName = u'2B样本互通表'
        type_project =  u"合同名称"
    else:
        print "Note: product type should be one of the 'GXY','research','2C','2B'.But your input is: %s, please check!" % type_product
        sys.exit(1)

#    file_XiaJiDan=u"HiseqX-PE150-20161230015155148.xls"
#    file_HuTongBiao=u"hutongbiao.xlsx"
    
    if False:
        file_HuTongBiao=r""    # 互通表
        file_XiaJiDan=r""  # 下机单
        
 #   print "file_XiaJiDan: %s" % file_XiaJiDan
 #   print "file_HuTongBiao: %s" % file_HuTongBiao
    print "type_product:%s" % type_product
    print "type_project:%s" % type_project
    print "sheetName:%s" % sheetName
    huTongBiao= excel_table_byname(file_HuTongBiao,colnameindex=1,sheet_name=sheetName,targetName=targetName_HTB)
    xiaJiDan  = excel_table_byname(file_XiaJiDan,colnameindex=0,sheet_name=' sheet1',targetName=targetName_XJD) # note that there is a space before "sheet1"
    
    xiaJiDan_flt=RowFilter(data=xiaJiDan)
    result=MatchXJDAndHTB(XJD=xiaJiDan_flt ,HTB=huTongBiao,colname_XJD=u"诺禾编号",colname_HTB=u"诺禾编号")
    
    writefile(result)
    return()        
###################################################################################################
type_product=""
type_project=""
sheetName=""
main()
#下机路径   文库名  样品名  姓名    样本类型    Lane    订单号
