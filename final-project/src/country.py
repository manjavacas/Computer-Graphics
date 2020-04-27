
"""
Computer Graphics. Course 2019/2020. ESI UCLM.
Final Project. Antonio Manjavacas.
Country class that gathers stats about total cases, deaths and recoveries
"""

class Country:
    
    def __init__(self, name, cases, deaths, recovered):
        
        self.id = name[:3]
        
        self.name = name
        self.cases = cases
        self.deaths = deaths
        self.recovered = recovered
