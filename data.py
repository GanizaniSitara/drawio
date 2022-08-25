# Architecture data file for a fictitious investment bank 
# Radley-Peters 
#
# In this example we're focusing primarily on risk processing systems and platforms, including pricing 
#
# 
# Credit Risk platforms
# Market Risk platforms both gods - Mars, Zeus, Hera - move to Roman
# Pricing - by asset class ... get from the book ... almost all asset classes have their own pricing systems whicha are sometimes legacy and in progress of being moved to newer platforms
# Market Data Generation
# Market Data Distribution
# Intraday Risk
# End of Day Risk
# Relgulatory Reporting
# Risk Aggregation
# Basel 3/4
#
#
# Many legacy platforms in different stage of being replaced, abandoned, or in maintenance mode
# Multiple straetgic programmes in various stage of completion, also unfinished
#
# Naming Convention - roman gods, geographical places (mountain ranges, highest mountaints), letters of alphabets (greek, hebrew), types of trees, nordic gods, birds of prey, big cats, unusual colour names, 
#
# Structure
#
# ## Macro ##
# FX Linear
# FX Options
# FX Swaps
# FX Hedged
# FX Hedged Options
# FX Hedged Swaps
# FX Hedged Hedged
# FX Hedged Hedged Options
# FX Hedged Hedged Swaps
# FX Variance
# FX Variance Options
# FX Variance Swaps
# FX Vanilla
# FX Vanilla Options
# FX Exotic
# Rates Linear
# Rates Options
# Macro TRS
# Rates Vanilla Options
# Structured Rates
# Structured Notes
# ## Financing ##
# Fixed Income Financing
# ## Credit ##
# Credit Default Swaps
# Bond Credit
# Futures
# Municipal Bonds
# Municipal Derivatives
# ## Securitized Products ##
# Securitized Products
# ## Equities ##
# EFS
# Non-US Flow
# US Flow
# Cash
# US Converts
# ## Commodities ##
# Commodities
# ## Commodity Futures ##
# Commodity Futures
# ## Commodity Options ##
# Commodity Options
# ## Prime Brokerage ##
# Prime Brokerage
# ## Derivatives ##
# Derivatives
# ## Cross Asset ##
# Credit Risk Trading / XVA

import csv
import pandas as pd

systems_loaded = []
df = None

def imported():
	global systems_loaded
	for system in systems:
		systems_loaded.append(System(system['name'], system['infra_size'], system['annualized_cost_in_thousands'], system['itsm_properties']['ResilienceCategory']))
		print(system)
	print("INFO: Loaded")
	# smallest go on top, largest get placed first
	systems_loaded.sort(key=lambda x: x.total_area, reverse=True)
	return True

class System:
	def __init__(self, name, infra_size, annualized_cost_in_thousands, itsm_resilience_category):
		self.name = name
		self.infra_size = infra_size
		self.annualized_cost_in_thousands = annualized_cost_in_thousands
		self.business_metrics = None
		self.business_metrics = {}
		self.business_metrics['NumberOfTradesProcessedDaily'] = None
		self.total_area = self.infra_size * self.annualized_cost_in_thousands
		self.itsm_resilience_category = itsm_resilience_category


	def __str__(self):
		return f"{self.name} {self.infra_size} {self.annualized_cost_in_thousands} \
{self.business_metrics['NumberOfTradesProcessedDaily']}"

	def set_name(self, name):
		self.name = name

	def set_infra_size(self, infra_size):
		self.infra_size = infra_size

	def set_annualized_cost_in_thousands(self, annualized_cost_in_thousands):
		self.annualized_cost_in_thousands = annualized_cost_in_thousands

	def set_business_metrics(self, business_metrics):
		self.business_metrics = business_metrics

	def set_business_metrics_NumberOfTradesProcessedDaily(self, NumberOfTradesProcessedDaily):
		self.business_metrics['NumberOfTradesProcessedDaily'] = NumberOfTradesProcessedDaily

	def get_name(self):
		return self.name

	def get_infra_size(self):
		return self.infra_size

	def get_annualized_cost_in_thousands(self):
		return self.annualized_cost_in_thousands

	def get_business_metrics(self):
		return self.business_metrics

	def get_business_metrics_NumberOfTradesProcessedDaily(self):
		return self.business_metrics['NumberOfTradesProcessedDaily']


systems = [
	{
		"name":"ABS Pricing",
		"class":"Desk Pricing",
		"description":"Front Office Pricing platfrom that only deals with Asset Backed Securities.",
		"notes":"ABS Pricing is regionally distributed with instances in APAC, EMEA and AMERS. Each regional implementation has subtle differences in how it is installed and what data it has available and which sub-types of trades it can price.",
		"id":0,
		"infra_size":2,
		"annualized_cost_in_thousands":4,
		"business_metrics":{"VaR":None,"RWA":None,"NumberOfTradesProcessedDaily":387000},
		"asset_classes":["ABS","MBS"],
		"organizational_metrics":{"AssociatedHeadcount":27,"KBArticles":880},	
		"capability":["On-demand Pricing"],
		"artchitectural_properties":{"Age":7,"Complexity":"Moderate"},
		"system_connections":[],
		"itsm_properties":{"ResilienceCategory": 2,"RTO":None,"RPO":None} # For IT Service Management
	},
	{
		"name":"Apollo",
		"class":"Credit Risk",
		"description":"Monte Carlo simulation engine for vanilla trades.",
		"notes":"Large infrastructure size and cost are driven by operating own valuation engines and own bespoke pricing model which is progress to being moved to the company standard library over the next 5 years",
		"id": 1,
		"infra_size":7, # in "servers" be it physical, virtual or charges container capacity
		"annualized_cost_in_thousands":15,
		"business_metrics":{"VaR_in_millions": None,"RWA_in_millions": None,"NumberOfTradesProcessedDaily":3500000},
		"asset_classes":["equities"],
		"organizational_metrics":{"AssociatedHeadcount":187,"KBArticles":4500},	
		"capability":["RWA generation","RWA aggregation","Monte Carlo simulation"],
		"artchitectural_properties":{"AgeInYears": 15,"Complexity":"High"}, #Low, Moderate, High
		"system_connections":["Market Data Distribution", "Market Risk", "Trade Feeds"],
		"itsm_properties":{"ResilienceCategory": 1,"RTO":None,"RPO":None} # For IT Service Management
	},
		{
		"name":"Trade DB",
		"class":"Trade Database",
		"description":"Trade Database providing data for every asset class except for Mortgage Backed Securities.",
		"notes":"Large RDBMS system prelviously unsuscessfuly migrated onto NoSQL solution, project which was abandoned. The the trade storage format makes special provision for trade feature which makes it hard to migrate.",
		"id": 2,
		"infra_size": 1 , # in "servers" be it physical, virtual or charges container capacity
		"annualized_cost_in_thousands":1,
		"business_metrics":{"VaR_in_millions": None,"RWA_in_millions": None,"NumberOfTradesProcessedDaily":10000000},
		"asset_classes":["<all>"],
		"organizational_metrics":{"AssociatedHeadcount":35,"KBArticles":2876},	
		"capability":["Trade Storage", "Trade Distribution"],
		"artchitectural_properties":{"AgeInYears": 25,"Complexity":"Moderate"}, #Low, Moderate, High
		"system_connections":["Trade Capture", "Trade Processing"],
		"itsm_properties":{"ResilienceCategory": 3,"RTO":None,"RPO":None} # For IT Service Management
	},
	{
		"name":"Thor",
		"class":"Equities Pricing",
		"description":"",
		"notes":"",
		"id": 3,
		"infra_size": 3 , # in "servers" be it physical, virtual or charges container capacity
		"annualized_cost_in_thousands":5,
		"business_metrics":{"VaR_in_millions": None,"RWA_in_millions": None,"NumberOfTradesProcessedDaily":10000000},
		"asset_classes":["<all>"],
		"organizational_metrics":{"AssociatedHeadcount":35,"KBArticles":2876},
		"capability":["Trade Storage", "Trade Distribution"],
		"artchitectural_properties":{"AgeInYears": 25,"Complexity":"Moderate"}, #Low, Moderate, High
		"system_connections":["Trade Capture", "Trade Processing"],
		"itsm_properties":{"ResilienceCategory": 2,"RTO":None,"RPO":None} # For IT Service Management
	},
	{
		"name": "Thor",
		"class": "Equities Pricing",
		"description": "",
		"notes": "",
		"id": 3,
		"infra_size": 1,  # in "servers" be it physical, virtual or charges container capacity
		"annualized_cost_in_thousands": 1,
		"business_metrics": {"VaR_in_millions": None, "RWA_in_millions": None,
							 "NumberOfTradesProcessedDaily": 10000000},
		"asset_classes": ["<all>"],
		"organizational_metrics": {"AssociatedHeadcount": 35, "KBArticles": 2876},
		"capability": ["Trade Storage", "Trade Distribution"],
		"artchitectural_properties": {"AgeInYears": 25, "Complexity": "Moderate"},  # Low, Moderate, High
		"system_connections": ["Trade Capture", "Trade Processing"],
		"itsm_properties": {"ResilienceCategory": 1, "RTO": None, "RPO": None}  # For IT Service Management
	},
]

def load_csv(file):
	global systems_loaded
	global df
	with open(file,"r") as f:
		reader = csv.reader(f)
		next(reader,None) # skip header
		for row in reader:
			systems_loaded.append(System(row[0], int(row[2]), int(row[3]), int(row[4])))
			print(systems_loaded[-1])
	print("INFO: Loaded")
	systems_loaded.sort(key=lambda x: x.total_area, reverse=True)
	df = pd.read_csv(file)
	print(df)
	return True

if __name__ == "__main__":
    pass
else:
	# imported()
	load_csv("data.csv")


