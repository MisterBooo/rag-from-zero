"""生成合成保险文档 PDF,作为本项目的测试数据(完全虚构,仅供学习)。

内容刻意与教程文章呼应:你在文章里读到的「核辐射除外条款」「等待期 90 天」
「现金价值公式」「犹豫期 15 天」,都能在这些 PDF 里找到,从而用代码亲手复现
文章描述的每一个现象。

中文渲染:用 reportlab 内置的 STSong-Light CID 字体,跨平台(macOS/Linux 通用),
无需任何外部字体文件;pypdf 也能正确抽取其中的中文。

用法:python scripts/generate_synthetic_data.py
"""

import sys
from pathlib import Path

# 让脚本无论从哪个目录运行,都能 import 到 src.config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from src.config import DATA_DIR

# 注册中文字体(reportlab 自带,无需下载)
_CJK_FONT = "STSong-Light"
pdfmetrics.registerFont(UnicodeCIDFont(_CJK_FONT))


def _styles() -> tuple[ParagraphStyle, ParagraphStyle, ParagraphStyle]:
    """构造支持中文的标题 / 小标题 / 正文样式。"""
    base = getSampleStyleSheet()
    title = ParagraphStyle("CnTitle", parent=base["Title"], fontName=_CJK_FONT, fontSize=18, leading=24)
    heading = ParagraphStyle("CnHeading", parent=base["Heading2"], fontName=_CJK_FONT, fontSize=13, leading=20)
    body = ParagraphStyle("CnBody", parent=base["BodyText"], fontName=_CJK_FONT, fontSize=10.5, leading=18)
    return title, heading, body


def _build(filename: str, doc_title: str, sections: list[tuple[str, str]]) -> None:
    """通用构建:把 (小标题, 正文) 列表渲染成一份 PDF。"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DATA_DIR / filename
    title_style, heading_style, body_style = _styles()

    story: list = [Paragraph(doc_title, title_style), Spacer(1, 16)]
    for heading, text in sections:
        story.append(Paragraph(heading, heading_style))
        story.append(Paragraph(text, body_style))
        story.append(Spacer(1, 10))

    SimpleDocTemplate(str(out_path), pagesize=A4, title=doc_title).build(story)
    size_kb = out_path.stat().st_size / 1024
    print(f"✅ 生成 {filename}（{size_kb:.1f} KB，{len(sections)} 节）")


def generate_insurance_policy() -> None:
    """主保险条款:含文章用到的全部关键案例。"""
    sections = [
        ("第一条 责任范围",
         "本保险承保被保险人在保险期间内因意外伤害导致的身故或残疾。意外伤害指外来的、"
         "突发的、非本意的、非疾病的客观事件。"),
        ("第二条 责任免除",
         "下列情形之一导致被保险人身故或残疾的，本公司不承担给付保险金的责任："
         "（一）战争、军事冲突、暴乱或武装叛乱；（二）核爆炸、核辐射或核污染；"
         "（三）被保险人酒后驾驶、无有效驾驶证驾驶；（四）从事潜水、攀岩、跳伞等高风险运动。"),
        ("第三条 等待期",
         "本产品等待期为 90 天，自本合同生效日起算。被保险人在等待期内因疾病出险的，"
         "本公司不承担给付保险金的责任，但意外伤害不受等待期限制。"),
        ("第四条 犹豫期",
         "本产品犹豫期为 15 天，自您签收本合同的次日 0 时起算。犹豫期内您可无理由解除合同，"
         "本公司全额退还已交保费，不收取任何费用。"),
        ("第五条 现金价值",
         "本合同的现金价值 = 累计已交保费 − 累计风险保费 − 累计管理费用。具体数值以合同附表"
         "「现金价值表」为准。退保时本公司按申请之日的现金价值给付。"),
        ("第六条 保险费交纳",
         "投保人应按合同约定的方式与期限交纳保险费。分期交费的，自首期保险费交纳之日起合同生效。"),
        ("第七条 宽限期",
         "分期交纳保险费的，自约定交费日的次日起 60 天为宽限期。宽限期内发生保险事故的，"
         "本公司仍承担保险责任，但应扣减欠交的保险费。"),
        ("第八条 理赔申请时效",
         "受益人或被保险人应在知道保险事故发生之日起 180 天内向本公司提出理赔申请，"
         "并提供本合同约定的证明与资料。"),
        ("第九条 受益人",
         "被保险人或投保人可指定一人或多人为身故保险金受益人。未指定的，保险金作为被保险人遗产，"
         "由本公司依法向继承人给付。"),
        ("第十条 合同解除",
         "投保人可随时书面申请解除本合同。犹豫期后解除的，本公司自收到解除申请之日起 30 日内"
         "退还本合同的现金价值。"),
    ]
    _build("insurance_policy_v1.pdf", "安心意外伤害保险条款（合成样例·仅供学习）", sections)


def generate_claim_guide() -> None:
    """理赔指南:把流程讲清楚,便于检索「怎么理赔」类问题。"""
    sections = [
        ("一、报案",
         "保险事故发生后，请在 48 小时内通过客服热线 400-000-0000 或官方 APP 报案，"
         "说明被保险人姓名、保单号、事故时间地点与经过。"),
        ("二、准备理赔资料",
         "需准备：理赔申请书、被保险人身份证件、事故证明（如意外事故的医院诊断书、交警责任认定书）、"
         "与保险金给付相关的费用票据原件、受益人银行账户信息。"),
        ("三、提交申请",
         "可通过官方 APP 上传影像件线上提交，或将纸质资料邮寄至理赔受理中心。资料齐全是加快理赔的关键。"),
        ("四、审核与给付",
         "本公司在收到齐全的理赔资料后 10 个工作日内完成审核；情形复杂的不超过 30 日。"
         "审核通过后 3 个工作日内将保险金划付至受益人账户。"),
        ("五、等待期与理赔的关系",
         "若属疾病责任，须确认出险时间已过 90 天等待期；意外伤害不受等待期限制，可直接申请。"),
        ("六、常见拒赔原因",
         "包括：属于责任免除范围（如核辐射、酒后驾驶）、未如实告知健康状况、超过 180 天申请时效、"
         "资料不全且经通知后仍未补齐。"),
    ]
    _build("claim_guide.pdf", "安心意外伤害保险 · 理赔指南（合成样例）", sections)


def generate_product_brochure() -> None:
    """产品手册:营销口吻的概览,与条款形成「同一事实、不同表述」,适合测试检索鲁棒性。"""
    sections = [
        ("产品亮点",
         "安心意外险，专为日常出行与运动场景设计。保额最高 100 万元，"
         "意外医疗 0 免赔、100% 报销社保内费用，一份保障全家可投。"),
        ("适合人群",
         "18 至 65 周岁、身体健康的自然人均可投保。尤其适合通勤族、经常出差人士与运动爱好者。"),
        ("保障期间与续保",
         "保障期间 1 年，到期可申请续保。续保无需重新审核健康状况，但等待期仅首次投保时计算。"),
        ("投保提示",
         "投保前请阅读完整条款，特别留意「责任免除」与「等待期」。犹豫期 15 天内不满意可全额退费，"
         "买得放心。"),
        ("价格示例",
         "30 岁标准体年缴约 366 元，平均每天约 1 元，即可获得最高 100 万元意外保障。"),
    ]
    _build("product_brochure.pdf", "安心意外伤害保险 · 产品手册（合成样例）", sections)


def main() -> None:
    print(f"📂 输出目录：{DATA_DIR}\n")
    generate_insurance_policy()
    generate_claim_guide()
    generate_product_brochure()
    print("\n🎉 合成数据生成完成！下一步：python scripts/ask.py \"等待期是多少天?\"")


if __name__ == "__main__":
    main()
