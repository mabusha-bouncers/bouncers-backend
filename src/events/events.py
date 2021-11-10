"""
    events module used to handle application events in real time
"""
import requests


class Events:
    """
        **Class Events**
           asynchronously triggers events when certain values are changed on the database
           events server must be instantiated or a ready made solution added

           **Suggestion:** or could use a memory based data-structure for now to control
           events, and then create a method which will continuously fetch and execute
           the events asynchronously.
    """

    def __init__(self, events_server_url: str):
        """
            **__init__**
                initializes the events server url

            :param events_server_url: the url of the events server
        """
        self.events_server_url = events_server_url

    def trigger_event(self, event_name: str, event_data: dict):
        """
            **trigger_event**
                triggers an event on the events server

            :param event_name: the name of the event to trigger
            :param event_data: the data to be sent to the event
        """
        requests.post(self.events_server_url, json={"event_name": event_name, "event_data": event_data})

    def fetch_events(self):
        """
            **fetch_events**
                fetches events from the events server

            :return: the events fetched from the events server
        """
        return requests.get(self.events_server_url).json()

    def process_events(self):
        """
            **process_events**
                processes events from the events server

            :return: the events fetched from the events server
        """
        events = self.fetch_events()
