"""
    **timesheet module**
        allows users to view & update their timesheet their timesheet
"""
from datetime import datetime

from flask import jsonify
from google.cloud import ndb

from src.models.timesheets.timesheets import TimeSheetModel
from src.exceptions.exceptions import DataServiceError, InputError, status_codes
from src.utils.utils import create_id
from src.views import ViewModel


class TimeSheetView(ViewModel):
    """ **Class TimeSheetView**
        allows users to view & update their timesheet their timesheet
    """
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def __init__(self):
        super().__init__()

    @staticmethod
    def get(timesheet_id: str) -> tuple:
        """ **get method**
            allows users to view their timesheet
        """
        if not timesheet_id:
            raise InputError(description='timesheet_id is required')

        timesheet_instance = TimeSheetModel.query(TimeSheetModel.timesheet_id == timesheet_id).get()
        if not isinstance(timesheet_instance, TimeSheetModel) or not bool(timesheet_instance):
            return jsonify(dict(status=True,
                                message='a timesheet with that id was not found')), status_codes.data_not_found_code

        return jsonify(dict(status=True,
                            payload=timesheet_instance.to_dict(),
                            message='')), status_codes.status_ok_code

    @staticmethod
    def post(timesheet_data: dict) -> tuple:
        """ **post method**
            allows users to create their timesheet
        """
        if not timesheet_data:
            raise InputError(description='Timesheet data is required')

        if not timesheet_data.get('uid'):
            raise InputError(description='user id is required')

        timesheet_instance: TimeSheetModel = TimeSheetModel(**timesheet_data, timesheet_id=create_id())
        key: ndb.Key = timesheet_instance.put()
        if not isinstance(key, ndb.Key):
            raise DataServiceError(description='Unable to create timesheet')

        return jsonify(dict(status=True,
                            payload=timesheet_instance.to_dict(),
                            message='successfully created timesheet')), status_codes.status_ok_code

    @staticmethod
    def put(timesheet_data: dict) -> tuple:
        """ **put method**
                allows users to update their timesheet
        """
        if not timesheet_data:
            raise InputError(description='Timesheet data is required')

        if not timesheet_data.get('timesheet_id'):
            raise InputError(description='Bouncer ID is required')

        timesheet_instance: TimeSheetModel = TimeSheetModel.query(
            TimeSheetModel.timesheet_id == timesheet_data.get('timesheet_id')).get()

        timesheet_instance.update(**timesheet_data)
        key: ndb.Key = timesheet_instance.put()
        if not isinstance(key, ndb.Key):
            raise DataServiceError(description='Unable to update timesheet')

        return jsonify(dict(status=True,
                            payload=timesheet_instance.to_dict(),
                            message='successfully updated timesheet')), status_codes.status_ok_code

    @staticmethod
    def delete(timesheet_id: str) -> tuple:
        """ 
            **delete method**  
                allows users to delete their timesheet
                
        """
        if not timesheet_id:
            raise InputError(description='Timesheet ID is required')

        timesheet_instance: TimeSheetModel = TimeSheetModel.query(TimeSheetModel.timesheet_id == timesheet_id).get()
        if not isinstance(timesheet_instance, TimeSheetModel) or not bool(timesheet_instance):
            return jsonify(dict(status=True,
                                message='No timesheet found wit that id')), status_codes.data_not_found_code

        timesheet_instance.key.delete()
        return jsonify(dict(status=True,
                            message='successfully deleted timesheet')), status_codes.successfully_updated_code


class TimeSheetByBouncerView(ViewModel):
    """ **Class TimeSheetListView**
            allows user to access timesheet lists
    """
    methods = ['GET']

    def __init__(self):
        super().__init__()

    @staticmethod
    def get(bouncer_id: str) -> tuple:
        """ **get method**
            allows users to view their timesheet
        """
        if not bouncer_id:
            raise InputError(description='Bouncer ID is required')

        timesheet_list: list = [timesheet.to_dict() for timesheet in
                                TimeSheetModel.query(TimeSheetModel.bouncer_id == bouncer_id).fetch()]
        if not isinstance(timesheet_list, list) or not bool(timesheet_list):
            return jsonify(dict(status=True,
                                message='No timesheet found for that bouncer')), status_codes.data_not_found_code

        return jsonify(dict(status=True,
                            payload=timesheet_list,
                            message='')), status_codes.status_ok_code


class TimeSheetByPeriodView(ViewModel):
    """ **Class TimeSheetListView**
            allows user to access timesheet lists
    """
    methods = ['GET']

    def __init__(self):
        super().__init__()

    @staticmethod
    def get(bouncer_id: str, start_date: str, end_date: str) -> tuple:
        """ **get method**
            allows users to view their timesheet
        """
        if not bouncer_id:
            raise InputError(description='Bouncer ID is required')

        if not start_date:
            raise InputError(description='Start date is required')

        if not end_date:
            raise InputError(description='End date is required')

        start_datetime: datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime: datetime = datetime.strptime(end_date, '%Y-%m-%d')

        timesheet_list: list = [timesheet.to_dict() for timesheet in
                                TimeSheetModel.query(TimeSheetModel.bouncer_id == bouncer_id,
                                                     TimeSheetModel.time_on_duty >= start_datetime,
                                                     TimeSheetModel.time_of_duty <= end_datetime).fetch()]
        if not isinstance(timesheet_list, list) or not bool(timesheet_list):
            return jsonify(dict(status=True,
                                message='No timesheet found for that bouncer')), status_codes.data_not_found_code

        return jsonify(dict(status=True,
                            payload=timesheet_list,
                            message='')), status_codes.status_ok_code


class TimeSheetByBouncerAndDateView(ViewModel):
    """
        **Class TimeSheetByBouncerAndDateView**
            allows user to access timesheet by bouncer and date

    """
    methods = ['GET']

    def __init__(self):
        super().__init__()

    @staticmethod
    def get(bouncer_id: str, date: str) -> tuple:
        """ **get method**
            allows users to view their timesheet
        """
        if not bouncer_id:
            raise InputError(description='Bouncer ID is required')

        if not date:
            raise InputError(description='Date is required')

        date_datetime: datetime = datetime.strptime(date, '%Y-%m-%d')

        timesheet_list: list = [timesheet.to_dict() for timesheet in
                                TimeSheetModel.query(TimeSheetModel.bouncer_id == bouncer_id,
                                                     TimeSheetModel.time_on_duty == date_datetime).fetch()]
        if not isinstance(timesheet_list, list) or not bool(timesheet_list):
            return jsonify(dict(status=True,
                                message='No timesheet found for that bouncer')), status_codes.data_not_found_code

        return jsonify(dict(status=True,
                            payload=timesheet_list,
                            message='successfully retrieved time sheet by bouncer and date')), status_codes.status_ok_code
