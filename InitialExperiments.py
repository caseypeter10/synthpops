import synthpops as sp

sp.validate()

datadir = r'C:\Users\casey\Desktop\source\synthpops\data' # this should be where your demographics data folder resides

location = 'seattle_metro'
state_location = 'Washington'
country_location = 'usa'
sheet_name = 'United States of America'
level = 'county'

npop = 10000 # how many people in your population
#sp.generate_synthetic_population_with_workplace_industries(npop,datadir,location=location,
#                                 state_location=state_location,country_location=country_location,
#                                 sheet_name=sheet_name, level=level, )
#
"""
Simple workplace construction - low data input
"""

age_brackets = spdata.get_census_age_brackets(datadir, state_location, country_location)
age_by_brackets_dic = get_age_by_brackets_dic(age_brackets)
num_agebrackets = len(age_brackets)
contact_matrix_dic = spdata.get_contact_matrix_dic(datadir,sheet_name)


household_size_distr = spdata.get_household_size_distr(datadir,location,state_location,country_location)

#N homes provided by user
hh_sizes = generate_household_sizes(Nhomes, household_size_distr)

#Generating heads of households
hha_brackets = spdata.get_head_age_brackets(datadir, country_location=country_location, use_default=use_default)
hha_by_size = spdata.get_head_age_by_size_distr(datadir, country_location=country_location, use_default=use_default)

#Creating homes
homes_dic, homes = generate_all_households(n, hh_sizes, hha_by_size, hha_brackets, age_brackets, age_by_brackets_dic,
                                           contact_matrix_dic, deepcopy(syn_age_distr))
homes_by_uids, age_by_uid_dic = assign_uids_by_homes(homes)


#Setting Up Schools
school_sizes_count_by_brackets = spdata.get_school_size_distr_by_brackets(datadir, location=location, state_location=state_location,
                                                                          country_location=country_location, counts_available=school_enrollment_counts_available,
                                                                          use_default=use_default)

school_size_brackets = spdata.get_school_size_brackets(datadir, location=location, state_location=state_location,
                                                       country_location=country_location, use_default=use_default)

# Figure out who's going to school as a student with enrollment rates (gets called inside sp.get_uids_in_school)
uids_in_school, uids_in_school_by_age, ages_in_school_count = get_uids_in_school(datadir, n, location, state_location, country_location, age_by_uid_dic, homes_by_uids, use_default=use_default)  # this will call in school enrollment rates

# Get school sizes
gen_school_sizes = generate_school_sizes(school_sizes_count_by_brackets, school_size_brackets, uids_in_school)

# Assign students to school
gen_schools, gen_school_uids = send_students_to_school(gen_school_sizes, uids_in_school, uids_in_school_by_age, ages_in_school_count, age_brackets, age_by_brackets_dic, contact_matrix_dic, verbose)

# Get employment rates
employment_rates = spdata.get_employment_rates(datadir, location=location, state_location=state_location, country_location=country_location, use_default=use_default)

# Find people who can be workers (removing everyone who is currently a student)
potential_worker_uids, potential_worker_uids_by_age, potential_worker_ages_left_count = get_uids_potential_workers(gen_school_uids, employment_rates, age_by_uid_dic)
workers_by_age_to_assign_count = get_workers_by_age_to_assign(employment_rates, potential_worker_ages_left_count, uids_by_age_dic)

# Assign teachers and update school lists
gen_schools, gen_school_uids, potential_worker_uids, potential_worker_uids_by_age, workers_by_age_to_assign_count = assign_teachers_to_work(gen_schools, gen_school_uids, employment_rates, workers_by_age_to_assign_count, potential_worker_uids, potential_worker_uids_by_age, potential_worker_ages_left_count, verbose=verbose)




#Setting up workplaces
workplace_size_brackets = spdata.get_workplace_size_brackets(datadir, state_location=state_location,
                                                             country_location=country_location, use_default=use_default)

workplace_size_distr_by_brackets = spdata.get_workplace_size_distr_by_brackets(datadir, state_location=state_location,
                                                                               country_location=country_location,
                                                                               use_default=use_default)

workplace_sizes = generate_workplace_sizes(workplace_size_distr_by_brackets, workplace_size_brackets, workers_by_age_to_assign_count)


# Assign all workers who are not staff at schools to workplaces
gen_workplaces, gen_workplace_uids, potential_worker_uids, potential_worker_uids_by_age, workers_by_age_to_assign_count = assign_rest_of_workers(workplace_sizes, potential_worker_uids, potential_worker_uids_by_age, workers_by_age_to_assign_count, age_by_uid_dic, age_brackets, age_by_brackets_dic, contact_matrix_dic, verbose=verbose)

workers_placed_by_age_count = dict.fromkeys(np.arange(0, 101), 0)
for w in gen_workplaces:
    for a in w:
        workers_placed_by_age_count[a] += 1


#Handling outputs
# save schools and workplace uids to file



if write:
    write_homes_by_age_and_uid(datadir, location, state_location, country_location, homes_by_uids, age_by_uid_dic)
    write_schools_by_age_and_uid(datadir, location, state_location, country_location, n, gen_school_uids, age_by_uid_dic)
    write_workplaces_by_age_and_uid(datadir, location, state_location, country_location, n, gen_workplace_uids, age_by_uid_dic)

if return_popdict:
    #this population dictionary carries all contacts on the person object in multiple layers (work, school, home
    popdict = spct.make_contacts_from_microstructure_objects(age_by_uid_dic, homes_by_uids, gen_school_uids, gen_workplace_uids)
    return popdict

