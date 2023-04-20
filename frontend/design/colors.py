import scheduling.planning as pl


def importance_color(importance: pl.Importance):
    if importance.value == 0:
        return [1, 1, 1, 1]
    elif importance.value == 1:
        return [1, 1, 0, 1]
    elif importance.value == 2:
        return [1, 0.35, 0, 1]
    elif importance.value == 3:
        return [1, 0, 0, 1]
    else:
        raise "unexpected importance type"
