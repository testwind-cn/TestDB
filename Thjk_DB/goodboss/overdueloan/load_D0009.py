#!coding:utf-8

import os
from goodboss.overdueloan.wj_tools.tool_load_excel_notype import LoadExcel
from goodboss.overdueloan.wj_tools import sftpUtil
from goodboss.overdueloan.wj_tools.str_tool import StrTool
from goodboss.overdueloan.wj_tools.tool_mysql import TheDB

# https://xlrd.readthedocs.io/en/latest/api.html?highlight=Cell#xlrd.sheet.Cell

# 0 没有，2 整数，1 字符串，3 日期
data_type_D0009 = [
    0, 2, 0, 0, 1, 0, 1, 0, 1, 1,
    0, 0, 0, 1, 1, 3, 3, 2, 2, 2,
    0, 0, 2, 2, 0, 1, 0, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 0, 2, 0, 2, 0, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
    1, 2
    ]

s_sql = """INSERT INTO d0009 ( 
col_01,col_02,col_03,col_04,col_05,col_06,col_07,col_08,col_09,col_10,
col_11,col_12,col_13,col_14,col_15,col_16,col_17,col_18,col_19,col_20,
col_21,col_22,col_23,col_24,col_25,col_26,col_27,col_28,col_29,col_30,
col_31,col_32,col_33,col_34,col_35,col_36,col_37,col_38,col_39,col_40,
col_41,col_42,col_43,col_44,col_45,col_46,col_47,data_dt
)
VALUES
{} ;
"""
s_sql2 = "DELETE from d0009 WHERE data_dt = str_to_date('{}','%Y%m%d')"


def load_excel_D0009(p_the_db: TheDB, p_date, p_f_name='D0009LoanSurplusRpt_1.xls'):  # : str = u'D0009LoanSurplusRpt_1_修改.xls'
    # u'D0009LoanSurplusRpt_1_修改_{}.xls'
    # file_name1 = os.path.join(os.getcwd(), u'D0009LoanSurplusRpt_1_修改_{}.xls'.format(p_date))

    file_name1 = os.path.join(os.getcwd(), 'data_tmp', p_date, p_f_name)

    a = LoadExcel()
    a.load_excel_by_row(p_the_db=p_the_db, p_file_name1=file_name1, p_first_row=4, p_total_col=62, p_sql=s_sql, p_sql2=s_sql2, p_data_type=data_type_D0009, the_date=p_date)


def download_excel_D0009(p_date, p_f_name='D0009LoanSurplusRpt_1.xls'):
    # /datateam/reports/REPORTS/20190325/S620000TranAdjSummary_000080000001_20190325.OK
    result = sftpUtil.getConnect("101.230.217.35", 9999, "report", "rep2018")
    file_name1 = "/datateam/reports/REPORTS/" + p_date + "/" + p_f_name
    file_name2 = os.path.join(os.getcwd(), 'data_tmp', p_date)
    if result[0] == 1:
        result2 = sftpUtil.download(result[2], file_name1, file_name2)
        sftpUtil.closeConnect(result[2])
        if result2[0] == 1:
            return True
        else:
            return False
    else:
        return False
        # myLog.Log('sftp 连接失败', False)


if __name__ == "__main__":
    """
    date = "20190329"
    fname = 'D0009LoanSurplusRpt_1.xls'

    for i in range(0, 342):
        date = StrTool.get_the_date_str("20180427", i)
        print("================   " + date)
        if download_excel_D0009(date, fname):
            load_excel_D0009(date, fname)
"""

    date = "20190404"
    fname = 'D0009LoanSurplusRpt_1.xls'

    the_db = TheDB()
    the_db.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='thbl123',
        db='echart'
    )

    for i in range(0, 1):
        date = StrTool.get_the_date_str("20190404", i)
        print("================   " + date)
        if download_excel_D0009(date, fname):
            load_excel_D0009(p_the_db=the_db, p_date=date, p_f_name=fname)

    # 关闭连接
    the_db.close()





