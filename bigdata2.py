# Author: Alan Wilms
# Updated: 4/3/2018
# This is a program that condenses .csv files based on a set of column names and writes them to new
# csv files.

import csv
import codecs
import os
import glob
# import pdb

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# def insertStr(resultStr, searchStr, newStr):
#     split = result.find(searchStr)
#     # print(split)
#     if (split > 0):
#         split = split +  + len(searchStr)
#         resultStr = resultStr[:split] + ' ' + newStr + resultStr[split:]
#     return resultStr
#
# def replaceStr(resultStr, searchStr, newStr):Big
#     split = result.find(searchStr)
#     if (split > 0):
#         resultStr = resultStr[:split] + newStr + resultStr[split+len(searchStr):]
#     return resultStr

path = '/Users/AlanWilms/Desktop/BigData4'
for filename in glob.glob(os.path.join(path, '*.csv')):
    infilename = filename
    outfilename = infilename[:-4] + 'part1' + '.sql'
    print("Converting " + infilename + " into " + outfilename + ".");

    reader = csv.reader(open(infilename, 'rb'), delimiter=",")
    row_count = len(list(reader))

    # CREATE TABLE
    with open(infilename, 'rb') as fp_in, open(outfilename, 'wb') as fp_out:
        reader = csv.reader(fp_in, delimiter=",")
        headers = next(reader)  # read first row
        tablename = filename.split("/")[-1][:-4]
        result = 'CREATE TABLE ' + '"' + tablename + '"' + '\n' + '(' + ' '.join('"'+ str(i) + '"' + " FLOAT,\n" for i in headers)[:-2] + ')\n' + 'GO'
        result = result.replace('UNITID" FLOAT', 'UNITID" FLOAT PRIMARY KEY')
        result = result.replace('INSTNM" FLOAT', 'INSTNM" TEXT')
        result = result.replace('STABBR" FLOAT', 'STABBR" TEXT')
        result = result.replace('CITY" FLOAT', 'CITY" TEXT')
        result = result.replace('ZIP" FLOAT', 'ZIP" TEXT')
        result = result.replace('OPEID" FLOAT', 'OPEID" TEXT')

        fp_out.write(result)

        insert = 'INSERT INTO ' + '"' + tablename + '"' + '\nVALUES '
        # fp_out2.write(insert)

        # row_count = 7000
        count = 0
        name_count = 2
        num_of_rows = 500 # per file
        for row in reader:
            if (count % num_of_rows == 0):
                fp_out2 = open(infilename[:-4] + 'part' + str(name_count) + '.sql', 'wb')
                name_count = name_count + 1
                fp_out2.write(insert)
            row = [r.replace("'", "''") for r in row] # to escape single quotes
            row = [x if x != 'PrivacySuppressed' else 'NULL' for x in row]
            row = ["'" + x + "'" if not is_number(x) and x != 'NULL' else x for x in row]
            # pdb.set_trace()
            if row[6][:1] != "'":
                row[6] = "'" + row[6] + "'" # for zip code since some are in the form XXXXX-XXXX
            if row[1][:1] != "'":
                row[1] = "'" + row[1] + "'"
            row = '(' + ' '.join(str(s) + "," for s in row)[:-1] + '),\n'
            if ((count + 1) % num_of_rows == 0 or count == row_count - 2):
                fp_out2.write(row[:-2] + ';\n' + '\n')
            else:
                fp_out2.write(row)
            count = count + 1

    print("Done!")
