"""
    **Module TimeSheets Cron Jobs**
        this module will run 

"""
import asyncio
from src.models.timesheets import TimeSheetModel
from src.models.payroll import PayrollProcessingModel
from src.models.context import get_client


class CronJobs:
    """
        **CronJobs Class**
            this class will run cron jobs
    """
    def __init__(self):
        """
            **__init__**
                this method will initialize the class
        """
        pass
    
    @staticmethod
    async def put_model(model):
        """
            **put_model**
                this method will put the asynchronously to the database model
        """
        with get_client().context() as context:
            return model.put_async()

        


class CalculateMonthlyPayroll(CronJobs):
    """
        **CalculateMonthlyPayroll**
            this class will calculate the monthly payroll
    """
    def __init__(self):
        """
            **__init__**
                this method will initialize the class
        """
        super()

    def run(self):
        """
            **run**
                this method will run the cron job
        """
        date_now: datetime = datetime.now().date()
        if date_now.day not in [27,28,29,30,31]:
            return

        start_datetime: datetime = datetime(date_now.year, date_now.month, 1) - relativedelta(months=1)
        end_datetime: datetime = date_now
        monthly_timesheets: list = TimeSheetModel.query(TimeSheetModel.time_on_duty >= start_datetime, 
                                                        TimeSheetModel.time_of_duty <= end_datetime).fetch()

        pay_list: list =[(timesheet.calculate_pay(), timesheet.uid) for timesheet in monthly_timesheets]
        _pay_routines: list = []
        for pay, uid in pay_list:
            payroll: PayrollProcessingModel = PayrollProcessingModel(uid=uid, amount_to_pay=pay)
            # Using coroutine to save all the PayRolls at once
            _pay_routines.append(self.put_model(payroll))
        asyncio.gather(*_pay_routines)
        return


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