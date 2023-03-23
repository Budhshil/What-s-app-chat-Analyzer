import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import preprocessor1
import analysis

# Main Web Design
st.sidebar.title("Whatsapp Chat Processor")
user_file = st.sidebar.file_uploader("Upload_file",type=['txt'],accept_multiple_files=False)

if user_file is not None:
    data = user_file.getvalue().decode('utf-8')

    df = preprocessor1.preprocess(data)
    v1 = st.title("Whatsapp Chat Data")
    v2 = st.dataframe(df)

    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['message'] != 'This Message was deleted']

    # fetech the unique data
    #Convert it to list to add it into the selection box
    user_list = df['user'].unique().tolist()
    #user_list.remove("group_notification")
    user_list.sort()
    # removing single value
    value = [')', '(', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'u', 'i']
    final_user = []
    for i in user_list:
        if i not in value:
            final_user.append(i)

    v3 = st.header("Total Memebrs")
    v4 = st.title(len(final_user))

    final_user.insert(0, 'Overall')
    sel_user = st.sidebar.selectbox("Show analysis for ", final_user)

    if st.sidebar.button('show analysis'):
        v1.empty()
        v2.empty()
        v3.empty()
        v4.empty()

        user_df = analysis.dataframe(sel_user, df)
        st.title("Selected User's Chart")
        st.dataframe(user_df)

        st.title("Selected User's Statistic")
        num_messages, words, num_media, links = analysis.fetch_stats(sel_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(num_media)
        with col4:
            st.header("Total Links")
            st.title(links)

        if user_df.empty:
            st.header("Non Active User")
        else:
            st.title("Monthly Timeline")
            timeline_df = analysis.monthly_timeline(sel_user, df)
            fig, ax = plt.subplots(1,1)
            ax.bar(timeline_df['time'], timeline_df['message'], width=0.4)
            ax.set_xlim(-0.5, 5)
            plt.xlabel("month")
            plt.ylabel("frequency of message")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.title("Daily Timeline")
            daily_timeline_df = analysis.daily_timeline(sel_user, df)
            fig, ax = plt.subplots()
            plt.scatter(daily_timeline_df['date'], daily_timeline_df['message'], color='black')
            plt.xlabel("days")
            plt.ylabel("frequency of message")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.title("Activity Map")
            col1, col2 = st.columns(2)

            with col1:
                st.header('Most Busy Day')
                busy_day = analysis.weekly_activity(sel_user, df)

                fig, ax = plt.subplots(1,1)
                ax.bar(busy_day.index, busy_day.values, color='red', width=0.5)
                ax.set_xlim(-0.5, 5)
                plt.xlabel("day")
                plt.ylabel("frequency of message")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header('Most Busy Month')
                busy_month = analysis.month_activity(sel_user, df)

                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange',width=0.5)
                ax.set_xlim(-0.5, 5)
                plt.xlabel("month")
                plt.ylabel("frequency of message")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            if sel_user == 'overall':
                st.title('Most Busy Users')

                x, new_df = analysis.most_busy_user(df)
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values, color='green',width=0.1)
                    plt.xlabel("users")
                    plt.ylabel("frequency of message")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                with col2:
                    st.dataframe(new_df)

            st.title('Most Common Words')
            common_df = analysis.most_common_words(sel_user, df)
            if common_df.empty:
                st.header(':blue[This user not send  any Message]')
            else:
                col1, col2 = st.columns(2)

                with col1:
                    fig, ax = plt.subplots()
                    ax.bar(common_df[0], common_df[1])
                    plt.xlabel("common words")
                    plt.ylabel("frequency of words")
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2:
                    st.dataframe(common_df)

            st.title('Common Emoji Used')
            emoji_df = analysis.show_emoji(sel_user, df)

            if emoji_df.empty:
                st.header(':blue[This user not used any emoji]')

            else:
                col1, col2 = st.columns(2)

                with col1:
                    st.dataframe(emoji_df)

                with col2:
                    fig, ax = plt.subplots()
                    ax.pie(emoji_df[1], labels=emoji_df[0])
                    plt.legend(emoji_df[0], loc="best")
                    st.pyplot(fig)