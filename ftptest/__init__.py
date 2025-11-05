#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .version import __version__

import sys, os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.table import Table
from matplotlib.gridspec import GridSpec

sys.path.append(os.getcwd())

def fit_heart_rate_power_linear(csv_file, lthr=None):
    """
    拟合心率和功率的线性关系: hr = a * power + b
    """
    
    # 从CSV文件读取数据
    try:
        data = np.loadtxt(csv_file, delimiter=',')
        if data.ndim != 2 or data.shape[1] != 2:
            raise ValueError("CSV文件格式错误，每行必须包含功率和心率两个数值，用逗号分隔")
        power_data = data[:, 0]
        hr_data = data[:, 1]
    except Exception as e:
        print(f"读取CSV文件失败: {str(e)}")
        sys.exit(1)
    
    # 线性回归拟合
    slope, intercept, r_value, p_value, std_err = stats.linregress(power_data, hr_data)
    
    # 打印拟合结果
    print("=" * 50)
    print("线性回归拟合结果")
    print("=" * 50)
    print(f"拟合方程: HR = {slope:.4f} * Power + {intercept:.4f}")
    print(f"R²值: {r_value**2:.4f}")
    print(f"相关系数: {r_value:.4f}")
    print(f"P值: {p_value:.6f}")
    print(f"标准误差: {std_err:.4f}")
    print("=" * 50)
    
    # 计算FTP（如果提供LTHR）
    ftp = None
    if lthr is not None:
        try:
            lthr_val = float(lthr)
            if slope == 0:
                print("无法计算FTP，斜率为0")
            else:
                ftp = (lthr_val - intercept) / slope
                print(f"\n根据乳酸阈值心率 {lthr_val} bpm 计算:")
                print(f"FTP (功能阈值功率) = {ftp:.2f} W")
            print("=" * 50)
        except ValueError:
            print(f"无效的乳酸阈值心率值: {lthr}")
            sys.exit(1)
    
    # 计算预测值（用于拟合线）
    hr_predicted = slope * power_data + intercept
    
    # 创建数据表格（仅包含功率和实际心率）
    df = pd.DataFrame({
        '功率 (W)': power_data,
        '心率 (bpm)': hr_data
    })
    
    print("\n数据表格:")
    print(df.to_string(index=False))
    
    # 图表布局设置
    data_rows = len(df)
    fig_width = 6  # 整体宽度改为6
    # 动态调整高度：顶部占2/3，底部占1/3，总高度根据数据量微调
    base_height = 8 + min(0.1 * data_rows, 2)  # 基础高度+数据量补偿（最多+2）
    plt.figure(figsize=(fig_width, base_height))
    
    # 布局划分：2行2列
    # 第1行：曲线横跨两列（占2/3高度）；第2行：左表格+右统计（共占1/3高度）
    gs = GridSpec(2, 2, figure=plt.gcf(), 
                 height_ratios=[3, 2],  # 上下高度比3:2（上3/5，下2/5）
                 width_ratios=[1, 1])   # 底部左右宽度比1:1
    
    # 中文字体设置
    try:
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Noto Sans CJK SC']
        plt.rcParams['axes.unicode_minus'] = False
    except:
        plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    # 顶部：拟合曲线图（横跨两列，占2/3高度）
    ax1 = plt.subplot(gs[0, :])
    plt.scatter(power_data, hr_data, color='blue', s=40, alpha=0.7, label='原始数据')  # 减小点大小适配窄图
    plt.plot(power_data, hr_predicted, color='red', linewidth=1.5, 
             label=f'HR = {slope:.4f} × Power + {intercept:.1f}')  # 简化标签文字
    plt.xlabel('功率 (W)', fontsize=12)
    plt.ylabel('心率 (bpm)', fontsize=12)
    plt.title('有氧骑行 心率-功率 拟合', fontsize=14, fontweight='bold')  # 简化标题
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8)  # 缩小图例字体
    plt.tick_params(axis='both', labelsize=9)  # 缩小坐标轴刻度
    
    # 底部左侧：数据表格
    ax2 = plt.subplot(gs[1, 0])
    plt.axis('off')
    plt.title('原始数据', fontsize=14, fontweight='bold', pad=5)  # 缩小标题
    
    # 创建表格
    table = Table(ax2, bbox=[0, 0, 1, 1])
    col_width = 1.0 / len(df.columns)
    
    # 添加表头（适配窄图的字体）
    for i, col_name in enumerate(df.columns):
        table.add_cell(0, i, width=col_width, height=0.025,  # 增加表头高度占比
                       text=col_name, loc='center', facecolor='#f0f0f0',
                       fontproperties={'size': 12, 'weight': 'bold'})  # 缩小表头字体
    
    # 添加数据行
    for row_idx in range(data_rows):
        for col_idx, col_name in enumerate(df.columns):
            value = df.iloc[row_idx, col_idx]
            text = f"{value:.0f}"
            facecolor = '#f9f9f9' if row_idx % 2 == 0 else '#e9e9e9'
            row_height = 0.12 / min(data_rows, 8)  # 适配1/3高度的行高
            table.add_cell(row_idx + 1, col_idx, width=col_width, height=row_height,
                           text=text, loc='center', facecolor=facecolor,
                           fontproperties={'size': 14})  # 缩小数据字体
    
    ax2.add_table(table)

    # 底部右侧：统计信息
    ax3 = plt.subplot(gs[1, 1])
    plt.axis('off')
    
    # 构建精简的统计信息文本（适配窄图）
    stats_text = f"""统计:
数据点: {len(power_data)}
功率范围: {power_data.min()}-{power_data.max()} W
心率范围: {hr_data.min()}-{hr_data.max()} bpm
R²: {r_value**2:.4f}
相关系数: {r_value:.4f}

拟合方程:
HR = {slope:.4f} × Power + {intercept:.1f}
Power = (HR - {intercept:.1f}) / {slope:.4f}
"""
    
    if ftp is not None:
        stats_text += f"\nLTHR（乳酸阈值心率）: {lthr} bpm\nFTP（功能阈值功率）: {ftp:.0f} W"
    
    # 调整文本大小和位置
    plt.text(0.03, 0.95, stats_text, transform=ax3.transAxes, 
             fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('./heart_rate_power_linear_fit.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n图表已保存为: ./heart_rate_power_linear_fit.png")
    
    return slope, intercept, r_value**2, df

# 运行拟合
def cli_main():
    if len(sys.argv) < 2:
        print("使用方法: ftptest <csv文件路径> [乳酸阈值心率]")
        print("示例: ftptest data.csv 165")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    lthr_value = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("有氧骑行心率-功率线性关系拟合")
    print("=" * 50)
    print(f"使用的数据文件: {csv_file_path}")
    if lthr_value:
        print(f"使用的乳酸阈值心率: {lthr_value} bpm")
    print("=" * 50)
    
    slope, intercept, r_squared, data_frame = fit_heart_rate_power_linear(csv_file_path, lthr_value)

if __name__ == "__main__":
    cli_main()