import math
from dataclasses import dataclass

@dataclass
class CompanyData:
    """企業の財務データを保持し、関連する経営指標を計算するデータクラス。

    Attributes:
        name (str): 企業名
        variable_cost_ratio (float): 変動費率 (0.0 ~ 1.0)
        fixed_cost (int): 固定費
        sales (int): 売上高
    """
    name: str
    variable_cost_ratio: float
    fixed_cost: int
    sales: int

    @property
    def marginal_profit_ratio(self) -> float:
        """限界利益率を計算して返します。

        Returns:
            float: 限界利益率 (1 - 変動費率)
        """
        return 1.0 - self.variable_cost_ratio

    @property
    def break_even_point(self) -> float:
        """損益分岐点売上高を計算して返します。

        Returns:
            float: 損益分岐点売上高。限界利益率が0の場合は0.0を返します。
        """
        if self.marginal_profit_ratio == 0:
            return 0.0
        return self.fixed_cost / self.marginal_profit_ratio

    @property
    def safety_margin_ratio(self) -> float:
        """安全余裕率を計算して返します。

        Returns:
            float: 安全余裕率 ((売上高 - 損益分岐点) / 売上高)。売上が0の場合は0.0を返します。
        """
        if self.sales == 0:
            return 0.0
        return (self.sales - self.break_even_point) / self.sales

    @property
    def safety_level(self) -> str:
        """安全余裕率に基づき、企業の安全性を3段階で判定します。

        Returns:
            str: "High" (安全), "Medium" (注意), "Low" (危険) のいずれか。
        """
        ratio = self.safety_margin_ratio
        if ratio > 0.4:
            return "High"
        elif ratio > 0.15:
            return "Medium"
        else:
            return "Low"
    
    @property
    def profit(self) -> int:
        """現在の売上における営業利益を計算して返します。

        Returns:
            int: 営業利益 (売上 - (固定費 + 変動費))
        """
        return int(self.sales - (self.fixed_cost + self.sales * self.variable_cost_ratio))