# 贡献指南

## 1 贡献范围

欢迎修复项目类型路由、双语同步、图片生产、科学制图、界面证据、页面稳定性、统计展示、隐私检测、链接检查、测试覆盖和 GitHub 渲染问题

单个仓库的品牌偏好只有在能够改进同类项目时才进入通用 Skill，避免把一次性案例固化成所有项目的强制规则

## 2 修改流程

- 第一步，使用合成仓库或临时目录复现问题，不复制真实用户数据、凭据、部署地址和本机路径

- 第二步，修改能够解释真实失败原因的最小规则、模板或审核逻辑

- 第三步，为审核程序增加一个能够复现问题的失败测试，并保留一个不会被误伤的正确测试

  视觉规则变更还需要提供合成资产，说明亮色、暗色、窄屏、图片失败和外部服务失败时的预期表现

- 第四步，运行以下检查：

  ```powershell
  python scripts/test_audit_readme.py # 运行审核程序的正向与反向行为测试
  python scripts/audit_readme.py "." --scan-repository # 扫描当前仓库的双语文件、视觉资源和敏感模式
  ```

- 第五步，检查中文与英文 README 的命令、状态、图片、表格、限制和安全入口是否一致

- 第六步，检查科学图的轴、单位、样本、不确定性和复现入口，确认项目动态仍位于页面末尾

- 第七步，检查提交作者名称、提交邮箱、分支名称和提交信息，确认 Git 元数据没有包含需要保护的身份或内部标识

## 3 Pull Request 要求

Pull Request 需要说明问题证据、修改范围、测试结果和剩余限制

隐私缺陷只能在完成脱敏后加入公开测试，真实秘密必须通过 [`SECURITY.md`](SECURITY.md) 中的私密流程处理

## 4 English contribution guide

Use synthetic repositories or temporary directories to reproduce defects. Do not copy real user data, credentials, deployment endpoints, or local absolute paths into fixtures

Make the smallest reusable change that explains the observed failure, add positive and negative tests, synchronize both README files, and repeat repository-wide privacy scanning before opening a pull request
