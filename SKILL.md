---
name: github-readme-standardizer
description: Audit, create, or upgrade GitHub repository READMEs with evidence-backed project routing, Chinese-first bilingual files, local visual assets, privacy redaction, and rendered validation. Use for repository landing-page standardization, visual improvement, or bilingual README maintenance
---

# GitHub README 标准化

## 1 目标

把仓库首页说明文件构建成可信的项目入口，让首次访问者能够判断项目价值、完成第一次成功操作、理解风险边界并找到正确协作渠道

保留仓库事实、项目品牌和现有优秀内容，删除无法核对的宣传、失效入口和泄露风险

## 2 授权边界

- README 修改授权只覆盖用户指定仓库或工作副本
- 默认只修改本地文件，不提交、不推送、不创建发布和拉取请求
- 远程提交、推送、发布或修改仓库设置需要用户明确授权
- 不展示真实部署地址、内部域名、用户标识、账号、密码、令牌、私有网络地址和未脱敏截图
- 不虚构版本、测试结果、兼容范围、采用者、赞助商、评价、性能数字或发布日期

## 3 项目路由

- 第一步，读取 [项目类型路由](references/profile-routing.md)，按照主要交付物和首次成功动作选择一个主路由

- 第二步，读取 [内容协议](references/content-protocol.md) 和 [模块目录](references/module-catalog.md)，建立所有项目共享的核心组件，并只启用证据充分的条件模块

- 第三步，任务包含视觉内容时，先读取 [视觉系统](references/visual-system.md)，再按需读取以下专用协议：

  - 生成图片、插画、主视觉或本地视觉资产：[图片生成与视觉生产](references/visual-production.md)
  - 实验、基准、统计或性能图：[科学制图](references/scientific-visualization.md)
  - 产品截图、用户流程、主题和窄屏稳定性：[UI、UX 与页面稳定性](references/ui-ux-evidence.md)
  - 徽章、星标、下载、活动或趋势：[徽章、统计与项目动态](references/metrics-and-badges.md)

- 第四步，公开仓库、部署说明、账户系统、用户数据、模型或外部服务进入范围时，读取 [安全与证据门禁](references/security-evidence.md)；存在任何图片、截图、SVG、视频、徽章或远程视觉时，同时读取 [视觉隐私与脱敏](references/visual-privacy.md)

- 第五步，准备交付时读取 [验证协议](references/validation.md)，运行确定性检查并完成视觉审核

需要核对模板来源和采用边界时，读取 [研究依据](references/research-basis.md)

## 4 执行流程

- 第一步，检查仓库说明、代码、配置、测试、许可证、贡献文件和现有视觉资产，建立可以公开核对的事实清单

- 第二步，检查当前 README 的信息顺序、链接、图片、双语状态和敏感信息，保留有效内容并记录证据缺口

- 第三步，选择一个主路由，建立中文优先的章节结构，再从模块目录中确定需要启用的条件模块

- 第四步，先完成中文 `README.md`，再创建或同步英文 `README.en.md`，两份文件共享命令、版本、图表、状态和限制

- 第五步，优先复用仓库内真实视觉资产。生成图只承担解释或品牌角色，不伪装成运行证据。对截图像素、SVG 源码、图片元数据和外部请求执行脱敏审核

- 第六步，运行 `scripts/audit_readme.py <仓库路径> --strict-warnings`，检查双语结构、链接、秘密、用户目录路径、Mermaid 方向、装饰性编号、SVG 活动内容、外部引用和图片元数据，修复全部硬错误并人工复核提醒

- 第七步，在亮色、暗色和窄屏环境渲染 README，检查图片、表格、代码、流程图、链接和页面级横向溢出

- 第八步，交付修改文件、验证结果、剩余证据缺口和远程状态，不把未执行的检查写成通过

## 5 核心门禁

- `README.md` 默认使用简体中文，`README.en.md` 提供英文镜像，项目惯例或用户指令可以调整主次
- 首屏保留项目标志或名称、一级标题、价值短句、可信状态、稳定入口和第一视觉证据
- 顶部只保留能够改变读者下一步的稳定入口，动态徽章和远程图片需要说明用途、隐私影响和维护责任
- 星标、访问量、下载量、贡献热力和趋势图只放页面末尾，不能代替第一视觉证据、功能证据或质量结论
- Mermaid 的 `flowchart` 和 `graph` 必须明确使用 `TD` 或 `TB`，横向方向和缺失方向返回硬错误
- 标题使用 `1`、`1.1` 等十进制编号，步骤使用自然语言顺序，装饰性圆圈数字和数字 Emoji 返回硬错误
- 代码、命令和配置示例必须有合法注释，并保持可复制执行
- 性能、效率和质量声明需要测试条件、数据来源、复现方法和更新时间
- 科学图需要标明轴、单位、样本量、不确定性、数据来源、处理方法和不能推出的结论
- 界面证据需要覆盖完整用户任务，并通过亮色、暗色、窄屏、图片失败和外部服务失败场景检查
- 自托管、高权限、数据管理和外部写入项目先展示风险门，再提供安全默认路径
- 在线演示只能使用隔离合成数据，公开演示凭据不能进入默认模板
- 上游文档确实需要保留私有地址示例时，只能使用验证协议规定的精确例外文件，并锁定路径、摘要和出现次数
- 多仓库项目需要说明仓库职责、官方维护范围和问题路由
- 根 README 保持入口职责，完整接口、参数和长篇排障内容下沉到 `docs/`
- 任一安全、事实、双语、链接或视觉硬门禁失败时停止交付并继续修复
- 普通 GitHub 发布任务只审核 README，不在未获得 README 修改授权时重写项目内容

## 6 可复用资源

- 中文骨架使用 [中文模板](assets/README.zh.template.md)
- 英文镜像使用 [英文模板](assets/README.en.template.md)
- 图片、科学图、界面、稳定性、脱敏和项目动态的中文片段使用 [中文视觉模块](assets/visual-modules.zh.md)
- 对应英文片段使用 [英文视觉模块](assets/visual-modules.en.md)
- 模板提供信息位置，不授权保留空章节、占位值或示例数据
- 项目缺少某项事实时删除相关模块，并在审核结果中记录证据缺口

## 7 交付要求

交付结果需要包含修改范围、主要结构、视觉证据、验证矩阵、剩余风险和远程仓库状态

用户审核试点前，不把同一改动扩展到其他仓库
