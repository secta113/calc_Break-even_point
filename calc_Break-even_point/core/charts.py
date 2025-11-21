import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np
from matplotlib.figure import Figure
from models import CompanyData
from utils import log_to_console

# --- フォント設定 (モジュール読み込み時に実行) ---
try:
    import japanize_matplotlib
except ImportError:
    # Windows/Macでのフォールバック
    mpl.rcParams['font.family'] = 'Meiryo' if os.name == 'nt' else 'Hiragino Sans'

def create_bep_chart(company: CompanyData) -> Figure:
    """個別の損益分岐点チャート(BEP図)を作成します。

    Args:
        company (CompanyData): 描画対象の企業データオブジェクト

    Returns:
        Figure: MatplotlibのFigureオブジェクト
    """
    max_x = max(company.sales * 1.2, company.break_even_point * 1.2)
    x = np.linspace(0, max_x, 100)

    y_sales = x
    y_total_cost = company.fixed_cost + (company.variable_cost_ratio * x)
    y_fixed_cost = np.full_like(x, company.fixed_cost)

    fig, ax = plt.subplots(figsize=(5, 4))
    
    ax.plot(x, y_sales, label='売上', color='#1f77b4')
    ax.plot(x, y_total_cost, label='総費用', color='#ff7f0e')
    ax.plot(x, y_fixed_cost, label='固定費', color='gray', linestyle='--', alpha=0.5)

    ax.fill_between(x, y_sales, y_total_cost, where=(y_sales > y_total_cost), color='blue', alpha=0.1)
    ax.fill_between(x, y_sales, y_total_cost, where=(y_sales < y_total_cost), color='red', alpha=0.1)

    # ポイント描画
    ax.plot(company.sales, company.sales, 'o', color='black', markersize=8, zorder=5, label='現在値')
    ax.plot(company.break_even_point, company.break_even_point, '*', color='red', markersize=12, zorder=5, label='分岐点')

    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', fontsize='small')

    ax.get_xaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.tight_layout()
    return fig

def create_comparison_pv_chart(companies: list[CompanyData]) -> Figure:
    """全企業を比較する利益図表(PV Chart)を作成します。

    現在値のポイント描画と、ラベル位置のオフセット調整を含みます。

    Args:
        companies (list[CompanyData]): 比較対象となる企業データのリスト

    Returns:
        Figure: MatplotlibのFigureオブジェクト
    """
    log_to_console("統合比較グラフの作成を開始します")
    
    # X軸の最大値を決定
    max_sales_all = max([c.sales for c in companies]) if companies else 1000
    limit_x = max_sales_all * 1.1
    
    x = np.linspace(0, limit_x, 100)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axhline(0, color='black', linewidth=1.5, linestyle='-')

    # カラーマップから色を取得 (最大20色まで対応できるタブカラーを使用)
    colors = cm.get_cmap('tab20', 20)

    for i, company in enumerate(companies):
        # カラーマップからi番目の色を取得
        color = colors(i % 20)
        
        # 利益線の計算
        y_profit = (company.marginal_profit_ratio * x) - company.fixed_cost
        
        # プロット
        ax.plot(x, y_profit, label=f"{company.name}", color=color, linewidth=2)
        
        # 現在地プロット
        current_profit = company.profit
        ax.plot(company.sales, current_profit, 'o', color=color, markersize=8, markeredgecolor='white', zorder=5)
        
        # テキスト表示（指示通り、位置を少しずらして表示）
        ax.annotate(f"{company.name}",
                    xy=(company.sales, current_profit),
                    xytext=(5, 5), 
                    textcoords='offset points',
                    color=color,
                    fontsize=9,
                    fontweight='bold')

    ax.set_title("【統合比較】 利益構造チャート (PV図)", fontsize=14)
    ax.set_xlabel("売上高 (Volume)", fontsize=10)
    ax.set_ylabel("利益 (Profit)", fontsize=10)
    
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend(loc='upper left', fontsize='small', ncol=2)
    
    ax.get_xaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.tight_layout()
    return fig