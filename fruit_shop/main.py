from datetime import datetime
from typing import Annotated
from fastapi import FastAPI, HTTPException, Header, Response
import uvicorn
from db.db_helper import DataBase
from models.request_models import AddSale, JWTHeader
from models.report_model import ReportMaker
from jwt.jwt import JWTDecoder
import json

app = FastAPI()

db = DataBase()


def can_post_sales(role: str):
    return role == 'shop_ceo'


def can_get_reports(role: str):
    return role == 'director_ceo'


def get_payload(token: str):
    decoder = JWTDecoder()
    payload = decoder.get_unverified_payload(token=token)
    return payload


def convert_to_datetime(date: str):
    year, month, day = map(int, date.split("-"))
    return datetime(year, month, day).strftime('%Y-%m-%d')


@app.post("/products/")
def post_sale(sale: AddSale, headers: Annotated[JWTHeader, Header()]):
    date = convert_to_datetime(sale.date)

    payload = get_payload(token=headers.user_jwt)

    if not can_post_sales(role=payload['role']):
        return {"Not authorized access"}
    result = db.add_sale(shop_name=payload['shop_id'],
                         sale_list=sale.items,
                         date=date)

    return {result}


@app.get("/report")
def get_report(headers: Annotated[JWTHeader, Header()]):
    payload = get_payload(token=headers.user_jwt)

    if not can_get_reports(role=payload['role']):
        return {"Not authorized access"}

    report = json.loads(db.get_plan(shop_id=payload['shop_id']))
    sales = db.get_sales_by_shop(shop_id=payload['shop_id'])
    product = db.get_prod_ids()
    report_maker = ReportMaker()
    result = report_maker.json_report(products=product, sales=sales, plan=report)

    return Response(
        content=result,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=report_shop{payload['shop_id']}.csv"}
    )



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
