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

```
Y1 = I3 + I2
Y0 = I3 + I1·I2'
```

### 接线

```
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

```
16位输入分为4组，每组4位，各接一个 4-2 编码器：

Encoder_0: I[3:0]   → Y0[1:0], V0
Encoder_1: I[7:4]   → Y1[1:0], V1
Encoder_2: I[11:8]  → Y2[1:0], V2
Encoder_3: I[15:12] → Y3[1:0], V3
```

### 高位输出 O[3:2]

```
O3 = V3
O2 = V3' · V2 + V3 = V2 + V3  (简化)
```

用优先级链：
```
O3 = V3
O2 = V2 + V3 (但V3优先)
```

### 低位输出 O[1:0]

```
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
```
NOT Gate × N: 对每一位取反
Priority Encoder: 输入取反后的数据
输出 = 前导零的数量
```

### 前导一 (CLO)

直接送入优先编码器：
```
Priority Encoder: 输入原始数据
输出 = 前导一的数量
```

### 尾部零/一

将输入位序反转后，分别用 CLZ/CLO 方法。

---

## 4. 1位 2选1 多路选择器

### 逻辑表达式

```
Y = S'·A + S·B
```

### 接线

```
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

```
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

```
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

```
实际传给译码器的最高位 = D[3] AND S

当 S=0（十进制）: 最高位被强制为0，只显示0-9
当 S=1（十六进制）: 最高位保持原值，显示0-F
```

### 接线

```
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

```
XNOR Gate 0: A[0] XNOR B[0] → eq0
XNOR Gate 1: A[1] XNOR B[1] → eq1
XNOR Gate 2: A[2] XNOR B[2] → eq2
XNOR Gate 3: A[3] XNOR B[3] → eq3

AND Gate (4输入): eq0 AND eq1 AND eq2 AND eq3 → A_eq_B
```

### 大于/小于检测

```
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

```
Sum  = A XOR B
Cout = A AND B
```

### 接线

```
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

```
Half Adder 1: A + B       → temp_sum, temp_cout1
Half Adder 2: temp_sum + Cin → Sum, temp_cout2
OR Gate: temp_cout1 + temp_cout2 → Cout
```

### 接线

```
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

```
FA0: A[0] + B[0], Cin=0   → Sum[0], Cout→C1
FA1: A[1] + B[1], Cin=C1  → Sum[1], Cout→C2
FA2: A[2] + B[2], Cin=C2  → Sum[2], Cout→C3
FA3: A[3] + B[3], Cin=C3  → Sum[3], Cout (进位输出)
```

### 输出显示

```
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

```
NOT Gate ×4: NOT(B[0])→Bn0, NOT(B[1])→Bn1, NOT(B[2])→Bn2, NOT(B[3])→Bn3

FA0: A[0] + Bn0, Cin=1(接VCC) → Sub[0], Cout→C1
FA1: A[1] + Bn1, Cin=C1       → Sub[1], Cout→C2
FA2: A[2] + Bn2, Cin=C2       → Sub[2], Cout→C3
FA3: A[3] + Bn3, Cin=C3       → Sub[3], Cout (借位)

Cin=1 接电源 (VCC / 高电平)
```

### 输出显示

```
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

```
同号: 结果幅度 = |A| + |B|, 符号 = A的符号
异号: 结果幅度 = ||A| - |B||, 符号 = 取幅度大的数的符号
```

### 子模块

#### 13.1 比较器 |A| ≥ |B|

```
减法器 A-B: borrow输出 = A_ge_B (有借位=0表示|A|<|B|)
```

#### 13.2 3位加法器 (|A|+|B|)

```
3个全加器级联: A[2:0] + B[2:0], Cin=0 → add_sum[2:0]
```

#### 13.3 3位减法器 (|A|-|B|)

```
NOT ×3 取反 B
3个全加器: A[2:0] + NOT(B[2:0]), Cin=1 → sub_ab[2:0]
```

#### 13.4 3位减法器 (|B|-|A|)

```
NOT ×3 取反 A
3个全加器: B[2:0] + NOT(A[2:0]), Cin=1 → sub_ba[2:0]
```

#### 13.5 MUX 选择结果幅度

```
MUX_d[i]: sel=A_ge_B, in0=sub_ba[i], in1=sub_ab[i] → diff_mag[i]
MUX_r[i]: sel=diff_sign, in0=add_sum[i], in1=diff_mag[i] → result_mag[i]
```

#### 13.6 MUX 选择结果符号

```
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

```
sm_sign = input[3]
sm_mag[i] = input[i] XOR input[3]  (i=0,1,2)
```

需要 3 个 XOR 门（每位 XOR 符号位）

### 14.2 原码加法器

复用上述第13节的原码加法器设计。

### 14.3 原码 → 反码转换器

```
result[3] = sm_result_sign
result[i] = sm_result_mag[i] XOR sm_result_sign  (i=0,1,2)
```

需要 3 个 XOR 门

### 完整信号流

```
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

```
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

```
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

```
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
