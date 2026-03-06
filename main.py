from flask import Flask, render_template_string, request
import requests
import json

app = Flask(__name__)

# The HTML template defined as a string
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Audio Test</title>
    <style>
        body { font-family: sans-serif; max-width: 900px; margin: 40px auto; line-height: 1.6; padding: 0 20px; }
        .box { border: 1px solid #ccc; padding: 15px; border-radius: 8px; background: #f9f9f9; margin-bottom: 20px; }
        textarea { width: 100%; height: 250px; font-family: monospace; font-size: 12px; }
        input[type="text"] { width: 250px; padding: 8px; }
        button { padding: 8px 15px; cursor: pointer; background: #007bff; color: white; border: none; border-radius: 4px; }
        .error { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>YouTube InnerTube API Test</h1>
    
    <div class="box">
        <form method="POST">
            <label>Enter Video ID:</label>
            <input type="text" name="video_id" value="{{ video_id }}" placeholder="e.g. dQw4w9WgXcQ" required>
            <button type="submit">Extract Audio</button>
        </form>
    </div>

    {% if audio_url %}
    <div class="box">
        <h3>Audio Player (itag 140)</h3>
        <audio controls src="{{ audio_url }}" style="width: 100%;"></audio>
        <p><small>Link extracted. If it doesn't play, the URL might be IP-restricted.</small></p>
    </div>
    {% elif video_id and not error %}
    <div class="box error">
        No itag 140 found in the response streaming data.
    </div>
    {% endif %}

    {% if error %}
    <div class="box error">{{ error }}</div>
    {% endif %}

    {% if response_json %}
    <h3>Raw JSON Response</h3>
    <textarea readonly>{{ response_json }}</textarea>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    video_id = ""
    audio_url = None
    response_json = None
    error = None

    if request.method == "POST":
        video_id = request.form.get("video_id")
        endpoint_url = "https://www.youtube.com/youtubei/v1/player?prettyPrint=false"
        
        headers = {
            "User-Agent": "com.google.android.apps.youtube.vr.oculus/1.60.19 (Linux; U; Android 12L; eureka-user Build/SQ3A.220605.009.A1) gzip",
            "Content-Type": "application/json",
            "X-Youtube-Client-Name": "28"
        }

        try:
            # 1. Get Visitor Data (WEB Client)
            data_1 = {
                "context": {"client": {"clientName": "WEB", "clientVersion": "2.20250523.01.00"}},
                "videoId": video_id
            }
            r1 = requests.post(endpoint_url, headers=headers, json=data_1)
            r1.raise_for_status()
            visitor_data = r1.json().get("responseContext", {}).get("visitorData")

            # 2. Get Audio URL (ANDROID_VR Client)
            data_2 = {
                "context": {
                    "client": {
                        "clientName": "ANDROID_VR",
                        "clientVersion": "1.60.19",
                        "visitorData": visitor_data
                    }
                },
                "videoId": video_id,
                "contentCheckOk": True
            }
            
            r2 = requests.post(endpoint_url, headers=headers, json=data_2)
            r2.raise_for_status()
            resp_data = r2.json()
            
            # Format JSON for the textarea
            response_json = json.dumps(resp_data, indent=2)

            # 3. Extract itag 140
            formats = resp_data.get("streamingData", {}).get("adaptiveFormats", [])
            for f in formats:
                if f.get("itag") == 140:
                    audio_url = f.get("url")
                    break
        
        except Exception as e:
            error = f"Request Failed: {str(e)}"

    return render_template_string(
        HTML_TEMPLATE, 
        video_id=video_id, 
        audio_url=audio_url, 
        response_json=response_json,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
