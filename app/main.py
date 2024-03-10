import json
import datetime
from app.car import Car
from app.shop import Shop
from app.customer import Customer


def shop_trip() -> None:
    with open("config.json") as file:
        date = json.load(file)
        fuel_price_date = date["FUEL_PRICE"]
        customers_date = date["customers"]
        shops_date = date["shops"]

    for customer in customers_date:
        name = customer["name"]
        customer_money = customer["money"]
        print(f"{name} has {customer_money} dollars")
        first_point = customer["location"]
        fuel_consumption = customer["car"]["fuel_consumption"]
        product_cart = customer["product_cart"]
        min_expenses = float("inf")
        name_of_shop = ""

        for shop in shops_date:
            second_point = shop["location"]
            product_shop = shop["products"]
            shop_name = shop["name"]
            money_for_trip = Car(
                first_point,
                second_point,
                fuel_price_date,
                fuel_consumption
            )
            money_for_products = Shop(product_shop, product_cart)
            money_for_all = (money_for_trip.get_cost_trip()
                             + money_for_products.get_cheapest_shop())
            money_for_all = round(money_for_all, 2)
            print(
                f"{name}'s trip to the {shop_name} costs {money_for_all}"
            )
            if (money_for_all < min_expenses
                    and customer_money > money_for_all):
                min_expenses = money_for_all
                name_of_shop = shop_name
                product = shop["products"]

        if not name_of_shop:
            print(
                f"{name} doesn't have enough money "
                f"to make a purchase in any shop"
            )
        else:
            print(f"{name} rides to {name_of_shop}\n")
            print("Date: "
                  + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                  )
            buy = Customer(name, customer["product_cart"], product)
            buy.buying_products()
            print(f"{name} rides home")
            change = customer["money"] - min_expenses
            print(f"{name} now has {change} dollars\n")
