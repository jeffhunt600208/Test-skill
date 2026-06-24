#!/usr/bin/env python3
"""
export_pdf.py — 把杂志风 HTML 幻灯片导出成 PDF(服务端,无需浏览器)。

用法:
    python3 export_pdf.py input.html output.pdf
    python3 export_pdf.py input.html output.pdf --cjk wqy   # 用更小的文泉驿字体加速

依赖(首次需安装):
    pip install weasyprint
    # 字体(任选其一)
    apt-get install -y --no-install-recommends fonts-noto-cjk fonts-noto-core   # 推荐:衬线+无衬线 CJK
    # 或仅 fonts-wqy-zenhei(更小、渲染更快,但只有无衬线)

为什么不用 Chromium:许多受控环境会拦截 Chromium 的下载域名(cdn.playwright.dev /
storage.googleapis.com 返回 403)。WeasyPrint 从 PyPI 安装即可,无需外部浏览器二进制。

为什么要做这些"打印改写"(关键经验,别删):
  1. .deck{display:flex} 包着多张 page-break 幻灯片 → WeasyPrint 会卡在"在 flex 容器里
     跨页分片",CPU 100% 跑几分钟也出不来。必须在打印时把 .deck 改成 display:block。
  2. .slide::after 的 4px 平铺 radial-gradient 纹理 → 每页要画约 5.7 万个小块,极慢。
     打印时 display:none 关掉(几乎看不见,无损观感)。
  3. Google Fonts 的 <link> 在受控网络里常常加载失败,还会让 WeasyPrint 反复重试拖慢。
     打印时剥离 <link>,改用本地已装字体。
  4. 本地字体名是 "Noto Serif CJK SC" / "Noto Sans CJK SC",和网页里写的
     "Noto Serif SC" / "Noto Sans SC" 不同 → 必须把 --serif/--sans/--display 变量重映射。

注意:大号公式里的 U+2212 减号在 WeasyPrint 下可能偏淡;若公式很重要,改用图片/SVG,
或提示用户用浏览器 Ctrl/⌘+P 导出可得到像素级一致、字体为原版 Playfair 的 PDF。
"""
import re
import sys
import argparse

# 本地字体映射:把网页字体变量指向 apt 安装的本地字体族
FONT_MAPS = {
    # 推荐:Noto 衬线 + 无衬线 CJK(apt: fonts-noto-cjk fonts-noto-core)
    "noto": {
        "serif":   '"Noto Serif","Noto Serif CJK SC",serif',
        "sans":    '"Noto Sans","Noto Sans CJK SC",sans-serif',
        "display": '"Noto Serif","Noto Serif CJK SC",serif',
    },
    # 更小更快,只有无衬线(apt: fonts-wqy-zenhei)
    "wqy": {
        "serif":   '"Noto Serif","WenQuanYi Zen Hei",serif',
        "sans":    '"Noto Sans","WenQuanYi Zen Hei",sans-serif',
        "display": '"Noto Serif","WenQuanYi Zen Hei",serif',
    },
}


def build_print_html(src: str, cjk: str = "noto") -> str:
    """对源 HTML 做打印安全改写,返回新的 HTML 字符串。"""
    fonts = FONT_MAPS[cjk]
    # 1) 剥离 Google Fonts / preconnect 链接,避免受控网络下的失败与重试
    src = re.sub(r"\s*<link[^>]*fonts\.(googleapis|gstatic)\.com[^>]*>", "", src)
    # 2) 注入打印覆盖样式:关纹理、deck 改 block、字体重映射
    override = f"""
  /* —— export_pdf.py 注入的打印覆盖 —— */
  .slide::after{{display:none!important}}                 /* 关掉昂贵的纹理 */
  .deck{{display:block!important;padding:0!important;gap:0!important}}  /* 避免 flex 跨页分片卡死 */
  :root{{
    --serif:{fonts['serif']};
    --sans:{fonts['sans']};
    --display:{fonts['display']};
  }}
"""
    if "</style>" in src:
        src = src.replace("</style>", override + "</style>", 1)
    else:  # 没有 <style> 就补一个
        src = src.replace("</head>", f"<style>{override}</style></head>", 1)
    return src


def main():
    ap = argparse.ArgumentParser(description="Magazine HTML slides → PDF via WeasyPrint")
    ap.add_argument("input", help="输入 HTML 文件")
    ap.add_argument("output", help="输出 PDF 文件")
    ap.add_argument("--cjk", choices=list(FONT_MAPS), default="noto",
                    help="CJK 字体方案:noto(默认,衬线+无衬线)或 wqy(更快,仅无衬线)")
    ap.add_argument("--keep-print-html", metavar="PATH",
                    help="另存改写后的打印 HTML 以便调试")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        src = f.read()
    print_html = build_print_html(src, args.cjk)

    if args.keep_print_html:
        with open(args.keep_print_html, "w", encoding="utf-8") as f:
            f.write(print_html)

    try:
        from weasyprint import HTML
    except ImportError:
        sys.exit("缺少 weasyprint。请先:pip install weasyprint")

    # base_url 用输入文件目录,以便解析相对路径的本地图片/资源
    import os
    base = os.path.dirname(os.path.abspath(args.input)) or "."
    HTML(string=print_html, base_url=base).write_pdf(args.output)
    print(f"✓ 已导出 {args.output}")


if __name__ == "__main__":
    main()
