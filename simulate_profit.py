from flask import Flask, render_template, request
from io import BytesIO
import base64
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
  return render_template('g_index.html')

@app.route('/profit/', methods=["POST"])
def profit():
  price = int(request.form["price"])
  pay = int(request.form["pay"])
  store = int(request.form["store"])
  store_num = np.arange(store+1)
  img_data = profit_simu(store_num, price, pay)
  return render_template('index.html', price=price, pay=pay, store=store, img_data=img_data)

def profit_simu(num, price, pay):
  fig = Figure()
  ax = fig.add_subplot(111)
  ax.plot(num, num*price, color="blue", label="profit")
  ax.axhline(pay, color="red", label="spend")
  ax.legend()
  io = BytesIO()
  fig.savefig(io, format="png")
  io.seek(0)
  base64_img = base64.b64encode(io.read()).decode()
  return base64_img

@app.route('/price/', methods=["POST"])
def price():
  min_price = int(request.form["min_price"])
  max_price = int(request.form["max_price"])
  pay = int(request.form["pay"])
  step = int(request.form["step"])
  store = int(request.form["store"])
  store_num = np.arange(store+1)
  img_data = price_simu(store_num, min_price, max_price, step, pay)
  return render_template('price_index.html', min_price=min_price, max_price=max_price, pay=pay, store=store, step=step, img_data=img_data)

def price_simu(num, min_price, max_price, step, pay):
  fig = Figure()
  ax = fig.add_subplot(111)
  ax.axhline(pay, color="red", label="spend")
  for i in range(min_price, max_price+step, step):
    ax.plot(num, num*i, label="{} yen".format(i))
  ax.legend()
  io = BytesIO()
  fig.savefig(io, format="png")
  io.seek(0)
  base64_img = base64.b64encode(io.read()).decode()
  return base64_img

if __name__ == "__main__":
  app.run(port=8000, debug=True)