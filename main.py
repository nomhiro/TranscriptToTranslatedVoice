# 翻訳先言語リストを定義
TRANSLATION_LANGUAGES = {
    "en": "英語",
    "ja": "日本語",
    "es": "スペイン語",
    "fr": "フランス語",
    "de": "ドイツ語",
    "zh": "中国語",
    "ko": "韓国語",
    "ru": "ロシア語",
    "it": "イタリア語",
    "pt": "ポルトガル語",
    "ar": "アラビア語",
    "hi": "ヒンディー語",
}

import streamlit as st
from util.openai_service import translate_target_language  # 翻訳関数をインポートefwefw
from util.openai_audio_speech_service import text_to_speech_with_openai  # 音声合成関数をインポート

# 画面全体を使う設定
st.set_page_config(
    page_title="音声化アプリ",
    page_icon=":microphone:",
    layout="wide",
)

# トップ画面
def top_screen():
    st.title("テキスト 音声化 アプリ")
    progress = 1 / (3 if st.session_state.get("translation_required") == "はい" else 2)
    st.progress(progress)  # 進捗バーを表示
    
    st.header("トランスクリプト入力")
    
    # トランスクリプト入力欄
    transcript_input = st.text_area(
        "トランスクリプトを入力してください",
        value=st.session_state.get("transcript", ""),  # セッション状態から値を取得
        height=400,
        disabled=st.session_state.get("processing", False)
    )
    
    # 翻訳有無の選択
    translation_required = st.radio(
        "翻訳が必要ですか？",
        ("はい", "いいえ"),
        index=0 if st.session_state.get("translation_required") == "はい" else 1,  # セッション状態から値を取得
        disabled=st.session_state.get("processing", False)
    )
    
    # 翻訳先言語の選択
    if translation_required == "はい":
        default_language = st.session_state.get("translation_language", "英語")
        if default_language not in TRANSLATION_LANGUAGES.values():
            default_language = "英語"  # デフォルト値を安全に設定
        translation_language = st.selectbox(
            "翻訳先言語を選択してください",
            list(TRANSLATION_LANGUAGES.values()),
            index=list(TRANSLATION_LANGUAGES.values()).index(default_language),  # セッション状態から値を取得
            disabled=st.session_state.get("processing", False)
        )
    else:
        translation_language = None
    
    # ボタン名を条件に応じて変更
    button_label = "翻訳して次へ" if translation_required == "はい" else "次へ"
    
    # ボタン
    if st.button(button_label, disabled=st.session_state.get("processing", False)):
        # 処理中フラグを設定
        st.session_state["processing"] = True
        with st.spinner("処理中です..."):
            # ボタンが押されたことをセッション状態に保存
            st.session_state["transcript"] = transcript_input
            st.session_state["translation_required"] = translation_required
            st.session_state["translation_language"] = translation_language
            
            # 翻訳処理を実行
            if translation_required == "はい" and transcript_input and translation_language:
                to_language_code = list(TRANSLATION_LANGUAGES.keys())[list(TRANSLATION_LANGUAGES.values()).index(translation_language)]
                try:
                    translated_item = translate_target_language(transcript_input, to_language_code)
                    st.session_state["translated_text"] = translated_item.translated_text  # 翻訳結果を保存
                except Exception as e:
                  st.error(f"翻訳中にエラーが発生しました: {e}")
                finally:
                    st.session_state["processing"] = False  # 処理中フラグを解除
            else:
                st.session_state["translated_text"] = transcript_input  # 翻訳不要の場合はそのまま保存
            
            st.session_state["page"] = "edit_translation" if translation_required == "はい" else "generate_audio"
            st.session_state["processing"] = False
            st.rerun()  # 状態変更後に即座に再レンダリング

# 翻訳結果編集と音声ファイル生成画面
def edit_and_generate_audio_screen():
    st.title("翻訳結果編集と音声ファイル生成")
    progress = 3 / 3 if st.session_state.get("translation_required") == "はい" else 2 / 2
    st.progress(progress)  # 進捗バーを表示

    # 翻訳結果の表示と編集
    if "edited_translation" not in st.session_state or st.session_state.get("translated_text") != st.session_state.get("last_translated_text"):
        # 翻訳結果が変更された場合に初期化
        st.session_state["edited_translation"] = st.session_state.get("translated_text", st.session_state.get("transcript", ""))
        st.session_state["last_translated_text"] = st.session_state.get("translated_text")
    
    edited_translation = st.text_area(
        "翻訳結果を編集してください",
        value=st.session_state["edited_translation"],
        height=400,
        key="edited_translation_widget"
    )
    
    # ボタン
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("戻る"):
            st.session_state["page"] = "top"
            st.session_state["processing"] = False
            # st.session_stateのaudio_dataをクリア
            if "audio_data" in st.session_state:
                del st.session_state["audio_data"]
            st.rerun()  # 状態変更後に即座に再レンダリング
    with col2:
        if st.button("音声化する", disabled=st.session_state.get("processing", False)):
            st.session_state["processing"] = True  # 処理中フラグを設定
            with st.spinner("音声化処理中です..."):
              try:
                  # 音声合成を実行（セッションの値を変更せずに使用）
                  audio_data = text_to_speech_with_openai(edited_translation)
                  st.session_state["audio_data"] = audio_data  # 音声データをセッションに保存
                  st.success("音声ファイルが生成されました！以下で再生またはダウンロードしてください。")
              except Exception as e:
                  st.error(f"音声合成中にエラーが発生しました: {e}")
                  st.session_state["audio_data"] = None
              finally:
                  st.session_state["processing"] = False  # 処理中フラグを解除
    with col3:
        if "audio_data" in st.session_state:
            # 音声をブラウザ上で再生する機能を追加
            st.audio(st.session_state["audio_data"], format="audio/mpeg")
            # ダウンロードボタンを保持
            st.download_button(
                "音声ファイルをダウンロード",
                data=st.session_state["audio_data"],
                file_name="output.mp3",
                mime="audio/mpeg"
            )

# ページ遷移の管理
if "page" not in st.session_state:
    st.session_state["page"] = "top"

# ページをレンダリング
page = st.session_state["page"]
if page == "top":
    top_screen()
elif page == "edit_translation":
    edit_and_generate_audio_screen()
elif page == "generate_audio":
    edit_and_generate_audio_screen()

