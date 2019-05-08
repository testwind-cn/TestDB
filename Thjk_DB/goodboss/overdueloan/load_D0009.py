#!coding:utf-8

import os
from py_tools.file_load_base import FileLoad
from py_tools import sftpUtil
from py_tools.str_tool import StrTool
from py_tools.tool_mysql import TheDB
import pathlib

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
s_sql2 = "DELETE from d0009 WHERE data_dt = str_to_date('{}','%Y-%m-%d')"


def load_excel_D0009(p_the_db: TheDB,p_table, p_date, p_f_path, p_f_name):
    date_08 = StrTool.get_the_date_str(p_date, 0, 8)
    p_f_name = p_f_name.format(date_08)
    file_name1 = str(pathlib.PurePath(p_f_path.format(date_08)).joinpath(p_f_name))
    path_1 = pathlib.Path(file_name1)
    file_name1 = str(path_1.resolve(strict=False))

    a = FileLoad(p_file_name1=file_name1, p_first_row=4, p_total_col=62, p_ctl_col=1, p_data_type=data_type_D0009)
    a.LoadHive_Mysql(p_thedate=p_date, file_type=0, p_the_db=p_the_db, p_table=p_table, p_sql=s_sql, p_sql2=s_sql2)


def download_excel_D0009(p_host,p_port,p_user,p_pass,p_date, p_f_path,p_f_name,p_l_path):
    date_08 = StrTool.get_the_date_str(p_date, 0, 8)
    result = sftpUtil.getConnect(p_host, p_port, p_user, p_pass)
    p_f_name = p_f_name.format(date_08)
    file_name1 = str(pathlib.PurePosixPath(p_f_path.format(date_08)).joinpath(p_f_name))
    file_name2 = p_l_path.format(date_08)
    path_1 = pathlib.Path(file_name2)
    file_name2 = str(path_1.resolve(strict=False))

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
    the_db = TheDB()
    the_db.connect(
        host='10.91.1.19',
        port=3306,
        user='risk',
        passwd='fTO@J5jmW&Q4',
        db='thbl_rpt'
    )

    f_host="172.31.130.14"
    f_port=22
    f_user="report"
    f_pass="rep2018"

    date = "20190404"
    f_path = "/datateam/reports/REPORTS/{}/"
    fname = 'D0009LoanSurplusRpt_1.xls'
    local_path = os.path.join(os.getcwd(), '..', '..', '..', 'data_tmp', '{}')
    f_table = "allinpal_rpt.thbl_rpt_d0009"

    date_10 = StrTool.get_the_date_str("", -1, 10)
    print("================   " + date_10)
    if download_excel_D0009(p_host=f_host,p_port=f_port,p_user = f_user, p_pass=f_pass,p_date=date_10, p_f_path=f_path, p_f_name=fname, p_l_path=local_path):
        load_excel_D0009(p_the_db=the_db, p_table=f_table, p_date=date_10, p_f_path=local_path, p_f_name=fname)

    # 关闭连接
    the_db.close()
