from flask import Flask,redirect, render_template, make_response,url_for, request,Response
import csv
import io
import pandas as pd
import matplotlib.pyplot as plt
import base64,cv2
from io import BytesIO
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)
c=0
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')
global df
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    f = request.files['file']
    if not f:
        return "No file"
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    data = pd.read_csv(stream)
    # pair = sns.pairplot(data)
    # plt.savefig("static/pair.png")
    df_cols = data.columns.tolist()
    stream.seek(0)
    result = stream.read().replace("=", ",")
    global df
    df = data
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return  render_template('dashboard.html',df_cols=df_cols,data=data.to_html(header=True, index=False), response=response)

@app.route('/graph', methods=['GET','POST'])
def display():
    output = io.BytesIO()
    x=request.form.get("x_value")
    y=request.form.get("y_value")
    x=str(x)
    x1=df[x].tolist()
    y=str(y)
    y1=df[y].tolist()
    fig,ax=plt.subplots(2,2,figsize=(15,15))
    plt.title(x+" vs "+y)
    ax[0,0].plot(x1,y1,'r--',marker='D')
    ax[0,1].bar(x1,y1,color=['black', 'red', 'green', 'blue', 'cyan'])
    ax[1,0].pie(y1,labels=x1,radius=1.3 ,autopct='%.0f%%')
    
    fig.tight_layout()
    img="plot.jpg"
    plt.savefig(img,dpi=150)

    img = cv2.imread(img)
    image_content1 = cv2.imencode('.jpg', img)[1].tostring()
    encoded_image1 = base64.encodestring(image_content1)
    to_send1 = 'data:image/jpg;base64, ' + str(encoded_image1, 'utf-8')
    return render_template("graph.html", url=to_send1)
    # except:
    #     return redirect(url_for("index"))
if __name__ == "__main__":
    app.run(debug=True)