# Logisim 运行问题及解决方法

## 问题描述

Windows 更新后环境发生变化，导致 Logisim 无法正常运行，具体表现为：

- 新建文件无法保存
- 无法添加库文件

## 解决方法

1. 卸载 Logisim 和 Java 17 环境。
2. 安装 Java 21 环境。
3. 下载 `logisim-evolution.jar` 的最新版本。
4. 通过 Java 21 运行 `logisim-evolution.jar`（运行在 Java 环境下的命令，例如：`java -jar D:\logisim_jar\logisim-evolution-4.1.0-all.jar`）。
5. 创建脚本文件自动运行命令。