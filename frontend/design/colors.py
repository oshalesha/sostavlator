def task_category_color(cat):
    if cat == 0:
        return 1, 1, 1, 1
    elif cat == 1:
        return 1, 0, 0, 1
    elif cat == 2:
        return 0, 1, 0, 1
    elif cat == 3:
        return 0, 0, 1, 1
    elif cat == 4:
        return 1, 1, 0, 1



def task_importance_color(imp):
    if imp == 0:
        return 1, 1, 1, 1
    elif imp == 1:
        return 1, 1, 0, 1
    elif imp == 2:
        return 1, 0.35, 0, 1
    else:
        return 1, 0, 0, 1

