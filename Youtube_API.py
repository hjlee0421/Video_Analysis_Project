import requests
import pandas as pd

################
# GET VIDEO ID #
################

API_KEY_LIST = ['xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-2
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-3
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-4
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-5
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-6
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-7
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-8
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-9
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-10
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-11
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-12
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-13
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-14
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-15
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-16
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-17
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-18
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-19
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-20
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-21
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # YoutubeAPI-22
                'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'] # YoutubeAPI-23

API_KEY_INDEX = 0
API_KEY = API_KEY_LIST[API_KEY_INDEX]
REGION = "US"
QUERY = "vlog"
#CATEGORY_LIST = ["10", "15", "19", "26",
CATEGORY_LIST = ["22"]
#OUTPUT_LIST =[]

for CATEGORY in CATEGORY_LIST:

    # https://developers.google.com/youtube/v3/docs/search/list   -   search parameter information

    # can sort by date rating relevance title viewCount  with "order"
    # can specify after or before date with "publishedAfter" and "publishedBefore"
    # query Your request can also use the Boolean NOT (-) and OR (|) operators to exclude videos or to find videos that are associated with one of several search terms. boating|sailing -fishing

    video_id_list = []

    response = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&videoCategoryId='+CATEGORY+'&regionCode='+REGION+'&maxResults=50&q='+QUERY+'&type=video&key='+API_KEY)
    #response.text
    if "Exceeded" in response.text:
        if API_KEY_INDEX < (len(API_KEY_LIST) - 1):
            API_KEY_INDEX = API_KEY_INDEX + 1
        else:
            print("NEED NEW API KEY")
            break
        API_KEY = API_KEY_LIST[API_KEY_INDEX]
        response = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&videoCategoryId='+CATEGORY+'&regionCode='+REGION+'&maxResults=50&q='+QUERY+'&type=video&key='+API_KEY)

    for i in range(len(dict(response.json())['items'])):
        video_id_list.append(dict(response.json())['items'][i]['id']['videoId'])

    PAGE_TOKEN = dict(response.json())['nextPageToken']
    print(len(video_id_list))

    len(set(video_id_list))
    len(video_id_list)


    while len(dict(response.json())['items']) > 0:   # MAX NUM ???

        response = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&videoCategoryId='+CATEGORY+'&pageToken='+PAGE_TOKEN+'&regionCode='+REGION+'&maxResults=50&q='+QUERY+'&type=video&key='+API_KEY)

        if "Exceeded" in response.text:
            if API_KEY_INDEX < (len(API_KEY_LIST)-1):
                API_KEY_INDEX = API_KEY_INDEX + 1
            else:
                print("NEED NEW API KEY")
                break
            API_KEY = API_KEY_LIST[API_KEY_INDEX]
            response = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&videoCategoryId='+CATEGORY+'&pageToken='+PAGE_TOKEN+'&regionCode='+REGION+'&maxResults=50&q='+QUERY+'&type=video&key='+API_KEY)

        for i in range(len(dict(response.json())['items'])):
            video_id_list.append(dict(response.json())['items'][i]['id']['videoId'])

        PAGE_TOKEN = dict(response.json())['nextPageToken']

        print(len(video_id_list), API_KEY, CATEGORY)


    video_id_list = list(set(video_id_list))
    print(len(video_id_list))

    ##################
    # GET VIDEO INFO #
    ##################

    video_info_list = []
    #VIDEO_ID = video_id_list[0]

    i=1
    VIDEO_ID = video_id_list[0]
    for VIDEO_ID in video_id_list:

        print(i,len(video_id_list), API_KEY, CATEGORY)
        i=i+1

        response = requests.get('https://www.googleapis.com/youtube/v3/videos?id='+VIDEO_ID+'&key='+API_KEY+'&part=snippet,statistics,contentDetails')

        if "Exceeded" in response.text:
            if API_KEY_INDEX < (len(API_KEY_LIST) - 1):
                API_KEY_INDEX = API_KEY_INDEX + 1
            else:
                print("NEED NEW API KEY")
                break
            API_KEY = API_KEY_LIST[API_KEY_INDEX]
            response = requests.get('https://www.googleapis.com/youtube/v3/videos?id='+VIDEO_ID+'&key='+API_KEY+'&part=snippet,statistics,contentDetails')

        url = "https://www.youtube.com/watch?v="+VIDEO_ID
        publishedAt = dict(response.json())['items'][0]["snippet"]["publishedAt"] if "publishedAt" in response.text else ""
        title = dict(response.json())['items'][0]["snippet"]["title"] if "title" in response.text else ""
        description = dict(response.json())['items'][0]["snippet"]["description"] if "description" in response.text else ""
        channelTitle = dict(response.json())['items'][0]["snippet"]["channelTitle"] if "channelTitle" in response.text else ""
        tags = dict(response.json())['items'][0]["snippet"]["tags"] if "tags" in response.text else ""
        categoryId = dict(response.json())['items'][0]["snippet"]["categoryId"] if "categoryId" in response.text else ""
        defaultLanguage = dict(response.json())['items'][0]["snippet"]["defaultLanguage"] if "defaultLanguage" in response.text else ""

        viewCount = dict(response.json())['items'][0]["statistics"]["viewCount"] if "viewCount" in response.text else 0
        likeCount = dict(response.json())['items'][0]["statistics"]["likeCount"] if "likeCount" in response.text else 0
        dislikeCount = dict(response.json())['items'][0]["statistics"]["dislikeCount"] if "dislikeCount" in response.text else 0
        commentCount = dict(response.json())['items'][0]["statistics"]["commentCount"] if "commentCount" in response.text else 0

        PlayTime = dict(response.json())['items'][0]["contentDetails"]["duration"][2:] if "duration" in response.text else ""

        video_info_list.append([url, publishedAt, title, description, channelTitle, tags, categoryId, defaultLanguage,
                                viewCount, likeCount, dislikeCount, commentCount, PlayTime])

    video_info_df = pd.DataFrame(video_info_list)

    video_info_df.columns = ["url",
                             "publishedAt", "title", "description", "channelTitle", "tags", "categoryId", "defaultLanguage",
                             "viewCount", "likeCount", "dislikeCount", "commentCount", "PlayTime"]
    OUTPUT_LIST.append(video_info_df)

len(OUTPUT_LIST)

OUTPUT_LIST

AAAA = OUTPUT_LIST[3]

# US_VLOG_People_Blogs = video_info_df
# KR_VLOG_People_Blogs = video_info_df
# KR_VLOG_PET = video_info_df

with pd.ExcelWriter('YOUTUBE_API_INFO_V3.xlsx') as writer:
    OUTPUT_LIST[0].to_excel(writer, sheet_name='US_VLOG_Music', index=False, encoding="utf-8")
    OUTPUT_LIST[1].to_excel(writer, sheet_name='US_VLOG_Pet', index=False, encoding="utf-8")
    OUTPUT_LIST[2].to_excel(writer, sheet_name='US_VLOG_Travel_Events', index=False, encoding="utf-8")
    OUTPUT_LIST[3].to_excel(writer, sheet_name='US_VLOG_Howto_Style', index=False, encoding="utf-8")
    OUTPUT_LIST[4].to_excel(writer, sheet_name='US_VLOG_People_Blogs', index=False, encoding="utf-8")



us = US_VLOG["title"].tolist()
kr = KR_VLOG["title"].tolist()
kr_sports = KR_SPORTS_VLOG["title"].tolist()

len(set(kr_sports) & set(kr))