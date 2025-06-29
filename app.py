from flask import Flask, render_template, redirect, url_for, request, jsonify
from logic.bin_simulator import generate_fake_bins
from logic.urgency_scorer import score_bin
from logic.bin_selector import select_bins_by_capacity
from logic.route_planner import plan_route
from logic.report_writer import generate_daily_report

app = Flask(__name__)

bins = []
bin_order = []
collected = set()
report = ""
TRUCK_CAPACITY = 150
report_generated = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/demo")
def demo():
    global bins, bin_order, collected, report_generated, TRUCK_CAPACITY

    bins.clear()
    bin_order.clear()
    collected.clear()
    report_generated = False

    #  bins
    raw_bins = generate_fake_bins()
    hyderabad_names = [
        "SR Residency", "Cyber Enclave", "My Home Avatar", "Meenakshi Towers",
        "Lodha Bellezza", "Aparna Sarovar", "SMR Vinay City", "Jubilee Homes"
    ]

    for i, b in enumerate(raw_bins):
        b["Urgency Score"] = score_bin(b)
        b["Volume"] = round((b["Fill Level"] / 100) * b["Bin Capacity"], 2)
        b["Location Name"] = hyderabad_names[i % len(hyderabad_names)]
        b["collected"] = False

    # AI selects optimal bins
    selected_bins = select_bins_by_capacity(raw_bins, TRUCK_CAPACITY)
    selected_bins.sort(key=lambda x: x["Urgency Score"], reverse=True)
    bin_order[:] = plan_route(selected_bins)

    return render_template("demo.html",
                           all_bins=raw_bins,
                           route_bins=[b for b in raw_bins if b["Bin ID"] in bin_order],
                           capacity=TRUCK_CAPACITY)


@app.route("/demo2")
def demo2():
    return render_template("demo2.html", capacity=TRUCK_CAPACITY)


@app.route("/api/demo2_data")
def demo2_data():
    global TRUCK_CAPACITY

    raw_bins = generate_fake_bins(num_bins=8) 
    hyderabad_names = [
        "SR Residency", "Cyber Enclave", "My Home Avatar", "Meenakshi Towers",
        "Lodha Bellezza", "Aparna Sarovar", "SMR Vinay City", "Jubilee Homes",
        "Fortune Heights", "Green Gates"
    ]

    for i, b in enumerate(raw_bins):
        b["Urgency Score"] = score_bin(b)
        b["Volume"] = round((b["Fill Level"] / 100) * b["Bin Capacity"], 2)
        b["Location Name"] = hyderabad_names[i % len(hyderabad_names)]

    selected_bins = select_bins_by_capacity(raw_bins, TRUCK_CAPACITY)
    selected_bins.sort(key=lambda x: x["Urgency Score"], reverse=True)
    route = plan_route(selected_bins)

    return jsonify({
        "all_bins": raw_bins,
        "route_bins": [b for b in raw_bins if b["Bin ID"] in route],
        "route_order": route
    })

@app.route("/api/generate_report", methods=["POST"])
def generate_report():
    try:
        data = request.json
        bins = data.get("bins", [])
        report = generate_daily_report(bins)
        return jsonify({"report": report})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/mark/<bin_id>")
def mark_collected(bin_id):
    collected.add(bin_id)
    return redirect(url_for("demo"))


if __name__ == "__main__":
    app.run(debug=True)
