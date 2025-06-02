def calculate_PFC(calories: int, goal: str, weight_str: int) -> tuple[int, int, int]:
    weight = int(weight_str)
    match goal:
        case "weight_gain":
            print("YES")
            protein: float = weight * 1.8
            fat: float = (calories * 0.25) / 9
            carbohydrates: float = weight*5
        case "weight_loss":
            protein: float = weight * 1.2
            fat: float = (calories * 0.3) / 9
            carbohydrates: float = weight*3
        case "maintenance":
            protein: float = weight * 1.2
            fat: float = (calories * 0.3) / 9
            carbohydrates: float = weight*4
        case _:
            protein: float = (calories * 0.25) / 4
            fat: float = (calories * 0.3) / 9
            carbohydrates: float = (calories * 0.45) / 4
    return int(protein), int(fat), int(carbohydrates)