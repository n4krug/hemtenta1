test = {
    "company-yearly": 6000000,
    "salaries-monthly": {
        "Anna": 155000,
        "Björn": 55000,
        "Cecilia": 55000,
        "David": 55000,
        "Erik": 55000,
        "Filip": 40000,
        "Greta": 40000,
        "Hans": 40000,
        "Ingrid": None,
        "Johannes": None,
        "Kent": None,
    },
}

print(list(test["salaries-monthly"].keys())[1])
