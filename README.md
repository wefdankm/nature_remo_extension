# About
nature_remo_extension is a tiny script to extend IR signal received on one Nature Remo device to another.

## Usage

Extend IR signal from Nature Remo Mini 1st Gen at 192.168.11.1 to Nature Remo Mini 1st Gen at 192.168.11.2

```
python3 remote.py -t 192.168.11.2 -f 192.168.11.1 -i iod -s s
```

## Help

```
wefdankm@laptop project % python3 remote.py --help
usage: remote.py [-h] [-t TO_ADDR] [-f FROM_ADDR] [-i IGNORE] [-s SHOW]

optional arguments:
  -h, --help            show this help message and exit
  -t TO_ADDR, --to_addr TO_ADDR
                        Specify where IR signal data should be sent to
  -f FROM_ADDR, --from_addr FROM_ADDR
                        Specify where IR signal data should come from
  -i IGNORE, --ignore IGNORE
                        Specify which error to ignore old signal - o duplicate
                        - d illegal data - i if all then specify odi
  -s SHOW, --show SHOW  Specify which status to show receive - r send - s if
                        both then rs
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
GPL-3.0 License