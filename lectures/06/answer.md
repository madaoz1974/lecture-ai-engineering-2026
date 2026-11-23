# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 バージョニング 概要'}) / aws_aws___search_documentation({'search_phrase': 'Versioning Amazon S3 overview what is it', 'topics': ['general']})
- 気づき・疑問：設定ファイル（app/mcp_servers.json）に command や url を書き足すだけで、ローカルの自作サーバー、uvx で取得する公開サーバー、外部ホスティングのサーバーを統一的にエージェントへ接続できる点が非常に便利だと感じた。また、STEP 4 では日本語クエリで期待した情報が得られなかった際に、モデルが自律的に英語クエリへ言い換えて再検索する挙動が確認できた。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎
- やったこと：
  - サーバー側の `app/mcp_server.py` のみを編集し、`server.tool()(tools.get_lecture_summary)` の 1 行を追加して `get_lecture_summary` ツールを公開した。
  - エージェント側（`app/mcp_servers.json`・`app/mcp_agent.py`）は一切変更せずに、`git status`、`--list-tools`、`--trace` での質問実行、および `uv run pytest -q` を実行して動作を確認した。
- 結果：
  - `git status`：変更ファイルが `app/mcp_server.py` のみであることを確認した。
  - `--list-tools`：エージェント側を変更していない状態で、一覧に `glossary_get_lecture_summary` が追加され、モデルに見えているツールが 7 個から 8 個に増えたことを確認した。
  - `--trace "第2回では何を学びますか？"`：
    - `[tool call]`：`glossary_get_lecture_summary({'lecture': 2})`
    - MCP サーバー経由で第2回「ファインチューニングとLoRA」の要点が返却され、モデル応答 2 回（入力 5,942 tokens / 出力 221 tokens）で正しく回答された。
  - `uv run pytest -q`：`21 passed in 4.33s` となり、すべてのテストが通過した。
- 気づき・疑問：
  - エージェント側のコードや設定を一切変更せず、サーバー側でツールを公開する 1 行を足すだけでエージェントから利用可能になることを体験できた。起動時に `tools/list` でツール定義を動的に取得する MCP の仕組みにより、サーバーとエージェントの責務が分離され、保守性や再利用性が高まるメリットを実感した。
  - 一方で、STEP 2（入力 715 tokens）と比べて、AWS サーバーを含めツールが 8 個になった状態での宿題実行時は入力が 5,942 tokens まで増えており、講義で扱った通りツール定義の増加がコンテキスト消費に直結することも数値で確認できた。