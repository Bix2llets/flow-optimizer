def flow_fairness_metric(output_flow: list[float]):
    n = len(output_flow)
    normal_sum = sum(output_flow)
    square_sum = 0
    for value in output_flow:
        square_sum += value**2
    return normal_sum**2 / (square_sum * n) if (square_sum * n != 0) else 0
