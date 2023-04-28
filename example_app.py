#!/usr/bin/env python3
#
# Copyright (c) 2022, Michael Shafae
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
#

"""Example of how to use us_state.pckl and ca_county.pckl pickle files."""

from collections import namedtuple
import pickle
import locale

State = namedtuple(
    'State',
    [
        'name',
        'area_sq_mi',
        'land_area_sq_mi',
        'water_area_sq_mi',
        'population',
        'n_rep_votes',
        'n_senate_votes',
        'n_ec_votes',
    ],
)

CACounty = namedtuple(
    'CACounty', ['name', 'county_seat', 'population', 'area_sq_mi']
)


def _str(item):
    """Handy function to return the named field name of a state or county."""
    return f'{item.name}'


State.__str__ = _str
CACounty.__str__ = _str


def main():
    """Main function"""
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    with open('ca_county.pckl', 'rb') as file_handle:
        ca_counties = pickle.load(file_handle)

    with open('us_state.pckl', 'rb') as file_handle:
        states = pickle.load(file_handle)

    states.sort(key=lambda x: x.area_sq_mi)
    print(
        f'The largest state or territory by area is {states[-1]} ' \
        f'and the smallest one is {states[0]}.'
    )

    ca_counties.sort(key=lambda x: x.area_sq_mi)
    print(
        f'The largest CA county by area is {ca_counties[-1]}'
        f' and the smallest one is {ca_counties[0]}.'
    )

    total_us_population = sum([s.population for s in states])
    print(f'The total US population is {total_us_population:n}.')
    # territories_only = [s for s in states if s.n_ec_votes == 0]
    states_only = [s for s in states if s.n_ec_votes > 0]
    total_states_only_population = sum([s.population for s in states_only])
    print(
        f'The total US population from states is {total_states_only_population:n}.'
    )
    print(
        'This means that there are '
        f'{total_us_population - total_states_only_population:n} people'
        ' who live in US territories.'
    )
    total_ec_votes = sum([s.n_ec_votes for s in states])
    print(f'The total number of Electoral College votes is {total_ec_votes}.')

    total_ca_population = sum([c.population for c in ca_counties])
    print(f'The total population of California is {total_ca_population:n}.')
    print(
        'California is '
        f'{(total_ca_population / total_us_population) * 100:.2f}% of '
        ' the US total population.'
    )
    ca_counties.sort(key=lambda x: x.population, reverse=True)
    n_counties = 3
    ca_population_largest_counties = sum(
        [c.population for c in ca_counties[:n_counties]]
    )
    county_names = ', '.join(map(str, ca_counties[:n_counties]))
    print(
        f'The population of the largest {n_counties} counties '
        f'({county_names}) in CA is {ca_population_largest_counties:n} '
        'which is '
        f'{(ca_population_largest_counties / total_ca_population) * 100:.2f}%'
        ' of CA total population or '
        f'{(ca_population_largest_counties / total_us_population) * 100:.2f}%'
        ' of the US population.'
    )
    
    print('\n\n\n\n')
    print('-----Quiz 8-----')
    # 1. Given the sum of the population from the third, fourth
    # and fifth most populated counties in CA, how many US states
    # have a population less than the sum of these three counties?
    ca_counties.sort(key=lambda x: x.population, reverse=True)
    counties_pop_one = ca_counties[2].population + ca_counties[3].population + ca_counties[4].population
    one_solution = 0
    for s in states_only:
        if s.population < counties_pop_one:
            one_solution += 1
    
    print(f'1. {one_solution}')



    # 2. Find the county in CA that has the largest area.
    # How many US states have a land area <= to this county?
    ca_counties.sort(key=lambda x: x.area_sq_mi)
    num_states_two = 0
    for s in states_only:
        if s.land_area_sq_mi <= ca_counties[-1].area_sq_mi:
            num_states_two += 1

    print(f'2. {num_states_two}')

    # 3. Make a list of states from least to most populated 
    # where their combined population is no less than 37,956,694
    # and no greater than 41,119,752.
    # 
    # Once you have this list, sum up the total number of Electoral College
    # votes these states have in total. Call this ec_sum.
    # 
    # What is the difference between ec_sum and the number of
    # Electoral College votes CA has? 
    # In other words: ec_sum - california.n_ec_votes
    states_only.sort(key=lambda x: x.population)
    three_min_bound = 0
    three_min_index = 0
    three_upper_bound = 0
    three_upper_index = 0
    for s in states_only:
        if three_min_bound >= 37956694 and three_min_bound <= 41119752:
            break
        three_min_bound += s.population
        three_min_index += 1

    three_upper_bound += three_min_bound
    for s in states_only:
        if three_upper_bound >= 41119752:
            break
        three_upper_bound += s.population
        three_upper_index += 1

    print(f'3. three_upper_index = {three_upper_index}, with pop: {three_min_bound}')
    print(f'three_min_index = {three_min_index}')


if __name__ == '__main__':
    main()
