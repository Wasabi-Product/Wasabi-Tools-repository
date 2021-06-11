GUI EGRESS VOLUME CALCULATOR
--

uses the billing api : https://billing.wasabisys.com/utilization/bucket/

Create standalone from the python files using:
--

```shell
pyinstaller --clean -F --add-data="my.kv:." main.py
```