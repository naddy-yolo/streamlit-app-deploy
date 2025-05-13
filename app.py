from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# タイトルと説明
st.title("専門家に相談できるAIアプリ")
st.write("以下の入力欄に質問を入力し、相談したい専門家の種類を選んでください。")

# ラジオボタンで専門家を選択
expert_type = st.radio(
    "相談したい専門家を選んでください：",
    ("栄養士", "メンタルコーチ")
)

# ユーザー入力欄
user_input = st.text_area("質問内容を入力してください")

# 送信ボタンで処理開始
if st.button("送信"):
    # 専門家に応じてシステムプロンプトを変更
    if expert_type == "栄養士":
        system_prompt = "あなたは有能な栄養士です。相手の健康やダイエットについて専門的にアドバイスしてください。"
    elif expert_type == "メンタルコーチ":
        system_prompt = "あなたは有能なメンタルコーチです。相談者の心の支えになるよう、丁寧で思いやりのある返答をしてください。"

    # OpenAI APIキーを環境変数から取得
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("OpenAI APIキーが設定されていません。")
    else:
        # Chatモデルの準備
        chat = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=openai_api_key
        )

        # メッセージ構築
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]

        # 回答生成
        response = chat.invoke(messages)

        # 回答表示
        st.write("AIからの回答：")
        st.write(response.content)
