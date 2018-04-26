# Author: Alan Wilms
# Updated: 4/3/2018
# This is a program that condenses .csv files based on a set of column names and writes them to new
# csv files.

import csv
import codecs
import os
import glob

# order does not matter - write all column names that need to be included in the condensed .csv file
col_names_to_include = set(['UNITID', 'OPEID', 'OPEID6', 'INSTNM', 'CITY', 'STABBR', 'ZIP', 'DEBT_MDN', 'GRAD_DEBT_MDN', 'WDRAW_DEBT_MDN', 'LO_INC_DEBT_MDN', 'MD_INC_DEBT_MDN', 'HI_INC_DEBT_MDN', 'DEP_DEBT_MDN', 'IND_DEBT_MDN', 'PELL_DEBT_MDN', 'NOPELL_DEBT_MDN', 'FEMALE_DEBT_MDN', 'MALE_DEBT_MDN', 'FIRSTGEN_DEBT_MDN', 'NOTFIRSTGEN_DEBT_MDN', 'DEBT_N', 'GRAD_DEBT_N', 'WDRAW_DEBT_N', 'LO_INC_DEBT_N', 'MD_INC_DEBT_N', 'HI_INC_DEBT_N', 'DEP_DEBT_N', 'IND_DEBT_N', 'PELL_DEBT_N', 'NOPELL_DEBT_N', 'FEMALE_DEBT_N', 'MALE_DEBT_N', 'FIRSTGEN_DEBT_N', 'NOTFIRSTGEN_DEBT_N', 'GRAD_DEBT_MDN10YR', 'CUML_DEBT_N', 'CUML_DEBT_P90', 'CUML_DEBT_P75', 'CUML_DEBT_P25', 'CUML_DEBT_P10', 'ADM_RATE', 'ADM_RATE_ALL', 'NPT4_PUB', 'NPT4_PRIV', 'NPT4_PROG', 'NPT4_OTHER', 'NPT41_PUB', 'NPT42_PUB', 'NPT43_PUB', 'NPT44_PUB', 'NPT45_PUB', 'NPT41_PRIV', 'NPT42_PRIV', 'NPT43_PRIV', 'NPT44_PRIV', 'NPT45_PRIV', 'NPT41_PROG', 'NPT42_PROG', 'NPT43_PROG', 'NPT44_PROG', 'NPT45_PROG', 'NPT41_OTHER', 'NPT42_OTHER', 'NPT43_OTHER', 'NPT44_OTHER', 'NPT45_OTHER', 'NPT4_048_PUB', 'NPT4_048_PRIV', 'NPT4_048_PROG', 'NPT4_048_OTHER', 'NPT4_3075_PUB', 'NPT4_3075_PRIV', 'NPT4_75UP_PUB', 'NPT4_75UP_PRIV', 'NPT4_3075_PROG', 'NPT4_3075_OTHER', 'NPT4_75UP_PROG', 'NPT4_75UP_OTHER', 'TUITIONFEE_IN', 'TUITIONFEE_OUT', 'TUITIONFEE_PROG', 'TUITFTE', 'PCTFLOAN', 'UGDS', 'UG', 'UGDS_WHITE', 'UGDS_BLACK', 'UGDS_HISP', 'UGDS_ASIAN', 'UGDS_AIAN', 'UGDS_NHPI', 'UGDS_2MOR', 'UGDS_NRA', 'UGDS_UNKN', 'UGDS_WHITENH', 'UGDS_BLACKNH', 'UGDS_API', 'UGDS_AIANOLD', 'UGDS_HISPOLD', 'UG_NRA', 'UG_UNKN', 'UG_WHITENH', 'UG_BLACKNH', 'UG_API', 'UG_AIANOLD', 'UG_HISPOLD', 'COUNT_NWNE_P10', 'COUNT_WNE_P10', 'MN_EARN_WNE_P10', 'MD_EARN_WNE_P10', 'PCT10_EARN_WNE_P10', 'PCT25_EARN_WNE_P10', 'PCT75_EARN_WNE_P10', 'PCT90_EARN_WNE_P10', 'SD_EARN_WNE_P10', 'COUNT_WNE_INC1_P10', 'COUNT_WNE_INC2_P10', 'COUNT_WNE_INC3_P10', 'COUNT_WNE_INDEP0_INC1_P10', 'COUNT_WNE_INDEP0_P10', 'COUNT_WNE_INDEP1_P10', 'COUNT_WNE_MALE0_P10', 'COUNT_WNE_MALE1_P10', 'GT_25K_P10', 'MN_EARN_WNE_INC1_P10', 'MN_EARN_WNE_INC2_P10', 'MN_EARN_WNE_INC3_P10', 'MN_EARN_WNE_INDEP0_INC1_P10', 'MN_EARN_WNE_INDEP0_P10', 'MN_EARN_WNE_INDEP1_P10', 'MN_EARN_WNE_MALE0_P10', 'MN_EARN_WNE_MALE1_P10', 'COUNT_NWNE_P6', 'COUNT_WNE_P6', 'MN_EARN_WNE_P6', 'MD_EARN_WNE_P6', 'PCT10_EARN_WNE_P6', 'PCT25_EARN_WNE_P6', 'PCT75_EARN_WNE_P6', 'PCT90_EARN_WNE_P6', 'SD_EARN_WNE_P6', 'COUNT_WNE_INC1_P6', 'COUNT_WNE_INC2_P6', 'COUNT_WNE_INC3_P6', 'COUNT_WNE_INDEP0_INC1_P6', 'COUNT_WNE_INDEP0_P6', 'COUNT_WNE_INDEP1_P6', 'COUNT_WNE_MALE0_P6', 'COUNT_WNE_MALE1_P6', 'GT_25K_P6', 'MN_EARN_WNE_INC1_P6', 'MN_EARN_WNE_INC2_P6', 'MN_EARN_WNE_INC3_P6', 'MN_EARN_WNE_INDEP0_INC1_P6', 'MN_EARN_WNE_INDEP0_P6', 'MN_EARN_WNE_INDEP1_P6', 'MN_EARN_WNE_MALE0_P6', 'MN_EARN_WNE_MALE1_P6', 'COUNT_NWNE_P7', 'COUNT_WNE_P7', 'MN_EARN_WNE_P7', 'SD_EARN_WNE_P7', 'GT_25K_P7', 'COUNT_NWNE_P8', 'COUNT_WNE_P8', 'MN_EARN_WNE_P8', 'MD_EARN_WNE_P8', 'PCT10_EARN_WNE_P8', 'PCT25_EARN_WNE_P8', 'PCT75_EARN_WNE_P8', 'PCT90_EARN_WNE_P8', 'SD_EARN_WNE_P8', 'GT_25K_P8', 'COUNT_NWNE_P9', 'COUNT_WNE_P9', 'MN_EARN_WNE_P9', 'SD_EARN_WNE_P9', 'GT_25K_P9', 'SAT_AVG_ALL', 'ACTCMMID', 'PCIP14', 'PCIP26', 'PCIP27', 'PCIP40', 'PCIP41', 'C150_4', 'C150_L4', 'C150_4_POOLED', 'C150_L4_POOLED', 'POOLYRS', 'PFTFTUG1_EF', 'C150_4_WHITE', 'C150_4_BLACK', 'C150_4_HISP', 'C150_4_ASIAN', 'C150_4_AIAN', 'C150_4_NHPI', 'C150_4_2MOR', 'C150_4_NRA', 'C150_4_UNKN', 'C150_4_WHITENH', 'C150_4_BLACKNH', 'C150_4_API', 'C150_4_AIANOLD', 'C150_4_HISPOLD'])

path = '/Users/AlanWilms/Desktop/BigData'
for filename in glob.glob(os.path.join(path, '*.csv')):
    infilename = filename
    outfilename = filename.split("/")
    outfilename[-1] = outfilename[-1][6:-7] + '.csv'
    outfilename = "/".join(outfilename)
    print("Copying " + infilename + " into " + outfilename + ".");

    col_indices = []
    # calculate which rows to keep
    with codecs.open(infilename, 'rb', encoding="utf-8-sig") as fp_in:
            reader = csv.reader(fp_in, delimiter=",")
            headers = next(reader)  # read first row
            count = 0
            for header in headers:
                if header in col_names_to_include:
                    col_indices.append(count)
                count += 1

    # only keep the columns designated above
    with open(infilename, 'rb') as fp_in, open(outfilename, 'wb') as fp_out:
        reader = csv.reader(fp_in, delimiter=",")
        writer = csv.writer(fp_out, delimiter=",")
        for row in reader:
            content = list(row[i] for i in col_indices)
            writer.writerow(content)

    print("Done!")
