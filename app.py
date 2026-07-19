import streamlit as st
import time
import subprocess
from api import generate_response
import streamlit.components.v1 as components
    
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>
        .main {
            padding-top: 1rem;
        }

        .chat-title{
            text-align:center;
            font-size:20px;
            font-weight:700;
            margin-bottom:1px;
        }

        .block-container{
            max-width:900px;
        }

        .stChatMessage{
            border-radius:15px;
        }
            
        div.stButton > button:first-child {
        position: fixed;
        top: 60px;
        left: 10px;
        width: 40px;
        height: 38px;
        z-index: 999;
        background:#202123;
        color:white;
        padding:0.3rem 0.8rem;
        font-size:14px;
        border:1px solid #3a3a3a;
        border-radius: 16px;
        }   
        div.stButton > button:first-child:hover{
            border-color:#666;
        }
            
        .chat-container{
        display:flex;
        flex-direction:column;
        gap:12px;
        margin-top:15px;
        }

        .user-row{
            display:flex;
            justify-content:flex-end;
            margin-bottom:5px;
        }

        .bot-row{
            display:flex;
            justify-content:flex-start;
            margin-bottom:15px;
        }

        .user-bubble{
            background:#2563EB;
            color:white;
            padding:12px 16px;
            border-radius:18px 18px 4px 18px;
            max-width:70%;
            font-size:16px;
            line-height:1.5;
            word-wrap:break-word;
        }

        .bot-bubble{
            background:#2B2D31;
            color:white;
            padding:12px 16px;
            border-radius:18px 18px 18px 4px;
            max-width:70%;
            font-size:16px;
            line-height:1.5;
            word-wrap:break-word;
        }

        /* Input container */
        [data-testid="stChatInput"] {
            border-radius: 28px !important;
            overflow: hidden;
        }

        /* Input field */
        [data-testid="stChatInput"] textarea {
            border-radius: 28px !important;
        }

        /* Send button */
        [data-testid="stChatInput"] button {
            border-radius: 50% !important;
            width: 32px !important;
            height: 32px !important;
        }
        
        /* Main chat input */
        [data-testid="stChatInput"]{
            border-radius:30px !important;
        }
        /* Remove Streamlit focus ring */
        [data-testid="stChatInput"]:focus-within{
            outline:none !important;
            box-shadow:none !important;
            border-color:transparent !important;
        }
        /* Target the inner container */
        [data-testid="stChatInput"] > div{
            outline:none !important;
            box-shadow:none !important;
            border:none !important;
        }
        /* Textarea */
        [data-testid="stChatInput"] textarea{
            outline:none !important;
            box-shadow:none !important;
            border:none !important;
        }
            
        /* Add space on the left inside the input */
        [data-testid="stChatInput"] textarea{
            padding-left: 30px !important;   /* Increase if needed */
        }

        /* If using a text input instead of chat_input */
        [data-testid="stTextInput"] input{
            padding-left: 60px !important;
        }

        /* ---------- Popover Button ---------- */
        [data-testid="stPopover"] button{
            width:42px;
            height:45px;
            border-radius:50% !important;
            border:none !important;
            background:#2b2d31 !important;
            color:white !important;
            font-size:22px;
            transition:.2s;
        }

        [data-testid="stPopover"] button:hover{
            background:#3a3d42 !important;
            transform:scale(1.05);
        }

        /* Position */
        [data-testid="stPopover"]{
            position: fixed;
            bottom: 65px;
            left: 20px;
            width: 42px;
            height: 42px;
            z-index: 999;
        }

        /* ---------- Popup ---------- */
        [data-testid="stPopoverContent"]{
            border-radius:18px !important;
            border:1px solid #404040 !important;
            background:#202123 !important;
            padding:15px !important;
            min-width:240px;
        }

        /* ---------- Selectbox ---------- */
        [data-baseweb="select"]{
            border-radius:12px !important;
        }

        /* ---------- Label ---------- */
        [data-testid="stPopoverContent"] h4{
            margin-top:0;
            margin-bottom:12px;
            color:white;
            font-size:16px;
        }

        /* ---------- Remove extra spacing ---------- */
        [data-testid="stPopoverContent"] .stMarkdown{
            margin-bottom:8px;
        }
            
        @keyframes blink {
            50% {
                opacity: 0;
            }
        }
        .cursor {
            animation: blink 1s infinite;
        }
            
        .thinking {
            display: flex;
            align-items: center;
            gap: 6px;
            color: #bdbdbd;
        }

        .thinking-dot {
            width: 8px;
            height: 8px;
            background: #bdbdbd;
            border-radius: 50%;
            animation: bounce 1.4s infinite ease-in-out;
        }

        .thinking-dot:nth-child(2) {
            animation-delay: .2s;
        }

        .thinking-dot:nth-child(3) {
            animation-delay: .4s;
        }

        @keyframes bounce {
            0%,80%,100% {
                transform: scale(0.6);
                opacity: .4;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
# st.markdown('<div class="chat-title">🤖 College AI Assistant</div>', unsafe_allow_html=True)

# ---------- User Name ----------

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if st.session_state.user_name == "":

    st.title("👋 Welcome I'm Sora")

    Name = st.text_input(
        "Enter your name",
        placeholder="e.g. Dip",
    )

    if Name.strip():
        st.session_state.user_name = Name.strip()
        st.rerun()

    st.caption("Press Enter to continue")
    st.stop()

# new chat
if st.button("✛"):
    name = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[name] = [
        {
            "role": "assistant",
            "content": "What’s on your mind today?"
        }
    ]
    st.session_state.current_chat = name
    st.session_state.pending_response = False
    st.rerun()

with st.popover(""):
    st.markdown("##### Models")
    model = st.selectbox(
        "",
        ["💨 gemini 3.1 flash lite", "🧠 Gemini 3 (creative)","⚡ Gemini 3.5 Flash (complex)"],
        label_visibility="collapsed"
    )
    st.markdown("##### Voices")
    voice_mode = st.checkbox("Voice Mode",True)
    voice = st.selectbox(
        "voice",
        ["Karen","Samantha","Soumya","Moira"],
        label_visibility="collapsed"
    )


# ---------- Session ----------
if "chats" not in st.session_state:
    st.session_state.chats = {
        "New Chat": [
            {
                "role": "assistant",
                "content": f"Hello {st.session_state.user_name} 👋 How can I help you today?"
            }
        ]
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# ---------- Display Messages ----------
messages = st.session_state.chats[
    st.session_state.current_chat
]

for msg in messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="user-row">
                <div class="user-bubble">
                    {msg["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="bot-row">
                <div class="bot-bubble">
                    {msg["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------- Chat Input ----------#

if "pending_response" not in st.session_state:
    st.session_state.pending_response = False

if prompt := st.chat_input("Message..."):

    # User message
    st.session_state.chats[
    st.session_state.current_chat
        ].append(
            {
                "role":"user",
                "content":prompt
            }
        )

    st.session_state.pending_response = True
    st.rerun()

if (
    st.session_state.pending_response
    and messages
    and messages[-1]["role"] == "user"
):

    placeholder = st.empty()
    placeholder.markdown("""
    <div class="bot-row">
        <div class="bot-bubble">
            <div class="thinking">
                Thinking
                <div class="thinking-dot"></div>
                <div class="thinking-dot"></div>
                <div class="thinking-dot"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    response = generate_response(
        st.session_state.user_name,
        messages[-20:],
        model
    )

    if voice_mode:
        components.html(
        f"""
        <script>
        const selectedVoice = {voice!r};
        const text = {response!r};

        function speak() {{
            speechSynthesis.cancel();

            const utterance = new SpeechSynthesisUtterance(text);

            const voices = speechSynthesis.getVoices();

            const found = voices.find(v => v.name === selectedVoice);

            if (found) {{
                utterance.voice = found;
            }} else {{
                console.log("Voice not found:", selectedVoice);
                utterance.voice = voices[0];
            }}

            speechSynthesis.speak(utterance);
        }}

        if (speechSynthesis.getVoices().length === 0) {{
            speechSynthesis.onvoiceschanged = speak;
        }} else {{
            speak();
        }}
        </script>
        """,
        height=0,
    )

    text = ""
    for ch in response:

        text += ch
        placeholder.markdown(
            f"""
            <div class="bot-row">
                <div class="bot-bubble">
                    {text}<span style="animation:blink 1s infinite;">▌</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if voice_mode:
            time.sleep(0.05)
        else: time.sleep(0.0045)

    # Remove cursor at the end
    placeholder.markdown(
        f"""
        <div class="bot-row">
            <div class="bot-bubble">
                {response}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.session_state.chats[
    st.session_state.current_chat
].append(
    {
        "role":"assistant",
        "content":response
    }
)

    st.session_state.pending_response = False
    st.rerun()

