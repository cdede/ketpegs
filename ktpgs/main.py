from .ktp_client import KtpClient
from .animal import solve_m12
from .buri_donk import BuriDonk
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m','--mode', help='select game'
            , default='0')
    parser.add_argument('--donk', action ='store_true',help = 'buri donk',default=False)
    parser.add_argument('--m12', help = 'm12',default='')
    parser.add_argument('--ketpegs', action ='store_true',help = 'ketpegs (default)',default=False)

    args = parser.parse_args()
    if args.donk:
        bd1 = BuriDonk()
        bd1.loop()
    elif args.ketpegs:
        KtpClient().gui.loop.run()
    elif args.m12 != '':
        t1 = solve_m12(args.m12)
        print(t1[0],"\n",t1[1])
    else:
        KtpClient().gui.loop.run()
