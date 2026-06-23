# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是 **ysyx（一生一芯）** 项目的学习记录仓库。"ysyx" 取自"一生一世芯"，是中国科学院计算技术研究所开设的 RISC-V 处理器设计教学项目。当前处于 **F 阶段（数字电路实验）**，主要使用 **Logisim-evolution** 完成从组合逻辑、时序逻辑到 RISC-V 单周期处理器设计的实验。

仓库根目录包含 `git_ai.docx` 与若干 `.docx` 实验报告（按阶段归档），正文设计文件是 `.circ`（Logisim 电路文件）。

## 目录结构

```
.
├── E/                          # E 阶段（早期实验）
│   ├── E1/
│   └── E3/E3.1.2.png
├── F/                          # F 阶段（数字电路）
│   ├── F3/                     # 组合逻辑 + 时序逻辑
│   │   ├── F3.2.docx, F3.4.docx, F3.5.docx, F3.6.docx, F3.7.docx  # 实验报告
│   │   ├── F3.3/  F3.4/  F3.5/  F3.6/  F3.7/                    # 子阶段电路与笔记
│   ├── F4/F4.docx              # F4 实验报告
│   ├── F5/                     # F5：复杂数字系统设计
│   │   ├── F5.circ             # 主电路
│   │   ├── F5_library.circ     # 库电路（可复用子模块）
│   │   └── f5.docx             # 实验报告
│   └── F6/                     # F6：MiniRV 单周期 RISC-V 处理器
│       ├── minirv.circ         # ★ 核心：MiniRV 处理器（8 条 RV32I 指令）
│       ├── minirv_instructions_analysis.md  # 8 条指令详细数据通路分析
│       ├── F6.docx             # 实验报告
│       └── logisim-bin/        # 测试程序（hex/txt 格式）
│           ├── mem.hex, sum.hex, vga.hex
│           └── mem.txt, sum.txt, vga.txt
├── logisim_release/            # Logisim 启动脚本
│   ├── run_logisim.bat
│   ├── run_commands.py
│   ├── logisim.txt             # 实际执行的 java 命令
│   └── issue.md                # Java 环境踩坑记录
└── README.md                   # 仅一句话说明
```

## 运行 Logisim（Windows）

**重要**：在 Windows 上 Logisim 需要 **Java 21**（不能使用 Java 17），否则会出现"无法新建/保存文件、无法添加库"的问题。详见 `logisim_release/issue.md`。

### 启动方式

`logisim_release/logisim.txt` 内的命令是实际启动命令，示例：

```
java -jar D:\logisim_jar\logisim-evolution-4.1.0-all.jar
```

启动有两种方式：

1. 双击 `logisim_release/run_logisim.bat`（自动 `cd` 到该目录并执行 `python run_commands.py`）。
2. 直接在命令行执行 `logisim.txt` 中的 `java -jar ...` 命令。

`run_commands.py` 会按行读取 `logisim.txt` 并依次执行（`#` 开头为注释）。可传入自定义命令文件作为参数：`python run_commands.py <other.txt>`。

## F6 MiniRV 处理器架构（当前主项目）

完整分析见 `F/F6/minirv_instructions_analysis.md`。要点：

- **架构**：单周期数据通路（每条指令一个时钟周期完成）。
- **指令集**：RV32I 的 8 条子集——`ADDI, JALR, ADD, LUI, LW, LBU, SW, SB`。
- **寄存器堆**：16 个 32 位寄存器（x0-x15，x0 硬连线为 0），双端口读、单端口写。
- **存储**：24 位地址、32 位数据 ROM/RAM，支持字节使能（BE0-BE3）。
- **指令格式**：I-Type / R-Type / U-Type / S-Type 四种。
- **核心文件**：`F/F6/minirv.circ`（电路）+ `F/F6/logisim-bin/`（测试程序 hex 文件）。

### 重点指令的数据通路要点

- **JALR**：`(rs1 + sign_extend(imm)) & ~1` 计算目标地址；返回地址 = PC + 1；控制信号 `is_jalr = (opcode==0x67) && (funct3==000)`。
- **LBU**：根据 `byte_addr[1:0]` 决定移位量（0/8/16/24），右移后 `AND 0xFF` 零扩展。
- **SB**：S-Type 立即数需要把 `imm[11:5]` 与 `imm[4:0]` 重新拼接为 12 位；按偏移量移位后通过字节使能仅写一个字节。
- **SW**：激活全部字节使能 BE0-BE3。

## 实验报告（.docx）说明

`.docx` 文件包含真值表、电路截图、问题分析。每次在 Logisim 中完成一个新电路后，对应的 `.circ` 与 `.docx` 应同步更新。仓库里还遗留一个 Office 锁文件 `F/F6/~$F6.docx`，提交前注意删除。

## 用户偏好（已记忆，见 `~/.claude/.../memory/MEMORY.md`）

- **权限询问与需求确认使用中文**。
- **导出真值表使用 Logisim 标准格式**（与 Logisim 自带真值表组件输出保持一致，便于与 `.circ` 对照验证）。

## Git 工作流

`.claude/settings.local.json` 已放行 `git status / add / commit / push / clone`。近期 commit 风格：中文一句话概括（如"完成F阶段"、"初步完成miniriscv的jalr与addi指令的搭建"）。主分支为 `main`。
