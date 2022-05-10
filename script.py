import numpy as np
from numpy.linalg import *




def user_input():
    print('Plane informations: \n')

    def throw_error():
        print('Enter only integer values')
        user_input()

    max_economy = input('Max economy: ')
    try:
        int(max_economy)
        max_business = input('Max business: ')
        try:
            int(max_business)
            max_first = input('Max first: ')
            try:
                int(max_first)
                max_cargo = input('Max cargo: ')
                try:
                    int(max_cargo)
                    print('\n Demand informations: \n')
                    economy_demand = input('Economy: ')
                    try:
                        int(economy_demand)
                        business_demand = input('Business: ')
                        try:
                            int(business_demand)
                            first_demand = input('First: ')
                            try:
                                int(first_demand)
                                cargo_demand = input('Cargo: ')
                                try:
                                    int(cargo_demand)
                                    compute_plans(max_economy=int(max_economy), max_business=int(max_business),
                                                  max_first=int(max_first), max_cargo=int(max_cargo),
                                                  economy_demand=int(economy_demand),
                                                  business_demand=int(business_demand), first_demand=int(first_demand),
                                                  cargo_demand=int(cargo_demand))
                                except ValueError:
                                    throw_error()
                            except ValueError:
                                throw_error()
                        except ValueError:
                            throw_error()
                    except ValueError:
                        throw_error()
                except ValueError:
                    throw_error()
            except ValueError:
                throw_error()
        except ValueError:
            throw_error()
    except ValueError:
        throw_error()



def compute_plans(max_economy: int, max_business: int, max_first: int, max_cargo: int,
                  economy_demand: int, business_demand: int, first_demand: int, cargo_demand: int):
    demand = np.array([
        [economy_demand, 0, 0, 0],
        [0, business_demand, 0, 0],
        [0, 0, first_demand, 0],
        [0, 0, 0, cargo_demand]
    ])
    capacity = [
        [max_economy, 0, 0, 0],
        [0, max_business, 0, 0],
        [0, 0, max_first, 0],
        [0, 0, 0, max_cargo]
    ]
    place_element = [[capacity[0][0]], [capacity[0][0]], [capacity[0][0]], [capacity[0][0]]]
    equivalence = solve(capacity, place_element)
    equivalent_demand = np.matmul(demand, equivalence)
    total_equivalent_demand = np.matmul(np.array([1, 1, 1, 1]), equivalent_demand)
    demand_capacity_ratio = total_equivalent_demand/place_element[0][0]
    eq_plans = equivalent_demand/demand_capacity_ratio
    final_plans = eq_plans/equivalence
    print('\n Plans have been computed: \n')
    print('Economy: ', final_plans[0][0])
    print('Business: ', final_plans[1][0])
    print('First: ', final_plans[2][0])
    print('Cargo: ', final_plans[3][0])


user_input()

