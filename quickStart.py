import synthpops as sp


datadir = r'C:\Users\Peter\Desktop\Source\synthPops\synthpops\data' # this should be where your demographics data folder resides

location = 'seattle_metro'
state_location = 'Washington'
country_location = 'usa'
sheet_name = 'United States of America'
level = 'county'



npop = 5000 # how many people in your population




#Generating household sizes

#Household Size Distribution

houseSizeDict = {1:.05 , 2:.10 , 3:.10 , 4:.20 , 5:.20, 6:.10, 7:.10 , 8:.075 , 9: .075}

householdSizes = contact_networks.generate_household_sizes(50,houseSizeDict)

print("householdSizes: "+ str(householdSizes))