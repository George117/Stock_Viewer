from pandas_datareader.data import get_quote_yahoo
import time
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

stock_to_look_at = "AMD"

invested_shares = 53.39041644

buy_price = 74.92

time_last = 0

current_value_last = 0

app = QtGui.QApplication([])
old_value = 0

win = pg.GraphicsLayoutWidget(show=True, title="{} stock".format(stock_to_look_at))
win.resize(800,480)
win.setWindowTitle("{} stock".format(stock_to_look_at))

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


p1 = win.addPlot(title="Current Value:")
p1.setLabel('left', '$', '$')
p1.setYRange(0, 100, padding=0)

text_value = pg.TextItem("$ = {}".format(" "))
p1.addItem(text_value)

curve1 = p1.plot(pen='g')
data1 = [0] * 200
ptr1 = 0


win.nextRow()

p2 = win.addPlot(title="Profit")
p2.setLabel('left', '$', '$')
p2.setYRange(-100, 100, padding=0)

text_profit = pg.TextItem("$ = {}".format(" "))
p2.addItem(text_profit)

curve2 = p2.plot(pen='r')
data2 = [0] * 200
ptr2 = 0

def get_data():
    stock_data = get_quote_yahoo(stock_to_look_at)

    current_stock_price =  stock_data["price"].tolist()

    return current_stock_price

def update():
    global curve1, data1, ptr1, p1, p2, curve2, data2, ptr2, text, p3, curve3, data3, ptr3, old_value, time_last, current_value_last

    if time.time() - time_last > 1 :
        current_value_now = get_data()
        current_value_last = current_value_now
        time_last = time.time()
    else:
        current_value_now = current_value_last

    current_value_pp = float(current_value_now[0])#float('{:1.2f}'.format(voltage))
    profit_pp = (current_value_pp * invested_shares) - (invested_shares * buy_price)



    # print('I = {:1.2f} A'.format(current))
    # print('U = {:1.2f} V\n'.format(voltage_pp))

    data1[:-1] = data1[1:]  # shift data in the array one sample left
    data1[-1] = current_value_pp

    text_value.setText('{:1.2f} $'.format(current_value_pp))
    text_value.setPos((len(data1) - 3), (data1[-1] + 4))

    data2[:-1] = data2[1:]  # shift data in the array one sample left
    data2[-1] = profit_pp
    #
    # data3[:-1] = data3[1:]  # shift data in the array one sample left
    # data3[-1] = rolling_counter

    text_profit.setText('{:1.2f} $'.format(profit_pp))
    text_profit.setPos((len(data1) - 3), (data2[-1] + 0.3))

    # set data
    curve1.setData(data1)
    curve2.setData(data2)

    # curve3.setData(data3)

    if ptr1 == 0:
        p1.enableAutoRange('y', False)  ## stop auto-scaling after the first data set is plotted
    if ptr2 == 0:
        p2.enableAutoRange('y', False)  ## stop auto-scaling after the first data set is plotted
    # if ptr3 == 0:
    #     p3.enableAutoRange('y', False)  ## stop auto-scaling after the first data set is plotted

    ptr1 += 1
    ptr2 += 1
    # ptr3 += 1


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(60)

if __name__ == '__main__':
    import sys


    while True:
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()