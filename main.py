from __future__ import division

import math
import sqlite3
from decimal import Decimal


def create_table(conn):
    idTask = set()
    fileWithResult = open('test.txt')
    # print(fileWithResult.read())

    for line in fileWithResult:
        string = line.split(";")
        # print(string)
        for val in string:
            if val.__contains__("="):
                idTask.add(", id" + val.split("=")[0] + " varchar(255)")

    inquiry = "create table TESTS(idStudent int"
    for val in sorted(idTask):
        inquiry += val
    inquiry += ");"
    # print(inquiry)
    # conn.execute("drop table TESTS") раскомментировать после создания таблицы.
    conn.execute(inquiry)


def filling_table(conn):
    fileWithResult = open('test.txt')

    for line in fileWithResult:
        string = line.split(";")
        inquiry = "insert into TESTS("
        idStudent = False
        for val in string:
            if not val.__contains__("=") and idStudent == False:
                idStudent = True
                inquiry += "idStudent"
            if val.__contains__("="):
                inquiry += ", id" + val.split("=")[0]
        inquiry += ") values("
        idStudent = False
        for val in string:
            if not val.__contains__("=") and idStudent == False:
                idStudent = True
                inquiry += val
            if val.__contains__("="):
                inquiry += ", " + val.split("=")[1]
        inquiry += ");"
        # print(inquiry)
        cur = conn.cursor()
        cur.execute(inquiry)
        conn.commit()


def solve_tests(conn):
    idTask = set()
    fileWithResult = open('test.txt')

    for line in fileWithResult:
        string = line.split(";")
        # print(string)
        for val in string:
            if val.__contains__("="):
                idTask.add("id" + val.split("=")[0])
    i = 0
    array = []
    resultArr = []
    for val in sorted(idTask):
        inquery = "select " + val + " from TESTS where " + val + "=1 or " + val + "=0"
        arr = conn.execute(inquery)
        rows = arr.fetchall()
        all = 0
        one = 0
        zero = 0
        for row in rows:
            if row.__contains__("1"):
                one += 1
            if row.__contains__("0"):
                zero += 1
            all += 1
        # print(all)
        array.append([])
        array[i].append(one)
        array[i].append(zero)
        array[i].append(all)
        array[i].append(one / all)
        array[i].append(1 - array[i][3])
        d = Decimal(array[i][4] / array[i][3])
        resultArr.append([])
        resultArr[i].append(val)
        resultArr[i].append(float('{:.3f}'.format(float(d.ln()))))
        i += 1
    inquiry = "insert into TESTS("
    idStudent = False
    i = 0
    for val in sorted(idTask):
        if not val.__contains__("=") and idStudent == False:
            idStudent = True
            inquiry += "idStudent"
        if idStudent == True:
            inquiry += ", " + val
    inquiry += ") values("
    idStudent = False
    for val in sorted(idTask):
        if not val.__contains__("=") and idStudent == False:
            idStudent = True
            inquiry += str(0)
        if idStudent == True:
            inquiry += ", " + "'" + str(resultArr[i][1]) + "'"
            i += 1
    inquiry += ");"
    cur = conn.cursor()
    cur.execute(inquiry)
    conn.commit()
    print(inquiry)
    print(resultArr)


if __name__ == '__main__':
    conn = sqlite3.connect("pythonsqlite.db")
    create_table(conn)
    filling_table(conn)
    solve_tests(conn)
