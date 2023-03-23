import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import time
import datetime
import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[\w][\w][\s]-'

    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'date_time': dates, 'user_message': message})

    df['date_time'] = pd.to_datetime(df['date_time'], format='%d/%m/%Y, %I:%M %p -')

    df['date'] = df['date_time'].dt.date
    df['time'] = df['date_time'].dt.time

    user =[]
    messages =[]
    for i in df['user_message']:
        entry = re.split('([\w\W]+?):\s', i)
        if entry[1:]:
            user.append(entry[1])
            messages.append(entry[2])
        else:
            for j in entry:
                entry2 = re.split('([\w\W])\sj',j)
                if entry2[1:]:
                    user.append(entry2[1])
                    messages.append(entry2[2])
                else:
                    user.append('group_notification')
                    messages.append(entry2[0])

    df['user'] = user
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date_time'].dt.year
    df['month_num']=df['date_time'].dt.month
    df['month'] = df['date_time'].dt.month_name()
    df['day'] = df['date_time'].dt.day
    df['day_name'] =df['date_time'].dt.day_name()
    df['hour'] =df['date_time'].dt.hour
    df['minute'] =df['date_time'].dt.minute
    df.drop(columns=['date_time'], inplace=True)

    return df
