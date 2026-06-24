---
name: guizang-ppt-skill
description: Build magazine-style ("杂志风") HTML slide decks with an editorial design system, then export them to PDF. Use when the user wants a 杂志风 / magazine-style PPT, presentation, slide deck, or 演示文稿 (especially in Chinese), or wants to turn long-form text / an article / a paper into stylish slides, or needs to export such an HTML deck to PDF. Provides a token-driven template, a recolorable color system, a catalog of editorial slide layouts, and a WeasyPrint HTML→PDF export script that renders CJK offline.
---

# 杂志风 PPT(Guizang Magazine-Style Deck)

做"杂志风"幻灯片:满版大标题、衬线 × 无衬线反差、刊眉刊脚、明暗节奏、强调色块。
产物是一份**自包含的 HTML**(浏览器全屏播放,16:9),可一键导出 PDF。

## 工作流程

1. **拿到主题/文字。** 若用户只说"做杂志风 PPT"没给内容,先问两件事:① 主题/要放的文字(或先做示例样板)
   ② 是否有主色偏好。格式默认 HTML 网页幻灯片(杂志排版最自由)。

2. **复制模板。** 把 `assets/template.html` 拷到工作目录(如 `slides.html`)。它含 9 类版面与播放/打印脚本。

3. **填内容、排版面。** 把占位文字换成真实内容,按需增删页。版面类型与复用法见
   `references/layouts.md`。提炼原则:**每页一个主角**,深浅页交替,宁可分多页也不要塞满
   (`.slide` 固定 720px 高,**内容溢出会被裁切**)。长文/论文 → 先抽出"核心命题 + 章节 + 关键表/图/数据",
   再映射到版面(命题页、目录、卷首语、表格、双栏图文、深底数据、三栏对比、封底)。

4. **换色(可选)。** 整套配色由 `:root` 6 个 token 驱动。换主色只改这几个变量,**不要逐处改色**。
   现成调色板(经典红/深航蓝/森绿/墨黑金/酒红)与三条铁律见 `references/color-system.md`。
   ⚠️ 换 `--accent` 必须同步换 `--accent-lt`(深色页上的高亮),否则深底高亮会"消失"。

5. **交付 HTML。** 告诉用户:浏览器打开 → `P` 全屏播放,`← →` 翻页,`Esc` 退出,`Ctrl/⌘+P` 导出 PDF。

6. **导出 PDF(若用户要)。** 见下。

## 导出 PDF

**最佳像素级效果**:让用户在浏览器里 `Ctrl/⌘+P → 另存为 PDF`(已设好 16:9 无边距,字体为原版)。

**服务端自动导出**(无浏览器时)——用 `assets/export_pdf.py`,基于 WeasyPrint:

```bash
pip install weasyprint
apt-get install -y --no-install-recommends fonts-noto-cjk fonts-noto-core   # CJK 字体
python3 assets/export_pdf.py slides.html slides.pdf
# 慢/想更快:--cjk wqy(改用更小的文泉驿字体,仅无衬线)
```

脚本会自动做四件**必须**的打印改写(细节见脚本头注释),这些是踩坑总结,别绕过:
- `.deck` 由 `flex` 改 `block`——否则 WeasyPrint 会卡在 flex 容器跨页分片,CPU 100% 几分钟不出结果;
- 关掉 `.slide::after` 的平铺渐变纹理——每页约 5.7 万小块,极慢;
- 剥离 Google Fonts `<link>`——受控网络常加载失败并拖慢;
- 把字体变量重映射到本地 Noto 字体(本地族名 `Noto Serif/Sans CJK SC` ≠ 网页的 `Noto * SC`)。

**别用 Chromium/Playwright 导出**:很多受控环境会拦截其浏览器下载域名(403),WeasyPrint 从 PyPI 装即可,无需外部二进制。

## 验证产物

环境无浏览器时,用 PyMuPDF 把几页转成 PNG 自检(页数、尺寸、配色、字体、上标):

```bash
pip install pymupdf
python3 -c "import fitz; d=fitz.open('slides.pdf'); print(d.page_count, [round(x,1) for x in d[0].rect[2:]]); \
[d[i].get_pixmap(matrix=fitz.Matrix(0.85,0.85)).save(f'check_{i+1}.png') for i in (0,4,8,d.page_count-1)]"
```
页面尺寸应为 `960×540 pt`(= 1280×720 px @96dpi)。

## 已知小瑕疵

大号公式里的减号 `−`(U+2212)在 WeasyPrint 下可能偏淡。若公式很关键,改成图片/SVG,
或提示用户用浏览器 `Ctrl/⌘+P` 导出(可得原版字体、零瑕疵)。

## 文件

- `assets/template.html` — 9 类版面的杂志风模板(token 化配色 + 播放/打印脚本)
- `assets/export_pdf.py` — HTML→PDF 导出(WeasyPrint,含全部打印改写)
- `references/color-system.md` — 6 个配色 token、三条铁律、即取即用调色板
- `references/layouts.md` — 9 类版面结构、公式/流程图写法、节奏建议
