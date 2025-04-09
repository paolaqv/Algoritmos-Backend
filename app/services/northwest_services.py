from pulp import LpProblem, LpMinimize, LpMaximize, lpSum, LpVariable, LpStatus, value
from flask import jsonify

def solve_transportation_problem(data, maximize=False):
    try:
        origins = data["Origins"]
        targets = data["Targets"]
        supply = data["supply"]
        demand = data["demand"]
        costs = data["costs"]

        # Crear el problema de optimización
        prob = LpProblem("Transportation Problem", LpMaximize if maximize else LpMinimize)

        # Variables de decisión
        route_vars = LpVariable.dicts("Route", (origins, targets), lowBound=0, cat='Integer')

        # Función objetivo
        prob += lpSum([
            route_vars[o][t] * costs[origins.index(o)][targets.index(t)]
            for o in origins for t in targets
        ]), "Total Cost"

        # Restricciones de oferta
        for o in origins:
            prob += lpSum([route_vars[o][t] for t in targets]) <= supply[o], f"Supply_{o}"

        # Restricciones de demanda
        for t in targets:
            prob += lpSum([route_vars[o][t] for o in origins]) >= demand[t], f"Demand_{t}"

        # Resolver
        prob.solve()

        return {
            "status": LpStatus[prob.status],
            "objective": value(prob.objective),
            "solution": {
                o: {t: route_vars[o][t].varValue for t in targets}
                for o in origins
            },
            "origins": origins,
            "targets": targets
        }

    except Exception as e:
        return {"error": str(e)}
