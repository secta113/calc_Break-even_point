import streamlit as st
from models import CompanyData
from utils import log_to_console
from data_loader import load_data_from_csv
from charts import create_bep_chart, create_comparison_pv_chart

def main() -> None:
    """アプリケーションのメインエントリポイント。
    
    Streamlitのページ設定、データ読み込み、各コンポーネントの描画を制御します。
    """
    log_to_console("アプリ起動")
    st.set_page_config(page_title="企業安全性分析", layout="wide")
    st.title("📊 経営分析ダッシュボード")

    csv_file = "companies.csv"
    company_list = load_data_from_csv(csv_file)

    if not company_list:
        st.warning("CSVファイル (companies.csv) が見つかりません。")
        return

    # === 上段：サマリー ===
    st.markdown("### 📋 企業財務サマリー")
    for company in company_list:
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 3])
            with col1:
                st.markdown(f"**{company.name}**")
                level = company.safety_level
                if level == "High":
                    st.success("安全")
                elif level == "Medium":
                    st.warning("注意")
                else:
                    st.error("危険")
            with col2:
                st.caption("基礎数値")
                st.text(f"売上: {company.sales:,}")
                st.text(f"固定: {company.fixed_cost:,}")
            with col3:
                st.caption("分析指標")
                st.progress(max(0.0, min(1.0, company.safety_margin_ratio)))
                st.caption(f"安全余裕率: {company.safety_margin_ratio:.1%} (分岐点: {int(company.break_even_point):,})")
            st.divider()

    # === 中段：個別グラフ (3列折り返し) ===
    st.markdown("### 📉 損益分岐点グラフ (個別詳細)")
    COLS_PER_ROW = 3
    for i in range(0, len(company_list), COLS_PER_ROW):
        cols = st.columns(COLS_PER_ROW)
        batch = company_list[i : i + COLS_PER_ROW]
        for j, company in enumerate(batch):
            with cols[j]:
                st.subheader(f"{company.name}")
                fig = create_bep_chart(company)
                st.pyplot(fig, use_container_width=True)

    # === 下段：統合比較グラフ ===
    st.markdown("---")
    st.markdown("### ⚔️ 戦略比較マップ (利益構造の比較)")
    
    # ユーザー指定の「見方のポイント」および現在の値（〇）の説明
    st.markdown("""
    <middle>
    <b>見方のポイント：</b><br>
    ・線の<b>「スタート位置」</b>が低いほど、固定費が重い（リスクが高い）ことを示します。<br>
    ・線の<b>「傾き」</b>が急なほど、1個売れた時の利益率が高い（爆発力がある）ことを示します。<br>
    ・線が<b>「0(黒線)」</b>と交わる点が損益分岐点です。<br>
    ・線上の<b>「● (丸印)」</b>は、現在の売上・利益位置を示します。
    </middle>
    """, unsafe_allow_html=True)
    
    if company_list:
        fig_comp = create_comparison_pv_chart(company_list)
        st.pyplot(fig_comp, use_container_width=True)
    
    log_to_console("全描画完了")

if __name__ == "__main__":
    main()