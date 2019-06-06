from flask import Flask, render_template, request
from src.SearchEngine import SearchEngine
from src.Pagination import Pagination
from src.search_engine.main import se, rs

app = Flask(__name__, template_folder="template", static_folder="static")


@app.route('/')
def root():
    return render_template("index.html")


@app.route('/search/')
def search():
    cur_page = request.args.get("page", default=1, type=int)
    query = request.args.get("q", default="", type=str)
    associate_switch = request.args.get("ast_sw", default="on", type=str)
    se = SearchEngine(query=query)
    se.search()
    result_num, link_list = se.get_result(cur_page)
    pagination = Pagination(cur_page, result_num)
    return render_template("answer.html", query=query, result_num=result_num,
                           link_list=link_list, pagination=pagination, ast_sw=associate_switch)


if __name__ == "__main__":
    se.load_reverse_index()
    rs.load_doc()

    app.run(host='0.0.0.0')
