# GitHub リポジトリ説明 AI

GitHubリポジトリのソースコードを学習し、そのリポジトリに関する質問に回答するAIツールです。コマンドラインとGUIの両方のインターフェースを提供しています。

## 機能

- GitHubリポジトリのソースコードを自動で読み込み
- リポジトリの内容に関する質問に日本語で回答
- トークン使用量とコストの表示
- Streamlit ベースのWebインターフェース
- GPT-4による高精度な回答生成

## システム要件

- Python 3.7以上
- OpenAI APIキー（GPT-4へのアクセス権が必要）
- インターネット接続

## インストール方法

1. リポジトリをクローン:
```bash
git clone https://github.com/base1551/github-repo-analyzer.git
cd github-repo-analyzer
```

2. 依存パッケージをインストール:
```bash
pip install -r requirements.txt
```

3. OpenAI APIキーを設定:
   - プロジェクトルートに`.env`ファイルを作成
   ```
   OPENAI_API_KEY="your-api-key"
   ```

## 実装の詳細

### 主要コンポーネント

1. **GitHubExplainer（github_explain.py）**
   ```python
   class GitHubExplainer:
       def __init__(self):
           # .envファイルから環境変数を読み込み
           load_dotenv()
           self.api_key = os.getenv("OPENAI_API_KEY")
   
       def load_repository(self, clone_url: str, branch: str = "master"):
           # GitHubリポジトリのクローンと読み込み
           loader = GitLoader(...)
           # ベクターストアの作成
           self.index = RetrievalQA.from_chain_type(...)
   
       def ask_question(self, query: str) -> str:
           # 質問に対する回答を生成
           return self.index.run(query)
   ```

2. **Streamlitインターフェース（app.py）**
   ```python
   def main():
       st.title("GitHub リポジトリ 説明AI 🤖")
       
       # サイドバー：リポジトリ設定
       with st.sidebar:
           repo_url = st.text_input("GitHubリポジトリURL")
           branch = st.text_input("ブランチ名", "main")
   
       # メインコンテンツ：質問応答
       if st.session_state.repo_loaded:
           question = st.text_area("質問を入力")
           if st.button("質問する"):
               answer = st.session_state.explainer.ask_question(question)
   ```

### アーキテクチャの特徴

1. **ドキュメント処理**
   - GitLoaderによるリポジトリのクローンと読み込み
   - CharacterTextSplitterによるテキストの分割
   - OpenAI Embeddingsによるベクトル化

2. **検索と質問応答**
   - ChromaDBによる効率的なベクターストア
   - RetrievalQAチェーンによる関連コンテキストの抽出
   - GPT-4による高品質な回答生成

3. **ユーザーインターフェース**
   - コマンドライン（github_explain.py）
   - Webインターフェース（app.py）
   - トークン使用量の可視化

## 使用方法

### コマンドラインインターフェース

```bash
python github_explain.py
```

実行すると、対話式のプロンプトが表示されます：
- 質問を入力して Enter
- 「exit」と入力して終了

### Webインターフェース

```bash
streamlit run app.py
```

ブラウザで http://localhost:8501 が開き、以下の機能が利用可能：
1. サイドバーでGitHubリポジトリのURLとブランチを設定
2. 「リポジトリを読み込む」をクリック
3. メイン画面で質問を入力して「質問する」をクリック
4. 回答とトークン使用状況が表示されます

## エラー対応

1. APIキー関連:
   - `.env`ファイルが正しく配置されているか確認
   - APIキーがGPT-4にアクセス可能か確認

2. リポジトリのクローン失敗:
   - インターネット接続を確認
   - リポジトリのURLとブランチ名を確認
   - アクセス権限を確認

3. メモリ使用量の最適化:
   - `chunk_size`のパラメータ調整
   - 処理対象ファイルの制限
   - 大規模リポジトリの場合は段階的な読み込み

## トークン使用量とコスト

トークン使用量は自動的に表示され、以下の情報が含まれます：
- Prompt Tokens: 入力テキストのトークン数
- Completion Tokens: 生成された回答のトークン数
- Total Tokens: 合計トークン数
- コスト: USD単位での概算コスト

## カスタマイズ

1. チャンクサイズの調整:
```python
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
```

2. 対象ファイルの制限:
```python
file_filter=lambda file_path: file_path.endswith('.py')
```

3. モデルの変更:
```python
llm=ChatOpenAI(model_name="gpt-4")
```

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。
