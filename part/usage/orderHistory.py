import datetime
from datetime import date, timedelta
from part.usage.usageDataClasses import Order, Date

"""
Original program:
    - total order size
    - annual average - DONE
    - orderByMonth - DONE
    - monthly average - DONE (some things left to do)
    - max monthly consom
    - commande typique
    - freq order - DONE
    
"""

class PastOrders:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def sort_orders(self):
        """
        sorts orders by date
        :return: void
        """
        self.orders = sorted(self.orders, key=lambda order: order.date.get_date())

    def total_order_by_month(self, start_date):
        """
        From original program (dataAnalyser.js line 63, orderByMonth), simplified
        :param start_date: Date dataclass
        :return: dict of total order for each month {yyyymm: total}
        """
        rec = {}
        start_date = datetime.date(start_date.year, start_date.month, start_date.day)
        for order in self.orders:
            if date(order.date.year, order.date.month, order.date.day) > start_date:
                if str(order.date.year) + str(order.date.month) not in rec:
                    rec[str(order.date.year) + str(order.date.month)] = order.quantity
                else:
                    rec[str(order.date.year) + str(order.date.month)] = rec[str(order.date.year) +
                                                                            str(order.date.month)] + order.quantity
        return rec

    def annual_average(self, start_year):
        """
        From original program (dataAnalyser.js line 41, annualAve), simplified
        :param start_year: int
        :return: yearly average
        """
        current_year = date.today().year
        ordered_quantity = 0
        for order in self.orders:
            if order.date.year in range(start_year, current_year):
                ordered_quantity += order.quantity

        return ordered_quantity / (current_year - start_year)

    def monthly_average(self, start_date, timeframe, type):
        """
        From original program (dataAnalyser.js line 174, monthlyAve), refait
        :param start_date: Date dataclass
        :param timeframe: timeframe basis for the monthly average
        :param type:
        :return:
        """
        rec = {}

        current_date = date.today()
        group_counter = 0

        # makes dict with date entries yyyymm from last month to start_date with timeframe between each entries
        for y in range(current_date.year, start_date.year - 1, -1):
            if y == current_date.year:
                for m in range(current_date.month - 1, 0, -1):
                    if group_counter == timeframe - 1:
                        rec[str(y) + str(m)] = []
                        group_counter = 0
                    else:
                        group_counter += 1
            elif y == start_date.year:
                for m in range(12, start_date.month - 1, -1):
                    if group_counter == timeframe - 1:
                        rec[str(y) + str(m)] = []
                        group_counter = 0
                    else:
                        group_counter += 1
            else:
                for m in range(12, 0, -1):
                    if group_counter == timeframe - 1:
                        rec[str(y) + str(m)] = []
                        group_counter = 0
                    else:
                        group_counter += 1

        # puts orders in their place in the previous dict
        for entry in rec:
            for order in self.orders:
                if order.date.year == int(entry[:4]):
                    if int(entry[4:]) <= order.date.month < int(entry[4:]) + timeframe:
                        rec[entry].append(order)
                elif order.date.year == int(entry[:4]) + 1:
                    if order.date.month < int(entry[4:]) + timeframe - 12:
                        rec[entry].append(order)

        for month_group in rec:
            total = 0
            for order in rec[month_group]:
                total += order.quantity
            rec[month_group] = total / timeframe

        return rec



    def order_frequency(self, start_year):
        """
        From original program (dataAnalyser.js line 297, freqOrder), refait
        :param start_year: int
        :return: average duration (days) between orders
        """
        self.sort_orders()
        start_date = datetime.date(start_year, 1, 1)
        sum = 0
        for i in range(len(self.orders) - 1):
            if self.orders[i].date.get_date() >= start_date:
                d0 = date(self.orders[i].date.year, self.orders[i].date.month, self.orders[i].date.day)
                d1 = date(self.orders[i+1].date.year, self.orders[i+1].date.month, self.orders[i+1].date.day)
                delta = d1 - d0
                sum += delta.days
        return sum / (len(self.orders) - 1)



d1 = Date(2017, 7, 25)
o1 = Order(d1, 200)

d2 = Date(2017, 7, 23)
o2 = Order(d2, 4000)

d3 = Date(2018, 4, 17)
o3 = Order(d3, 600)

d4 = Date(2018, 3, 25)
o4 = Order(d4, 1350)

d5 = Date(2019, 11, 6)
o5 = Order(d5, 250)

d6 = Date(2021, 5, 12)
o6 = Order(d6, 750)

o = PastOrders()
o.add_order(o1)
o.add_order(o2)
o.add_order(o3)
o.add_order(o4)
o.add_order(o5)
o.add_order(o6)
print('monthly average ', o.monthly_average(Date(2017, 1, 1), 4, 'test'))
print('annual average ', o.annual_average(2017))
print('order frequency ', o.order_frequency(2017))
print(o.order_frequency(2019))
