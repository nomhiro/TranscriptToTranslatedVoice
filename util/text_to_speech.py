import os
import azure.cognitiveservices.speech as speechsdk

# この例では、環境変数 "SPEECH_KEY" と "SPEECH_REGION" が必要です
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

# 出力ファイルの設定
output_file = "output.mp3"
audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)

# ニューラル多言語音声は、入力テキストに基づいて異なる言語を話すことができます。
speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# コンソールからテキストを取得し、MP3ファイルに合成します。
text = "Hello. My name is Hiroki Nomura. What is the weather for tomorrow?"

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("テキスト [{}] の音声合成が完了しました。ファイル: {}".format(text, output_file))
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("音声合成がキャンセルされました: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("エラーの詳細: {}".format(cancellation_details.error_details))
            print("音声リソースキーとリージョン値を設定しましたか？")
        # 接続エラーの詳細を出力
        print("接続エラーの詳細:")
        print("エンドポイント: {}".format(speech_config.get_property(speechsdk.PropertyId.SpeechServiceConnection_Endpoint)))
        print("リージョン: {}".format(os.environ.get('SPEECH_REGION')))
        print("キー: {}".format(os.environ.get('SPEECH_KEY')))