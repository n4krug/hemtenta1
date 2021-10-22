def car_rent_calc():
    days = int(input("Ange antalet dagar som ni hyr bilen:\n"))

    if days > 3:
        sum = 1200 * days
    else:
        miles = int(input("Ange antalet mil som ska köras:\n"))

        sum = 700 + 20 * miles

    if sum > 0:
        print(f"Summan är {sum}")
