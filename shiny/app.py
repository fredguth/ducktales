# import micropip
# await micropip.install("itables")
import urllib.request
from pathlib import Path
from typing import List, Optional
from shiny import App, Inputs, Outputs, Session, reactive, render, ui, module
from menu import toggleButtons_ui, toggleButtons_server
from tableshell import tableShell_ui, tableShell_server
# import duckdb 

# from htmltools import HTML,li, a



# =============================================================================
# App 
# =============================================================================

panels = [ui.accordion_panel(p, p) for p in ["Entradas/Saídas", "Reúsos", "Discussão"]]

# inout = ui.accordion_panel("Entradas/Saídas", toggleButtons_ui("menuInOut"))
tables = ui.accordion_panel("Tables", toggleButtons_ui("menuTables"))
metadata= ui.accordion_panel("Base Metadata","data meta")
accordion = ui.accordion(tables, metadata)


app_ui = ui.page_sidebar(

    ui.sidebar(  toggleButtons_ui("menuOverview"), accordion,  id="main_sb", open="open", title="br_ms.siops", position="left"),
    ui.output_ui("shell"),
    ui.tags.style(".bslib-sidebar-layout > .main { padding: 0px; padding-top: 0px;}"),
    ui.tags.style(".card { --bs-card-border-radius: 0px 0px 8px 0px}"),
)


def server(input, output, session):
    tables = ["Entes", "Receitas", "Despesas"]
    selected = reactive.value(tables[0])    
    # selected = reactive.value("Visão Geral")    
    toggleButtons_server("menuOverview", ["Overview"], selected)
    toggleButtons_server("menuTables", tables, selected)
    toggleButtons_server("menuInOut", ["In", "Out"], selected)
    tableShell_server(id="table_shell", selected=selected)
    
    @render.ui
    def shell():
        if selected and (selected() in tables): return tableShell_ui(id="table_shell")
        else: return ui.card(  
            ui.card_header(f"{selected()}"),
            ui.p("Card  body"),
            id="overview"
        ), 
        
    # @react.effect
    # @render.ui
    # def shell(id="shell"):
    #     return 
        # else: return "oi"
            # return ui.card(id="base_shell", title="Visão Geral")
    
app = App(app_ui, server)
