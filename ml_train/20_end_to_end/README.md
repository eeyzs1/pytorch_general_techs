# 20_end_to_end — 项目级串联案例

把库内专题收成可跑通的交付流水线，适合作为复习课 / 面试项目 / 内部培训主线。

## 案例列表

| Notebook | 主题 | 串联模块 |
|----------|------|----------|
| [01_moe_from_mixture_to_serving.ipynb](01_moe_from_mixture_to_serving.ipynb) | MoE：配比→训练观测→EP→Serving→Go-Live | 01 / 03 / 04 / 05 / 09 / 18 |

## 怎么用

1. 按表内「串联模块」快速回看专题 notebook（可选）
2. 从头到尾运行本目录案例（CPU 可跑）
3. 尝试课后扩展：前缀缓存、PD 分离、GRPO on code

## 设计原则

- **自包含**：不依赖其他 notebook 的运行态
- **可门禁**：用 Go-Live checks 表达“上线”，而不是只看 loss
- **可替换**：每个玩具组件都标明生产对应系统
