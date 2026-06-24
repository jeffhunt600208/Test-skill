# 版面目录(Layout Catalog)

`assets/template.html` 内含以下 9 类版面,每张幻灯片是一个 `1280×720`(16:9)的 `.slide`。
内容通过 `.pad`(`position:absolute;inset:58px 64px`)定位,所以**固定高度不会被内容撑破**——
但也意味着**内容溢出会被裁切**,务必控制每页文字量。

| # | class | 用途 | 关键结构 |
|---|---|---|---|
| 01 | `.slide.cover` | 封面 | 刊眉 `.mast` + 巨号 `h1`(可含 `<mark>`/`<em>`)+ `.midrule` 英文副线 + `.sub`(导语 + meta) |
| 02 | `.slide.thesis` | 满版大命题 | 强调色满铺,一句话 `.q` + 一段 `.lead`。整套最有冲击力的一页 |
| 03 | `.slide.toc` | 目录 | `.grid` 双栏,每条 `.num`+`.tt`+`.desc` |
| 04 | `.slide.ed` | 卷首语 | 左强调色块大引文 `.quote` + 右多栏正文 `.body`(首字下沉) |
| 05 | `.slide.pg`(表格) | 数据表 | `.runhead`+`.head` 页头 + `<table>`,关键值用 `.hl`/`.hl2`,`.tnote` 脚注 |
| 06 | `.slide.pg`(`.split`) | 图文双栏 | 左 `.fig`(深底,可放 `.flow` ASCII 流程图)+ 右 `.points` 编号要点 |
| 07 | `.slide.dark` | 深底数据/公式 | 深底 + `.stats` 三栏大数字(`.big`/`.lbl`),适合放关键指标或公式 |
| 08 | `.slide.pg.three` | 三栏并列对比 | `.cols` 三列,每列顶部色条 `.x/.y/.z`(主色/对照色/金) |
| 09 | `.slide.back` | 封底 | 收束大标题 + `.kw` 关键词标签 + `.foot`(总结 + 出品信息) |

## 复用与扩展

- **页头**:`.pg .head`(`.kicker` 小标 + `h2` 大标 + 可选 `.dek` 引言)+ `.runhead`(刊眉:左栏目右页码)+ `.folio`(角标页码),可拼到任意浅色页。
- **公式**:用 CSS 分数即可,无需 MathJax:
  ```html
  <span class="frac"><span class="n">U</span><span class="d">K + U</span></span>
  ```
  ```css
  .frac{display:inline-flex;flex-direction:column;text-align:center;vertical-align:middle}
  .frac .n{border-bottom:2px solid currentColor;padding:0 .45em}
  .frac .d{padding:0 .45em}
  ```
  上标用 `<sup>`(如 `10<sup>−9</sup>`)。注意大号减号 `−` 在 WeasyPrint 下偏淡。
- **流程图**:`.fig` 里用 `<div class="flow">` + `white-space:pre` 手绘 ASCII 箭头图,
  用 `<span class="a">`/`<span class="b">` 给两条路径上色。轻量、可控、导出无依赖。
- **新版面**:任何新页都套 `.slide` 外壳 + `.pad` 内边距,保持 `1280×720`;深色页加 `.dark` 同款配色处理。

## 节奏建议(让它"像杂志")

- **深浅交替**:封面(深)→ 命题(满色)→ 目录(浅)→ 卷首语(半色)→ 内容(浅)→ 数据(深)…… 明暗节奏是杂志感的核心。
- **大小反差**:每页一个"主角"(巨号标题 / 一个大数字 / 一句引文),其余克制。
- **留白**:`.pad` 已给足边距;宁可少放字、分多页,也不要塞满。
- **统一刊眉刊脚**:`.runhead` + `.folio` 贯穿全篇,形成"同一本刊物"的连贯感。
- **页数**:一个专题 8–14 页为宜。
