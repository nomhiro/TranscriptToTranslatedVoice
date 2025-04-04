# TranscriptToTranslatedVoice
トランスクリプト（テキスト文字列）を翻訳し、音声Mp3ファイルとして出力するツールです。このツールはAzure OpenAIサービスを活用して、翻訳と音声合成を行います。

## 主な機能
- テキストの翻訳（Azure OpenAI GPTモデルを使用）
- 翻訳結果を音声（Mp3形式）に変換（Azure Text-to-Speechを使用）

## 必要なAzureリソース
- **Azure OpenAI リソース**
  - リージョン：Text-to-Speechモデルが利用可能なリージョン（例：SwedenCentral）
  - モデル：`gpt-4o`（翻訳用）、`tts-hd`（音声合成用）
- **Azure App Service**

## Azure App Serviceの設定
### 環境変数
以下の環境変数をAzure App Serviceに設定してください：
```
AZURE_OPENAI_ENDPOINT="GPT-4oのAzure OpenAIエンドポイント"
AZURE_OPENAI_API_KEY="GPT-4oのAzure OpenAI APIキー"
AZURE_OPENAI_ENDPOINT_SPEECH="Text-to-SpeechのAzure OpenAIエンドポイント"
AZURE_OPENAI_API_KEY_SPEECH="Text-to-SpeechのAzure OpenAI APIキー"
```

### スタートアップコマンド
以下のコマンドを使用してアプリケーションを起動します：
```
python -m streamlit run main.py --server.port 8000 --server.address 0.0.0.0
```

## 使用方法
1. 必要なAzureリソースを作成し、環境変数を設定します。
2. アプリケーションをデプロイし、スタートアップコマンドを実行します。
3. Webブラウザでアプリケーションにアクセスし、トランスクリプトを入力して翻訳と音声生成を行います。