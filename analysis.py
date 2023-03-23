import pandas as pd
from urlextract import URLExtract
from collections import Counter
import emoji
from wordcloud import WordCloud

# Perticular User's Details
def dataframe(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df

# User's Statistic
def fetch_stats(selected_user, df):
    if selected_user!= 'overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    word =[]
    links=[]
    for message in df['message']:
        word.extend(message.split())
        extract = URLExtract()
        links.extend(extract.find_urls(message))

    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    return num_messages, len(word), num_media, len(links)

# Monthly Timeline
def monthly_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    timeline_df = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline_df.shape[0]):
        time.append(timeline_df['month'][i]+"-"+str(timeline_df['year'][i]))

    timeline_df['time'] = time

    return timeline_df

#Daily Timeline
def daily_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    daily_timeline_df = df.groupby(['date']).count()['message'].reset_index()

    return daily_timeline_df

# Weekly_Activity
def weekly_activity(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

#Month_activity
def month_activity(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user']== selected_user]

    return df['month'].value_counts()

# Most busy user
def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


# def create_wordcloud(selected_user, df):
#     if selected_user!='overall':
#        df=df[df['user']== selected_user]
#     wc= WordCloud(width=500, height=500, min_font_size=10, background_color='black')
#     df_wc= wc.generate(df['message'].str.cat(sep=" "))
#     return df_wc

# Most Common Words
def most_common_words(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in df['message']:
        for word in message.lower().split():
            words.append(word)

    common_df = pd.DataFrame(Counter(words).most_common(10))

    return common_df

#Show Emoji Details
def show_emoji(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        # emoji=emojis.get('message')
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
        # emojis1=emojis.unique()
        # emojis2= emojis.count()

    emoji_df = pd.DataFrame(Counter(emojis).most_common(10))

    return emoji_df