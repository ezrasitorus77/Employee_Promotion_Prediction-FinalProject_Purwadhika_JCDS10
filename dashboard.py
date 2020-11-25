import plotly, pandas as pd, json, joblib, plotly.graph_objs as go
from flask import Flask, render_template, request

app = Flask(__name__)

def category_plot(
    cat_plot = "histplot",
    cat_x = "department", cat_y = "avg_training_score",
    estimator = "count", hue = "is_promoted"):

    if cat_plot == "histplot":
        data = []
        for val in df[hue].unique():
            hist = go.Histogram(
                x = df[df[hue] == val][cat_x],
                y = df[df[hue] == val][cat_y],
                histfunc = estimator,
                name = "Promoted" if val == 1 else "Not Promoted"
            )
            data.append(hist)
        title = "Histogram"

    elif cat_plot == "boxplot":
        data = []

        for val in df[hue].unique():
            box = go.Box(
                x = df[df[hue] == val][cat_x],
                y = df[df[hue] == val][cat_y],
                name = "Promoted" if val == 1 else "Not Promoted"
            )
            data.append(box)
        title = "Box"

    if cat_plot == "histplot":
        layout = go.Layout(
            title = title,
            xaxis = dict(title = cat_x),
            yaxis = dict(title = "employees"),
            boxmode = "group"
        )

    else:
        layout = go.Layout(
            title = title,
            xaxis = dict(title = cat_x),
            yaxis = dict(title = cat_y),
            boxmode = "group"
        )

    result = {"data" : data, "layout" : layout}

    graphJSON = json.dumps(result, cls = plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route("/")
def index():
    plot = category_plot()
    list_plot = [("histplot", "Histogram"), ("boxplot", "Box")]
    list_x = [("department", "Department"), ("education", "Education"), ("gender", "Gender"), ("recruitment_channel", "Recruitment Channel"), ("ageRange", "Age"), ("serviceRange", "Length of Service"), ("region", "Region")]
    list_y = [("avg_training_score", "Average Training Score"), ("previous_year_rating", "Previous Year Rating"), ("no_of_trainings", "Number of Trainings")]
    list_est = [("count", "Count")]
    list_hue = [("is_promoted", "Promotion Decision")]

    return render_template(
        "category.html",
        plot = plot,
        focus_plot = "histplot",
        focus_x = "department",
        focus_estimator = "count",
        focus_hue = "is_promoted",
        drop_plot = list_plot,
        drop_x = list_x,
        drop_y = list_y,
        drop_estimator = list_est,
        drop_hue = list_hue)
 
@app.route("/cat_fn/<nav>")
def cat_fn(nav):
    if nav == "True":
        cat_plot = "histplot"
        cat_x = "department"
        cat_y = "avg_training_score"
        estimator = "count"
        hue = "is_promoted"
    
    else:
        cat_plot = request.args.get("cat_plot")
        cat_x = request.args.get("cat_x")
        cat_y = request.args.get("cat_y")
        estimator = request.args.get("estimator")
        hue = request.args.get("hue")

    if estimator == None:
        estimator = "count"
    
    if cat_y == None:
        cat_y = "age"

    list_plot = [("histplot", "Histogram"), ("boxplot", "Box")]
    list_x = [("department", "Department"), ("education", "Education"), ("gender", "Gender"), ("recruitment_channel", "Recruitment Channel"), ("ageRange", "Age Range"), ("serviceRange", "Length of Service")]
    list_y = [("avg_training_score", "Average Training Score"), ("previous_year_rating", "Previous Year Rating"), ("no_of_trainings", "Number of Trainings")]
    list_est = [("count", "Count")]
    list_hue = [("is_promoted", "Promotion Decision")]

    plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)
    return render_template(
        "category.html",
        plot = plot,
        focus_plot = cat_plot,
        focus_x = cat_x,
        focus_y = cat_y,
        focus_estimator = estimator,
        focus_hue = hue,
        drop_plot = list_plot,
        drop_x = list_x,
        drop_y = list_y,
        drop_estimator = list_est,
        drop_hue = list_hue
    )

def scatter_plot(cat_x, cat_y, hue):
    data = []

    for val in df[hue].unique():
        scatt = go.Scatter(
            x = df[df[hue] == val][cat_x],
            y = df[df[hue] == val][cat_y],
            mode = "markers",
            name = "Promoted" if val == 1 else "Not Promoted"
        )
        data.append(scatt)

    layout = go.Layout(
        title = "Scatter",
        title_x = 0.5,
        xaxis = dict(title = cat_x),
        yaxis = dict(title = cat_y)
    )

    result = {"data" : data, "layout" : layout}

    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route("/scatt_fn")
def scatt_fn():
    cat_x = request.args.get("cat_x")
    cat_y = request.args.get("cat_y")
    hue = request.args.get("hue")

    if cat_x == None and cat_y == None and hue == None:
        cat_x = "age"
        cat_y = "no_of_trainings"
        hue = "is_promoted"

    list_x = [("age", "Age"), ("length_of_service", "Length of Service"), ("avg_training_score", "Average Training Score"), ("no_of_trainings", "Number of Trainings"), ("previous_year_rating", "Previous Year Rating")]
    list_y = [("age", "Age"), ("length_of_service", "Length of Service"), ("avg_training_score", "Average Training Score"), ("no_of_trainings", "Number of Trainings"), ("previous_year_rating", "Previous Year Rating")]
    list_hue = [("is_promoted", "Promotion Decision")]

    plot = scatter_plot(cat_x, cat_y, hue)

    return render_template(
        "scatter.html",
        plot = plot,
        focus_x = cat_x,
        focus_y = cat_y,
        focus_hue = hue,
        drop_x = list_x,
        drop_y = list_y,
        drop_hue = list_hue
    )

def pie_plot(hue = "is_promoted"):
    vcounts = df[hue].value_counts()

    labels = []
    values = []
    for item in vcounts.iteritems():
        labels.append(str(item[0]))
        values.append(item[1])
    
    data = [
        go.Pie(
            labels = labels,
            values = values
        )
    ]

    layout = go.Layout(title = "Pie", title_x = 0.48)

    result = {"data" : data, "layout" : layout}

    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route("/pie_fn")
def pie_fn():
    hue = request.args.get("hue")

    if hue == None:
        hue = "is_promoted"

    list_hue = [("is_promoted", "Promotion Decision"), ("KPIs_met_above80%", "KPIs Achievement"), ("awards_won?", "Winning Awards"), ("gender", "Gender"), ("previous_year_rating", "Previous Year Rating"), ("education", "Education")]

    plot = pie_plot(hue)
    return render_template(
        "pie.html",
        plot = plot,
        focus_hue = hue,
        drop_hue = list_hue
    )

@app.route("/pred_lr")
def pred_lr():
    return render_template("predict.html")

@app.route("/pred_result", methods = ["POST", "GET"])
def pred_result():
    if request.method == "POST":
        input = request.form
        
        if input["education"] == "Below Secondary":
            education = 0
        elif input["education"] == "Bachelor's":
            education = 1
        else:
            education = 2

        rating = float(input["rating"])

        if input["kpi"] == "Below 80%":
            kpi = 0
        else:
            kpi = 1

        if input["awards"] == "Yes":
            awards = 1
        else:
            awards = 0
        
        sr, a, count = [y for y in range(1, 37, 2)], int(input["service"]), -1
        for i, r in enumerate(sr):
            count += 1
            try:
                if (r + count) <= a <= (sr[i + 1] + count):
                    service = i
                    break

                elif (sr[i + 1] + count + 1) <= a <= (sr[i + 2] + count + 1):
                    service = i + 1
                    break

            except:
                service = i + 1
                break

        tr, z = [x for x in range(39, 99, 10)], int(input["trainingsScore"])
        if tr[0] <= z <= tr[1]:
            trainingsScore = 0
        elif tr[1] + 1 <= z <= tr[2]:
            trainingsScore = 1
        elif tr[2] + 1 <= z <= tr[3]:
            trainingsScore = 2
        elif tr[3] + 1 <= z <= tr[4]:
            trainingsScore = 3
        elif tr[4] + 1 <= z <= tr[5]:
            trainingsScore = 4
        else:
            trainingsScore = 5

        if input["channel"] == "Other":
            channel = (1, 0, 0)
        elif input["channel"] == "Referred":
            channel = (0, 1, 0)
        else:
            channel = (0, 0, 1)
        
        if int(input["trainingsNum"]) > 6:
            trainingsNum = 1
        else:
            trainingsNum = 0

        dept = input["department"]
        if (dept == "Technology") or (dept == "Legal"):
            isTechLegal = 1
        else:
            isTechLegal = 0

        if dept == "Analytics":
            department = (1, 0, 0, 0, 0, 0, 0, 0, 0)
        elif dept == "Finance":
            department = (0, 1, 0, 0, 0, 0, 0, 0, 0)
        elif dept == "HR":
            department = (0, 0, 1, 0, 0, 0, 0, 0, 0)
        elif dept == "Legal":
            department = (0, 0, 0, 1, 0, 0, 0, 0, 0)
        elif dept == "Operations":
            department = (0, 0, 0, 0, 1, 0, 0, 0, 0)
        elif dept == "Procurement":
            department = (0, 0, 0, 0, 0, 1, 0, 0, 0)
        elif dept == "R&D":
            department = (0, 0, 0, 0, 0, 0, 1, 0, 0)
        elif dept == "Sales & Marketing":
            department = (0, 0, 0, 0, 0, 0, 0, 1, 0)
        else:
            department = (0, 0, 0, 0, 0, 0, 0, 0, 1)

        temp = pd.DataFrame([
            {
                "previous_year_rating" : rating,
                "KPIs_met_above80%" : kpi,
                "awards_won?" : awards,
                "eduInt" : education,
                "isTechLegal" : isTechLegal,
                "isTrainAbv6" : trainingsNum,
                "serviceRangeInt" : service,
                "avgTrainRange" : trainingsScore,
                "department_Analytics" : department[0],
                "department_Finance" : department[1],
                "department_HR" : department[2],
                "department_Legal" : department[3],
                "department_Operations" : department[4],
                "department_Procurement" : department[5],
                "department_R&D" : department[6],
                "department_Sales & Marketing" : department[7],
                "department_Technology" : department[8],             
                "recruitment_channel_other" : channel[0],
                "recruitment_channel_referred" : channel[1],
                "recruitment_channel_sourcing" : channel[2]
               }
            ]
        )

        pred = round((model.predict_proba(temp)[0][1]), 2)

        return render_template("result.html",
            rating = int(rating),
            kpis = input["kpi"],
            awards = input["awards"],
            edu = input["education"],
            trainnum = input["trainingsNum"] + " trainings",
            servicerange = str(input["service"]) + " years",
            avgts = int(input["trainingsScore"]),
            depart = input["department"],
            recruitmentchannel = input["channel"],
            pred = str(pred) + "% promote"
            )

if __name__ == "__main__":
    df = pd.read_csv("./static/fullprocesseddata.csv").rename(
        columns = {"KPIs_met >80%" : "KPIs_met_above80%"}
    )
    model = joblib.load("./bestModel")
    app.run(debug = True)