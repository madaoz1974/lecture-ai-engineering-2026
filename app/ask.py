"""第1回: LLMに質問し、会話を続けるスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールを使わない「素の」呼び出し。
初回の回答後は、質問を入力すると同じチャットで会話を続けられる。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def print_response(response: object) -> str:
    usage = response.usage_metadata
    print(
        f"[usage] input_tokens={usage.prompt_token_count}, "
        f"output_tokens={usage.candidates_token_count}"
    )
    print(response.text)
    return response.text


def ask(chat: object, question: str) -> str:
    response = chat.send_message(question)
    return print_response(response)


def main() -> None:
    parser = argparse.ArgumentParser(description="会話履歴を保ったままLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")
    try:
        ask(chat, args.question)
        while True:
            try:
                question = input("\n質問> ").strip()
            except EOFError:
                print()
                break
            if not question or question.lower() in {"exit", "quit"}:
                break
            ask(chat, question)
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
