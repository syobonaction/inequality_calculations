import math
import pandas as pd

class PopulationSubset:
    def __init__(self, pct_population, pct_income, pct_richer):
        self.pct_population = pct_population
        self.pct_income = pct_income
        self.pct_richer = pct_richer

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
    population_arr = get_population_characteristics(data_set.income_arr)
    print("Inequality data for", data_set.country, "for the year", data_set.year)
    print("---------------------------------------------")
    print("Dividing the population into ", len(data_set.income_arr), " percentiles:")
    for i, n in enumerate(population_arr):
        print("Percentile", i+1, "owns", round(n.pct_income*100,2), "percent of total income")
    print("--Measurements--")
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
    header = ("Inequality data for the", data_set.country, "for the year", data_set.year)
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
        theil += (n/mean)*math.log(n/mean)
    return (theil/len(arr))*100
   
def get_theil_l(arr):
    mean = get_mean(arr)
    theil = 0
    for n in arr:
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

pp2000 = DataSet(
    "The Philippines", 
    2000, 
    [1135.707949, 1892.846582, 2828.135482, 4453.756665, 11958.33664]
)
pp2015 = DataSet(
    "The Philippines", 
    2015, 
    [4088.076278, 6716.125314, 9782.182522, 15111.28196, 37230.69467]
)
pp2018 = DataSet(
    "The Philippines", 
    2018, 
    [2640.00233, 4215.487592, 5961.295584, 8814.201328, 20949.69591]
)

display_population_characteristics(pp2000)
display_population_characteristics(pp2015)
display_population_characteristics(pp2018)
# export_population_characteristics(pp2000)