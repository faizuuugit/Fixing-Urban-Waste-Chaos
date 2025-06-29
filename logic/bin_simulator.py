import random

def generate_fake_bins(num_bins=5):  # Default still 5
    waste_types = ['General', 'Recyclable', 'Organic', 'Hazardous-Simulated']
    bins = []

    for i in range(num_bins):
        capacity = random.choice([60, 80, 100])
        fill_percent = random.randint(20, 100)

        bin_data = {
            "Bin ID": f"BIN-{100 + i}",
            "Waste Type": random.choice(waste_types),
            "Days Since Last Collection": random.randint(0, 4),
            "Fill Level": fill_percent,
            "Bin Capacity": capacity,
            "Volume": round((fill_percent / 100) * capacity, 2)
        }
        bins.append(bin_data)

    return bins
