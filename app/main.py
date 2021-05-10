import config
import csv
import os

import pandas as pd
import pymongo
import requests
from flask import Flask, flash, request, redirect, abort, render_template,send_file

app = Flask(__name__)

DOWNLOAD_FOLDER = config.DOWNLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
DATASET = []


@app.route('/', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        player_number = request.form['inlineRadioOptions']
        position = request.form['dropdown_1']
        goal = request.form['inlineRadioOptions10']
        data = {"player_number": player_number,
                "position": position,
                "goal": goal
                }
        print("data", data)
        save_data(data)

    return render_template("check.html")


def save_data(data):
    # repo_df = import_database_from_csv("../tmp/dataset.csv")
    # output = pd.DataFrame()
    # output = output.append(data, ignore_index=True)
    DATASET.append(data)
    print("DATASET", DATASET)
    save_dataset(DATASET)





def import_database_from_csv(filepath):
    try:
        repo_df = pd.read_csv(filepath)
    except:
        repo_df = pd.DataFrame(columns=["player_number", "position", "goal"])
    return repo_df


def save_dataset(repo_df):
    with open("../tmp/dataset.csv", "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=DATASET[0].keys(),)
        dict_writer.writeheader()
        dict_writer.writerows(DATASET)

@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "../tmp/dataset.csv"
    return send_file(path, as_attachment=True)




if __name__ == "__main__":
    app.run(port=5000, debug=True)
    import_database_from_csv("../tmp/dataset.csv")
