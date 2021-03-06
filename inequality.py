import math
import pandas as pd
from InquirerPy import prompt

dataset_filename = "WID_data_PH.csv"

questions = [
    {
        "type": "list",
        "name": "country",
        "message": "Which country would you like to analyze?",
        "choices": ["The Philippines"],
    },
    {
        "type": "list",
        "name": "year",
        "message": "Please select a year:",
        "choices": ["2000","2003", "2006", "2009", "2012", "2015", "2018"],
    },
    {
        "type": "list",
        "name": "measurement",
        "message": "Please select an inequality measurement:",
        "choices": ["Income", "Wealth"],
    },
]
result = prompt(questions)

class PopulationSubset:
    def __init__(self, pct_population, pct_income, pct_richer):
        self.pct_population = pct_population
        self.pct_income = pct_income
        self.pct_richer = pct_richer

def get_data(inquiry):
    year = int(inquiry["year"])
    measurement = "thweal992j" if inquiry["measurement"]=="Wealth" else "tptinc992j"
    data = []
    df = pd.read_csv(
        dataset_filename, 
        index_col=None,
        sep=";",
        usecols=[1,2,3,4],
    )
    subset = df.loc[(df["year"] == year) & (df["variable"]==measurement)]
    for n in range(0, len(subset)):
        percentile = "p" + str(n) + "p100"
        record = subset["value"].loc[subset["percentile"]==percentile].values.tolist()
        if(record):
            data.append(record[0])
    return data

def get_population_characteristics(arr):
    population_arr = []
    total_income = sum(arr)
    for i, n in enumerate(arr):
        pct_pop = (100/len(arr))/100
        pct_inc = n/total_income
        pct_richer = (i+1)*pct_pop
        population_arr.append(PopulationSubset(pct_pop, pct_inc, pct_richer))
    return population_arr
    
def display_population_characteristics(data_set):
    print("Inequality data for", data_set.country, "for the year", data_set.year)
    print("---------------------------------------------")
    print("The log variance of this distribution is:", round(data_set.income_log_variance,2))
    print("The relative mean deviation is:", round(data_set.income_mean_deviation,2))
    print("The related gini coefficient is:", round(data_set.gini,1))
    print("The thiel T index is:", round(data_set.theil_t,2))
    print("The thiel L index is:", round(data_set.theil_l,2))
    print()

def export_population_characteristics(data_set):
    population_arr = get_population_characteristics(data_set.income_arr)
    pct_pop_arr = []
    pct_income_arr = []
    for i, n in enumerate(population_arr):
        idx = i+1
        ordinal = "th"
        if idx == 1:
            ordinal = "st"
        pct_pop_arr.append(str(idx) + str(ordinal))
        pct_income_arr.append(round(n.pct_income*100, 2))
    data = pd.DataFrame({
        "Population Percentile": pct_pop_arr,
        "Income Share": pct_income_arr
    })
    data.to_excel('inequality_data.xlsx', sheet_name='sheet1', index=False)

def get_mean(arr):
    return sum(arr)/len(arr)

def get_log_variance(arr):
    mean = get_mean(arr)
    log_arr = []
    for n in arr:
        n = abs(n)
        if n == 0:
            log_arr.append(0)
        else:
            log_arr.append(math.pow(math.log(n/mean), 2))
    return sum(log_arr)/len(arr)
    
def get_relative_mean_deviation(arr):
    mean = get_mean(arr)
    diff_arr = []
    for n in arr:
        diff_arr.append(abs(n - mean))
    return (sum(diff_arr)/len(diff_arr))/mean
    
def get_gini(arr):
    population_arr = get_population_characteristics(arr)
    score_arr = []
    for n in population_arr:
        score_arr.append(n.pct_income*(n.pct_population+2*(1-n.pct_richer)))
    return (1-sum(score_arr))*100
    
def get_theil_t(arr):
    mean = get_mean(arr)
    theil = 0
    for n in arr:
        if n > 0:
            theil += (n/mean)*math.log(n/mean)
    return (theil/len(arr))*100
   
def get_theil_l(arr):
    mean = get_mean(arr)
    theil = 0
    for n in arr:
        if n > 0:
            theil += math.log(mean/n)
    return (theil/len(arr))*100

class DataSet:
    def __init__(self, country, year, income_arr):
        self.country = country
        self.year = year
        self.income_arr = income_arr
        self.income_log_variance = get_log_variance(income_arr)
        self.income_mean_deviation = get_relative_mean_deviation(income_arr)
        self.gini = get_gini(income_arr)
        self.theil_t = get_theil_t(income_arr)
        self.theil_l = get_theil_l(income_arr)

data_set = DataSet(
    result["country"],
    result["year"],
    get_data(result)
)

display_population_characteristics(data_set)

questions = [
    {
        "type": "confirm",
        "name": "answer",
        "message": "Would you like to export the results?",
    },
]
result = prompt(questions)

if(result["answer"]):
    export_population_characteristics(data_set)
    print("Results exported as inequality_data.xslx")