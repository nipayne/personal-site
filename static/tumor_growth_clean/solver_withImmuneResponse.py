import numpy as np
from scipy.integrate import solve_ivp
import math

def solve_fisher_stefan(R0, mu, alpha_u, type_model, immune_response_select, model,largeR):
    # Spatial Grid Setup
    d =2
    N = 150
    rho = np.linspace(0, 1, N)
    drho = rho[1] - rho[0]
    if largeR:
        R0 = 100
            

    def pde_model(t, state):
        U = state[:N]
        #V = state[N+1:2*N]
        R = state[-1]

        if immune_response_select == 1:
            immune_response = U
        else:
            immune_response = (1 - (math.e)**(-rho))
        # Stefan condition        
        

        match model:
            case 'Continuous at Boundary':
                dRdt = -(mu / R) * ((-4*U[-2] + U[-3]) / (2 * drho))   
            case 'Shock at Boundary':
                dRdt = -(mu / R) * ((3*(1/mu) - 4*U[-2] + U[-3]) / (2 * drho))   
        # dRdt = -(mu / R) * ((-4*U[-2] + U[-3]) / (2 * drho))        # Time derivatives
        dUdt = np.zeros(N)

        # Origin BCs using l'Hopital's
        dUdt[0] = (4/((R*drho)**2))*(U[1] - U[0]) + U[0]*(1-U[0])


        dUdt[1:-1] = ((1/(R*drho)**2)*(U[2:] - 2*U[1:-1]+ U[:-2])) \
                    + ((1/(2*drho*rho[1:-1]*(R**2)))*(U[2:] - U[:-2]))\
                    + ((rho[1:-1]/(2*R*drho))*dRdt*(U[2:] - U[:-2]))\
                    + (U[1:-1]*(1 - U[1:-1]))
        
        
        match model:
            case 'Continuous at Boundary':
                dUdt[-1] = 0.0
            case 'Shock at Boundary':
                dUdt[-1] = ((1/(R*drho)**2)*(2/mu+ U[-2])) \
                    + ((1/(2*drho*rho[-1]*(R**2)))*(- U[-2]))\
                    + ((rho[-1]/(2*R*drho))*dRdt*(- U[-2]))\
                    + ((1 - 1/mu)/mu)            
             
        

       
        return np.append(dUdt, dRdt)

    # Initial Conditions
    
    U0 = 1*np.ones(N)
    match model:
            case 'Continuous at Boundary':
                U0[-1] = 0 
            case 'Shock at Boundary':
                U0[-1] = 1/mu
    
    # print(U0)
    state_0 = np.append(U0, R0)

    t_span = (0, 30)
    t_eval = np.linspace(t_span[0], t_span[1], 150)

    # Solve the system
    sol = solve_ivp(pde_model, t_span, state_0, t_eval=t_eval, method='BDF',rtol=1e-8, atol=1e-8)
    
    return sol, rho