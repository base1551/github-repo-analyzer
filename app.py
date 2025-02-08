import streamlit as st
from github_explain import GitHubExplainer
import os
from dotenv import load_dotenv

def init_session_state():
    if 'explainer' not in st.session_state:
        st.session_state.explainer = None
    if 'repo_loaded' not in st.session_state:
        st.session_state.repo_loaded = False

def load_repository(repo_url, branch):
    try:
        explainer = GitHubExplainer()
        explainer.load_repository(repo_url, branch=branch)
        st.session_state.explainer = explainer
        st.session_state.repo_loaded = True
        return True
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return False

def main():
    st.title("GitHub リポジトリ 説明AI 🤖")

    # 環境変数の読み込み
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OpenAI APIキーが設定されていません。.envファイルを確認してください。")
        st.stop()

    # セッション状態の初期化
    init_session_state()

    # サイドバー：リポジトリ設定
    with st.sidebar:
        st.header("リポジトリ設定")
        repo_url = st.text_input("GitHubリポジトリURL", value="https://github.com/base1551/sample-neo4j")
        branch = st.text_input("ブランチ名", value="main")

        if st.button("リポジトリを読み込む"):
            with st.spinner("リポジトリを読み込んでいます..."):
                success = load_repository(repo_url, branch)
                if success:
                    st.success("リポジトリの読み込みが完了しました！")

    # メインコンテンツ
    if not st.session_state.repo_loaded:
        st.info("👈 サイドバーでGitHubリポジトリを設定してください")
    else:
        st.header("リポジトリに質問する")

        # 質問入力
        question = st.text_area("質問を入力してください", height=100)

        if st.button("質問する"):
            if not question:
                st.warning("質問を入力してください")
            else:
                with st.spinner("回答を生成中..."):
                    answer = st.session_state.explainer.ask_question(question)
                    if answer:
                        st.subheader("回答:")
                        st.write(answer)
                    else:
                        st.error("回答の生成中にエラーが発生しました")

        # 使用例の表示
        with st.expander("💡 質問例"):
            st.markdown("""
            - このリポジトリの主な機能は何ですか？
            - コードの構造を説明してください
            - 実装されている機能について詳しく教えてください
            - このプロジェクトの目的は何ですか？
            """)

if __name__ == "__main__":
    main()
