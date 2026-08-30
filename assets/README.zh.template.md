<div align="center">

<img src="docs/assets/readme/brand-mark.svg" alt="{{项目名称}} 品牌标识" width="112">

<h1>{{项目名称}}</h1>

<p><strong>{{一句话价值}}</strong></p>

<p>{{目标用户}} · {{主要使用场景}}</p>

<p>
  <img src="docs/assets/readme/badges/status.svg" alt="项目状态：{{状态}}">
  <a href="README.en.md"><img src="docs/assets/readme/badges/language.svg" alt="文档语言：中文和英文"></a>
  <a href="SECURITY.md"><img src="docs/assets/readme/badges/security.svg" alt="安全策略：查看安全说明"></a>
  <a href="LICENSE"><img src="docs/assets/readme/badges/license.svg" alt="许可证：{{许可证}}"></a>
</p>

<p>
  <a href="#1-项目价值">项目价值</a> ·
  <a href="#3-快速开始">快速开始</a> ·
  <a href="#4-使用示例">使用示例</a> ·
  <a href="#5-系统架构">系统架构</a> ·
  <a href="#6-验证状态">验证状态</a> ·
  <a href="#10-参与维护">参与维护</a>
</p>

<p><a href="README.md">简体中文</a> · <a href="README.en.md">English</a></p>

</div>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/readme/hero-light.svg">
  <img src="docs/assets/readme/hero-light.svg" alt="{{主视觉展示的项目界面、终端行为或运行关系}}" width="100%">
</picture>

<div align="center">

图 1.1　{{主视觉的事实性图题}}

</div>

## 1. 项目价值

{{项目名称}} 帮助 {{目标用户}} 完成 {{主要任务}}，最终得到 {{可观察结果}}

### 1.1. 选择上手路径

<table>
  <tr>
    <td width="33%" valign="top">
      <h3>先了解项目</h3>
      <p>{{查看主视觉或能力矩阵的方法}}</p>
    </td>
    <td width="33%" valign="top">
      <h3>本地验证</h3>
      <p>{{完成第一次安全运行的方法}}</p>
    </td>
    <td width="33%" valign="top">
      <h3>准备集成</h3>
      <p>{{阅读架构、安全或接口边界的方法}}</p>
    </td>
  </tr>
</table>

## 2. 核心能力

<div align="center">

| 能力 | 读者得到的结果 | 当前状态 |
|---|---|---|
| {{能力一}} | {{可观察结果}} | {{证据支持的状态}} |
| {{能力二}} | {{可观察结果}} | {{证据支持的状态}} |
| {{能力三}} | {{可观察结果}} | {{证据支持的状态}} |

表 2.1 {{项目名称}} 核心能力

</div>

## 3. 快速开始

前置条件：{{运行环境、平台或权限要求}}

```bash
git clone https://github.com/example-org/example-repo.git # 克隆使用占位组织名的示例仓库
cd example-repo # 进入项目目录后再执行仓库命令
npm install # 按锁文件安装当前项目依赖
npm run dev # 启动本地开发环境并观察终端地址
```

预期结果：{{首次成功后能够观察到的界面、文件或终端输出}}

## 4. 使用示例

{{使用真实且脱敏的输入、操作和输出说明核心流程}}

## 5. 系统架构

以下流程图说明 {{主要输入}} 怎样经过 {{核心组件}} 形成 {{最终输出}}

<div align="center">

```mermaid
%% 使用普通中文节点展示核心数据方向和信任边界
flowchart TD
    A[{{主要输入}}] --> B[{{本地处理}}]
    B --> C[{{核心能力}}]
    C --> D[{{人工确认或安全门}}]
    D --> E[{{可观察输出}}]
```

图 5.1 {{项目名称}} 核心运行关系

</div>

### 5.1. 界面证据（条件模块）

仅在仓库具有真实用户界面且能够使用合成数据重新截图时保留

<table>
  <tr>
    <td width="50%"><img src="docs/assets/readme/ui/{{起始界面文件}}" alt="{{起始状态、主要操作和可观察对象}}" width="100%"></td>
    <td width="50%"><img src="docs/assets/readme/ui/{{结果界面文件}}" alt="{{结果状态、反馈和下一步}}" width="100%"></td>
  </tr>
</table>

<div align="center">

图 5.2　{{起始状态事实性图题}}

图 5.3　{{结果状态事实性图题}}

</div>

### 5.2. 科学结果（条件模块）

仅在数据、统计定义和复现入口均可公开时保留

<div align="center">

<img src="docs/assets/readme/plots/{{图形文件}}" alt="{{指标、比较对象和主要结论}}" width="100%">

图 5.4　横轴为 {{名称与单位}}，纵轴为 {{名称与单位}}；样本量 {{数量}}，误差表示 {{定义}}，更新于 {{日期}}

</div>

数据来源：[`{{数据文件}}`]({{数据相对路径}})　复现：`{{复现命令}}`　限制：{{不能由图形推出的结论}}

### 5.3. 视觉稳定性（存在视觉时保留）

<div align="center">

| 场景 | 验证对象 | 当前结果 | 证据边界 |
|---|---|---|---|
| GitHub 亮色 | {{对象}} | {{结果}} | {{范围}} |
| GitHub 暗色 | {{对象}} | {{结果}} | {{范围}} |
| 窄屏 | {{对象}} | {{结果}} | {{范围}} |
| 图片失败 | 替代文本、图题和正文 | {{结果}} | {{范围}} |

表 5.1　{{项目名称}} 视觉稳定性验证范围

</div>

## 6. 验证状态

以下结果来自 {{检查命令、持续集成记录或发布证据}}

<div align="center">

| 检查对象 | 验证方法 | 结果 | 证据边界 |
|---|---|---|---|
| {{对象一}} | `{{命令或记录}}` | {{结果}} | {{覆盖范围}} |
| {{对象二}} | `{{命令或记录}}` | {{结果}} | {{覆盖范围}} |

表 6.1 {{项目名称}} 验证范围

</div>

## 7. 数据安全

- {{项目保存的数据和保存位置}}
- {{外部服务的启用条件和最小权限}}
- {{日志、截图和导出内容的脱敏规则}}
- {{图片像素、SVG 源码、文件元数据和远程视觉请求的检查结果}}
- 安全问题通过 [安全说明](SECURITY.md) 中的私密渠道提交

## 8. 项目状态

项目状态：{{已发布、试验中、维护中或归档}}

支持范围：{{证据能够支持的版本、平台和能力}}

## 9. 限制说明

- {{当前不支持的用途}}
- {{尚未验证的平台或环境}}
- {{需要使用者自行承担的部署或数据责任}}

## 10. 参与维护

- 使用问题：{{讨论区或文档入口}}
- 可复现缺陷：{{问题跟踪入口}}
- 安全问题：[SECURITY.md](SECURITY.md)
- 贡献流程：[CONTRIBUTING.md](CONTRIBUTING.md)
- 使用许可：[LICENSE](LICENSE)

## 11. 项目动态（条件模块，始终位于页面末尾）

项目动态只补充当前维护与社区状态，不能代替功能、性能、质量或安全证据

<div align="center">

| 指标 | 当前状态 | 来源与更新时间 | 失效后备 |
|---|---|---|---|
| 当前发布 | {{状态}} | {{来源与日期}} | 发布记录入口 |
| 构建状态 | {{状态}} | {{来源与日期}} | 验证说明 |
| 社区趋势 | {{状态或删除此行}} | {{提供方、查询范围与日期}} | 仓库原生入口 |

表 11.1　{{项目名称}} 当前维护与社区状态

</div>
