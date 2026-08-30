# 安全报告

## 1. 支持范围

安全审核覆盖当前默认分支中的 Skill 指令、双语模板、参考文档、审核程序、测试夹具和本地视觉资产，包括图片像素、SVG 源码、文件元数据和远程视觉请求

历史版本可能缺少当前门禁，使用者需要先更新到默认分支，再根据当前审核程序复现问题

## 2. 私密报告流程

- 第一步，停止公开传播相关文件、日志、截图和链接

- 第二步，通过仓库已启用的 GitHub 私密漏洞报告入口提交问题

- 第三步，GitHub 私密漏洞报告入口没有启用时，使用仓库维护者已经授权的私密渠道联系维护者

- 第四步，报告只提供复现所需的最小信息，并使用不可用占位值替代完整秘密

- 第五步，维护者确认影响范围后，轮换可能暴露的凭据并清理工作副本、提交历史、发布附件和缓存副本

公开 Issue、Pull Request、讨论区和提交信息均不接收秘密值

## 3. 报告内容

报告应包含受影响文件的仓库相对路径、问题类别、最小复现步骤、预期安全行为和实际结果

截图需要使用合成数据，无法安全重现的截图可以省略，并在报告中说明证据边界

## 4. 发布阻断条件

以下任一情况都会阻止 Skill 或 README 发布：

- 真实姓名、个人邮箱、用户标识或账户信息仍然存在
- 密码、访问令牌、应用程序接口密钥、私钥或连接字符串仍然存在
- 本机绝对路径、内部主机名、私有网络地址或真实部署入口仍然存在
- 图片像素或元数据仍然包含身份、地址、路径、通知或设备信息
- 远程资源的权限、日志、缓存或失效行为无法解释
- SVG 包含脚本、事件处理器、外部引用、数据地址、文档类型或实体声明
- 科学图缺少数据来源、统计定义或复现边界，却被用于支持质量或性能结论

## 5. English reporting guide

Security review covers the skill instructions, bilingual templates, references, auditor, test fixtures, and local visual assets on the current default branch

Stop public distribution first, then use GitHub private vulnerability reporting when it is enabled. If that feature is unavailable, contact the repository maintainer through an existing authorized private channel

Share only the minimum reproduction material and replace complete secrets with unusable placeholders. Public issues, pull requests, discussions, and commit messages must never contain secret values
