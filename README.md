# 毛豆杯 · 重启好奇心 AI 游戏创作营

面向「暂时对课堂提不起劲」的同学的校园 AI 游戏创作邀请赛活动页。一个装得下毛豆、也装得下笨拙第一版的奖杯：不比谁更厉害，只看有没有把那件小事做完、再认真改过第二版。

- **在线公开页**：https://workbuddy.link/p/uAjM08Bx9PrEEVwdgchQPb
- **GitHub Pages**：https://qiangsi.github.io/maodou-cup-ai-game-camp/
- **编辑态（需登录）**：https://www.workbuddy.cn/space/d/uAjM08Bx9PrEEVwdgchQPb

## 目录

| 路径 | 说明 |
| --- | --- |
| `index.html` | 完整活动页，单文件即可运行，交互（细则、报名表、结果公示、赛题切换）均为前端演示 |
| `assets/favicon.svg` | 浏览器标签图标（像素风毛豆杯） |
| `assets/favicon.ico` | 16/32/48/64 多尺寸 ICO |
| `assets/maodou-cup-logo.svg` | 主 logo，32×32 像素网格，可无损缩放 |
| `assets/maodou-cup-logo.png` | 512×512 PNG（最近邻放大，保留硬边） |
| `assets/maodou-cup-logo-preview.png` | 288×288 预览图 |
| `tools/make_logo.py` | 零第三方依赖的图标生成脚本，可重新生成 SVG / PNG / ICO 并把 favicon 与品牌标识写入页面 |

图标为逐格 `rect` 绘制的内联 SVG，页面不引用任何外部图片、字体或脚本，离线打开也能完整显示。

## 本地预览

直接双击 `index.html`。无需构建、无需服务器、无需联网。若要用 GitHub Pages，把仓库 Settings → Pages 的 Source 设为 `main / (root)` 即可。

## 这个活动的设计口径

- **不淘汰、不排名**：没有一二三等奖、没有排行榜，完成并提交过程记录的小组都有证书。
- **评价只看过程**：100 分过程性量规（真实表达 25 / 创意可玩 25 / 迭代证据 25 / 协作反思 15 / AI 透明与安全 10），技术难度与画面精美度不单独加分，结果只给本组一页反馈。
- **去标签化**：页面、报名表、证书、公示都不出现任何身份标签，不筛查、不鉴定、不依据成绩或考勤筛选。
- **未成年人保护**：监护人书面同意 + 学生本人自愿；单次连续上机 ≤ 40 分钟；可随时退出且不受任何评价影响；活动不是心理诊断或干预，也不承诺提升成绩。
- **报名表只是流程演示**：不提交、不保存、不上传任何数据，正式报名以主办方公布渠道为准。

## 发布前需主办方确认（页面底部已高亮）

主办单位与协办单位、面向学段与年级、起止日期与每周活动时段、场地与设备、导师名单与心理教师对接人、报名渠道与联系人、奖项名额与证书落款、监护人知情同意书版本。

设计方案的完整文字版、量规与伦理边界见配套仓库：[school-refusal-children](https://github.com/qiangsi/school-refusal-children)。
