import pandas as pd
import numpy as np
from faker import Faker
import random 
# object from faker class to create fake data
fake = Faker()
random.seed(42)
np.random.seed(42)

# PROPERTIES
property_ids = [f"P{str(i).zfill(3)}" for i in range(1, 11)]
states = ["PA", "FL", "TX", "GA", "NC", "TN", "CO", "AZ", "MO", "IN"]
cities = [fake.city() for _ in property_ids]
property_info = pd.DataFrame({
    "Property_ID": property_ids,
    "Property_Name": [fake.company() for _ in property_ids],
    "Location": [f"{city}, {state}" for city, state in zip(cities, states)],
    "Units": np.random.randint(50, 300, size=10),
    "Year_Built": np.random.randint(1970, 2020, size=10)
})
property_info.to_csv("property_info.csv", index=False)

# RENT ROLL - for each unit of each property
unit_data = []
for prop in property_ids:
    num_units = property_info[property_info["Property_ID"] == prop]["Units"].values[0]
    for unit_num in range(1, num_units + 1):
        lease_start = fake.date_between(start_date='-2y', end_date='-1y')
        lease_end = fake.date_between(start_date='today', end_date='+1y')
        rent = np.random.randint(800, 2500)
        concession = np.random.choice([0, 50, 100], p=[0.7, 0.2, 0.1])
        occupied = np.random.choice(["Occupied", "Vacant"], p=[0.85, 0.15])
        unit_data.append([prop, f"U{unit_num}", lease_start, lease_end, rent, concession, occupied])

rent_roll = pd.DataFrame(unit_data, columns=[
    "Property_ID", "Unit_ID", "Lease_Start", "Lease_End", "Rent", "Concession", "Occupancy_Status"
])
rent_roll.to_csv("rent_roll.csv", index=False)

# EXPENSES 
expense_types = ["Repairs", "Marketing", "Taxes", "Utilities", "Landscaping", "Insurance"]
expenses_data = []

for prop in property_ids:
    # for each property create 10-20 fake expense reports 
    for _ in range(np.random.randint(10, 20)): # not using var in loop, can use _
        date = fake.date_between(start_date='-1y', end_date='today')
        expense_type = random.choice(expense_types)
        amount = round(np.random.uniform(500, 5000), 2)
        description = fake.sentence(nb_words=3)
        expenses_data.append([prop, date, expense_type, amount, description])

expenses = pd.DataFrame(expenses_data, columns=[
    "Property_ID", "Date", "Expense_Type", "Amount", "Description"
])
expenses.to_csv("expenses.csv", index=False)

# LEASING FUNNEL
lead_sources = ["Zillow", "Apartments.com", "Google Ads", "Referral", "Walk-in"]
leads_data = []

for i in range(1, 301):
    lead_id = f"L{str(i).zfill(4)}"
    prop = random.choice(property_ids)
    inquiry_date = fake.date_between(start_date='-6M', end_date='today')
    source = random.choice(lead_sources)
    toured = random.choices(["Yes", "No"], weights=[0.7, 0.3])[0]
    signed = "Yes" if toured == "Yes" and random.random() < 0.5 else "No"
    leads_data.append([lead_id, prop, inquiry_date, source, toured, signed])

leasing_funnel = pd.DataFrame(leads_data, columns=[
    "Lead_ID", "Property_ID", "Inquiry_Date", "Lead_Source", "Toured", "Lease_Signed"
])
leasing_funnel.to_csv("leasing_funnel.csv", index=False)

# MARKET COMPARABLES
property_city_map = dict(zip(property_ids, cities))
market_data = []

for city in set(property_city_map.values()):
    avg_rent = np.random.randint(1100, 2200)
    vacancy_rate = round(np.random.uniform(0.03, 0.1), 3)
    competitor_rent = avg_rent + np.random.randint(-100, 150)
    market_data.append([city, avg_rent, vacancy_rate, competitor_rent])

market_comps = pd.DataFrame(market_data, columns=[
    "City", "Average_Rent", "Vacancy_Rate", "Competitor_Rent"
])
market_comps.to_csv("market_comparables.csv", index=False)