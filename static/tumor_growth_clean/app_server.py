from shiny import render, reactive
import numpy as np
import matplotlib.pyplot as plt

from solver_withImmuneResponse import solve_fisher_stefan

def server(input, output, session):

    @reactive.calc
    def solve_model():
        R0 = input.R0()
        mu = input.mu()
        alpha_u = 0#input.alpha_u()
        type_model = 0#input.type_model()
        model = input.model()
        immune_response_select = 0#int(input.immune_response_select())
        largeR = input.largeR()
        nplots = input.nplots()
        sol, y = solve_fisher_stefan(R0, mu, alpha_u,type_model, immune_response_select, model,largeR)
        
        return sol, y, alpha_u, nplots

    @render.plot
    def sim_plot():
        sol, y, alpha_u, nplots = solve_model()

        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        # Plot 1: Spreading Density Profiles
        for i in range(0, len(sol.t), nplots):  
            t_curr = sol.t[i]
            R_curr = sol.y[-1, i]
            U_curr = sol.y[:-1, i]
            axs[0].plot(y * R_curr, U_curr, label=f't = {t_curr:.1f}')

        axs[0].set_xlabel('Radius ($r$)')
        axs[0].set_ylabel('Concentration of Tumor Cells ($u$)')
        axs[0].set_title('Radial Density')
        axs[0].legend()
        axs[0].grid(True)

        # Plot 2: Boundary Expansion
        axs[1].plot(sol.t, sol.y[-1, :], color='crimson', linewidth=2)
        axs[1].set_xlabel('Time ($t$)')
        axs[1].set_ylabel('Tumor Radius ($R(t)$)')
        axs[1].set_title('Tumor Expansion')
        axs[1].grid(True)

        # Plot 3: Density at Origin
        u_origin = sol.y[0, :]
        axs[2].plot(sol.t, u_origin, color='indigo', linewidth=2.5)

        axs[2].set_xlabel('Time ($t$)')
        axs[2].set_ylabel('Density ($u$)')
        axs[2].set_title('Density at $r = 0$')
        # axs[2].legend()
        axs[2].grid(True)

        fig.tight_layout()
        return fig