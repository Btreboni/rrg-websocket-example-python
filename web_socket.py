import json
import os
from dotenv import load_dotenv
from websocket._app import WebSocketApp

load_dotenv()

"""
DEV_NOTE:
    - Highly recommended to use a .env file to keep AUTH credentials secure. Here, we are using load_dotenv from dotenv
      docs can be found here - https://pypi.org/project/python-dotenv/
    - Print statements are helpful while trying to set up your websocket, but not required.
    
ENVIRONMENT VARIABLES: 
    - AUTH: "AUTH YourUserName|YourPassword"
    - SOCKET: "ws://SERVER_URL:PORT_NUMBER/"
"""


class RRG_Websocket:
    def __init__(self):
        self.result = ''

    def connect(self, xml_data):
        """
        Connects to RRG Websocket

        :param xml_data: accepts RRG formatted XML file
        :return: RRG JSON data
        """

        def create_message(message):
            pass

        def on_open(ws):
            print("Socket Opened...")
            pass

        def on_message(ws, message):
            """
            Step 1: AUTHORIZE
                - Wait for a JSON response/message {"MessageType":"MSG","Message":"AUTH_REQ"}
                - Send AUTH ENV

            Step 2: SEND REQUEST XML DATA
                - Wait for JSON response/message {"MessageType":"MSG","Message":"AUTH_CORRECT"}
                - You are now connected to the websocket and able to send requests
                - Send RRG XML file

            Step 3: RESPONSE
                - Once processed, the API will return a JSON response/message
                  {"MessageType":"RESULT","Message":"RRG_DATA_OBJECT"}
                - Convert object to JSON, and set equal to global self.result
                - Close websocket connection

            Step 4: RETURN JSON DATA

            :param ws: Websocket Connection
            :param message: Websocket response
            :raises: Exception as e
            :return: None, sets self.result
            """
            try:
                print("Received a message...")

                # Step 1
                message_json = json.loads(message)
                t = message_json['MessageType']
                m = message_json['Message']
                message_text = '' if message == 'AUTH_REQ' else json.loads(message)['Message']

                if message_text:
                    create_message(message)

                # Step 2
                if message_text == 'AUTH_REQ':
                    ws.send(os.environ.get("AUTH"))

                # Step 3
                if message_text == 'AUTH_CORRECT':
                    print('Sending RRG request...')
                    ws.send(xml_data)

                # Step 4
                if t == 'RESULT':
                    print('RRG result returned...')
                    self.result = json.loads(json.dumps(m, indent=4))
                    ws.close()

            except Exception as e:
                print('Message Exception: {}'.format(str(e)))
                pass

        def on_error(ws, e):
            """
            Helpful for error logging.
            :param ws: Websocket Connection
            :param e: Exception
            :return: None
            """
            print('Error RRG Websocket: {}'.format(str(e)))
            pass

        def on_close(ws):
            """
            Closes RRG websocket connection. Make sure to close the connection after
            each instance has concluded.
            :param ws: Websocket Connection
            :return: None
            """
            print("RRG Connection Closed")
            pass

        # Setup Websocket connection using WebSocketApp package
        ws_thread = WebSocketApp(os.environ.get("SOCKET"),
                                 on_open=on_open,
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close)

        # Needed to keep the websocket open, but will concluded once on_close() is called
        ws_thread.run_forever()

        # Step 5
        return self.result
