# Add Two Numbers

## Problem

[](desc.md ':include')

## Solution

引入一个空的头节点 `node` 可以减少很多判断，代码更加简洁。

使用 `l1 || l2` 而不是 `l1 && l2` 虽然效率上更低了，但是代码更加简洁了。

[](solution.cpp ':include :type=code cpp')