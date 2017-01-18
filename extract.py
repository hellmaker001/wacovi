'''
    Reads WhatsApp log file and extracts several statistics to csv files.

    Mnemonic: ego is you, vos is your conversation partner. Atthay isway atinlay, isthay isway igpay atinlay
'''

from datetime import datetime
import sys
import csv
import codecs
import argparse
import pytz
import time
import pandas as pd
from pandas import DataFrame

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse")
    parser.add_argument("-f", "--file",  help="log file", required=True)
    parser.add_argument("-i", "--ego", help="my name", required=True)
    parser.add_argument("-y", "--vos", help="his/her name", required = True)
    parser.add_argument("-t", "--tz", help="unaware timezone", required=False)

    args = vars(parser.parse_args())

    # TODO Correct unaware timezone in logs using the supplied timezone
    unaware_tz = args["tz"]

    fh = codecs.open(args["file"], 'r', "utf-8-sig")
    log = fh.read()
    lines = log.split("\n")
    #print len(lines)

    # 0 is total, 1 is ego, 2 is vos
    msg_count_0 = []
    msg_count_1 = []
    msg_count_2 = []
    date_0 = []
    date_1 = []
    date_2 = []
    df_0 = pd.DataFrame([])
    df_1 = pd.DataFrame([])
    df_2 = pd.DataFrame([])

    skipped = 0
    for l in lines:
        raw_dt, sym, msg = l.partition(" - ")
        name, sym, blahblah = msg.partition(": ")

        raw_dt = raw_dt.replace(',', '')
        # Malformed lines due to a new line in the text message
        try:
            msg_dt = datetime.strptime(raw_dt, "%m/%d/%y %I:%M %p")
        except:
            skipped = skipped+1
            #print "Parse error on line " + str(i)+".Skipping."

        date_0.append(msg_dt)
        msg_count_0.append(1)
        if name == args["ego"]:
            date_1.append(msg_dt)
            msg_count_1.append(1)
        elif name == args["vos"]:
            date_2.append(msg_dt)
            msg_count_2.append(1)

    print "skipped " + str(skipped) + " of " + str(len(lines)) + " lines. (" + str((float(skipped)/len(lines))*100) + " % loss)"

    # Add lists to pandas dataframes
    df_0["datetime"] = pd.to_datetime(date_0)
    df_0.index = df_0["datetime"]
    df_0["total"] = msg_count_0

    df_1["datetime"] = pd.to_datetime(date_1)
    df_1.index = df_1["datetime"]
    df_1[args["ego"]] = msg_count_1

    df_2["datetime"] = pd.to_datetime(date_2)
    df_2.index = df_2["datetime"]
    df_2[args["vos"]] = msg_count_2

    ### 1. Day activity
    # Sample by day. Binning of number of texts for each day. Fill NaN with 0.
    temp_df_0 = df_0.resample('D').sum().fillna(0)
    temp_df_1 = df_1.resample('D').sum().fillna(0)
    temp_df_2 = df_2.resample('D').sum().fillna(0)
    # Merge three dataframes to write to a single csv
    daily_bin = pd.merge(temp_df_0, temp_df_1, how="inner", left_index=True, right_index=True)
    daily_bin = pd.merge(daily_bin, temp_df_2, how="inner", left_index=True, right_index=True)
    daily_bin.to_csv("days.csv")

    ### 2. Hourly Activity - Heatmap

    # Group by day-of-week and hour and bin the count.
    hourly_bin = df_0.groupby([df_0["datetime"].dt.dayofweek, df_0["datetime"].dt.hour]).sum()
    hourly_bin.index.names = ["dow", "hour"]
    hourly_bin.to_csv("hour.csv")
