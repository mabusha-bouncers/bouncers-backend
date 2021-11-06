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
    def get(bouncer_id: str) -> tuple:
        """ **get method**
            allows users to view their timesheets
        """
        if not bouncer_id:
            raise InputError('Bouncer ID is required')

        timesheet_instance = TimeSheetModel.query(TimeSheetModel.bouncer_id == bouncer_id).get()
        if not isinstance(timesheet_instance, TimeSheetModel) or not bool(timesheet_instance):
            return jsonify(dict(status=True, message='No timesheet found for this bouncer')), status_codes.data_not_found_code

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

        if not timesheet_data.get('bouncer_id'):
            raise InputError('Bouncer ID is required')

        
        timesheet_instance: TimeSheetModel = TimeSheetModel(**timesheet_data)
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

        if not timesheet_data.get('bouncer_id'):
            raise InputError('Bouncer ID is required')

        timesheet_instance: TimeSheetModel = TimeSheetModel.query(TimeSheetModel.bouncer_id == timesheet_data.get('bouncer_id')).get()

        timesheet_instance: TimeSheetModel = timesheet_instance.update(**timesheet_data)
        key: ndb.Key = timesheet_instance.put()
        if not isinstance(key, ndb.Key):
            raise DataServiceError('Unable to update timesheet')

        return jsonify(dict(status=True, 
                            payload=timesheet_instance.to_dict(), 
                            message='successfully updated timesheet')), status_codes.status_ok_code