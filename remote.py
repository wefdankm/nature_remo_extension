import requests
import json
import time
import datetime
import argparse
import sys

## This script receives and pases it to the specified other Reno.


def receive(from_ip_addr, pnt=False):
    try:
        req = requests.get("http://{}/messages".format(from_ip_addr),headers={"X-Requested-With":"local"}, timeout=1)
        if pnt:
            print("{}:Received:{}".format(datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + 'Z',hash(req.content)))
        return req
    except Exception as e:
        print("*")
        requests.session()
        raise ValueError("Invalid data returned")

def send(to_ip_addr, data, pnt=False):
    try:
        r = requests.post("http://{}/messages".format(to_ip_addr),headers={"X-Requested-With":"local"}, data=data,timeout=1)
        if pnt:
            print("{}:Sent:{}".format(datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + 'Z',hash(data)))
        return r
    except Exception as e:
        requests.session()
        raise ValueError("Data transmission failed")

if __name__ == "__main__":

    ## Take arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--to_addr", help="Specify where IR signal data should be sent to")
    parser.add_argument("-f","--from_addr", help="Specify where IR signal data should come from")
    parser.add_argument("-i","--ignore", help="Specify which error to ignore \n \n old signal - o \n\n duplicate - d \n\n illegal data - i \n\n if all then specify odi")
    parser.add_argument("-s","--show", help="Specify which status to show \n\n receive - r \n\n send - s \n\n if both then rs")
    args = parser.parse_args()
    print("from_addr:{}\nto_addr:{}\n".format(args.from_addr, args.to_addr))

    ## Check connection remo [from]
    while True:
        try:
            d = receive(from_ip_addr=args.from_addr)
            if d.status_code != 200:
                print("Connection [FROM]:{} >NG".format(args.from_addr))
                input("Send IR signal to Nature Remo and hit Enter: ")
            else:
                print("Connection [FROM]:{} >OK".format(args.from_addr))
                break
        except Exception as e:
            print(e)
            continue
    

    pre_hash = 0
    nex_hash = 0
    spit_flag = 0

    
    ## Get pnt value for show statement
    pnt_receive = True if "r" in args.show else False
    pnt_send = True if "s" in args.show else False

    ## Get ignore flag for ignore statement
    ignore_i = True if "i" in args.ignore else False
    ignore_d = True if "d" in args.ignore else False
    ignore_o = True if "o" in args.ignore else False

    while True:
        ## Receive signal from the one end
        try:
            r = receive(from_ip_addr = args.from_addr,pnt=pnt_receive)
            if r.status_code == 200 and spit_flag == False:
                spit_flag += 1
                pre_hash = hash(r.content)
        except ValueError as e:
            continue

        try:
            if "[" in str(r.content) and spit_flag > 1:
                if pre_hash != hash(r.content):
                    nex_data = r.content
                    nex_hash = hash(nex_data)
                else:
                    pre_hash = hash(r.content)
                    if not ignore_d:
                        raise ValueError("Data duplicate")
                    else:
                        continue
            elif spit_flag and "[" in str(r.content) and pre_hash == hash(r.content):
                if not ignore_o:
                    raise ValueError("ignore old signal flag is on")
                else:
                    continue
            elif spit_flag and "[" in str(r.content) and pre_hash != hash(r.content):
                spit_flag += 1
                nex_data = r.content
                nex_hash = hash(nex_data)
            else:
                if not ignore_i:
                    raise ValueError("Received data illigal format")
                else:
                    continue
        except ValueError as e:
            print(e)
            continue

        ## Send signal to the other end 
        try:
            if spit_flag > 1:
                status = send(to_ip_addr = args.to_addr, data=nex_data, pnt=pnt_send)
                pre_hash = nex_hash
        except ValueError as e:
            continue
