from shiny import ui

mathjax_script = ui.tags.script(
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
)

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h4("Model Parameters"),
        ui.input_slider("R0", "Initial Radius (R0)", min=0.1, max=5, value=1.0, step=0.1),
        ui.input_slider("mu", "Expansion Parameter (mu)", min=-4, max=5, value=5.0, step=0.25),
        # ui.input_slider("alpha_u", "Death Rate (alpha_u)", min=0.0, max=0.99, value=0.0, step=0.05),
        # ui.input_switch("type_model","Include 1/mu", value = False),
        # ui.input_select("immune_response_select","Immune Response", {"1":"v = 1 always", "2": "v = 1 - e^-r"}),
        ui.input_select("model","Select a model:", choices=["Continuous at Boundary", "Shock at Boundary"]),
        ui.input_switch("largeR", "Large R0 (overrides Initial Radius slider)", value = False),
        ui.input_slider("nplots", "Number of time steps", min=5, max=20, value=5, step=5)
    ),
    
    ui.head_content(mathjax_script),
    
    ui.card(
        ui.h2("Fisher-Stefan Tumor Simulation"),      
        ui.markdown(""), 
        ui.output_plot("sim_plot", width="100%", height="500px")
    )
)