from shiny import App
from layout import app_ui
from app_server import server

app = App(app_ui, server)