import streamlit as st
import yt_dlp
import subprocess
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Dixon Pro", page_icon="🫧", layout="centered")

# 2. ADVANCED BUBBLE CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .main { background: linear-gradient(135deg, #eef2f3 0%, #8e9eab 100%); }
    
    /* Bubble Element Styling */
    .stTextInput, .stSelectbox, .stSlider, .stTabs, .stVideo, [data-testid="stMarkdownContainer"] {
        background: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.4);
        margin-bottom: 15px;
    }

    /* Professional Button */
    .stButton>button {
        width: 100%;
        border-radius: 25px !important;
        background: linear-gradient(90deg, #007AFF, #00C6FF) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 15px !important;
        border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(0,122,255,0.4); }
    
    /* Hide Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: CONTROL PANEL
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🫧 Controls</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # NEW: Duration Selection (Bubble Style)
    st.subheader("⏱️ Clip Duration")
    duration = st.select_slider(
        "Select length (seconds):",
        options=[15, 30, 60, 90, 120],
        value=30
    )
    
    # NEW: Quality Selection
    st.subheader("📺 Quality")
    quality = st.radio("Select resolution:", ["720p", "1080p (HQ)"], horizontal=True)
    
    st.markdown("---")
    st.subheader("⚙️ Advanced")
    start_time = st.text_input("Start Time (HH:MM:SS)", value="00:00:10")
    ratio = st.selectbox("Aspect Ratio", ["9:16 Vertical (TikTok)", "16:9 Landscape"])
    
    st.markdown("---")
    st.markdown(f"""
        <a href="https://saweria.co/your_username" target="_blank" style="text-decoration:none;">
            <div style="background:#000; color:#fff; padding:12px; border-radius:20px; text-align:center; font-weight:bold;">
                ☕ Support My Work
            </div>
        </a>
    """, unsafe_allow_html=True)

# 4. MAIN INTERFACE
st.markdown("<h1 style='text-align: center; color: #1d1d1f; font-weight: 800;'>BubbleClip AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #86868b;'>Simple, Fast, High-Quality Clips</p>", unsafe_allow_html=True)

url = st.text_input("🔗 Paste YouTube URL:", placeholder="https://youtube.com/watch?v=...")

tab1, tab2, tab3 = st.tabs(["🚀 Generator", "📖 Guide", "🛡️ Privacy"])

with tab1:
    if st.button("GENERATE MAGIC CLIP"):
        if url:
            with st.spinner(f"Creating {duration}s clip in {quality}..."):
                try:
                    # Logic for Resolution
                    h_val = "1080" if "1080p" in quality else "720"
                    
                    ydl_opts = {
                        'format': f'bestvideo[height<={h_val}][ext=mp4]+bestaudio[ext=m4a]/best[height<={h_val}][ext=mp4]/best',
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        video_url = info['url']
                        video_title = info.get('title', 'clip')

                    output_file = "bubble_final.mp4"
                    
                    # FFmpeg Command
                    if "9:16" in ratio:
                        # Crop & Scale to selected quality
                        cmd = [
                            'ffmpeg', '-ss', start_time, '-i', video_url, '-t', str(duration),
                            '-vf', f'crop=ih*9/16:ih,scale=-1:{h_val}', 
                            '-c:v', 'libx264', '-crf', '20', '-c:a', 'aac', '-y', output_file
                        ]
                    else:
                        # Original & Scale to selected quality
                        cmd = [
                            'ffmpeg', '-ss', start_time, '-i', video_url, '-t', str(duration),
                            '-vf', f'scale=-1:{h_val}',
                            '-c:v', 'libx264', '-crf', '20', '-c:a', 'aac', '-y', output_file
                        ]
                    
                    subprocess.run(cmd, check=True)

                    if os.path.exists(output_file):
                        st.balloons()
                        st.success(f"✅ {quality} Clip Ready!")
                        st.video(output_file)
                        with open(output_file, "rb") as f:
                            st.download_button("📥 DOWNLOAD MP4", f, file_name=f"Bubble_{video_title}.mp4")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please paste a link first!")

with tab2:
    st.write("Settings updated! You can now choose up to 120 seconds and 1080p resolution.")

with tab3:
    st.caption("Temporary files are deleted after each session.")
                          
