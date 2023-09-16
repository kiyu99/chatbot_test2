
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting},
        {"role": "bot", "content": "今日は何を学びましたか？"}
    ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("AI Study Mate")
st.image("chatbot.png")
st.write("ChatGPT APIを使ってアウトプット習慣をつけよう。")

# メッセージ表示エリア
if st.session_state["messages"]:
    messages = st.session_state["messages"]
    for message in messages:
      if message["role"] != "system":  # systemメッセージはスキップ
        speaker = "🙂" if message["role"] == "user" else "🤖"
        st.write(speaker + ": " + message["content"])

# メッセージ入力ボックス
user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)
