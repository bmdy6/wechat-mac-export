---
name: wechat-mac-export
description: "Use when a user has their own macOS WeChat 4.2.0 database snapshot and an authorized existing key, or wants help exporting, checking, or resuming that offline export."
---

# 离线导出 macOS 微信 4.2.0 私聊

先读仓库的 `README.md`。在仓库目录安装入口，在仓库外创建权限为 `700` 的工作目录。确认用户选择的账号 `db_storage`、已有密钥文件路径、快照及导出位置。密钥只通过本地文件路径传入，聊天内容和联系人映射留在本地。

1. 需要用户补齐输入时运行 `wechat-mac-export handoff --action user --directory <工作目录>`，告诉用户提示文件的位置并等待。官方微信界面实际显示扫码要求且与当前任务相关时，才写 `--action scan` 的提示文件。扫码由本人核对并完成。
2. 有来源后运行 `snapshot --source <db_storage> --output <新快照目录>`。遇到源文件变化时，保留原目录并从一致的副本重新复制。
3. 运行 `verify --snapshot <快照目录> --key-file <已有密钥文件> --handoff-dir <工作目录>`。只有所有库通过首页 HMAC 才能继续。找不到密钥或 HMAC 不匹配就停在此处，请用户检查输入。
4. 运行 `export --snapshot <快照目录> --key-file <已有密钥文件> --output <新导出目录> --handoff-dir <工作目录>`。账号识别失败时让用户提供数据库内的本人账号标识，再加 `--self-id` 重试。
5. 读 `统计.md` 和导出清单的统计字段，核对实际编号目录、JSONL 行数和 Markdown 文件数。检查私有工作目录是否残留本次明文 SQLite 临时目录。汇报导出路径、会话和消息数、未识别会话表数及需要本人处理的事项。

遇到现用微信正在运行、目标已存在、版本不同或用户仅授权比较时，按原任务边界继续处理。复制只读，导出需要新目录。终端、聊天、Git 和其他外部服务只保留用户授权的汇总信息。
