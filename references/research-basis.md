# README 模板研究依据

## 1. 研究结论

### 1.1. 本次核对与采用依据

本轮于 2026-09-09 核对官方说明及项目当前首页，以下是本仓库的设计选择，不代表已经证明某一种模板普遍最好

- [平台首页说明](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) 明确首页回答用途、上手、求助和维护信息，并建议详细内容另行组织，本次据此缩短默认骨架
- 同一官方说明指出平台会根据标题提供目录，仓库内文件建议使用相对链接，本次采用少量任务入口并保留本地资源路径
- [绘图项目首页](https://github.com/excalidraw/excalidraw) 区分在线产品和开发组件的使用入口，本次保留按主要交付物选择首次成功路径的做法
- [开发工具首页](https://github.com/astral-sh/uv) 提供安装和使用入口，本次借鉴按操作组织说明，不照搬该项目的性能主张
- [课程项目首页](https://github.com/rust-lang/book) 同时提供阅读与构建说明，本次将课程的首次成功定义为进入阅读，不强制安装流程
- [开发组件首页](https://github.com/fastapi/fastapi) 提供代码示例和运行说明，本次要求示例同时说明输入与可观察结果

本次没有复制这些项目的图片、标志或原文版式，新的头图直接绘制，素材角色见 [制作说明](../docs/assets/readme/hero-notes.md)

### 1.2. 保留的结构判断

高质量 README 共享项目身份、价值范围、第一证据、首次成功、可信边界和维护入口

项目之间的首次成功动作存在显著差异，因此模板采用主路由和条件模块，不固定统一篇幅

本研究中的独特表示当前样本具有明显辨识度，不表示全球首次出现

## 2. 模式来源

<div align="center">

| 来源 | 采用模式 | 使用边界 |
|---|---|---|
| Excalidraw [1] | 产品能力、在线体验和生态入口 | 在线入口需要稳定维护 |
| Dify [2] | 云端、自托管和企业路径分流 | 徽章和语言入口需要控制密度 |
| OpenHands [3] | 权限风险、沙箱路径和仓库职责 | 高风险路径需要安全默认值 |
| Pydantic [4] | 版本迁移、安装和最小验证 | 版本说明需要随发布同步 |
| FastAPI [5] | 代码、运行结果和交互文档组成渐进证据 | 效率数字需要公开依据 |
| Aider [6] | 大型终端演示证明核心交互 | 演示内容需要合成和脱敏 |
| uv [7] | 主题适配基准图和方法入口 | 性能图需要复现条件 |
| ripgrep [8] | 适用边界、反向选择和可复现比较 | 比较对象需要保持当前状态 |
| Prometheus [9] | 架构、部署渠道和运维扩展 | 根文件保持入口职责 |
| Supabase [10] | 架构组件、客户端矩阵和支持分流 | 社区维护范围需要标记 |
| n8n [11] | 紧凑入口和许可证边界 | 动态数量需要持续更新 |
| Cosmos [12] | 模型矩阵、资源要求和任务范围 | 模型状态需要准确分层 |
| AiEDA [13] | 数据流和人工智能任务关系 | 研究路径需要可复现证据 |
| FinRL [14] | 生命周期提示和后继项目职责 | 旧版本状态不能隐含 |
| Transformers [15] | 模型范围、安装、示例和引用 | 大型生态入口需要分类 |
| Rust Book [16] | 阅读、构建、贡献和翻译路径 | 内容版本需要明确 |
| Immich [17] | 数据备份警告和平台能力矩阵 | 公开演示凭据不进入默认模板 |

表 2.1 README 模式来源

</div>

## 3. 参考资料

[1] Excalidraw, “README,” [GitHub 仓库](https://github.com/excalidraw/excalidraw)

[2] LangGenius, “Dify README,” [GitHub 仓库](https://github.com/langgenius/dify)

[3] OpenHands, “README,” [GitHub 仓库](https://github.com/All-Hands-AI/OpenHands)

[4] Pydantic, “README,” [GitHub 仓库](https://github.com/pydantic/pydantic)

[5] FastAPI, “README,” [GitHub 仓库](https://github.com/fastapi/fastapi)

[6] Aider-AI, “README,” [GitHub 仓库](https://github.com/Aider-AI/aider)

[7] Astral, “uv README,” [GitHub 仓库](https://github.com/astral-sh/uv)

[8] BurntSushi, “ripgrep README,” [GitHub 仓库](https://github.com/BurntSushi/ripgrep)

[9] Prometheus, “README,” [GitHub 仓库](https://github.com/prometheus/prometheus)

[10] Supabase, “README,” [GitHub 仓库](https://github.com/supabase/supabase)

[11] n8n, “README,” [GitHub 仓库](https://github.com/n8n-io/n8n)

[12] NVIDIA, “Cosmos README,” [GitHub 仓库](https://github.com/NVIDIA/cosmos)

[13] OSCC-Project, “AiEDA README,” [GitHub 仓库](https://github.com/OSCC-Project/AiEDA)

[14] AI4Finance Foundation, “FinRL README,” [GitHub 仓库](https://github.com/AI4Finance-Foundation/FinRL)

[15] Hugging Face, “Transformers README,” [GitHub 仓库](https://github.com/huggingface/transformers)

[16] Rust Project, “The Rust Programming Language README,” [GitHub 仓库](https://github.com/rust-lang/book)

[17] Immich, “README,” [GitHub 仓库](https://github.com/immich-app/immich)
