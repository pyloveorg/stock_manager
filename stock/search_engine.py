from sqlalchemy_searchable import search
from database import db
from invoices.models import Products


def search_engine(query):
    product_list = {"Products":[]}
    if query:
        search_results = Products.query.order_by(Products.products_id)
        search_results = search(search_results, query)

    else:
        search_results = Products.query.order_by(Products.products_id)

    for r in search_results:
        product_name = str(r)
        product_list["Products"].append({"name": product_name[1:-1], "columns": [
            r.products_id,
            r.name,
            r.group,
            r.stock_quantity,
            r.price,
            r.supplier_id
        ]})

    return product_list


if __name__ == '__main__':
    from main import app
    app.app_context().push()
    db.create_all()
    search_engine(query)