# ----------------------
# Filename: cleaning.py
# Author: Anu R
# Created: May 2020
# Python version: 3.7
# ----------------------

import pandas as pd
import numpy as np

# Import raw csv of nypd data + format date-based columns to YYYY-MM-DD
nypd_date_cols = ['CMPLNT_TO_DT', 'CMPLNT_FR_DT', 'RPT_DT']
df = pd.read_csv('NYPD_Complaint_Data_Historic.csv')
df = df.copy()

# Filter chronologically correct dates
#   e.g. report date should be same-day/after first instance of the exact date of/starting date of occurrence
df = df[(df['CMPLNT_FR_DT'] <= df['CMPLNT_TO_DT']) & (df['CMPLNT_TO_DT'] <= df['RPT_DT'])]

# Drop rows missing borough data
df.loc[:, 'BORO_NM'].replace(' ', np.nan, inplace=True)
df.dropna(subset=['BORO_NM'], inplace=True)

# Select relevant strings to classify common offenses
# I determine frequencies for "common" offenses i.e. focus on categories w/ >200 instances
crime_freq = pd.crosstab(index=df['OFNS_DESC'], columns='OFNS_COUNT').sort_values(by='OFNS_COUNT', ascending=True)

admin_rpts = ['MISCELLANEOUS PENAL LAW', 'OFF. AGNST PUB ORD SENSBLTY &', 'OFFENSES AGAINST PUBLIC ADMINI']

fraud_rpts = ['FORGERY', 'FRAUDS', 'OFFENSES INVOLVING FRAUD']

sex_rpts = ['RAPE', 'SEX CRIMES', 'HARRASSMENT 2']

theft_rpts = ['PETIT LARCENY', 'CRIMINAL MISCHIEF & RELATED OF',
              'GRAND LARCENY', 'BURGLARY', 'THEFT-FRAUD']

transport_rpts = ['GRAND LARCENY OF MOTOR VEHICLE', 'UNAUTHORIZED USE OF A VEHICLE']

violence_rpts = ['ASSAULT 3 & RELATED OFFENSES', 'FELONY ASSAULT']

crime_rpts = [admin_rpts, fraud_rpts, sex_rpts, theft_rpts, transport_rpts, violence_rpts]
ofns_cats = ['ADMINISTRATIVE', 'FRAUD', 'SEX', 'THEFT', 'TRANSPORT', 'VIOLENCE']

# Reassign with bucketed offense categories
for i in range(0, len(crime_rpts)):
    df['OFNS_DESC'] = df['OFNS_DESC'].apply(lambda x: ofns_cats[i] if x in crime_rpts[i] else x)

# Filter df to keep categorised offenses
df = df[df['OFNS_DESC'].isin(ofns_cats)]

# Select relevant strings to classify common locations
#   For blank/unknown premise descriptions, I classify these under 'OTHER'. I am keeping these
#   observations since not all crimes occur at a physical location e.g. larceny
df.loc[:, ['PREM_TYP_DESC']].replace(' ', np.nan, inplace=True)

comm_loc = ['BAR/NIGHT CLUB', 'COMMERCIAL BUILDING', 'PUBLIC BUILDING', 'BANK', 'GYM/FITNESS FACILITY',
            'LOAN COMPANY', 'HOSPITAL', 'DOCTOR/DENTIST OFFICE', 'HOTEL/MOTEL', 'GAS STATION',
            'FACTORY/WAREHOUSE', 'RESTAURANT/DINER', 'FAST FOOD', 'CHAIN STORE', 'DEPARTMENT STORE',
            'CLOTHING/BOUTIQUE', 'GROCERY/BODEGA', 'CANDY STORE', 'FOOD SUPERMARKET', 'STORE UNCLASSIFIED',
            'DRUG STORE', 'SMALL MERCHANT', 'DRY CLEANER/LAUNDRY', 'BEAUTY & NAIL SALON', 'VARIETY STORE',
            'CHECK CASHING BUSINESS', 'TELECOMM. STORE', 'SHOE', 'LIQUOR STORE', 'JEWELRY', 'BOOK/CARD',
            'VIDEO STORE', 'PHOTO/COPY']

other_loc = ['OTHER', 'ATM', 'ABANDONED BUILDING', 'CHURCH', 'MOSQUE', 'SYNAGOGUE',
             'OTHER HOUSE OF WORSHIP', 'SOCIAL CLUB/POLICY', 'MAILBOX INSIDE',
             'STORAGE FACILITY', 'CONSTRUCTION SITE', 'HOMELESS SHELTER', 'HOSPITAL', np.nan]

public_loc = ['PARKING LOT/GARAGE (PUBLIC)', 'MAILBOX OUTSIDE', 'PARK/PLAYGROUND', 'STREET', 'HIGHWAY/PARKWAY',
              'BRIDGE', 'OPEN AREAS (OPEN LOTS)', 'TUNNEL', 'CEMETERY', 'PARKING LOT/GARAGE (PRIVATE)']

res_loc = ['RESIDENCE - APT. HOUSE', 'RESIDENCE-HOUSE', 'RESIDENCE - PUBLIC HOUSING']

school_loc = ['PUBLIC SCHOOL', 'PRIVATE/PAROCHIAL SCHOOL']

transit_loc = ['TRANSIT - NYC SUBWAY',	'BUS (NYC TRANSIT)', 'TAXI (LIVERY LICENSED)',	'AIRPORT TERMINAL',
               'BUS (OTHER)',	'BUS TERMINAL',	'TAXI (YELLOW LICENSED)', 'BUS STOP', 'TAXI/LIVERY (UNLICENSED)',
               'TRANSIT FACILITY (OTHER)',	'FERRY/FERRY TERMINAL',	'MARINA/PIER',	'TRAMWAY']

crime_locs = [comm_loc, other_loc, public_loc, res_loc, school_loc, transit_loc]
loc_cats = ['COMMERCIAL', 'OTHER', 'PUBLIC', 'RESIDENTIAL', 'SCHOOL', 'TRANSIT']

# Reassign with bucketed crime locations
for i in range(0, len(crime_locs)):
    df['PREM_TYP_DESC'] = df['PREM_TYP_DESC'].apply(lambda x: loc_cats[i] if x in crime_locs[i] else x)

# Filter df to keep categorised offenses
df = df[df['PREM_TYP_DESC'].isin(loc_cats)]

# Export cleaned df to csv
df.to_csv('NYPD_Complaint_Data_Historic_Clean.csv', header=True, index=False)
