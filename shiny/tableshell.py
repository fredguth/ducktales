import urllib.request
from pathlib import Path
from typing import List, Optional
from shiny import App, Inputs, Outputs, Session, reactive, render, ui, module

import duckdb
from explorer import explorer_ui, explorer_server
    
    


# ============================================================
# tableShell module
# ============================================================

app_dir = Path(__file__).parent
db_file = app_dir / "local.db"
db = duckdb.connect(str(db_file), read_only=True)
db.install_extension('httpfs')
db.load_extension('httpfs')

@module.ui
def tableShell_ui() -> ui.TagChild: return ui.output_ui("shell")
    

@module.server
def tableShell_server(input, output, session, selected=None):
    selected = selected or reactive.value("")
    explorer_server("explorer", con=db, remove_id="initial_query")
    
    @render.ui
    def shell():        
        t = f"Table: {selected()}"
        download_panel = ui.nav_panel("Download", "Download panel content")
        explore_panel =  explorer_ui(id="explorer", qry = "SELECT * from trips LIMIT 10", remove_id="initial_query")
        panels = ["API", None, None, "Documentation", "Lineage", "Quality", "Metadata", None, None, None, None, None]
        children = [download_panel, explore_panel] + [ui.nav_panel(c, f"Panel {c} content") if c else ui.nav_spacer() for c in panels]
        sb = ui.sidebar("tbl_sb", open="closed", title=t, position="right")
        return ui.navset_card_underline(id="tbl_card", selected="Explore", sidebar=sb, title=t, *children)

        
        
          
                
        
        
        
