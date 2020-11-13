# Longest Palindromic Substring

## Problem

[](desc.md ':include')

## Solution

### Dynamic Programming

用 $dp[i][j](i \leq j)$ 表示子串 $s[i..j]$ 是否为回文串

$$
dp[i][j] =
\begin{cases}
1 & dp[i+1][j-1] = 1 \text{ AND } s[i] = s[j] \\
1 & i = j \\
0 & \text{other}
\end{cases}
$$

计算依赖

![](dp-1.drawio.svg)

计算顺序：从 level 1 按箭头顺序一直计算到 level 4

![](dp-2.drawio.svg)

[](dp.cpp ':include :type=code cpp')

### Expand Around Center

[](expand-around-center.cpp ':include :type=code cpp')