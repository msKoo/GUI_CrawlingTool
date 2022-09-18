# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
#
# config = configparser.ConfigParser()
# config.read('config.ini', encoding='utf-8')
#
#
#
# # youtube_openapi에 query 검색 결과 요청 함수
# def get_youtube(query):
#     DEVELOPER_KEY = config['CRAWLING_CONFIG']['Youtube_DEVELOPER_KEY']
#     YOUTUBE_API_SERVICE_NAME = config['CRAWLING_CONFIG']['Youtube_YOUTUBE_API_SERVICE_NAME']
#     YOUTUBE_API_VERSION = config['CRAWLING_CONFIG']['Youtube_YOUTUBE_API_VERSION']
#
#     youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
#
#     search_response = youtube.search().list(
#         q=query,
#         order="date",
#         part="snippet",
#         maxResults=100
#     ).execute()
#
#     result_list = []
#
#     for document in search_response['items']:
#         try:
#             val = [query, document['snippet']['title'],
#                    document['snippet']['channelTitle'],
#                    document['id']['videoId']]
#             result_list.append(val)
#         except:
#             continue
#
#     return result_list
#
# # 검색 결과 요청 및 json 응답 결과 중 원하는 값 추출
# def request_youtube(query):
#     DEVELOPER_KEY = config['CRAWLING_CONFIG']['Youtube_DEVELOPER_KEY']
#     YOUTUBE_API_SERVICE_NAME = config['CRAWLING_CONFIG']['Youtube_YOUTUBE_API_SERVICE_NAME']
#     YOUTUBE_API_VERSION = config['CRAWLING_CONFIG']['Youtube_YOUTUBE_API_VERSION']
#     youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
#
#     search_response = youtube.search().list(
#         q=query,
#         order="date",
#         part="snippet",
#         maxResults=100
#     ).execute()
#
#     result_list = []
#     urls =[]
#
#     for document in search_response['items']:
#         try:
#             val = [query, document['snippet']['title'],
#                    document['snippet']['channelTitle'],
#                    document['id']['videoId']]
#             result_list.append(val)
#             urls.append(document['id']['videoId'])
#         except Exception as e:
#             continue
#
#     return result_list, urls
#
# # 추출한 값 db에 저장
# def url_youtube(query):
#     DEVELOPER_KEY = config['CRAWLING_CONFIG']['Youtube_DEVELOPER_KEY']
#     YOUTUBE_API_SERVICE_NAME = config['CRAWLING_CONFIG']['Youtube_YOUTUBE_API_SERVICE_NAME']
#     YOUTUBE_API_VERSION = config['CRAWLING_CONFIG']['Youtube_YOUTUBE_API_VERSION']
#
#     request_youtube(query)
#
#     comments = []
#     api_obj = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
#
#     result, urls = request_youtube(query)
#
#     for title,  url in enumerate(zip(result, urls)):
#         # print(title, url)
#         try:
#             response = api_obj.commentThreads().list(part='snippet,replies', videoId=url, maxResults=100).execute()
#             while response:
#                 for item in response['items']:
#                     comment = item['snippet']['topLevelComment']['snippet']
#                     text = comment['textDisplay']
#                     comments = [{'id': id, 'url': url, 'keyword': query, 'content': text,
#                                  'author': comment['authorDisplayName'],
#                                  'date': comment['publishedAt'].replace("-", ""), 'source': 'Youtube',
#                                  'num_likes': comment['likeCount']}]
#                     print(comments)
#                     # db_connection.execute(sql, (id, query, 'youtube_comment', url, text, comment['authorDisplayName'], comment['publishedAt'].replace("-", "")[:8],
#                     # comment['likeCount'], comment['likeCount']))
#
#                     if item['snippet']['totalReplyCount'] > 0:
#                         for reply_item in item['replies']['comments']:
#                             reply = reply_item['snippet']
#                             text = reply['textDisplay']
#                             comments = [{'id': id, 'url': url, 'keyword': query, 'content': text,
#                                          'author': reply['authorDisplayName'],
#                                          'date': reply['publishedAt'].replace("-", ""), 'source': 'Youtube',
#                                          'num_likes': reply['likeCount']}]
#
#                             print(comments)
#                             # db_connection.execute(sql,
#                             #                       (id, query, 'youtube_comment', url, text, reply['authorDisplayName'],
#                             #                        reply['publishedAt'].replace("-", "")[:8], comment['likeCount'], comment['likeCount']))
#                 if 'nextPageToken' in response:
#                     response = api_obj.commentThreads().list(part='snippet,replies', videoId=url,
#                                                              pageToken=response['nextPageToken'],
#                                                              maxResults=100).execute()
#                 else:
#                     break
#             # result.append(comments)
#         except:
#             continue
#         time.sleep(0.4)
#
#     return result