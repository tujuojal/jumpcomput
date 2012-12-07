from flask import Flask, make_response
app = Flask(__name__)

@app.route("/")
def simple(self):
    data_uri = open("plot.png", "rb").read().encode("base64").replace("\n", "")
    img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(data_uri)
    print img_tag



if __name__ == "__main__":
    app.run()
