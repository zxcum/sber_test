import json
import csv
from io import StringIO
import pandas as pd


class ReportMaker:
    def json_report(self, products: dict, sales: dict, plan: dict):
        current_results = self.count_percentages(plan=plan, sales=sales, product=products)
        overall_results = self.count_overall_percentage(plan=plan, sales=sales)
        result = ({
            "current_results": current_results,
            "overall_results": overall_results
        })
        csv_content = self.create_csv(data=result)
        return csv_content

    def count_percentages(self, plan: dict, sales: dict, product: dict):

        result = {}
        for product_id in plan.keys():
            if int(product_id) in sales.keys():
                result[product[int(product_id)]] = float(sales[int(product_id)]) / plan[product_id] * 100
            else:
                result[product[int(product_id)]] = 0

        return result

    def count_overall_percentage(self, plan: dict, sales: dict):
        return sum(sales.values()) / sum(plan.values()) * 100

    def create_csv(self, data: dict):
        df = pd.DataFrame(list(data["current_results"].items()), columns=["фрукт", "процент выполнения плана"])
        csv_content = df.to_csv(index=False, encoding="utf-8")
        csv_content += f"\n\nОбщий процент выполнения плана,{data['overall_results']}"
        return csv_content
