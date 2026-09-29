# -*- coding: utf-8 -*-
"""生成项目计划书配图（PDF 矢量 + PNG 位图）。"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "项目计划书", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 10

C_BLUE = "#1B4DB1"
C_TEAL = "#0EA89E"
C_ORANGE = "#E8A33D"
C_GRAY = "#6B7280"
C_LIGHT = "#EAF2FF"


def save(fig, name):
    fig.savefig(os.path.join(FIG_DIR, name + ".pdf"), format="pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(os.path.join(FIG_DIR, name + ".png"), format="png", dpi=300, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print("saved", name)


def box(ax, x, y, w, h, text, fc, ec, tc="white", fs=10, bold=True):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.018",
        fc=fc, ec=ec, lw=1.4, mutation_aspect=0.9,
    ))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            color=tc, fontsize=fs, fontweight="bold" if bold else "normal", wrap=True)


def arrow(ax, x1, y1, x2, y2, color=C_BLUE, lw=2.0, mutation_scale=16):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=mutation_scale, lw=lw, color=color))


def fig_arch():
    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    layers = [
        (6.0, "应用层", "学校筛查工作台 · 家长报告 · 危机预警 · 分级干预建议", C_BLUE),
        (4.4, "算法层", "差分熵与功率谱特征 · 跨被试 Transformer · 风险分级 · 可解释模块", C_TEAL),
        (2.8, "数据层", "脱敏与加密 · 时序对齐 · 质量评估 · 联邦学习数据流", "#3E7CB1"),
        (1.2, "感知层", "干电极脑电头环 · 心率皮电手环 · 心理量表终端", "#5A6B7B"),
    ]
    for y, name, desc, color in layers:
        box(ax, 0.3, y, 9.4, 1.05, name + "\n" + desc, color, color, fs=11)
    arrow(ax, 5.0, 2.25, 5.0, 2.75)   # 感知层 -> 数据层
    arrow(ax, 5.0, 3.85, 5.0, 4.35)   # 数据层 -> 算法层
    arrow(ax, 5.0, 5.45, 5.0, 5.95)   # 算法层 -> 应用层
    # 右侧隐私保护纵栏
    ax.add_patch(FancyBboxPatch((9.72, 1.2), 0.28, 5.85, boxstyle="square,pad=0",
                                fc="#F2F7FF", ec=C_BLUE, lw=1.0, ls="--"))
    ax.text(9.86, 4.0, "本地推理\n加密存储\n知情同意", ha="center", va="center",
            fontsize=8.2, color=C_BLUE)
    fig.suptitle("「心聆」平台总体技术架构", fontsize=13, fontweight="bold", color="#123F8F", y=0.985)
    save(fig, "fig_arch")


def fig_flow():
    fig, ax = plt.subplots(figsize=(11.5, 4.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.2)
    ax.axis("off")

    steps_top = [
        (0.15, "知情同意\n与建档"),
        (2.15, "佩戴头环\n五分钟采集"),
        (4.15, "标准化情绪\n诱发任务"),
        (6.15, "信号预处理\n与质量评估"),
        (8.15, "多模态\n特征提取"),
    ]
    for x, label in steps_top:
        box(ax, x, 2.05, 1.6, 0.85, label, C_BLUE, C_BLUE, fs=9.5)
    # 下排自右向左排列，形成 S 形流程
    bottom_labels = [
        (8.15, "跨被试\n情绪识别", C_TEAL),
        (6.15, "风险分级\n低中高", C_TEAL),
        (4.15, "心理教师\n复核确认", C_ORANGE),
        (2.15, "分级干预\n与持续追踪", "#D9534F"),
        (0.15, "高危预警\n转介通道", "#D9534F"),
    ]
    for x, label, fc in bottom_labels:
        box(ax, x, 0.35, 1.6, 0.85, label, fc, fc, fs=9.5)

    # 上排水平箭头（左→右），对准方框侧边中心
    for i in range(4):
        arrow(ax, 1.75 + i * 2.0, 2.475, 2.15 + i * 2.0, 2.475,
              mutation_scale=12)
    # 下排水平箭头（右→左），对准方框侧边中心
    for i in range(4):
        xr = 8.15 - i * 2.0          # 右侧方框左边缘
        arrow(ax, xr, 0.775, xr - 0.4, 0.775, color=C_TEAL, mutation_scale=12)
    # 上下行连接：多模态特征提取 → 跨被试情绪识别（垂直居中）
    arrow(ax, 8.95, 2.0, 8.95, 1.2, color=C_ORANGE, lw=2.2, mutation_scale=14)
    ax.text(9.82, 1.64, "云端/本地模型推理", rotation=90, fontsize=8.5,
            color=C_ORANGE, ha="center", va="center")
    ax.text(0.15, 3.02, "学校心理健康年度筛查流程（单次约 8 分钟）", fontsize=12,
            fontweight="bold", color="#123F8F")
    save(fig, "fig_flow")


def fig_compare():
    fig, ax = plt.subplots(figsize=(7.6, 6.2), subplot_kw={"projection": "polar"})
    dims = ["客观性", "抗伪装性", "可解释性", "采集便捷性", "综合成本友好"]
    n = len(dims)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]
    data = {
        "传统问卷量表": [2.0, 1.5, 4.2, 5.0, 5.0],
        "智能手环": [3.4, 2.5, 3.0, 4.5, 4.5],
        "消费级脑电竞品": [4.0, 4.0, 3.0, 3.4, 3.0],
        "「心聆」平台": [5.0, 5.0, 4.5, 4.0, 3.8],
    }
    colors = {"传统问卷量表": "#9AA5B1", "智能手环": "#E8A33D",
              "消费级脑电竞品": "#5A6B7B", "「心聆」平台": C_TEAL}
    for name, vals in data.items():
        v = vals + vals[:1]
        ax.plot(angles, v, lw=2, label=name, color=colors[name])
        ax.fill(angles, v, alpha=0.08, color=colors[name])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dims, fontsize=10.5)
    ax.set_ylim(0, 5.3)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=8, color=C_GRAY)
    ax.set_title("主流心理健康筛查方案能力对比（评分 1–5）", fontsize=12.5,
                 fontweight="bold", color="#123F8F", pad=22)
    ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.10), fontsize=9, frameon=False)
    save(fig, "fig_compare")


def fig_market():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.3), gridspec_kw={"width_ratios": [2, 1]})
    labels = ["青少年抑郁检出率\n（中科院心理研究所）",
              "6–16 岁学生精神障碍\n总患病率（流行病学调查）",
              "焦虑障碍患病率\n（同源调查）"]
    vals = [24.6, 17.5, 4.7]
    colors = [C_BLUE, C_TEAL, C_ORANGE]
    bars = ax1.barh(range(len(labels)), vals, color=colors, height=0.5)
    for b, v in zip(bars, vals):
        ax1.text(v + 0.6, b.get_y() + b.get_height() / 2, f"{v}%",
                 va="center", fontsize=10, fontweight="bold")
    ax1.set_yticks(range(len(labels)))
    ax1.set_yticklabels(labels, fontsize=9)
    ax1.set_xlim(0, 30)
    ax1.set_xlabel("检出率 / 患病率（%）", fontsize=9.5)
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.set_title("检出率与患病率", fontsize=11, fontweight="bold", color="#123F8F")

    bars2 = ax2.barh([0], [800], color=C_GRAY, height=0.5)
    ax2.text(812, 0, "800 万通", va="center", fontsize=10, fontweight="bold")
    ax2.set_yticks([0])
    ax2.set_yticklabels(["心理援助热线\n年接听量"], fontsize=9)
    ax2.set_xlim(0, 950)
    ax2.set_xlabel("接听量（万通）", fontsize=9.5)
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.set_title("心理热线服务量", fontsize=11, fontweight="bold", color="#123F8F")
    fig.suptitle("我国青少年心理健康核心现状数据", fontsize=12.5, fontweight="bold",
                 color="#123F8F", y=1.02)
    save(fig, "fig_market")


def fig_roadmap():
    fig, ax = plt.subplots(figsize=(12.0, 4.8))
    # 横轴：以 2026 年 6 月为 0，每 3.5 个月一个单位
    tasks = [
        ("2026 下半年", 0.9, 1.7, "原型开发 · 伦理审查 · 数据采集", C_BLUE),
        ("2027 上半年", 2.8, 1.7, "五十所试点学校 · 临床对照预试验", C_TEAL),
        ("2027 下半年", 4.7, 1.7, "产品迭代 · 区域代理商网络", C_TEAL),
        ("2028 全年", 6.6, 3.6, "三百所学校规模化 · 医院心理科试点", C_ORANGE),
        ("2029 全年", 10.4, 3.2, "企业员工关怀 · 东南亚市场拓展", "#D9534F"),
    ]
    for i, (label, start, dur, desc, color) in enumerate(tasks):
        y = len(tasks) - i
        ax.barh(y, dur, left=start, height=0.34, color=color, alpha=0.92)
        ax.text(start + dur / 2, y + 0.30, desc, ha="center", va="center",
                color="#1F2937", fontsize=9.2)
        ax.text(start + dur + 0.18, y, label, ha="left", va="center",
                fontsize=9.2, color="#374151")
    ax.set_xlim(0, 14.5)
    ax.set_ylim(0.2, len(tasks) + 0.75)
    ax.set_yticks([])
    ax.set_xticks([0, 1.7, 3.4, 5.1, 6.9, 8.6, 10.3, 12.0])
    ax.set_xticklabels(["2026.6", "2026.12", "2027.6", "2027.12",
                        "2028.6", "2028.12", "2029.6", "2029.12"], fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("「心聆」三年发展路线图", fontsize=12.5, fontweight="bold", color="#123F8F", pad=12)
    save(fig, "fig_roadmap")


def fig_revenue():
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    years = ["2027 年", "2028 年", "2029 年"]
    sub = [60, 220, 520]
    hard = [25, 90, 180]
    svc = [15, 60, 150]
    ax.bar(years, sub, label="软件订阅服务", color=C_BLUE)
    ax.bar(years, hard, bottom=sub, label="硬件租赁", color=C_TEAL)
    ax.bar(years, svc, bottom=[i + j for i, j in zip(sub, hard)], label="增值服务", color=C_ORANGE)
    for i, total in enumerate([100, 370, 850]):
        ax.text(i, total + 18, f"{total} 万元", ha="center", fontsize=10.5, fontweight="bold")
    ax.set_ylabel("收入（万元）", fontsize=10)
    ax.set_ylim(0, 1000)
    ax.legend(frameon=False, fontsize=9.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("「心聆」未来三年收入预测（基准情景）", fontsize=12.5,
                 fontweight="bold", color="#123F8F", pad=12)
    save(fig, "fig_revenue")


if __name__ == "__main__":
    fig_arch()
    fig_flow()
    fig_compare()
    fig_market()
    fig_roadmap()
    fig_revenue()
    print("ALL FIGURES DONE")
