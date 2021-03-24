import os
import pandas as pd
from google.cloud import videointelligence
from google.protobuf.json_format import MessageToDict

credential_path = "KEYFILE.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

########################################################################################################################

"""Detect labels given a file path."""
video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.LABEL_DETECTION]

operation = video_client.annotate_video('gs://video_analysis_result/wnewyork.mp4', features=features,
                                        output_uri="gs://video_analysis_result/test.txt")
print('\nProcessing video for label annotations:')

result = operation.result(timeout=120)
print('\nFinished processing.')

serialized = MessageToDict(result)

seg_label_list = serialized["annotationResults"][0]["segmentLabelAnnotations"]
shot_label_list = serialized["annotationResults"][0]["shotLabelAnnotations"]

########################################################################################################################

seg_data = pd.DataFrame()

for i in range(len(seg_label_list)):
    if "categoryEntities" in seg_label_list[i]:
        seg_data = pd.concat([seg_data, pd.DataFrame([seg_label_list[i]["entity"]["description"],
                                                      seg_label_list[i]["categoryEntities"][0]["description"],
                                                      round(seg_label_list[i]["segments"][0]["confidence"], 4)]).T])
    else:
        seg_data = pd.concat([seg_data, pd.DataFrame([seg_label_list[i]["entity"]["description"],
                                                      "NA",
                                                      round(seg_label_list[i]["segments"][0]["confidence"], 4)]).T])

seg_data.columns = ['Annotation', 'Annotation_Category', 'Confidence']
seg_data = seg_data.sort_values('Confidence', ascending=False)
seg_data = seg_data.reset_index(drop=True)

########################################################################################################################

shot_data = pd.DataFrame()

for i in range(len(shot_label_list)):
    if "categoryEntities" in shot_label_list[i]:
        for j in range(len(shot_label_list[i]["segments"])):
            shot_start_time = shot_label_list[i]["segments"][j]["segment"]["startTimeOffset"]
            shot_end_time = shot_label_list[i]["segments"][j]["segment"]["endTimeOffset"]
            shot_len = str(pd.to_timedelta(shot_end_time) - pd.to_timedelta(shot_start_time))[7:15]

            shot_data = pd.concat([shot_data, pd.DataFrame([shot_label_list[i]["entity"]["description"],
                                                            shot_label_list[i]["categoryEntities"][0]["description"],
                                                            round(shot_label_list[i]["segments"][0]["confidence"], 4),
                                                            str(pd.to_timedelta(shot_start_time))[7:15],
                                                            str(pd.to_timedelta(shot_end_time))[7:15],
                                                            shot_len]).T])
    else:
        for j in range(len(shot_label_list[i]["segments"])):
            shot_start_time = shot_label_list[i]["segments"][j]["segment"]["startTimeOffset"]
            shot_end_time = shot_label_list[i]["segments"][j]["segment"]["endTimeOffset"]
            shot_len = str(pd.to_timedelta(shot_end_time) - pd.to_timedelta(shot_start_time))[7:15]

            shot_data = pd.concat([shot_data, pd.DataFrame([shot_label_list[i]["entity"]["description"],
                                                            "NA",
                                                            round(shot_label_list[i]["segments"][0]["confidence"], 4),
                                                            str(pd.to_timedelta(shot_start_time))[7:15],
                                                            str(pd.to_timedelta(shot_end_time))[7:15],
                                                            shot_len]).T])


shot_data.columns = ['Annotation', 'Annotation_Category', 'Confidence', 'Shot_Start_Time', 'Shot_End_Time', 'Shot_Length']
shot_data = shot_data.sort_values(['Shot_End_Time', 'Confidence'], ascending=[True, False])
shot_data = shot_data.reset_index(drop=True)

########################################################################################################################

with pd.ExcelWriter('Video_Analysis_Pilot.xlsx') as writer:
    seg_data.to_excel(writer, sheet_name='Segment', index=False,  encoding='utf-8')
    shot_data.to_excel(writer, sheet_name='Shot', index=False, encoding='utf-8')
