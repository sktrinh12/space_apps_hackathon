from flask import Flask, render_template, jsonify
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import Span
from random import gauss 

app = Flask(__name__)

x = [gauss(1,1.3) for _ in range(6)] + [gauss(11,1.3) for _ in range(6)] 
y = [gauss(3,1.6) for _ in range(12)]
colour = ['red']*6 + ['blue']*6
x_imp = [gauss(1,1) for _ in range(2)] + [gauss(11,2) for _ in range(2)]
y_imp = [gauss(3,1.6) for _ in range(4)]
colour_imp = ['black']*4

@app.route('/')
def main():
    return render_template('test.html')

def make_plot_raw():
    plot = figure(sizing_mode='scale_width',title="Plot with null values")
    # x = [gauss(1,1.3) for _ in range(6)] + [gauss(11,1.3) for _ in range(6)] 
    # y = [gauss(3,1.6) for _ in range(12)]
    # hline = Span(location=gauss(2,1.4), dimension='width', line_color='black', line_width=3,line_dash='dashed')
    # hline2 = Span(location=gauss(3,1.4), dimension='width', line_color='black', line_width=3,line_dash='dashed')
    # hline3 = Span(location=gauss(4,1.4), dimension='width', line_color='black', line_width=3,line_dash='dashed')
    # hline4 = Span(location=gauss(5,1.4), dimension='width', line_color='black', line_width=3,line_dash='dashed')
    hline = Span(location=y_imp[0], dimension='width', line_color='black', line_width=3,line_dash='dashed')
    hline2 = Span(location=y_imp[1], dimension='width', line_color='black', line_width=3,line_dash='dashed')
    hline3 = Span(location=y_imp[2], dimension='width', line_color='black', line_width=3,line_dash='dashed')
    hline4 = Span(location=y_imp[3], dimension='width', line_color='black', line_width=3,line_dash='dashed')
    plot.circle(x,y,color = colour,size=20)
    plot.renderers.extend([hline])
    plot.renderers.extend([hline2])
    plot.renderers.extend([hline3])
    plot.renderers.extend([hline4])
    plot.toolbar.logo = None
    plot.toolbar_location = None
    plot.axis.visible = False
    script, div = components(plot)
    return script, div

def make_plot_impute():
    plot = figure(sizing_mode='scale_width',title="Plot with imputed Data")
    # x = [gauss(1,1.3) for _ in range(6)] + [gauss(11,1.3) for _ in range(6)] + [gauss(5,2.4) for _ in range(4)]
    # y = [gauss(4,3.7) for _ in range(16)]
    # colour = ['red']*6 + ['blue']*6 + ['black']*4
    plot.circle(x+x_imp,y+y_imp,color = colour + colour_imp,size=20)
    plot.toolbar.logo = None
    plot.toolbar_location = None
    plot.axis.visible = False
    script, div = components(plot)
    return script, div

def make_plot_ml():
    plot = figure(sizing_mode='scale_width',title="Plot after processing")
    # x = [gauss(1,1.2) for _ in range(6)] + [gauss(11,1.3) for _ in range(6)] + [gauss(5,3.5) for _ in range(4)]
    # y = [gauss(5,4.5) for _ in range(16)]
    # colour = ['red' if xi <5 else 'blue' for xi in x]
    plot.circle(x+x_imp,y+y_imp,color = colour + ['red']*2 + ['blue']*2,size=20)
    plot.toolbar.logo = None
    plot.toolbar_location = None
    plot.axis.visible = False
    script, div = components(plot)
    return script, div

@app.route('/updatePlot_raw/' )
def updatePlot_raw():
    script, div = make_plot_raw()
    return jsonify(html_plot=render_template('update_plot.html', plot_div=div,plot_script=script))

@app.route('/updatePlot_impute/' )
def updatePlot_impute():
    script, div = make_plot_impute()
    return jsonify(html_plot=render_template('update_plot_impute.html', plot_div=div,plot_script=script))

@app.route('/updatePlot_ml/' )
def updatePlot_ml():
    script, div = make_plot_ml()
    return jsonify(html_plot=render_template('update_plot_ml.html', plot_div=div,plot_script=script))

if __name__ == '__main__':
    app.run(debug=True)
