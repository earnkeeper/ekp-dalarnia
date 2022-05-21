import sys
import time
import requests
import datetime
from decouple import config

BSCSACN_API_KEY = config('BSCSCAN_API_KEY')

def get_transactions_by_timestamp(contract_address, start_time, end_time):
    url = f"https://api.bscscan.com/api?module=account&action=txlist&address={contract_address}&apikey={BSCSACN_API_KEY}"
    # &startblock=17396904
    response = requests.get(url)

    for r in response.json()['result']:
        start_offset = int(time.mktime(datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timetuple()))
        end_offset = int(time.mktime(datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").timetuple()))
        t_stamp = int(r['timeStamp'])
        ignore_list = ['0x1a1ec25dc08e98e5e93f1104b5e5cdd298707d31', '0x16a1cfb99782ebc3cd4ecd9cf1c589d6eb548c0d',
                       '0x10ed43c718714eb63d5aa57b78b54704e256024e']
        if start_offset < t_stamp < end_offset and r['to'] not in ignore_list:
            print(r)


if __name__ == '__main__':
    stdoutOrigin = sys.stdout
    sys.stdout = open("output.txt", "w")

    get_transactions_by_timestamp(
        contract_address='0x553a463f365c74EdA00B7E5aaF080B066d4CA03C',
        start_time='2022-05-10 23:29:37',
        end_time='2022-05-11 00:31:47'
    )

    sys.stdout.close()
    sys.stdout=stdoutOrigin
