# from shinyswatch import theme
import urllib.request
from pathlib import Path
import duckdb

from querycore import query_output_server, query_output_ui
from shiny import App, reactive, ui, render


app_dir = Path(__file__).parent
# db_file = app_dir / "db.db"
# con = duckdb.connect(str(db_file), read_only=True)
con = duckdb.connect(':memory:')
con.install_extension('httpfs')
con.load_extension('httpfs')

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_action_button("add_query", "Add Query", class_="btn btn-primary"),
        ui.input_action_button(
            "show_meta", "Show Metadata", class_="btn btn-secondary"
        ),
        ui.markdown(
            """
            This app lets you explore a dataset using SQL and duckdb.
            The data is stored in an on-disk [duckdb](https://duckdb.org/) database,
            which leads to extremely fast queries.
            """
        ),
    ),
    ui.tags.div(
        query_output_ui("initial_query", remove_id="initial_query"),
        id="module_container",
    ),
    title="DuckDB query explorer",
    class_="bslib-page-dashboard",
    # theme=theme.sandstone, 
)


def server(input, output, session):
    mod_counter = reactive.value(0)

    query_output_server("initial_query", con=con, remove_id="initial_query")

    @reactive.effect
    @reactive.event(input.add_query)
    def _():
        counter = mod_counter.get() + 1
        mod_counter.set(counter)
        id = "query_" + str(counter)
        ui.insert_ui(
            selector="#module_container",
            where="afterBegin",
            ui=query_output_ui(id, remove_id=id),
        )
        query_output_server(id, con=con, remove_id=id)

    @reactive.effect
    @reactive.event(input.show_meta)
    def _():
        counter = mod_counter.get() + 1
        mod_counter.set(counter)
        id = "query_" + str(counter)
        ui.insert_ui(
            selector="#module_container",
            where="afterBegin",
            ui=query_output_ui(
                id, qry="SELECT * from information_schema.columns", remove_id=id
            ),
        )
        query_output_server(id, con=con, remove_id=id)


app = App(app_ui, server)


