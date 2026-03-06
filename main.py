import streamlit as st
import requests
st.title("YouTube Test")
video_id=st.text_input("Enter YouTube Video ID")
if video_id:
    endpoint_url="https://www.youtube.com/youtubei/v1/player?prettyPrint=false"
    header={
        'User-Agent': 'com.google.android.apps.youtube.vr.oculus/1.60.19 (Linux; U; Android 12L; eureka-user Build/SQ3A.220605.009.A1) gzip',
        'accept-language': 'en-US,en',
        'Content-Type': 'application/json',
        'X-Youtube-Client-Name': '28'
    }
    data_1 ={
        "context":
            {"client":
                 {"clientName": "WEB",
                  "osName": "Windows",
                  "osVersion": "10.0",
                  "clientVersion": "2.20250523.01.00",
                  "platform": "DESKTOP"
                  }
             }, "videoId": video_id,
        "contentCheckOk": "true"
    }
    response=requests.get("https://www.youtube.com/results?search_query=test")
    st.text_area(response.text)
