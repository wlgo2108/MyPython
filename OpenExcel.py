#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import xlrd
import os


class OpenExcel:
    def __init__(self, file="file.xls", colnameindex=0, by_name="Sheet1"):
        self.file = file
        self.colnameindex = colnameindex
        self.by_name = by_name

    def open_excel(self, file="file.xls"):
        self.file = file
        try:
            data = xlrd.open_workbook(self.file)
            return data
        except Exception, e:
            print e

    def excel_table_byname(self):
        data = self.open_excel(self.file)
        table = data.sheet_by_name(self.by_name)
        nrows = table.nrows
        colnames = table.row_values(self.colnameindex)

        list = []
        for rownum in range(1, nrows):
            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = row[i]
                list.append(app)
        return list

    def read_value(self, key):
        table = self.excel_table_byname()
        list = []
        for row in table:
            list.append(row[key])
        return list


if __name__ == "__main__" :
    openE = OpenExcel(file = "test.xlsx",by_name="3D")
    table = openE.excel_table_byname()
    for i in range(0,len(table)) :
        print int(table[i]["PlayType"])




