import os
from datetime import datetime
from notion_client import Client

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
notion = Client(auth=NOTION_TOKEN)

def get_approved_pages():
    """Notionで『承認』にチェックが入っている記事を取得"""
    pages = []
    response = notion.databases.query(
        database_id=NOTION_DATABASE_ID,
        filter={"property": "承認", "checkbox": {"equals": True}}
    )
    return response["results"]

def generate():
    print("📝 承認済み記事を抽出中...")
    pages = get_approved_pages()
    
    if not pages:
        print("承認済みの記事が見つかりませんでした。")
        return

    md_content = f"# 📝 厳選：美容マーケティング戦略レポート ({datetime.now().strftime('%Y/%m/%d')})\n\n"
    
    for page in pages:
        props = page["properties"]
        title = props["タイトル"]["title"][0]["text"]["content"]
        link = props["URL"]["url"]
        insight = props["潜在インサイト"]["rich_text"][0]["text"]["content"] if props["潜在インサイト"]["rich_text"] else ""
        action = props["PRアクション"]["rich_text"][0]["text"]["content"] if props["PRアクション"]["rich_text"] else ""
        
        md_content += f"## {title}\n🔗 [記事原文]({link})\n\n"
        md_content += f"### 💡 インサイト\n{insight}\n\n"
        md_content += f"### 🚀 戦略アクション\n{action}\n\n---\n\n"

    filename = f"Final_Report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✨ レポートを生成しました: {filename}")

if __name__ == "__main__":
    generate()
