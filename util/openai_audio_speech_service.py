import os
import requests

def text_to_speech_with_openai(input_text, voice: str = "fable"):
    """
    Azure OpenAI Service を使用してテキストを音声に変換し、音声データを返却します。

    Args:
        input_text (str): 音声合成するテキスト。
        voice (str): 使用する音声の種類。

    Returns:
        bytes: 音声データ。
    """
    # 環境変数からエンドポイントとAPIキーを取得
    openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT_SPEECH")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY_SPEECH")
    deployment_name = "tts-hd"

    if not openai_endpoint or not api_key:
        raise ValueError("AZURE_OPENAI_ENDPOINT または AZURE_OPENAI_API_KEY が設定されていません。")

    # リクエストURL
    url = f"{openai_endpoint}/openai/deployments/{deployment_name}/audio/speech?api-version=2024-02-15-preview"

    # リクエストヘッダーとデータ
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "model": deployment_name,
        "input": input_text,
        "voice": voice
    }

    # リクエスト送信
    response = requests.post(url, headers=headers, json=data, stream=True)

    if response.status_code == 200:
        # 音声データを返却
        return response.content
    else:
        # エラー処理
        raise Exception(f"音声合成に失敗しました。ステータスコード: {response.status_code}, レスポンス: {response.text}")

# 使用例
if __name__ == "__main__":
    text = "日本の中心に位置する愛知県は、伝統、革新、そして自然美が見事に融合した魅力的なエリアです。象徴的な名古屋城や活気あふれる名古屋市を有し、愛知県は歴史と文化の中心地です。瀬戸では伝統的な陶器づくりを体験したり、地元の名物である味噌カツというトンカツのユニークなアレンジを堪能したりできます。車好きには、トヨタ産業技術記念館で愛知の製造業における先進的な姿を学ぶことができます。自然愛好家にとって、香嵐渓の美しい景色、特に秋の紅葉は必見です。その豊かな遺産、近代的な観光地、または壮大な自然景観に惹かれる方にとって、愛知県は忘れられない体験を提供してくれます。"
    try:
        audio_data = text_to_speech_with_openai(text)
        with open("speech.mp3", "wb") as f:
            f.write(audio_data)
        print("音声合成が完了しました。ファイル: speech.mp3")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
