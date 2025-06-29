def select_bins_by_capacity(bins, truck_capacity):
    """
    Select bins based on urgency and actual volume, within the truck's capacity.
    Priority = urgency per liter.
    """
    # Sort bins by urgency-to-volume ratio
    scored_bins = sorted(
        bins,
        key=lambda b: b["Urgency Score"] / (b["Volume"] + 1),  # Avoid divide-by-zero
        reverse=True
    )

    selected = []
    current_total = 0

    for bin_data in scored_bins:
        volume = bin_data["Volume"]
        if current_total + volume <= truck_capacity:
            selected.append(bin_data)
            current_total += volume

    return selected
