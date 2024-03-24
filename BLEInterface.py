"""
Was able to fix this by myself. I'm publishing the code below. Basically, what I believe it was happening was the
following. The connection with the device was being created in a given event loop A, while the disconnection was being
 requested on event loop B. When the device replied back with telling the disconnection was successfully, that event
 was received in event loop A and not in event loop B. The event loop B was waiting for the reply event and,
 therefore, raised the timeout.
"""

import asyncio
import array
from bleak import BleakClient, BleakScanner
import datetime
from pandas import DataFrame
import time

class BLEInterface:

    def __init__(self, communication_address: str):
        """
        Initialises and sets the Bluetooth connection and runs a loop in a different thread to keep the BLEInterface
        instance running until the user closes the connection

        :param communication_address: communication address of the Bluetooth device we want to connect with
        """
        devices = asyncio.run(BleakScanner.discover())
        device_list = [d.address for d in devices]
        print(device_list)
        if communication_address in device_list:
            print('Found Device.')
            self.loop = asyncio.new_event_loop()
            # Establish the Bluetooth connection and keep the object reference for further use
            try:
                self.connection = self.loop.run_until_complete(self.establish_connection(communication_address))
            except:
                print('Failed to connect. Hit reset on the device.')
                self.loop = None
                self.connection = None
        else:
            self.loop = None
            self.connection = None
            print('Device not found')

    def on_incoming_bth_message(self, sender: int, data: bytearray) -> None:
        value = array.array('h', data)
        signal = float(value[0] + value[1])
        # Prevent overflow
        time.sleep(1)
        now = datetime.datetime.now()
        data_now = {'Time_sec': now, 'Signal': signal}
        df_signal = DataFrame([data_now], columns=list(data_now.keys()))

    async def establish_connection(self, communication_address: str):
        """
        Establishes the Bluetooth connection with the device

        :param communication_address: communication address of the Bluetooth device we want to connect with
        """
        print('Establishing connection with the device {mac}'.format(mac=communication_address))
        # Establish connection with the device
        client = BleakClient(communication_address, loop=self.loop)
        await client.connect()
        # Set on disconnect callback
        client.set_disconnected_callback(self.on_bth_disconnect)
        print('Connection successfully established!')
        # Obtain characteric
        #char_handler = client.services.characteristics[11]
        # Setup callback
        #asyncio.create_task(client.start_notify(char_handler, self.on_incoming_bth_message))
        return client

    def read_gatt(self):
        """
        Description: Read signal from bluetooth low energy device
        :param ble_interface: BLE Connect Established with read characteristics
        :return:
        """
        # Characteristic handler (int)
        char_handler = self.connection.services.characteristics[14]
        # Result from streaming data (byte array)
        result = asyncio.run(self.connection.read_gatt_char(char_handler))
        # Convert byte array to short little endian
        value = array.array('h', result)
        # Convert short little endian to float
        signal = float(value[0] + value[1])
        # Prevent overflow
        time.sleep(1)
        # Retrieve time when signal arrives
        now = datetime.datetime.now()
        data_now = {'Time_sec': now, 'Signal': signal}
        # Create python dataframe
        df_signal = DataFrame([data_now], columns=list(data_now.keys()))
        return df_signal

    def on_bth_disconnect(self, client: BleakClient) -> None:
        print('On Bluetooth disconnect')

    def close_connection(self):
        if self.loop:
            print('Closing the connection')
            self.loop.run_until_complete(self.close_device_connection_async())
            print('Successfully closed.')
            #self.loop.run_until_complete()

    async def close_device_connection_async(self):
        try:
            print('Disconnecting from device')
            await self.connection.disconnect()
            print('Successfully disconnected from device')
        except (ValueError, Exception) as e:
            print('Error disconnecting to device')
            raise Exception(e)


if __name__ == '__main__':
    ble_interface = BLEInterface("F4:12:FA:5A:81:D1")
    try:
        df_signal = ble_interface.read_gatt()
    except:
        print('Failed to read')
    ble_interface.close_connection()
