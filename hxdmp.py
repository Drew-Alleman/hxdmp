import binascii
import argparse
import re


class hxdmp:
    def __init__(self, args):
        self.bytes_to_process = args.bytes
        self.filename = args.filename
        self.exclude = args.exclude
        self.output = []
    

    def decode_byte(self, byte):
        if byte < 128 and byte > 32:
            return chr(byte)
        return  '.'



    def decode_bytes(self, chunk):
        byte_list = []
        for byte in chunk:
            byte_list.append(self.decode_byte(byte))
        return ''.join(byte_list)



    def display_hex(self, chunk):
        data = ''.join(re.findall('..?', binascii.hexlify(chunk).decode('utf-8')))
        return ' '.join(data[i:i+2] for i in range(0, len(data), 2))


    
    def process_file(self):
        offset = 0
        try:
            with open(self.filename, 'rb') as infile:
                while True:
                    chunk = infile.read(self.bytes_to_process)
                
                    if len(chunk) == 0:
                        break
                    
                    offset_text = '{:#08x}'.format(offset)
                    text = self.decode_bytes(chunk).strip()
                    if args.exclude:
                        if text.strip() == '................':
                            continue
                     
                    self.output.append(f'{offset_text}     {self.display_hex(chunk)}      {text}')
                    offset += self.bytes_to_process

        except FileNotFoundError:
            print(f'[-]  Failed to open file: {self.filename}')


    def run(self):
        try:
            if args.output:
                output_file = open(args.output, 'a+')
        except PermissionError:
            print(f'[-] Do not have the correct permissions to write to:{args.output} ')
            exit()

        self.process_file()
        for line in self.output:
            if args.output:
                output_file.write(line + '\n')
            else:
                print(line)

        if args.output:
            output_file.close()




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hex Dump Utitliy')
    parser.add_argument('-f', '--filename', help='Filename to process', required=True)
    parser.add_argument('-b', '--bytes', default=16, type=int, help='Bytes to process')
    parser.add_argument('-o', '--output', help='File to store output')
    parser.add_argument('-e', '--exclude', help='Only display output that can be decoded', default=False, action='store_true')
    args = parser.parse_args()
    
    h = hxdmp(args)
    h.run()
