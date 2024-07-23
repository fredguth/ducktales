
import urllib.request
import duckdb
from shiny import module, reactive, render, ui


@module.ui
# def query_output_ui(remove_id, qry=f"from read_parquet('https://blobs.duckdb.org/data/yellow_tripdata_2010-01.parquet') limit 10"):
# 'https://blobs.duckdb.org/databases/stations.duckdb'
def query_output_ui(remove_id, qry=f"from trips limit 10"):
    return (
        ui.card(
            {"id": remove_id},
            ui.card_header(f"{remove_id}"),
            ui.layout_columns(
                
                    ui.input_text_area(
                        "sql_query",
                        "",
                        value=qry,
                        width="100%",
                        height="200px",
                    ),
                [
                        ui.input_action_button("run", "Run", class_="btn btn-primary"),
                        ui.input_action_button(
                            "rmv", "Remove", class_="btn btn-secondary"
                        ),
                 
                ],
                col_widths={"xl": [9, 3], "lg": [8, 3], "md": [6, 3], "sm": [12, 3]},
            ),
            ui.output_ui("results"),
            
        ),
    )


@module.server
def query_output_server(
    input, output, session, con: duckdb.DuckDBPyConnection, remove_id
):
    @render.data_frame
    @reactive.event(input.run)
    def results():
        # qry = input.sql_query()
        # .replace("\n", " ")
        # return render.DataGrid(con.query(qry).to_df())
        return con.sql(input.sql_query()).df()
    
    @reactive.effect
    @reactive.event(input.rmv)
    def _():
        ui.remove_ui(selector=f"div#{remove_id}")
