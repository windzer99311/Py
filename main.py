import streamlit as st
import requests
import json

st.title("YouTube Test")
video_id = st.text_input("Enter Video ID")

if video_id:

    endpoint_url = "https://www.youtube.com/youtubei/v1/player?prettyPrint=false"

    headers = {
        "User-Agent": "com.google.android.apps.youtube.vr.oculus/1.60.19 (Linux; U; Android 12L; eureka-user Build/SQ3A.220605.009.A1) gzip",
        "accept-language": "en-US,en",
        "Content-Type": "application/json",
        "X-Youtube-Client-Name": "28"
    }

    data_1 = {
        "context": {
            "client": {
                "clientName": "WEB",
                "osName": "Windows",
                "osVersion": "10.0",
                "clientVersion": "2.20250523.01.00",
                "platform": "DESKTOP"
            }
        },
        "videoId": video_id,
        "contentCheckOk": True
    }

    data_2 = {
        "context": {
            "client": {
                "clientName": "ANDROID_VR",
                "clientVersion": "1.60.19",
                "deviceMake": "Oculus",
                "deviceModel": "Quest 3",
                "osName": "Android",
                "osVersion": "12L",
                "androidSdkVersion": "32"
            }
        }
    }

    r1 = requests.post(endpoint_url, headers=headers, json=data_1)
    visitor_response = r1.json()

    visitor_data = visitor_response["responseContext"]["visitorData"]

    data_2["context"]["client"]["visitorData"] = visitor_data
    data_2.update({
        "videoId": video_id,
        "contentCheckOk": True
    })

    r2 = requests.post(endpoint_url, headers=headers, json=data_2)

    st.text_area("Innertube Response", json.dumps(r2.json(), indent=2), height=400)
