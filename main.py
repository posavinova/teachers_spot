import pandas as pd


def process_class(df):
    df.columns = ["name", "sex", "hand", "glasses", "height"]
    df["sex"] = df["sex"].replace(
        {
            "М": "M",
            "Ж": "F"
        }
    ).infer_objects(copy=False)

    df["hand"] = df["hand"].replace(
        {
            "правая": "R",
            "левая": "L",
        }
    ).infer_objects(copy=False)

    df["height"] = df["height"].replace(
        {
            "низкий": 1,
            "средний": 2,
            "высокий": 3
        }
    ).infer_objects(copy=False)

    df = df.sort_values(["height", "glasses"], ascending=(True, False))
    df1 = df[:12]
    df2 = df[12:18]
    df3 = df[18:]
    return df1, df2, df3


def mix_students(df):
    # setting general priority list by sight and height
    df_b = df.loc[df["sex"] == "M"].sample(frac=1).reset_index(drop=True)

    df_g = df.loc[df["sex"] == "F"].sample(frac=1).reset_index(drop=True)

    if len(df_g) > len(df_b):
        to_div = [index for index in list(df_g.index) if index not in list(df_b.index)]
        to_add = df_g.iloc[len(df_b)+len(df_g.iloc[to_div[0]:]) // 2:]
        df_g = df_g.iloc[:len(df_b)+len(df_g.iloc[to_div[0]:]) // 2]
        df_b = pd.concat([df_b, to_add], ignore_index=True)
        mixed = pd.concat([df_g.reset_index(drop=True), df_b.reset_index(drop=True)], axis=1)

    elif len(df_g) < len(df_b):
        to_div = [index for index in list(df_b.index) if index not in list(df_g.index)]
        to_add = df_b.iloc[len(df_g)+len(df_b.iloc[to_div[0]:]) // 2:]
        df_b = df_b.iloc[:len(df_g)+len(df_b.iloc[to_div[0]:]) // 2]
        df_g = pd.concat([df_g, to_add], ignore_index=True)
        mixed = pd.concat([df_b.reset_index(drop=True), df_g.reset_index(drop=True)], axis=1)

    else:
        mixed = pd.concat([df_b.reset_index(drop=True), df_g.reset_index(drop=True)], axis=1)

    mixed.fillna("*здесь пусто*", inplace=True)

    pairs = mixed[["name", "hand"]].values.tolist()

    # rule for left- and right-handed students
    for pair in pairs:
        if pair[2] == "R" and pair[3] == "L":
            pair[0], pair[1] = pair[1], pair[0]

    pairs = [pair[:2] for pair in pairs]
    filtered = " ".join([" ".join(str(x) for x in pair) for pair in pairs]).split()

    list_length = len(filtered)
    paired_list = [filtered[i] + " " + filtered[i + 1] for i in range(0, list_length - 1, 2)]
    if list_length % 2 == 1:
        paired_list.append(filtered[list_length - 1])
    return paired_list


def make_html(filtered):
    html_plan = """<!DOCTYPE html>
    <head>
    <META charset="utf-8">
    <title>Desks Schema</title>
    <style>
    h1 {
    text-align: center;
    font-family: cursive;
    color: #333366;
    }
    table    {
    font-family: cursive;
    color: #333366;
    }
    </style>
    </head>
    <h1>План рассадки учеников</h1>
    """
    row = """
    <table width="95%" align="center">
            <tr>
                <td align="center" valign="top" width="10%"><img src=https://pickimage.ru/wp-content/uploads/images/detskie/schooldesk/parta5.jpg alt="desk" width="80%"></td>
                <td align="center" valign="top" width="10%"><img src=https://pickimage.ru/wp-content/uploads/images/detskie/schooldesk/parta5.jpg alt="desk" width="80%"></td>
                <td width="3%" rowspan="3"></td>
                <td align="center" valign="top" width="10%"><img src=https://pickimage.ru/wp-content/uploads/images/detskie/schooldesk/parta5.jpg alt="desk" width="80%"></td>
                <td align="center" valign="top" width="10%"><img src=https://pickimage.ru/wp-content/uploads/images/detskie/schooldesk/parta5.jpg alt="desk" width="80%"></td>
                <td width="3%" rowspan="3"></td>
                <td align="center" valign="top" width="10%"><img src=https://pickimage.ru/wp-content/uploads/images/detskie/schooldesk/parta5.jpg alt="desk" width="80%"></td>
                <td align="center" valign="top" width="10%"><img src=https://pickimage.ru/wp-content/uploads/images/detskie/schooldesk/parta5.jpg alt="desk" width="80%"></td>
            </tr>
            <tr>
                <td align="center" valign="top" width="10%">{}</td>
                <td align="center" valign="top" width="10%">{}</td>
                <td align="center" valign="top" width="10%">{}</td>
                <td align="center" valign="top" width="10%">{}</td>
                <td align="center" valign="top" width="10%">{}</td>
                <td align="center" valign="top" width="10%">{}</td>
            </tr>
            <tr>
                <td colspan="8" height="10"></td>
            </tr>
    </table>
    """
    while not len(filtered) % 6 == 0:
        filtered.append("*здесь пусто*")
    rows = row * (len(filtered) // 6)
    rows = rows.format(*filtered)
    html_plan += rows

    return html_plan
