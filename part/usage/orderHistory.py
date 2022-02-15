import datetime, math
from datetime import date, timedelta
from part.usage.usageDataClasses import Order, Date




class OrderHistory:
    """
    Notes:
        *should implement the filter_by_date method everywhere in the class to simplify algo
    functions:
        - add order
        - sort orders
        - total orders by month
        - annual average
        - monthly average
        - order frequency
        - average order size
    stats:
        - annual average
        - monthly average
        - average order frequency
        - average order size
    """
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        """
        Adds order to history if it isn't already
        :param order: order object
        :return: void
        """

        if order not in self.orders:
            self.orders.append(order)
        else:
            print('order already in history')

    def filter_by_dates(self, start_date, end_date):
        filtered_orders = []
        if start_date is None:
            start_date = datetime.date(1950, 1, 1)
        if end_date is None:
            end_date = datetime.date.today()

        for order in self.orders:
            if start_date <= order.date.get_date() <= end_date:
                filtered_orders.append(order)

        return filtered_orders


    def total_order(self):
        t = 0
        print('total order')
        for order in self.orders:
            t += order.quantity

        return t


    def sort_orders(self):
        """
        sorts orders by date
        :return: void
        """
        print('sorting orders')
        if len(self.orders) >= 2:
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
        print('annual average')
        current_year = date.today().year
        ordered_quantity = 0
        for order in self.orders:
            if order.date.year in range(start_year, current_year):
                ordered_quantity += order.quantity

        return ordered_quantity / (current_year - start_year)

    def monthly_average(self, start_date, timeframe, output_type):
        """
        From original program (dataAnalyser.js line 174, monthlyAve), refait
        :param start_date: Date dataclass
        :param timeframe: timeframe basis for the monthly average
        :param output_type: output type: single value or array, values: 'single', 'array'
        :return:
        """
        rec = {}
        if timeframe == 'auto' or timeframe is None:
            timeframe = math.ceil(self.order_frequency(start_date.year)) / 30   # might be better way to convert in\
            # month



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

        if output_type == 'single':
            total = 0
            for entry in rec:
                total += rec[entry]
            return total / len(rec)

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
        print('order frequency')

        # filter after date
        in_timeframe = []
        for order in self.orders:
            if order.date.get_date() >= start_date:
                in_timeframe.append(order)

        if len(in_timeframe) >= 2:
            print(len(in_timeframe))
            print(range(len(in_timeframe) - 1))
            for i in range(len(in_timeframe) - 2):
                d0 = date(in_timeframe[i].date.year, in_timeframe[i].date.month, in_timeframe[i].date.day)
                d1 = date(in_timeframe[i + 1].date.year, in_timeframe[i + 1].date.month, in_timeframe[i + 1].date.day)
                delta = d1 - d0
                sum += delta.days
            return sum / (len(in_timeframe) - 1)
        else:
            return 'only 1 order'

    def average_order_size(self, start_year):
        """
        Gets the average order size
        :param start_year:
        :return: average order size
        """
        start_date = date(start_year, 1, 1)
        order_count = 0
        total_ordered = 0

        orders = self.filter_by_dates(start_date, None)
        if len(orders) > 0:
            for order in orders:
                if order.date.get_date() >= start_date:
                    total_ordered += order.quantity
                    order_count += 1
            return total_ordered / order_count
        else:
            return 0



if __name__ == '__main__':
    # we want to test the class
    order_history = OrderHistory()
    part = 'part'
    supplier = 'supplier'

    date1 = Date(2017, 5, 6)
    order1 = Order(part, date1, 500, supplier)
    order_history.add_order(order1)

    date2 = Date(2017, 8, 10)
    order2 = Order(part, date2, 250, supplier)
    order_history.add_order(order2)

    date3 = Date(2017, 11, 23)
    order3 = Order(part, date3, 750, supplier)
    order_history.add_order(order3)

    date4 = Date(2018, 6, 4)
    order4 = Order(part, date4, 400, supplier)
    order_history.add_order(order4)

    date5 = Date(2018, 10, 14)
    order5 = Order(part, date5, 600, supplier)
    order_history.add_order(order4)

    date6 = Date(2019, 4, 2)
    order6 = Order(part, date6, 200, supplier)
    order_history.add_order(order5)

    date7 = Date(2020, 8, 10)
    order7 = Order(part, date7, 750, supplier)
    order_history.add_order(order6)

    date8 = Date(2020, 11, 20)
    order8 = Order(part, date8, 1000, supplier)
    order_history.add_order(order7)

    date9 = Date(2021, 4, 6)
    order9 = Order(part, date9, 500, supplier)
    order_history.add_order(order8)

    date10 = Date(2021, 11, 20)
    order10 = Order(part, date10, 750, supplier)
    order_history.add_order(order10)

    print(order_history.annual_average(2017))