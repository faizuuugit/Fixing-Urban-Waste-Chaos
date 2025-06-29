from bin_simulator import generate_fake_bins
from urgency_scorer import score_bin
from route_planner import plan_route
from bin_selector import select_bins_by_capacity
from report_writer import generate_daily_report

# 🚮 Step 1: Simulate bins
print("🚮 Simulating 5 Bins...\n")
bins = generate_fake_bins()

# 🧠 Step 2: Score bins with Granite
print("🧠 Scoring Bins using IBM Granite...\n")
for bin_data in bins:
    score = score_bin(bin_data)
    bin_data["Urgency Score"] = score

# 🚛 Step 3: Select bins that fit in the truck
TRUCK_CAPACITY = 150 
selected_bins = select_bins_by_capacity(bins, TRUCK_CAPACITY)

# 🗂 Step 4: Sort selected bins by urgency (for human view)
sorted_bins = sorted(selected_bins, key=lambda x: x["Urgency Score"], reverse=True)
print(f"🚛 Bins selected to fit within {TRUCK_CAPACITY}L capacity:\n")
total_volume = 0
for idx, bin_data in enumerate(sorted_bins, start=1):
    volume = bin_data['Volume']
    total_volume += volume
    print(f"{idx}. {bin_data['Bin ID']} - Urgency: {bin_data['Urgency Score']} - Waste: {bin_data['Waste Type']} - Fill: {bin_data['Fill Level']}% of {bin_data['Bin Capacity']}L = {volume}L")

print(f"\n📦 Total Waste Volume in Truck: {total_volume}L / {TRUCK_CAPACITY}L\n")


# 🧠 Step 5: Ask Granite to plan the route
print("\n🗺️ Sending selected bins to Granite for Route Planning...\n")
bin_order = plan_route(sorted_bins)

# ✅ Step 6: Display final AI-generated route
print("✅ Final Route Plan (by AI):\n")
for i, bin_id in enumerate(bin_order, start=1):
    bin_info = next((b for b in sorted_bins if b["Bin ID"] == bin_id), None)
    if bin_info:
        print(f"{i}. {bin_info['Bin ID']} - Urgency: {bin_info['Urgency Score']} - Waste: {bin_info['Waste Type']} - Fill: {bin_info['Fill Level']}%")

# 📝 Step 7: Generate summary report
print("\n📊 Generating Daily Summary Report with Granite...\n")
report = generate_daily_report(sorted_bins)
print("📄 Daily Summary Report:\n")
print(report)
