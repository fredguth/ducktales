import duckdb
from shiny import module, reactive, render, ui
from itables.shiny import DT
from itables import options, show, init_notebook_mode

@module.ui
def explorer_ui(remove_id, qry = "SELECT * from trips LIMIT 10"): 
    
    query_area = ui.input_text_area("sql_query","", value = qry,width = "100%", height = "80px")
    return ui.nav_panel("Explore", { "id": remove_id },
    # return ui.page_fluid({ "id": remove_id },
        ui.row(ui.column(9,query_area), ui.column(3,ui.input_action_button("run", "Run", width="100%", class_ = "btn btn-secondary"))),
        ui.row(ui.output_ui("results")))

@module.server
def explorer_server(input, output, session, con: duckdb.DuckDBPyConnection, remove_id):
    
    # @render.data_frame
    @render.ui
    @reactive.event(input.run)
    def results():
        qry = input.sql_query()
        print(qry)
        df = con.sql(qry.replace("\n", " ")).df().reset_index(drop=True)
        return ui.HTML(DT(df))
