import os
import pandas as pd
from models import CompanyData
from utils import log_to_console

def load_data_from_csv(file_path: str) -> list[CompanyData]:
    """CSVファイルから企業データを読み込み、データクラスのリストに変換します。

    Args:
        file_path (str): 読み込むCSVファイルのパス

    Returns:
        list[CompanyData]: 読み込みに成功した企業データのリスト。失敗時は空リストを返します。
    """
    log_to_console(f"データ読み込み開始: {file_path}")
    
    if not os.path.exists(file_path):
        log_to_console("CSVファイルが見つかりませんでした")
        return []
    
    try:
        df = pd.read_csv(file_path)
        companies = []
        for _, row in df.iterrows():
            companies.append(CompanyData(
                name=str(row['company_name']),
                variable_cost_ratio=float(row['variable_cost_ratio']),
                fixed_cost=int(row['fixed_cost']),
                sales=int(row['sales'])
            ))
        log_to_console(f"{len(companies)}件のデータをロードしました")
        return companies
    except Exception as e:
        log_to_console(f"データ読み込みエラー: {e}")
        return []