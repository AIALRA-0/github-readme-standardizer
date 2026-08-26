# README 中文条件模块

只复制证据充分的模块，替换全部占位值，并与英文模块保持同一编号

## A 主视觉

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/readme/hero-light.svg">
  <img src="docs/assets/readme/hero-light.svg" alt="{{主视觉展示的对象、关系和可得出的结论}}" width="100%">
</picture>

<div align="center">图 A.1　{{事实性图题，不使用无法核对的宣传语}}</div>

## B 科学结果

<div align="center">

![{{指标、比较对象和主要结论}}](docs/assets/readme/plots/{{图形文件}})

图 B.1　{{指标}}，横轴为 {{名称与单位}}，纵轴为 {{名称与单位}}；样本量 {{数量}}，误差表示 {{定义}}，更新于 {{日期}}

</div>

数据来源：[`{{数据文件}}`]({{数据相对路径}})　复现：`{{复现命令}}`　限制：{{不能由这张图推出的结论}}

## C 界面组图

<table>
  <tr>
    <td width="50%"><img src="docs/assets/readme/ui/{{界面一}}" alt="{{起始状态和主要操作}}" width="100%"></td>
    <td width="50%"><img src="docs/assets/readme/ui/{{界面二}}" alt="{{结果状态和可观察反馈}}" width="100%"></td>
  </tr>
  <tr>
    <td align="center">图 C.1　{{起始状态图题}}</td>
    <td align="center">图 C.2　{{结果状态图题}}</td>
  </tr>
</table>

## D 界面稳定性

| 场景 | 验证对象 | 当前结果 | 证据边界 |
|---|---|---|---|
| GitHub 亮色 | {{对象}} | {{结果}} | {{范围}} |
| GitHub 暗色 | {{对象}} | {{结果}} | {{范围}} |
| 窄屏 | {{对象}} | {{结果}} | {{范围}} |
| 图片失败 | 替代文本、图题和正文 | {{结果}} | {{范围}} |

## E 视觉隐私

> [!IMPORTANT]
> 本页视觉使用合成数据；发布前已检查像素、SVG 源码、图片元数据和外部请求。{{仍需说明的证据边界}}

## F 项目动态

项目动态只放在正文末尾，不能代替功能、性能和安全证据

| 指标 | 当前状态 | 来源与更新时间 | 失效后备 |
|---|---|---|---|
| 当前发布 | {{状态}} | {{来源与日期}} | 发布记录入口 |
| 构建状态 | {{状态}} | {{来源与日期}} | 验证说明 |
| 社区趋势 | {{状态或删除此行}} | {{提供方、范围与日期}} | 仓库原生入口 |
