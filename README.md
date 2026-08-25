<div align="center">

<img src="assets/brand-mark.svg" alt="GitHub README Standardizer 标志，文档、隐私盾牌和验证勾组成安全发布入口" width="132">

<h1>GitHub README Standardizer</h1>

<p><strong>把仓库首页构建成有证据、可执行、可审计的中英双语项目入口</strong></p>

<p>项目维护者 · 文档负责人 · 安全审核者</p>

<p>
  <img src="docs/assets/readme/badges/status.svg" alt="维护状态：持续维护">
  <a href="README.en.md"><img src="docs/assets/readme/badges/bilingual.svg" alt="文档语言：中文优先并提供英文版本"></a>
  <a href="SECURITY.md"><img src="docs/assets/readme/badges/privacy.svg" alt="隐私状态：发布前执行安全门禁"></a>
  <img src="docs/assets/readme/badges/tests.svg" alt="自动测试：11 项通过">
</p>

<p>
  <a href="#1-项目价值">项目价值</a> ·
  <a href="#3-标准化流程">标准化流程</a> ·
  <a href="#4-快速开始">快速开始</a> ·
  <a href="#5-项目路由">项目路由</a> ·
  <a href="#7-隐私门禁">隐私门禁</a> ·
  <a href="#8-验证状态">验证状态</a>
</p>

<p><a href="README.md">简体中文</a> · <a href="README.en.md">English</a></p>

</div>

<div align="center">

<img src="docs/assets/readme/hero.svg" alt="仓库证据依次经过双语写作、隐私门禁、视觉组织和渲染验证，全部硬门禁通过后才能发布" width="100%">

图 1.1　GitHub README Standardizer 的证据驱动发布流程

</div>

本文全部数值来自当前仓库文件、审核程序输出和 2026-08-25 的验证记录，HTML 与 SVG 尺寸值取自各文件的版式属性

## 1 项目价值

GitHub 是托管代码和项目协作记录的平台，README 是访问仓库时首先展示的项目说明

GitHub README Standardizer 是面向 Codex 的仓库首页标准化 Skill

Codex 是能够在授权工作区中读取、修改和验证文件的编码智能体，Skill 是一组可复用执行规则和配套资源

这组规则让不同任务能够采用同一套事实、隐私和质量门禁

这个 Skill 先读取代码、配置、测试、文档和真实视觉资产，再生成中文优先、英文同步的 README，最终使用确定性扫描和 GitHub 渲染结果判断是否可以发布

<div align="center">

表 1.1　使用入口

<table>
  <tr>
    <td width="33%" valign="top"><strong>审核现有 README</strong><br><br>找出事实缺口、失效链接、视觉不足和隐私风险</td>
    <td width="33%" valign="top"><strong>构建双语首页</strong><br><br>按照项目交付物选择结构，并同步命令、状态和限制</td>
    <td width="33%" valign="top"><strong>执行发布验收</strong><br><br>扫描文本与资源，检查 GitHub 实际渲染，再决定是否发布</td>
  </tr>
</table>

</div>

## 2 核心能力

<div align="center">

表 2.1　核心能力与可观察结果

| 能力 | 可观察结果 | 证据位置 |
|---|---|---|
| 项目类型路由 | 应用、接口、命令行、基础设施、人工智能数据和技术内容采用不同首页结构 | [`references/profile-routing.md`](references/profile-routing.md) |
| 双语事实同步 | `README.md` 使用简体中文，`README.en.md` 同步命令、状态、图表和限制 | [`references/content-protocol.md`](references/content-protocol.md) |
| 视觉表达 | 首屏、徽章、图片、表格和 Mermaid 流程图服务于识别、理解或验证 | [`references/visual-system.md`](references/visual-system.md) |
| 隐私门禁 | 真实身份、凭据、内部地址、本机路径和未脱敏图片会阻止发布 | [`references/security-evidence.md`](references/security-evidence.md) |
| 确定性审核 | 审核程序检查双语文件、链接、图片、标题、敏感模式和资源元数据 | [`scripts/audit_readme.py`](scripts/audit_readme.py) |
| 渲染验收 | GitHub 页面需要正确保留图片、表格、链接、详情块和 Mermaid 标记 | [`references/validation.md`](references/validation.md) |

</div>

## 3 标准化流程

以下流程图说明证据怎样进入 README，以及安全门禁为什么能够阻止不可信发布

<div align="center">

```mermaid
%% 流程从仓库事实开始，任何硬错误都会返回修订环节
flowchart TD
    A[读取代码、配置、测试与现有文档] --> B[建立可公开核对的事实清单]
    B --> C[选择一个项目主路由]
    C --> D[编写中文 README]
    D --> E[同步英文 README]
    E --> F[加入本地视觉资产与流程图]
    F --> G[扫描身份、凭据、地址、路径与图片元数据]
    G --> H{全部硬门禁通过}
    H -- 否 --> B
    H -- 是 --> I[检查亮色、暗色、窄屏与 GitHub 渲染]
    I --> J[提交发布结果与剩余证据边界]
```

图 3.1　从仓库证据到可信 README 的执行关系

</div>

## 4 快速开始

前置条件：本机已经配置 Codex Skill 目录，并安装 Python 3.10 或更高版本，Python 版本要求来自审核程序使用的联合类型语法

- 第一步，在已经检出的仓库根目录安装 Skill：

  ```powershell
  $SkillSource = (Get-Location).Path # 从当前仓库根目录读取经过审核的 Skill 文件
  $SkillTarget = Join-Path $env:CODEX_HOME "skills/github-readme-standardizer" # 在已配置的 Codex 目录下建立目标位置
  New-Item -ItemType Directory -Path $SkillTarget -Force | Out-Null # 确保目标目录存在，避免复制因目录缺失而失败
  Copy-Item -Path (Join-Path $SkillSource "*") -Destination $SkillTarget -Recurse -Force # 复制 Skill 指令、参考资料、模板和审核程序
  ```

- 第二步，对目标仓库运行完整审核：

  ```powershell
  python scripts/audit_readme.py "<repository-path>" --scan-repository # 使用仓库路径占位值扫描 README、源码、测试夹具和视觉资源
  ```

- 第三步，读取审核程序返回的 JSON 数据交换格式（JavaScript Object Notation）结果：

  `errors` 中的项目会阻止发布，`warnings` 中的项目需要人工确认，程序不会自动修改目标仓库

预期结果：审核程序返回 `PASS` 或带有明确问题代码的 `FAIL`，输出不会回显已经识别的完整秘密值

## 5 项目路由

Skill 按主要交付物选择一个主路由，混合项目可以增加少量条件模块，避免把多个完整模板机械拼接到同一首页

<div align="center">

表 5.1　项目主路由

| 主路由 | 主要交付物 | 第一视觉证据 | 第一次成功 |
|---|---|---|---|
| 用户应用 | 网页、桌面或移动应用 | 脱敏界面截图 | 完成一个安全用户流程 |
| 开发接口 | 开发库、软件开发工具包或接口组件 | 最小调用与输出 | 完成一次可观察调用 |
| 命令行工具 | 终端工具或本地自动化程序 | 合成终端演示 | 执行一条安全命令 |
| 基础设施服务 | 持续运行的服务或控制平面 | 架构与信任边界 | 启动隔离服务并检查健康状态 |
| 人工智能数据 | 模型、数据集、训练或评测项目 | 任务范围或评测关系 | 使用合成输入完成最小运行 |
| 技术内容 | 书籍、课程、知识库或规范 | 内容地图 | 打开阅读入口或构建预览 |

</div>

## 6 仓库结构

<div align="center">

表 6.1　Skill 文件职责

| 路径 | 内容 | 何时读取或执行 |
|---|---|---|
| `SKILL.md` | 目标、授权边界、主流程和硬门禁 | 每次调用 Skill 时 |
| `agents/openai.yaml` | Codex 界面名称、图标和默认提示 | Skill 被发现或调用时 |
| `assets/` | 双语模板和 Skill 图标 | 新建 README 或展示 Skill 时 |
| `references/` | 路由、内容、视觉、安全、研究和验证细则 | 当前任务命中对应条件时 |
| `scripts/audit_readme.py` | 只读 README 与隐私审核程序 | 交付前 |
| `scripts/test_audit_readme.py` | 审核程序的正向与反向测试 | 修改审核逻辑后 |

</div>

## 7 隐私门禁

仓库发布副本没有保存个人名称、个人邮箱、真实用户标识、密码、访问令牌、应用程序接口密钥、本机绝对路径、私有网络地址或实际部署地址

测试程序需要验证秘密检测能力，因此测试程序会在运行时合成凭据形状和私网地址

完整测试值由多个无敏感含义的片段组成，不会作为源代码字面量进入 Git 版本控制历史

<div align="center">

表 7.1　发布阻断范围

| 检查对象 | 安全替代值 | 失败后果 |
|---|---|---|
| 账号与用户标识 | `synthetic-user` 等明确合成值 | 停止发布并重新生成内容 |
| 密码、令牌和密钥 | 环境变量名或不可用占位值 | 停止发布并轮换可能暴露的凭据 |
| 内部域名与部署地址 | `example.com` 或 `.invalid` 保留域名 | 停止发布并替换全部入口 |
| 本机路径与生产目录 | `<repository-path>` 等语义占位值 | 停止发布并检查关联日志与图片 |
| 截图和图片元数据 | 合成画面或重新生成的本地矢量图 | 停止发布并重新执行像素审核 |

</div>

完整报告流程位于 [`SECURITY.md`](SECURITY.md)，公开问题跟踪不接收秘密值

## 8 验证状态

以下结果来自 2026-08-25 对当前发布副本执行的本地检查，日期表示本次验证时间，后续修改需要重新运行全部门禁

<div align="center">

表 8.1　当前验证范围

| 检查对象 | 验证方法 | 当前结果 | 证据边界 |
|---|---|---|---|
| Skill 结构与元数据 | Skill Creator `quick_validate.py` | 通过 | 检查命名、前置元数据和脚手架占位 |
| 审核程序行为 | `python scripts/test_audit_readme.py` | 11 项测试通过 | 覆盖双语、链接、图片和敏感模式 |
| 仓库内容 | `audit_readme.py --scan-repository` | 通过，0 个错误和 0 个提醒 | 扫描 2 份 README 和 22 个文本文件 |
| 中文可读性 | `Test-HumanReadableChinese.ps1` | 通过，0 个硬错误和 10 个术语提醒 | 检查编号、禁用句式、术语和代码注释 |
| GitHub 渲染 | 远端 README HTML 与资源核对 | 通过 | GitHub HTML 保留全部表格、图片、链接与 Mermaid 标记 |

</div>

## 9 限制

- 自动审核无法判断营销声明是否合理，维护者仍需核对代码、测试和发布记录
- 自动审核无法仅凭文件内容确认截图中所有文字，正式发布仍需视觉检查
- Skill 不会自动获得提交、推送、发布或修改仓库设置的权限，远端写入需要用户明确授权
- 当前私有分发没有附带开源许可证，仓库访问权限不等同于再分发授权

## 10 贡献指南

- 可复现缺陷按照 [`CONTRIBUTING.md`](CONTRIBUTING.md) 提交，并使用合成数据构造最小案例
- 安全问题按照 [`SECURITY.md`](SECURITY.md) 使用私密渠道报告
- 模板研究和采用边界记录在 [`references/research-basis.md`](references/research-basis.md)
- Skill 修改后需要同步中文与英文 README，并重新运行测试、隐私扫描和 GitHub 渲染验收
