import urllib.request
from pathlib import Path

import duckdb
from query import query_server, query_ui
from shiny import App, reactive, ui

app_dir = Path(__file__).parent
db_file = app_dir / "local.db"

con = duckdb.connect(str(db_file), read_only=True)
app_ui = ui.page_fluid(
    ui.tags.div(
        query_ui("initial_query", remove_id="initial_query")
    , id="module_container"), width=1, class_="bslib-page-dashboard")

def server(input, output, session):
    query_server("initial_query", con=con, remove_id="initial_query")
    
    # mod_counter = reactive.value(0)


    # @reactive.effect
    # @reactive.event(input.add_query)
    # def _():
    #     counter = mod_counter.get() + 1
    #     mod_counter.set(counter)
    #     id = "query_" + str(counter)
    #     ui.insert_ui(
    #         selector="#module_container",
    #         where="afterBegin",
    #         ui=query_ui(id, remove_id=id),
    #     )
    #     query_server(id, con=con, remove_id=id)

    # @reactive.effect
    # @reactive.event(input.show_meta)
    # def _():
    #     counter = mod_counter.get() + 1
    #     mod_counter.set(counter)
    #     id = "query_" + str(counter)
    #     ui.insert_ui(
    #         selector="#module_container",
    #         where="afterBegin",
    #         ui=query_ui(
    #             id, qry="SELECT * from information_schema.columns", remove_id=id
    #         ),
    #     )
    #     query_server(id, con=con, remove_id=id)


app = App(app_ui, server)