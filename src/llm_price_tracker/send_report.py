from __future__ import annotations

import argparse
import os
import smtplib
import ssl
from datetime import UTC, datetime
from email.message import EmailMessage
from pathlib import Path

from .catalogue import ROOT, load_catalogue


def make_message(sender: str, recipient: str, report: Path) -> EmailMessage:
    catalogue = load_catalogue()
    message = EmailMessage()
    message["Subject"] = f"LLM 价格日报 · {catalogue['snapshot_date']}"
    message["From"] = sender
    message["To"] = recipient
    plain_text = (
        "LLM Token Price Tracker 已完成本次定时校验。\n\n"
        f"生成时间（UTC）：{datetime.now(UTC).replace(microsecond=0).isoformat()}\n"
        f"目录快照日期：{catalogue['snapshot_date']}\n"
        f"覆盖模型数：{len(catalogue['models'])}\n"
        "\n附件为最新的 Markdown 价格目录。请以每行链接的官方定价页为最终计费依据。\n"
        "Coding Agent 的套餐/积分与原生 API Token 单价分开呈现，不能直接等同。\n"
    )
    message.set_content(plain_text)
    message.add_alternative(
        f"""<!doctype html><html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#172033;line-height:1.55">
        <h2 style="margin-bottom:4px">LLM 价格报告已生成</h2>
        <p style="color:#5b6474">快照日期：<strong>{catalogue['snapshot_date']}</strong> · 覆盖 <strong>{len(catalogue['models'])}</strong> 个模型</p>
        <p>附件为带样式的 HTML 价格目录，可直接在浏览器打开。每个模型均附官方来源链接；请以该页面为最终计费依据。</p>
        <p style="padding:12px;background:#fff7ed;border-left:4px solid #f97316">Coding Agent 的套餐、积分与原生 API Token 单价分开呈现，不能直接等同。</p>
        </body></html>""",
        subtype="html",
    )
    message.add_attachment(
        report.read_bytes(),
        maintype="text",
        subtype="html",
        filename=report.name,
    )
    return message


def main() -> int:
    parser = argparse.ArgumentParser(description="Email the generated LLM price report via Gmail SMTP")
    parser.add_argument("--report", type=Path, default=ROOT / "docs" / "PRICEBOOK.html")
    args = parser.parse_args()

    sender = os.environ["SMTP_USERNAME"].strip()
    recipient = os.environ["REPORT_RECIPIENT"].strip()
    # Google displays an App Password in groups for readability. Treat all
    # Unicode whitespace as a separator so pasted groups cannot break SMTP AUTH.
    password = "".join(os.environ["SMTP_PASSWORD"].split())
    server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    if not args.report.is_file():
        raise FileNotFoundError(f"Report not found: {args.report}")

    message = make_message(sender, recipient, args.report)
    with smtplib.SMTP_SSL(server, port, context=ssl.create_default_context(), timeout=30) as smtp:
        smtp.login(sender, password)
        smtp.send_message(message)
    print(f"Report sent to {recipient}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
