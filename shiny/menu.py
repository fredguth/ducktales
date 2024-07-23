import urllib.request
from pathlib import Path
from typing import List, Optional
from shiny import App, Inputs, Outputs, Session, reactive, render, ui, module

# ============================================================
# toggleButtons module
# ============================================================

@module.ui
def toggleButtons_ui() -> ui.TagChild:
    return ui.output_ui("menu")
    

@module.server
def toggleButtons_server(input: Inputs, output: Outputs, session: Session, choices: List[str], selected=None):
    selected = selected or reactive.value("")
    @render.ui
    def menu():
        buttons = []
        for choice in choices:
            klass = "btn-secondary" if (selected and (selected() == choice)) else "btn-outline-secondary"
            buttons.append(ui.input_action_button(f"menubtn_{choices.index(choice)}", f"{choice}", class_=klass))
        return ui.div(*buttons, class_="d-grid gap-2")

    
    def create_choice_listener(choice, index):
        @reactive.effect
        @reactive.event(getattr(input, f"menubtn_{index}"))
        def listener(): selected.set(choice)
        return listener
    
    for choice in choices:
        create_choice_listener(choice, choices.index(choice))