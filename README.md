# TranscriptToTranslatedVoice
トランスクリプト（テキスト文字列）を翻訳して音声Mp3にするツールです。

# Azureリソース
- Azure OpenAI リソース
  - リージョン：TextToSpeechモデルが利用できる、SwedenCentral
  - モデル：gpt-4o, tts-hd
- Azure App Service

AzureAppServiceの環境変数
```
AZURE_OPENAI_ENDPOINT="GPT-4oのAzureOpenAIののエンドポイント"
AZURE_OPENAI_API_KEY="GPT-4oのAzureOpenAIののAPIキー"
AZURE_OPENAI_ENDPOINT_SPEECH="TextToSpeechのAzureOpenAIののエンドポイント"
AZURE_OPENAI_API_KEY_SPEECH="TextToSpeechのAzureOpenAIののAPIキー"
```

AzureAppServiceのスタートアップコマンド
```
python -m streamlit run main.py --server.port 8000 --server.address 0.0.0.0
```