#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from dotenv import load_dotenv
from typing import Optional

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import GitLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

class GitHubExplainer:
    def __init__(self):
        load_dotenv()  # .envファイルから環境変数を読み込む
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY環境変数が設定されていません。.envファイルを確認してください。")

        self.repo_path = "./temp/"
        self.index = None

    def load_repository(self, clone_url: str, branch: str = "master", file_filter: str = "") -> None:
        """
        GitHubリポジトリを読み込み、インデックスを作成します。

        Args:
            clone_url (str): GitHubリポジトリのURL
            branch (str, optional): 使用するブランチ名. デフォルト: "master"
            file_filter (str, optional): 読み込むファイルの拡張子. デフォルト: ".py"
        """
        try:
            if os.path.exists(self.repo_path):
                # 既にクローン済みの場合はURLをNoneに設定
                loader = GitLoader(
                    clone_url=None,
                    branch=branch,
                    repo_path=self.repo_path,
                    file_filter=lambda file_path: file_path.endswith(file_filter)
                )
            else:
                loader = GitLoader(
                    clone_url=clone_url,
                    branch=branch,
                    repo_path=self.repo_path,
                    file_filter=lambda file_path: file_path.endswith(file_filter)
                )

            # ドキュメントの読み込み
            documents = loader.load()

            # テキストの分割
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.split_documents(documents)

            # ベクトルストアの作成
            embeddings = OpenAIEmbeddings(disallowed_special=())
            vectorstore = Chroma.from_documents(texts, embeddings)

            # 検索チェーンの作成
            self.index = RetrievalQA.from_chain_type(
                llm=ChatOpenAI(model_name="gpt-4"),
                chain_type="stuff",
                retriever=vectorstore.as_retriever()
            )

            print("リポジトリの読み込みとインデックス作成が完了しました")

        except Exception as e:
            raise Exception(f"リポジトリの読み込み中にエラーが発生しました: {str(e)}")

    def ask_question(self, query: str) -> Optional[str]:
        """
        リポジトリに関する質問に回答します。

        Args:
            query (str): 質問内容

        Returns:
            Optional[str]: 回答。エラーの場合はNone
        """
        if not self.index:
            raise ValueError("先にリポジトリを読み込んでください")

        try:
            with get_openai_callback() as cb:
                answer = self.index.run(query)
                print(f"\nトークン使用状況:")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"コスト: ${cb.total_cost:.4f}")
                return answer
        except Exception as e:
            print(f"質問への回答中にエラーが発生しました: {str(e)}")
            return None

def main():
    try:
        explainer = GitHubExplainer()

        # Neo4jのサンプルリポジトリを使用
        repo_url = "https://github.com/base1551/sample-neo4j"
        print(f"リポジトリを読み込んでいます: {repo_url}")
        explainer.load_repository(repo_url, branch="main")

        while True:
            query = input("\n質問を入力してください（終了する場合は'exit'と入力）: ")
            if query.lower() == 'exit':
                break

            answer = explainer.ask_question(query)
            if answer:
                print("\n回答:")
                print(answer)
            else:
                print("\nエラーが発生しました。もう一度試してください。")

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
