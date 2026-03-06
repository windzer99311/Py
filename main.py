import streamlit as st
import requests

audio_url = "https://rr3---sn-ab5l6nrr.googlevideo.com/videoplayback?expire=1772852633&ei=OUGraaqhG_z4sfIP6sfHwQw&ip=fda3%3Ae722%3Aac3%3A10%3A3a%3Ad817%3Ac0a8%3A16f&id=o-AIMOhP6pO6kYNqCawhjo81IMv6DVBFuwTGUiZGKfoLRJ&itag=140&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1772831033%2C&mh=g7&mm=31%2C29&mn=sn-ab5l6nrr%2Csn-ab5sznzr&ms=au%2Crdu&mv=D&mvi=3&pl=0&rms=au%2Cau&gcr=zz&bui=AVNa5-wsTotJj1kZovY7ra9Gg2gzsQCNVr0JHPuB3edIeHLGSSaneAobUgMlH6DvrgyXil1ifH2dFR-5&spc=6dlaFPwDwfc33gG7roxhVysxkGzUg5ScjobIM3RSyD4f9NmO&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=2863548&dur=176.889&lmt=1731252361545034&mt=1772830820&fvip=3&keepalive=yes&fexp=51565116%2C51565681%2C51791334&c=ANDROID_VR&txp=4532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cgcr%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgWPige3Sm2q9UjgydABspbidfyuZrHeSny3Vbv9W34yYCIQDKCr1g7zqRqsdHHEr_Wxt8TyeDD4H_wmo2XbLChIGWBg%3D%3D&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms&lsig=APaTxxMwRAIgKGqwTSCKKOMMIcbMNBjrzmOl0QlTwwxlkc6h4WHGDi0CIB4FqJMLsSbH3QdJkObtJfDB_G_B6bv9Bwrn7WsF_Qk2"

st.title("Google Audio Player")

try:
    # 1. Fetch the data
    response = requests.get(audio_url)

    # 2. Check the response status
    if response.status_code == 200:
        st.success("Audio loaded successfully!")
        
        # 3. Play the audio using binary content
        st.audio(response.content, format="audio/mp4")
        
        # 4. Debug info (to check what you're actually getting)
        with st.expander("View Response Headers"):
            st.write(response.headers)
    else:
        st.error(f"Failed to load audio. Status code: {response.status_code}")
        if response.status_code == 403:
            st.warning("The link has likely expired or access is forbidden.")

except Exception as e:
    st.error(f"An error occurred: {e}")
