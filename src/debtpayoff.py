from decimal import *

getcontext().prec = 2


class Loan():
    def __init__(self, presentvalue, rate, periods, periodsperyear=12):
        self.presentvalue = presentvalue
        self.rate = rate
        self.rateperperiod = rate / periodsperyear
        self.periods = periods

    def loanpayment(self):
        payment = self.presentvalue * (self.rateperperiod *
                                       (1 + self.rateperperiod) ** self.periods) / (
                      ((1 + self.rateperperiod) ** self.periods) - 1)
        return round(payment, 2)

    def payoffschedule(self, payment=None):
        principalpaid = 0
        interestpaid = 0
        futurevalue = self.presentvalue

        while futurevalue > 0:
            interestperperiod = round(futurevalue * self.rateperperiod, 2)
            interestpaid += interestperperiod
            if payment is None:
                payment = self.loanpayment()

            if (futurevalue < payment):
                # payment = round(futurevalue - interestperperiod, 2)
                principalperperiod = round(futurevalue - interestperperiod, 2)
                futurevalue = 0
            else:
                principalperperiod = round(payment - interestperperiod, 2)
                futurevalue -= principalperperiod
            principalpaid += principalperperiod
            print("{0}, {1}, {2}".format(interestperperiod, payment, futurevalue))

        print("principal paid: {0}, interest paid: {1}".format(principalpaid, interestpaid))


def main():
    # lendingclub = Loan(8000, 0.0824, 36)
    # print(repr(lendingclub))
    # lendingclub.payoffschedule(300)
    cuofco = Loan(11300, 0.09, 36)
    cuofco.payoffschedule(1350)


if __name__ == '__main__':
    main()
