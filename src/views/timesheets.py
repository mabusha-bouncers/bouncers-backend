"""
    **timesheets module**
        allows users to view & update their timesheets their timesheets
"""
from flask import jsonify
from src.models.timesheets.timesheets import TimeSheetModel
from src.exceptions.exceptions import DataServiceError, BadRequestError, InputError, status_codes


class TimeSheetView(ViewModel):
    """ **Class TimeSheetView**
        allows users to view & update their timesheets their timesheets
    """
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get(timesheet_id: str) -> tuple:
        """ **get method**
            allows users to view their timesheets
        """
        if not timesheet_id:
            raise InputError('timesheet_id is required')

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
            allows users to create their timesheets
        """
        if not timesheet_data:
            raise InputError('Timesheet data is required')

        if not timesheet_data.get('uid'):
            raise InputError('user id is required')

        
        timesheet_instance: TimeSheetModel = TimeSheetModel(**timesheet_data, timesheet_id=create_id())
        key: ndb.Key = timesheet_instance.put()
        if not isinstance(key, ndb.Key):
            raise DataServiceError('Unable to create timesheet')

        return jsonify(dict(status=True, 
                            payload=timesheet_instance.to_dict(), 
                            message='successfully created timesheet')), status_codes.status_ok_code
                


    @staticmethod
    def put(timesheet_data: dict) -> tuple:
        """ **put method**
            allows users to update their timesheets
        """
        if not timesheet_data:
            raise InputError('Timesheet data is required')

        if not timesheet_data.get('timesheet_id'):
            raise InputError('Bouncer ID is required')

        timesheet_instance: TimeSheetModel = TimeSheetModel.query(TimeSheetModel.timesheet_id == timesheet_data.get('timesheet_id')).get()

        timesheet_instance: TimeSheetModel = timesheet_instance.update(**timesheet_data)
        key: ndb.Key = timesheet_instance.put()
        if not isinstance(key, ndb.Key):
            raise DataServiceError('Unable to update timesheet')

        return jsonify(dict(status=True, 
                            payload=timesheet_instance.to_dict(), 
                            message='successfully updated timesheet')), status_codes.status_ok_code

    @staticmethod
    def delete(timesheet_id: str) -> tuple:
        """ 
            **delete method**  
                allows users to delete their timesheets
                
        """
        if not timesheet_id:
            raise InputError('Timesheet ID is required')

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

    def get(self, bouncer_id: str) -> tuple:
        """ **get method**
            allows users to view their timesheets
        """
        if not bouncer_id:
            raise InputError('Bouncer ID is required')

        timesheet_list: list = TimeSheetModel.query(TimeSheetModel.bouncer_id == bouncer_id).fetch()
        if not isinstance(timesheet_list, list) or not bool(timesheet_list):
            return jsonify(dict(status=True, 
                                message='No timesheets found for that bouncer')), status_codes.data_not_found_code

        return jsonify(dict(status=True, 
                            payload=timesheet_list, 
                            message='')), status_codes.status_ok_code
