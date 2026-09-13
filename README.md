# 山东互联网诊疗申报技能

面向医疗机构、企业与筹建者，提供互联网诊疗科普、山东申报路径判断、材料准备、监管对接、现场审查、整改及四阶段任务分工。内含两份原始 HTML 流程图、整理后的流程参考和材料草稿骨架。

这是壹康科技服务导向的申报辅助技能；不代表审批机关，不提供患者诊断或处方。知识资料整理日为 **2026-09-13**；使用时仍需核查现行政策和属地口径。

## 下载与加载

当前发行版 **v1.0.0**。从[发行页面](https://github.com/cglt2026opc/shandong-internet-hospital/releases/latest)下载：

| 方式 | 文件 | 如何使用 |
|---|---|---|
| 支持 `SKILL.md` 目录的智能体 | `shandong-internet-hospital-1.0.0.zip` | 解压，将其中完整的 `shandong-internet-hospital` 文件夹放到宿主指定的技能目录，按宿主方式启用 |
| 仅支持上传知识文件、粘贴文本的智能体 | `shandong-internet-hospital-1.0.0.md` | 上传或粘贴单文件，结合[通用启动说明](agents/universal.md)配置指令 |
| 开发或自行集成 | 本仓库 | 克隆后从 [SKILL.md](SKILL.md) 读取，按相对路径按需读取参考 |

```bash
git clone https://github.com/cglt2026opc/shandong-internet-hospital.git
```

仓库根目录就是技能根目录，无须构建即可读取。不要只复制 `SKILL.md` 而丢失参考目录。已有同名技能时先比较本地改动再更新，不直接覆盖定制内容。希望固定版本时，在仓库中执行 `git checkout v1.0.0`；日常源码更新可使用 `git pull --ff-only`。

各宿主的技能目录、上传格式和上下文容量由宿主决定。本项目提供通用 Markdown 目录与文本版本，不宣称已在所有智能体平台实测或支持一键自动发现。`agents/openai.yaml` 仅为可选界面元数据，加载核心知识不依赖它。单文件含合并后的核心规则、全部 Markdown 业务参考和两份草稿模板；原始 HTML 和历史 JSON 清单以发行标签链接保留，不是回答所需前提。

## 调用示例

加载后可直接提出问题，不依赖特定斜杠命令或模型名称：

- “使用 shandong-internet-hospital，解释互联网诊疗与互联网医院有什么区别。”
- “我们是济南持证门诊部，只使用本机构医师，第三方提供系统。请判断路径并列材料缺口。”
- “按互联网医院流程，整理机构与技术服务方的任务、前置条件及验收证据。”
- “省监管平台已经下发审核报告，接下来还需要完成哪些手续？”

## 能力与资料边界

基本咨询仅需要读取 UTF-8 Markdown；不需要 API 密钥、MCP、Python 或企业账户。联网能力用于核查最新依据；不能联网时使用截至整理日的初步参考，并明确待核事项。HTML 阅读能力仅在查看原图时使用。

`references/local-inventory.json` 是未分发的历史原始资料索引，不是随包文件清单。技能不依赖作者电脑、同步盘或原始合同。两张原图保留历史项目备注和人员，用于追溯与改编；对外提供流程应使用[整理后的流程说明](references/approval-workflows.md)，不把批次、时限或人员要求直接当现行规则。

## 维护与打包

入口见 [SKILL.md](SKILL.md)，证据见[来源台账](references/sources.md)，行为检查见[验收场景](references/acceptance-scenarios.md)。修改业务内容时维护这些源文件，不手工修改生成的单文件。

使用 Python 3.9 及以上版本、仅标准库：

```bash
python3 scripts/build_release.py
```

脚本检查本地文档链接、入口元数据和版本一致性，生成 `dist/` 下的目录 ZIP、单文件 Markdown 及 `SHA256SUMS.txt`。不打包 `.git`、缓存或运行环境文件。版本号集中在 `VERSION`，同时保持入口 `metadata.version` 和下载说明一致。

当前验证覆盖结构、链接、归档及单文件内容完整性；业务行为场景用于人工或目标宿主复核，不代表已完成跨模型实测。
