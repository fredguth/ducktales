import duckdb
from shiny import module, reactive, render, ui


@module.ui
def query_ui(remove_id, qry = "SELECT * from trips LIMIT 10"): 
    
    query_area = ui.input_text_area("sql_query","", value = qry,width = "100%", height = "100px")
    return ui.page_fluid({ "id": remove_id },
        ui.row(ui.column(8,query_area), ui.column(4,ui.input_action_button("run", "Run", width="100%", class_ = "btn btn-secondary"))),
        ui.row(ui.output_data_frame("results")))

@module.server
def query_server(input, output, session, con: duckdb.DuckDBPyConnection, remove_id):
    @render.data_frame
    @reactive.event(input.run)
    def results():
        qry = input.sql_query()
        return con.query(qry).df()
