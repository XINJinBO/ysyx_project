# Logisim 数字逻辑电路设计总结

## 目录

1. [4-2 优先编码器](#1-4-2-优先编码器)
2. [16-4 优先编码器](#2-16-4-优先编码器)
3. [前导零/一计数](#3-前导零一计数)
4. [1位 2选1 多路选择器](#4-1位-2选1-多路选择器)
5. [1位 4选1 多路选择器](#5-1位-4选1-多路选择器)
6. [3位 4选1 多路选择器](#6-3位-4选1-多路选择器)
7. [可切换进制的七段数码管](#7-可切换进制的七段数码管)
8. [4位比较器](#8-4位比较器)
9. [半加器](#9-半加器)
10. [全加器](#10-全加器)
11. [4位加法器](#11-4位加法器)
12. [4位减法器](#12-4位减法器)
13. [4位原码加法器](#13-4位原码加法器)
14. [4位反码加法器](#14-4位反码加法器)
15. [SR 锁存器](#15-sr-锁存器)

---

## 1. 4-2 优先编码器

### 逻辑表达式

```text
Y1 = I3 + I2
Y0 = I3 + I1·I2'
```

### 接线

```text
AND Gate: in1=I1, in2=NOT(I2) → temp
OR Gate (Y1): in1=I3, in2=I2 → Y1
OR Gate (Y0): in1=I3, in2=temp → Y0
NOT Gate: in=I2 → I2'
```

### 元件清单

| 元件 | 数量 |
|------|------|
| NOT Gate | 1 |
| AND Gate | 1 |
| OR Gate | 2 |
| DipSwitch (4位) | 1 |
| LED | 2 |

---

## 2. 16-4 优先编码器

### 原理

用4个 4-2 优先编码器 + 有效信号 Vi + 额外逻辑组成。

### 结构

```text
16位输入分为4组，每组4位，各接一个 4-2 编码器：

Encoder_0: I[3:0]   → Y0[1:0], V0
Encoder_1: I[7:4]   → Y1[1:0], V1
Encoder_2: I[11:8]  → Y2[1:0], V2
Encoder_3: I[15:12] → Y3[1:0], V3
```

### 高位输出 O[3:2]

```text
O3 = V3
O2 = V3' · V2 + V3 = V2 + V3  (简化)
```

用优先级链：
```text
O3 = V3
O2 = V2 + V3 (但V3优先)
```

### 低位输出 O[1:0]

```text
O1 = Y3[1]·V3 + Y2[1]·V3'·V2 + Y1[1]·V3'·V2'·V1 + Y0[1]·V3'·V2'·V1'·V0
O0 = Y3[0]·V3 + Y2[0]·V3'·V2 + Y1[0]·V3'·V2'·V1 + Y0[0]·V3'·V2'·V1'·V0
```

### 元件清单

| 元件 | 数量 |
|------|------|
| 4-2 Priority Encoder | 4 |
| AND Gate | 多个 |
| OR Gate | 多个 |
| NOT Gate | 若干 |
| DipSwitch (16位) | 1 |
| 7-Segment Display | 1 |

---

## 3. 前导零/一计数

### 前导零 (CLZ)

对输入取反后送入优先编码器：
```text
NOT Gate × N: 对每一位取反
Priority Encoder: 输入取反后的数据
输出 = 前导零的数量
```

### 前导一 (CLO)

直接送入优先编码器：
```text
Priority Encoder: 输入原始数据
输出 = 前导一的数量
```

### 尾部零/一

将输入位序反转后，分别用 CLZ/CLO 方法。

---

## 4. 1位 2选1 多路选择器

### 逻辑表达式

```text
Y = S'·A + S·B
```

### 接线

```text
NOT Gate: in=S → S'
AND Gate 1: in1=S', in2=A → temp1
AND Gate 2: in1=S,  in2=B → temp2
OR Gate: in1=temp1, in2=temp2 → Y
```

### 元件清单

| 元件 | 数量 |
|------|------|
| NOT Gate | 1 |
| AND Gate | 2 |
| OR Gate | 1 |

---

## 5. 1位 4选1 多路选择器

### 结构

用3个 2选1 MUX 组成树形结构：

```text
        A ──┐
            MUX1 ──┐
        B ──┘      │
                   MUX3 ── Y
        C ──┐      │
            MUX2 ──┘
        D ──┘

MUX1: sel=S0, in0=A, in1=B
MUX2: sel=S0, in0=C, in1=D
MUX3: sel=S1, in0=MUX1.out, in1=MUX2.out
```

### 元件清单

| 元件 | 数量 |
|------|------|
| 2-to-1 MUX | 3 |

---

## 6. 3位 4选1 多路选择器

### 原理

3个独立的 1位 4选1 MUX 并行工作，共享选择信号 S[1:0]。

```text
MUX_bit0: sel=S[1:0], in0=X[0], in1=Y[0], in2=Z[0], in3=W[0] → out[0]
MUX_bit1: sel=S[1:0], in0=X[1], in1=Y[1], in2=Z[1], in3=W[1] → out[1]
MUX_bit2: sel=S[1:0], in0=X[2], in1=Y[2], in2=Z[2], in3=W[2] → out[2]
```

每个 MUX_bit 由3个 2选1 MUX 树形组成。

### 元件清单

| 元件 | 数量 |
|------|------|
| 2-to-1 MUX | 9 |

---

## 7. 可切换进制的七段数码管

### 原理

4位输入 D[3:0]，模式选择 S（0=十进制，1=十六进制）。

当 D[3]=1 且 S=0（十进制模式，输入>9）时，数码管不显示。

### 技巧

```text
实际传给译码器的最高位 = D[3] AND S

当 S=0（十进制）: 最高位被强制为0，只显示0-9
当 S=1（十六进制）: 最高位保持原值，显示0-F
```

### 接线

```text
AND Gate: in1=D[3], in2=S → 译码器输入 bit3
D[2:0] 直接连接译码器输入 bit[2:0]
7-Segment Display ← 译码器输出
```

### 元件清单

| 元件 | 数量 |
|------|------|
| AND Gate | 1 |
| Decoder_4to16 (子电路) | 1 |
| 7-Segment Display | 1 |
| DipSwitch (4位) | 1 |
| DipSwitch (1位) | 1 (模式 S) |

---

## 8. 4位比较器

### 用 XNOR 门实现相等检测

```text
XNOR Gate 0: A[0] XNOR B[0] → eq0
XNOR Gate 1: A[1] XNOR B[1] → eq1
XNOR Gate 2: A[2] XNOR B[2] → eq2
XNOR Gate 3: A[3] XNOR B[3] → eq3

AND Gate (4输入): eq0 AND eq1 AND eq2 AND eq3 → A_eq_B
```

### 大于/小于检测

```text
大于 (A > B) 逐位比较：
  gt3 = A[3] AND NOT(B[3])
  gt2 = eq3 AND A[2] AND NOT(B[2])
  gt1 = eq3 AND eq2 AND A[1] AND NOT(B[1])
  gt0 = eq3 AND eq2 AND eq1 AND A[0] AND NOT(B[0])
  A_gt_B = gt3 OR gt2 OR gt1 OR gt0

小于：
  A_lt_B = NOT(A_eq_B OR A_gt_B)
```

### 元件清单

| 元件 | 数量 |
|------|------|
| XNOR Gate | 4 |
| AND Gate | 多个 |
| OR Gate | 多个 |
| NOT Gate | 4 |
| LED | 3 (eq, gt, lt) |

---

## 9. 半加器

### 逻辑表达式

```text
Sum  = A XOR B
Cout = A AND B
```

### 接线

```text
XOR Gate: in1=A, in2=B → Sum
AND Gate: in1=A, in2=B → Cout
```

### 元件清单

| 元件 | 数量 |
|------|------|
| XOR Gate | 1 |
| AND Gate | 1 |

---

## 10. 全加器

### 用2个半加器 + 1个OR门

```text
Half Adder 1: A + B       → temp_sum, temp_cout1
Half Adder 2: temp_sum + Cin → Sum, temp_cout2
OR Gate: temp_cout1 + temp_cout2 → Cout
```

### 接线

```text
XOR Gate 1: in1=A, in2=B → temp_sum
AND Gate 1: in1=A, in2=B → temp_cout1

XOR Gate 2: in1=temp_sum, in2=Cin → Sum
AND Gate 2: in1=temp_sum, in2=Cin → temp_cout2

OR Gate: in1=temp_cout1, in2=temp_cout2 → Cout
```

### 元件清单

| 元件 | 数量 |
|------|------|
| XOR Gate | 2 |
| AND Gate | 2 |
| OR Gate | 1 |

---

## 11. 4位加法器 (Ripple Carry Adder)

### 结构

4个全加器级联：

```text
FA0: A[0] + B[0], Cin=0   → Sum[0], Cout→C1
FA1: A[1] + B[1], Cin=C1  → Sum[1], Cout→C2
FA2: A[2] + B[2], Cin=C2  → Sum[2], Cout→C3
FA3: A[3] + B[3], Cin=C3  → Sum[3], Cout (进位输出)
```

### 输出显示

```text
A数码管:  D[0]=A[0], D[1]=A[1], D[2]=A[2], D[3]=A[3]
B数码管:  D[0]=B[0], D[1]=B[1], D[2]=B[2], D[3]=B[3]
结果数码管: D[0]=Sum[0], D[1]=Sum[1], D[2]=Sum[2], D[3]=Sum[3]
进位LED ← FA3.Cout
```

### 元件清单

| 元件 | 数量 |
|------|------|
| Full Adder 子电路 | 4 |
| DipSwitch (4位) | 2 |
| 7-Segment Display | 3 |
| LED | 1 |

---

## 12. 4位减法器

### 原理

A - B = A + NOT(B) + 1

### 接线

```text
NOT Gate ×4: NOT(B[0])→Bn0, NOT(B[1])→Bn1, NOT(B[2])→Bn2, NOT(B[3])→Bn3

FA0: A[0] + Bn0, Cin=1(接VCC) → Sub[0], Cout→C1
FA1: A[1] + Bn1, Cin=C1       → Sub[1], Cout→C2
FA2: A[2] + Bn2, Cin=C2       → Sub[2], Cout→C3
FA3: A[3] + Bn3, Cin=C3       → Sub[3], Cout (借位)

Cin=1 接电源 (VCC / 高电平)
```

### 输出显示

```text
结果数码管: D[0]=Sub[0], D[1]=Sub[1], D[2]=Sub[2], D[3]=Sub[3]
借位LED ← FA3.Cout (Cout=1表示无借位，Cout=0表示有借位，可加NOT门取反)
```

### 元件清单

| 元件 | 数量 |
|------|------|
| Full Adder 子电路 | 4 |
| NOT Gate | 4 |
| DipSwitch (4位) | 2 |
| 7-Segment Display | 3 |
| LED | 1 |

---

## 13. 4位原码加法器

### 原码格式

4位：bit[3]=符号位(0正1负)，bit[2:0]=幅度(0~7)

### 加法规则

```text
同号: 结果幅度 = |A| + |B|, 符号 = A的符号
异号: 结果幅度 = ||A| - |B||, 符号 = 取幅度大的数的符号
```

### 子模块

#### 13.1 比较器 |A| ≥ |B|

```text
减法器 A-B: borrow输出 = A_ge_B (有借位=0表示|A|<|B|)
```

#### 13.2 3位加法器 (|A|+|B|)

```text
3个全加器级联: A[2:0] + B[2:0], Cin=0 → add_sum[2:0]
```

#### 13.3 3位减法器 (|A|-|B|)

```text
NOT ×3 取反 B
3个全加器: A[2:0] + NOT(B[2:0]), Cin=1 → sub_ab[2:0]
```

#### 13.4 3位减法器 (|B|-|A|)

```text
NOT ×3 取反 A
3个全加器: B[2:0] + NOT(A[2:0]), Cin=1 → sub_ba[2:0]
```

#### 13.5 MUX 选择结果幅度

```text
MUX_d[i]: sel=A_ge_B, in0=sub_ba[i], in1=sub_ab[i] → diff_mag[i]
MUX_r[i]: sel=diff_sign, in0=add_sum[i], in1=diff_mag[i] → result_mag[i]
```

#### 13.6 MUX 选择结果符号

```text
MUX_s1: sel=A_ge_B, in0=B[3], in1=A[3] → sign_mid
MUX_s2: sel=diff_sign, in0=A[3], in1=sign_mid → result_sign
```

### 元件清单

| 元件 | 数量 |
|------|------|
| Full Adder | 9 (加法器3 + 减法器×2共6) |
| NOT Gate | 6 |
| XOR Gate | 1 (符号比较) |
| 2-to-1 MUX | 8 (幅度6 + 符号2) |
| DipSwitch (4位) | 2 |
| 7-Segment Display | 4 (A, B, 结果, 符号) |

---

## 14. 4位反码加法器

### 原理

先将反码转换为原码，用原码加法器计算，再将结果转回反码。

### 14.1 反码 → 原码转换器

```text
sm_sign = input[3]
sm_mag[i] = input[i] XOR input[3]  (i=0,1,2)
```

需要 3 个 XOR 门（每位 XOR 符号位）

### 14.2 原码加法器

复用上述第13节的原码加法器设计。

### 14.3 原码 → 反码转换器

```text
result[3] = sm_result_sign
result[i] = sm_result_mag[i] XOR sm_result_sign  (i=0,1,2)
```

需要 3 个 XOR 门

### 完整信号流

```text
反码A → [XOR] → 原码A → ┐
                         ├→ 原码加法器 → 原码结果 → [XOR] → 反码结果
反码B → [XOR] → 原码B → ┘
```

### 元件清单

| 元件 | 数量 |
|------|------|
| XOR Gate | 7 (转换器6 + 符号比较1) |
| Full Adder | 9 |
| NOT Gate | 6 |
| 2-to-1 MUX | 8 |
| DipSwitch (4位) | 2 |
| 7-Segment Display | 4 |

---

## 15. SR 锁存器

### 电路结构

两个 NOR 门交叉耦合：

```text
NOR1: in1=S, in2=Q' → out=Q
NOR2: in1=R, in2=Q  → out=Q'
```

### 真值表

| S | R | Q |
|---|---|---|
| 0 | 0 | 保持 |
| 0 | 1 | 0 (复位) |
| 1 | 0 | 1 (置位) |
| 1 | 1 | 禁止 |

### 接线

```text
NOR Gate 1: in1=S, in2=NOR2.out → out=Q
NOR Gate 2: in1=R, in2=NOR1.out → out=Q'

交叉耦合:
  NOR1.out → NOR2.in2
  NOR2.out → NOR1.in2

LED Q  ← NOR1.out
LED Q' ← NOR2.out
```

### 亚稳态触发器

在 S、R 前各加 AND 门，共用 Enable 开关 E：

```text
AND_S: in1=S, in2=E → NOR1.in1
AND_R: in1=R, in2=E → NOR2.in1
```

操作：设 S=1, R=1, E=1（禁止状态），再将 E 切为 0 → 触发亚稳态

### 元件清单

| 元件 | 数量 |
|------|------|
| NOR Gate | 2 |
| AND Gate | 2 (亚稳态触发) |
| DipSwitch (1位) | 3 (S, R, E) |
| LED | 2 (Q, Q') |

---

## 附录：常用子电路

### Half Adder (半加器)
- 输入: A, B
- 输出: Sum (=A⊕B), Cout (=A·B)

### Full Adder (全加器)
- 输入: A, B, Cin
- 输出: Sum, Cout
- 内部: 2× Half Adder + 1× OR Gate

### 2-to-1 MUX
- 输入: A, B, S
- 输出: Y (=S'·A + S·B)
- 内部: 1× NOT + 2× AND + 1× OR

### Decoder_4to16
- 输入: D[3:0]
- 输出: O[15:0] (独热码)

### Encoder_16to4
- 输入: I[15:0]
- 输出: O[3:0]

---

# F3.7 时序逻辑电路设计总结

## 目录

16. [SR 锁存器 (NAND版本)](#16-sr-锁存器-nand版本)
17. [D 锁存器](#17-d-锁存器)
18. [带复位的 D 锁存器](#18-带复位的-d-锁存器)
19. [D 触发器](#19-d-触发器)
20. [带复位的 D 触发器](#20-带复位的-d-触发器)
21. [下降沿触发的 D 触发器](#21-下降沿触发的-d-触发器)
22. [带使能端的 D 触发器](#22-带使能端的-d-触发器)
23. [4位寄存器](#23-4位寄存器)
24. [4位计数器](#24-4位计数器)
25. [数列求和电路](#25-数列求和电路)
26. [6-bit 2:1 MUX](#26-6-bit-21-mux)
27. [电子时钟 (MM:SS)](#27-电子时钟-mmss)

---

## 16. SR 锁存器 (NAND版本)

### 电路结构

两个 NAND 门交叉耦合（与 NOR 版本输入取反）：

```text
NAND1: in1=S', in2=Q' → out=Q
NAND2: in1=R', in2=Q  → out=Q'
```

### 真值表

| S' | R' | Q |
|----|----|---|
| 1 | 1 | 保持 |
| 1 | 0 | 0 (复位) |
| 0 | 1 | 1 (置位) |
| 0 | 0 | 禁止 |

### 接线

```text
NAND Gate 1: in1=S', in2=NAND2.out → out=Q
NAND Gate 2: in1=R', in2=NAND1.out → out=Q'

交叉耦合:
  NAND1.out → NAND2.in2
  NAND2.out → NAND1.in2
```

### 元件清单

| 元件 | 数量 |
|------|------|
| NAND Gate | 2 |
| DipSwitch (1位) | 2 (S', R') |
| LED | 2 (Q, Q') |

---

## 17. D 锁存器

### 原理

D锁存器在WE=1时透明（输出跟随D），WE=0时保持。

### 电路结构

```text
NOT Gate: WE → WE'
AND Gate 1: D, WE → S
AND Gate 2: D', WE' → R
SR Latch: S, R → Q, Q'
```

### 真值表

| WE | D | Q |
|----|---|---|
| 0 | X | 保持 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

### 接线

```text
NOT Gate: in=WE → WE'
AND Gate 1: in1=D, in2=WE → S → SR_Latch.S
AND Gate 2: in1=NOT(D), in2=WE' → R → SR_Latch.R
SR_Latch: S, R → Q, Q'
```

### 元件清单

| 元件 | 数量 |
|------|------|
| NOT Gate | 2 |
| AND Gate | 2 |
| SR Latch (子电路) | 1 |
| DipSwitch (2位) | 1 (D, WE) |
| LED | 2 (Q, Q') |

---

## 18. 带复位的 D 锁存器

### 原理

在D锁存器基础上添加RESET信号，RESET=1时强制Q=0。

### 电路结构

```text
AND Gate: D, NOT(RESET) → D_clean
OR Gate S: D_clean, WE → S_eff (控制置位)
AND Gate R: NOT(D_clean), WE → R_raw
OR Gate R: R_raw, RESET → R_eff (控制复位)
SR Latch: S_eff, R_eff → Q, Q'
```

### 接线

```text
NOT Gate 1: in=RESET → RESET'
NOT Gate 2: in=D → D'
AND Gate 1: in1=D, in2=RESET' → D_clean
AND Gate 2: in1=D_clean, in2=WE → S
AND Gate 3: in1=D', in2=RESET' → D_clean'
AND Gate 4: in1=D_clean', in2=WE → R_raw
OR Gate 1: in1=R_raw, in2=RESET → R
SR Latch: S, R → Q, Q'
```

### 元件清单

| 元件 | 数量 |
|------|------|
| NOT Gate | 2 |
| AND Gate | 4 |
| OR Gate | 1 |
| SR Latch (子电路) | 1 |
| DipSwitch (3位) | 1 (D, WE, RESET) |
| LED | 2 (Q, Q') |

---

## 19. D 触发器

### 原理

主从D触发器：两个D锁存器，时钟互补，实现边沿触发。

### 电路结构

```text
Master Latch: D, CLK → Q_master (CLK=1时透明)
Slave Latch: Q_master, CLK' → Q (CLK=0时透明)
NOT Gate: CLK → CLK'
```

### 工作过程

1. CLK=1: Master透明，Slave保持
2. CLK↓: Master保持，Slave采样Master的值
3. CLK=0: Master保持，Slave保持

### 接线

```text
NOT Gate: in=CLK → CLK'
D_Latch_RST (Master): D, CLK, RESET → Q_master
D_Latch_RST (Slave): Q_master, CLK', RESET → Q
```

### 元件清单

| 元件 | 数量 |
|------|------|
| NOT Gate | 1 |
| D_Latch_RST (子电路) | 2 |
| DipSwitch (2位) | 1 (D, CLK) |
| LED | 2 (Q, Q') |

---

## 20. 带复位的 D 触发器

### 原理

在D触发器基础上添加同步/异步复位功能。

### 电路结构

与D触发器相同，但RESET信号连接到两个锁存器。

### 接线

```text
NOT Gate: in=CLK → CLK'
D_Latch_RST (Master): D, CLK, RESET → Q_master
D_Latch_RST (Slave): Q_master, CLK', RESET → Q
```

### 元件清单

| 元件 | 数量 |
|------|------|
| NOT Gate | 1 |
| D_Latch_RST (子电路) | 2 |
| DipSwitch (3位) | 1 (D, CLK, RESET) |
| LED | 2 (Q, Q') |

---

## 21. 下降沿触发的 D 触发器

### 原理

与上升沿触发的D触发器结构相同，但CLK信号连接方式相反。

### 接线

```text
NOT Gate: in=CLK → CLK'
D_Latch_RST (Master): D, CLK', RESET → Q_master
D_Latch_RST (Slave): Q_master, CLK, RESET → Q
```

### 与上升沿触发的区别

- 上升沿：Master在CLK=1时透明
- 下降沿：Master在CLK'=1时透明（即CLK=0时）

### 元件清单

| 元件 | 数量 |
|------|------|
| NOT Gate | 1 |
| D_Latch_RST (子电路) | 2 |
| DipSwitch (3位) | 1 (D, CLK, RESET) |
| LED | 2 (Q, Q') |

---

## 22. 带使能端的 D 触发器

### 原理

EN=1时，触发器正常工作；EN=0时，触发器保持当前值。

### 电路结构

用MUX选择：EN=1时输入D，EN=0时反馈Q。

```text
MUX: sel=EN, in0=Q, in1=D → D_eff
D_Flip_Flop_RST: D_eff, CLK, RESET → Q
```

### 接线

```text
MUX (2-to-1):
  sel=EN
  in0=Q (反馈)
  in1=D (新数据)
  out → D_Flip_Flop_RST.D

D_Flip_Flop_RST: D_eff, CLK, RESET → Q
```

### 元件清单

| 元件 | 数量 |
|------|------|
| 2-to-1 MUX | 1 |
| D_Flip_Flop_RST (子电路) | 1 |
| DipSwitch (4位) | 1 (D, CLK, RESET, EN) |
| LED | 2 (Q, Q') |

---

## 23. 4位寄存器

### 原理

4个D触发器并行，共享CLK和RESET信号。

### 电路结构

```text
DFF0: D[0], CLK, RESET → Q[0]
DFF1: D[1], CLK, RESET → Q[1]
DFF2: D[2], CLK, RESET → Q[2]
DFF3: D[3], CLK, RESET → Q[3]
```

### 接线

```text
D_Flip_Flop_RST ×4:
  所有CLK连接在一起
  所有RESET连接在一起
  每个D输入连接对应的D[i]
  每个Q输出连接对应的Q[i]
```

### 元件清单

| 元件 | 数量 |
|------|------|
| D_Flip_Flop_RST (子电路) | 4 |
| DipSwitch (4位) | 1 (D[3:0]) |
| DipSwitch (1位) | 1 (CLK) |
| Button | 1 (RESET) |
| LED | 4 (Q[3:0]) |

---

## 24. 4位计数器

### 原理

寄存器 + 加法器 + 反馈，实现自动计数。

### 电路结构

```text
Register: D[3:0], CLK, RESET → Q[3:0]
Adder: Q[3:0] + 1 → Sum[3:0]
反馈: Sum[3:0] → Register.D[3:0]
```

### 接线

```text
D_Register_4bit:
  D[3:0] ← Adder.Sum[3:0]
  CLK ← 时钟信号
  RESET ← 复位信号
  Q[3:0] → 输出 + Adder.A[3:0]

Full_Adder_4bit:
  A[3:0] ← Register.Q[3:0]
  B[3:0] ← Constant(1)
  Cin ← Ground(0)
  Sum[3:0] → Register.D[3:0]
```

### 元件清单

| 元件 | 数量 |
|------|------|
| D_Register_4bit (子电路) | 1 |
| Full_Adder_4bit (子电路) | 1 |
| Constant (4位) | 1 (值=1) |
| Clock | 1 |
| Button | 1 (RESET) |
| 7-Segment Display | 1 |

---

## 25. 数列求和电路

### 原理

计算 1+2+...+10=55，需要两个寄存器分别存储累加和与计数器。

### 电路结构

```text
Sum Register: 存储累加和
Counter Register: 存储当前计数
Adder1: Sum + Counter → New_Sum
Adder2: Counter + 1 → New_Counter
```

### 接线

```text
Sum_Register (8-bit):
  D ← Adder1.Sum
  CLK ← 时钟
  RESET ← 复位
  Q → 输出 + Adder1.A

Counter_Register (8-bit):
  D ← Adder2.Sum
  CLK ← 时钟
  RESET ← 复位
  Q → Adder1.B + Adder2.A

Adder1 (8-bit): Sum.Q + Counter.Q → New_Sum
Adder2 (8-bit): Counter.Q + 1 → New_Counter
```

### 终止条件

当 Counter = 10 时停止计数（需要比较器和控制逻辑）。

### 元件清单

| 元件 | 数量 |
|------|------|
| D_Register_8bit (子电路) | 2 |
| Full_Adder_8bit (子电路) | 2 |
| Constant (8位) | 1 (值=1) |
| Clock | 1 |
| Button | 1 (RESET) |
| 7-Segment Display | 2 (Sum, Counter) |

---

## 26. 6-bit 2:1 MUX

### 逻辑表达式

```text
out = (NOT(sel) AND in0) OR (sel AND in1)
```

### 1-bit MUX 接线

```text
NOT Gate: sel → sel_n
AND Gate 1: sel_n, in0 → temp0
AND Gate 2: sel, in1 → temp1
OR Gate: temp0, temp1 → out
```

### 6-bit MUX 结构

6个1-bit MUX并行，共享sel信号：

```text
MUX_bit0: sel, in0[0], in1[0] → out[0]
MUX_bit1: sel, in0[1], in1[1] → out[1]
...
MUX_bit5: sel, in0[5], in1[5] → out[5]
```

### 元件清单 (1-bit MUX)

| 元件 | 数量 |
|------|------|
| NOT Gate | 1 |
| AND Gate | 2 |
| OR Gate | 1 |

### 元件清单 (6-bit MUX)

| 元件 | 数量 |
|------|------|
| NOT Gate | 6 |
| AND Gate | 12 |
| OR Gate | 6 |

---

## 27. 电子时钟 (MM:SS)

### 原理

使用两个6-bit计数器（秒和分），每60进位一次。

### 整体架构

```text
Clock (1Hz) → 秒计数器 → 秒显示
                  ↓ Carry
              分计数器 → 分显示
```

### 秒计数器

```text
6-bit Register: 存储当前秒数
6-bit Adder: 计算 current + 1
MUX: 选择正常计数或复位到0
Carry检测: 当秒数=60时输出Carry信号
```

### Carry检测逻辑

```text
60 = 111100 (二进制)
Carry = B[5] AND B[4] AND B[3] AND NOT(B[2]) AND NOT(B[1]) AND NOT(B[0])
```

### 分计数器

与秒计数器结构相同，但时钟信号来自秒的Carry输出。

### 显示逻辑

将6位二进制数(0-59)转换为十进制十位和个位：
- 十位 = value / 10
- 个位 = value % 10

### 元件清单

| 元件 | 数量 |
|------|------|
| Clock | 1 |
| 6-bit Register | 2 (秒+分) |
| 6-bit Adder | 2 (秒+分) |
| 6-bit 2:1 MUX | 2 (秒+分) |
| Constant(0) | 2 |
| Constant(1) | 2 |
| NOT Gate | 6 (Carry检测) |
| AND Gate (6输入) | 2 (Carry检测) |
| 显示译码器 | 2 |
| 7-Segment Decoder | 4 |
| 7-Segment Display | 4 |

### 设计要点

1. **同步复位**：使用MUX在寄存器输入端选择0，避免异步复位的毛刺问题
2. **Carry检测**：检测60(111100)的二进制模式
3. **进位传播**：秒Carry触发分计数器加1
4. **显示转换**：6位二进制→十进制十位/个位

---

## 附录B：F3.7 常用子电路

### D_Latch
- 输入: D, WE
- 输出: Q, Q'
- 功能: WE=1时透明，WE=0时保持

### D_Latch_RST
- 输入: D, WE, RESET
- 输出: Q, Q'
- 功能: 带复位的D锁存器

### D_Flip_Flop_RST
- 输入: D, CLK, RESET
- 输出: Q, Q'
- 功能: 边沿触发的D触发器，带复位

### D_Register_4bit
- 输入: D[3:0], CLK, RESET
- 输出: Q[3:0]
- 功能: 4位寄存器

### D_Register_6bit
- 输入: D[5:0], CLK, RESET
- 输出: Q[5:0]
- 功能: 6位寄存器

### D_Register_8bit
- 输入: D[7:0], CLK, RESET
- 输出: Q[7:0]
- 功能: 8位寄存器

### Full_Adder_4bit
- 输入: A[3:0], B[3:0], Cin
- 输出: Sum[3:0], Cout
- 功能: 4位加法器

### Full_Adder_6bit
- 输入: A[5:0], B[5:0], Cin
- 输出: Sum[5:0], Cout
- 功能: 6位加法器

### Full_Adder_8bit
- 输入: A[7:0], B[7:0], Cin
- 输出: Sum[7:0], Cout
- 功能: 8位加法器

### MUX_6bit_2to1
- 输入: in0[5:0], in1[5:0], sel
- 输出: out[5:0]
- 功能: 6位2选1多路选择器

---

## 附录C：设计规范与最佳实践

### 层次化设计

1. Level 1: 基本门电路 (NOT, AND, OR, XOR)
2. Level 2: 1-bit 功能模块 (MUX, Adder, Latch)
3. Level 3: 多-bit 功能模块 (Register, Adder_Nbit, MUX_Nbit)
4. Level 4: 子系统 (Counter, Display)
5. Level 5: 完整系统 (Clock)

### 信号命名规范

- 时钟信号: CLK
- 数据信号: D[7:0], Q[7:0]
- 控制信号: RESET, WE, EN
- 进位信号: Carry, Cout
- 选择信号: sel

### 颜色编码 (SVG)

- 蓝色 (#0055aa): 时钟信号
- 绿色 (#22aa22): 数据信号
- 橙色 (#e67e22): 进位信号
- 红色 (#cc0000): 复位信号

### 测试建议

1. 先测试基本门电路
2. 逐层构建和测试子电路
3. 使用LED/数码管观察输出
4. 添加手动时钟按钮便于调试
5. 最后使用自动时钟源
