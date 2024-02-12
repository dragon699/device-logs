from sys import argv
from datetime import datetime
import serial, argparse


# Number of log entries to write to the file;
# before exiting;
COUNT = 10
LOG_FILE = '/tmp/device.log'


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='device-logs',
            description='Device logs parser - extracts logs from a device connected via serial port and saves them to a file.'
        )

        self.parse()


    def parse(self):
        self.parser.add_argument(
            '-s', '--source',
            required=True,
            help='Source serial port of the device to read logs from.'
        )

        self.parser.add_argument(
            '-f', '--file',
            required=False,
            default=LOG_FILE,
            help='File path to continiously write logs to.'
        )



class Serial_Communicator:
    def __init__(self, source, file):
        self.source = source
        self.file = file
        self.current_count = 0

        self.log_msg = lambda msg: '[{}] {}'.format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            msg
        )

        self.reader = serial.Serial(
            port=source,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        self.write()


    def write(self):
        print(
            self.log_msg('Waiting for logs from {} to write to {}...\n'.format(self.source, self.file))
        )

        while True:
            serial_value = str(self.reader.readline(), 'UTF-8')

            if len(serial_value) > 0:
                self.current_count += 1

                print(
                    self.log_msg('WRITING: {}'.format(serial_value)),
                    end=''
                )

                with open(self.file, 'a') as dest:
                    dest.write(self.log_msg(serial_value))

            if self.current_count >= COUNT:
                break

        return True


if __name__ == '__main__':
    args = Parser().parser.parse_args()

    Serial_Communicator(args.source, args.file)
