
import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

# アプリ概要・操作説明
st.title("専門家LLM相談アプリ")
st.markdown("""
このアプリは、選択した専門家の視点でAI（LLM）に質問できるWebアプリです。\\
以下の手順でご利用ください：
1. 専門家の種類を選択してください（例：医療、法律、IT）。
2. 質問内容を入力し、送信ボタンを押してください。
3. AIが専門家として回答します。
""")

# 専門家の種類
expert_types = {
    "A 医療": "あなたは優秀な医師です。医学的知識に基づき、分かりやすく回答してください。",
    "B 法律": "あなたは経験豊富な弁護士です。法律的観点から、丁寧に回答してください。"
}

selected_expert = st.radio("専門家の種類を選択してください", list(expert_types.keys()))

user_input = st.text_area("質問内容を入力してください", height=100)

# LLM問い合わせ関数
def ask_expert_llm(question: str, expert_type: str) -> str:
    """
    入力テキストと専門家タイプを受け取り、LLMからの回答を返す
    """
    system_message = expert_types.get(expert_type, "あなたは優秀な専門家です。")
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=question)
    ]
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)
    response = llm.invoke(messages)
    return response.content

if st.button("送信"):
    if user_input.strip():
        with st.spinner("AIが回答中..."):
            answer = ask_expert_llm(user_input, selected_expert)
        st.markdown(f"### {selected_expert}の回答")
        st.write(answer)
    else:
        st.warning("質問内容を入力してください。")