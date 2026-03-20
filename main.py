# -*- coding: utf-8 -*-
import json
import os


def load_tokens(token_path):
    with open(token_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_new_tokens(new_path):
    if not os.path.exists(new_path):
        return []
    with open(new_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def html_escape(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def render_table(tokens):
    headers = [
        "id",
        "name",
        "description",
        "attribute",
        "ATK",
        "DEF",
        "level",
        "typeline",
    ]
    header_titles = ["ID", "名称", "描述", "属性", "ATK", "DEF", "等级", "种类"]
    rows = []
    for tid, t in sorted(tokens.items(), key=lambda x: x[0]):
        row = [
            html_escape(str(t.get("id", tid))),
            html_escape(str(t.get("name", ""))),
            html_escape(str(t.get("description", "")).replace("\n", " ")),
            html_escape(str(t.get("attribute", ""))),
            html_escape("？" if t.get("atk", None) == -1 else str(t.get("atk", ""))),
            html_escape("？" if t.get("def", None) == -1 else str(t.get("def", ""))),
            html_escape(
                "？" if t.get("level", None) == -1 else str(t.get("level", ""))
            ),
            html_escape(str(t.get("typeline", "")).replace("【", "").replace("】", "")),
        ]
        rows.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
    table = [
        '<table class="token-table">',
        "<thead><tr>"
        + "".join(f"<th>{title}</th>" for title in header_titles)
        + "</tr></thead>",
        "<tbody>",
        *rows,
        "</tbody></table>",
    ]
    return "\n".join(table)


def render_new_tokens(new_tokens):
    if not new_tokens:
        return ""
    html = [
        '<section class="new-token-section">',
        "<h2>未收录 Token</h2>",
        f"<p>发现 {len(new_tokens)} 个未收录 Token (未获得正式卡密或其他错误):</p>",
        "<ul>",
    ]
    html += [f"<li>{html_escape(tid)}</li>" for tid in new_tokens]
    html.append("</ul></section>")
    return "\n".join(html)


def render_html(tokens, new_tokens):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>YuGiOh Tokens 列表</title>
	<style>
		body {{ font-family: 'Segoe UI', 'Helvetica Neue', Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; background: #f8f9fa; margin: 0; padding: 0; }}
		.container {{ max-width: 1200px; margin: 40px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); padding: 32px; }}
		h1 {{ text-align: center; margin-bottom: 24px; }}
		.token-table {{ width: 100%; border-collapse: collapse; margin-top: 24px; }}
		.token-table th, .token-table td {{ border: 1px solid #dee2e6; padding: 8px 12px; text-align: center; }}
		.token-table th {{ background: #f1f3f5; }}
		.token-table tr:nth-child(even) {{ background: #f9fafb; }}
		.token-table tr:hover {{ background: #e9ecef; }}
		.new-token-section {{ margin-top: 32px; }}
		.new-token-section ul {{ list-style: disc; padding-left: 24px; }}
		@media (max-width: 800px) {{
			.container {{ padding: 8px; }}
			.token-table th, .token-table td {{ padding: 4px 6px; font-size: 12px; }}
		}}
	</style>
</head>
<body>
	<div class="container">
		<h1>YuGiOh 衍生物 Token 列表</h1>
		<p>共有 <b>{len(tokens)}</b> 张 token</p>
		{render_new_tokens(new_tokens)}
		<section>
			<h2>Token 列表</h2>
			{render_table(tokens)}
		</section>
	</div>
</body>
</html>"""


def main():
    token_path = "token.json"
    new_path = "new.txt"
    docs_dir = "docs"
    out_path = os.path.join(docs_dir, "index.html")
    os.makedirs(docs_dir, exist_ok=True)
    tokens = load_tokens(token_path)
    new_tokens = load_new_tokens(new_path)
    html = render_html(tokens, new_tokens)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"已生成 {out_path}")


if __name__ == "__main__":
    main()
