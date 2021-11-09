"""
    **Module TimeSheets Cron Jobs**
        this module will run 

"""
from src.models.timesheets import TimeSheetModel


class CalculateMonthlyPayroll:
    """
        **CalculateMonthlyPayroll**
            this class will calculate the monthly payroll
    """
    def __init__(self):
        """
            **__init__**
                this method will initialize the class
        """
        pass

    def run(self):
        """
            **run**
                this method will run the cron job
        """
        start_datetime: datetime = datetime.now().date()
        end_datetime: datetime = datetime.now().date()
        monthly_timesheets: list = TimeSheetModel.query(TimeSheetModel.time_on_duty >= start_datetime, 
                                                        TimeSheetModel.time_of_duty <= end_datetime).fetch()

        pay_list: list =[(timesheet.calculate_pay(), timesheet.uid) for timesheet in monthly_timesheets]
        for pay, uid in pay_list:
            payroll: PayrollProcessing = PayrollProcessing(uid=uid, amount_to_pay=pay)
            # TODO: This is very very slow i need to put this asynchronously
            payroll.put()


class CalculateWeeklyPayroll:
    """
        **CalculateWeeklyPayroll**
            this class will calculate the weekly payroll    
    """
    def __init__(self):
        """
            **__init__**
                this method will initialize the class
        """
        pass

    def run(self):
        """
            **run**
                this method will run the cron job
        """
        pass


class CreatePaySlip:
    """
        **CreatePaySlip**
            this class will create the payslip
    """
    def __init__(self):
        """
            **__init__**
                this method will initialize the class
        """
        pass

    def run(self):
        """
            **run**
                this method will run the cron job
        """
        pass



class SendPaySlip:
    """
        **SendPaySlip**
            this class will send the payslip by email
    """
    def __init__(self):
        """
            **__init__**
                this method will initialize the class
        """
        pass

    def run(self):
        """
            **run**
                this method will run the cron job
        """
        pass

class SendPayNotifications:
    """
        **SendPayNotifications**
            this class will send the payment Notification by email & sms
    """
    def __init__(self):
        """
            **__init__**
                this method will initialize the class
        """
        pass

    def run(self):
        """
            **run**
                this method will run the cron job
        """
        pass