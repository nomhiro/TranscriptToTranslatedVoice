import os
import openai
from util.model import TranslateItem

openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2025-03-01-preview"


def translate_target_language(transcript: str, to_language: str) -> TranslateItem:
    prompt = f'''
    あなたは登壇や説明用のトランスクリプトを、{to_language} に翻訳する翻訳家です。
    翻訳時には以下のルールを厳守してください。

    1. 情報を改変しない
    原文の意味・意図を変えず、正確に翻訳してください。
    原文中の専門用語や固有名詞（製品名やサービス名など）も、適切に翻訳してください。
    '''

    response = openai.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": transcript}
        ],
        response_format=TranslateItem
    )

    translated_item = response.choices[0].message.parsed
    return translated_item

# translate_target_language 関数をエクスポート可能にする
__all__ = ["translate_target_language"]