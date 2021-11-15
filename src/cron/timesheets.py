"""
    **Module TimeSheets Cron Jobs**
        this module will run 

"""
import asyncio
from datetime import datetime, date
from datetime import timedelta
from typing import List

from src.models.timesheets import TimeSheetModel
from src.models.payroll.payroll import PayrollProcessingModel
from src.models.context import get_client
from src.exceptions.exceptions import RequestError


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
        super().__init__()

    @staticmethod
    async def put_model(model):
        """
            **put_model**
                this method will put the asynchronously to the database model
        """
        with get_client().context() as context:
            return model.put_async()


class ProcessesCalculatePayroll(CronJobs):
    """Processes to calculate weekly and monthly payrolls"""

    def __init__(self):
        super().__init__()

    @staticmethod
    def _return_timesheet(end_datetime, start_datetime) -> List[TimeSheetModel]:
        """search for timesheet between the start and end date"""
        return TimeSheetModel.query(TimeSheetModel.time_on_duty >= start_datetime,
                                    TimeSheetModel.time_of_duty <= end_datetime).fetch()

    def _process_payroll(self, date_now, start_datetime):
        """given the present date and date to start processing from create payrolls"""
        pay_list: list = [(timesheet.calculate_pay, timesheet.uid) for timesheet in
                          self._return_timesheet(date_now, start_datetime)]
        _pay_routines: list = []
        for pay, uid in pay_list:
            payroll: PayrollProcessingModel = PayrollProcessingModel(uid=uid, amount_to_pay=pay)
            # Using coroutine to save all the PayRolls at once
            _pay_routines.append(self.put_model(payroll))
        asyncio.run(asyncio.gather(*_pay_routines))


class CalculateMonthlyPayroll(ProcessesCalculatePayroll):
    """
        **CalculateMonthlyPayroll**
            this class will calculate the monthly payroll
    """

    def __init__(self):
        """
            **__init__**
                this method will initialize the class
        """
        super().__init__()

    def run(self):
        """
            **run**
                this method will run the cron job
        """
        date_now: date = datetime.now().date()
        # NOTE: this only works if this cron job is called every end of the month
        if date_now.day not in [27, 28, 29, 30, 31]:
            raise RequestError(description='Invalid cron job request, date needs to be on the end of the month')

        start_datetime: date = date(year=date_now.year, month=date_now.month, day=1)
        self._process_payroll(date_now, start_datetime)
        return


class CalculateWeeklyPayroll(ProcessesCalculatePayroll):
    """
        **CalculateWeeklyPayroll**
            this class will calculate the weekly payroll    

    """

    def __init__(self):
        """
            **__init__**
                this method will initialize the class
        """
        super().__init__()
        self._friday = 6

    def run(self):
        """
            **run**
                this method will run the cron job
        """
        date_now: date = datetime.now().date()
        if date_now.weekday() != self._friday:
            # if not friday then return
            return

        start_datetime: date = date(year=date_now.year, month=date_now.month, day=date_now.day) - timedelta(days=7)

        self._process_payroll(date_now, start_datetime)
        return


class CreatePaySlip(CronJobs):
    """
        **CreatePaySlip**
            this class will create the payslip
    """

    def __init__(self):
        """
            **__init__**
                this method will initialize the class
        """
        super().__init__()

    def run(self):
        """
            **run**
                this method will run the cron job
        """
        pass


class SendPaySlip(CronJobs):
    """
        **SendPaySlip**
            this class will send the payslip by email

    """

    def __init__(self):
        """
            **__init__**
                this method will initialize the class
        """
        super().__init__()

    def run(self):
        """
            **run**
                this method will run the cron job
        """
        pass


class SendPayNotifications(CronJobs):
    """
        **SendPayNotifications**
            this class will send the payment Notification by email & sms
    """

    def __init__(self):
        """
            **__init__**
                this method will initialize the class
        """
        super().__init__()

    def run(self):
        """
            **run**
                this method will run the cron job
        """
        pass
