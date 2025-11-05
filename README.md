
A handy gadget for easily testing FTP (Functional Threshold Power) with a linear fit of stepped aerobic cycling

# Installation #

Please make sure your Python is v3.7 or above.

```bash
python3 --version
python3 -m pip install ftptest
```

Or, clone from GitHub:
```bash
git clone https://github.com/floatinghotpot/ftptest.git
cd ftptest
python3 -m pip install -e .
```

# How To Use #

```bash
ftptest <csv file> [lthr]
```

```bash
ftptest docs/demo.csv 165
```


csv format, each line with power and heartrate, seperated with comma, example:
```bash
124,117
146,127
174,142
197,153
224,161
```

# Demo #

Indoor cycling training with Zwift / MyWhoosh, finish a stepped aerobic workout:

![workout](https://github.com/floatinghotpot/ftptest/raw/main/docs/workout.jpg)

Obtain power / heartrate sample data from training result, calculate linear fit and FTP：

![linear](https://github.com/floatinghotpot/ftptest/raw/main/docs/demo.png)


# Credits #

A simple tool created by Raymond Xie.

Any comments are welcome.
