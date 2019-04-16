import json
import pandas as pd
from functools import reduce

expo = "assets/companies/eventRegistration_Expo.json"
smef = "assets/companies/eventRegistration_SMEF.json"
ie = "assets/companies/ie.json"

expo_conn = open(expo, "r")
expo_dict = json.load(expo_conn)
expo_conn.close()

smef_conn = open(smef, "r")
smef_dict = json.load(smef_conn)
smef_conn.close()

ie_conn = open(ie, "r")
ie_dict = json.load(ie_conn)
ie_conn.close()

expo_data = expo_dict["models"]
smef_data = smef_dict["models"]
ie_data = ie_dict["models"]


store_expo = list()
store_ie = list()
store_smef = list()
expo_companies = list()
ie_cols = dict()
for i in expo_data:
    name = i["name"]
    majors = i["majors"]
    majors = list(filter(lambda x: x["_id"] == 260, majors))
    if len(majors) > 0:
        ie = True
    else:
        ie = False
    work_auth = i["work_authorization"]
    work_auth = [i["_label"] for i in work_auth]
    work_auth = ', '.join(work_auth)
    industry = i["industry"]
    industry = [i["_label"] for i in industry]
    industry = ", ".join(industry)
    position = i["position_types"]
    position = [i["_label"] for i in position]
    position = ", ".join(position)

    ie_cols["cf"] = "expo"
    ie_cols["name"] = name
    ie_cols["ie"] = ie
    ie_cols["industry"] = industry
    ie_cols["position"] = position
    ie_cols["work"] = work_auth

    store_expo.append(ie_cols.copy())
    ie_cols.clear()


smef_companies = list()
for i in smef_data:
    name = i["name"]
    majors = i["majors"]
    majors = list(filter(lambda x: x["_id"] == 260, majors))
    if len(majors) > 0:
        ie = True
    else:
        ie = False
    work_auth = i["work_authorization"]
    work_auth = [i["_label"] for i in work_auth]
    work_auth = ', '.join(work_auth)
    industry = i["industry"]
    industry = [i["_label"] for i in industry]
    industry = ", ".join(industry)
    position = i["position_types"]
    position = [i["_label"] for i in position]
    position = ", ".join(position)

    ie_cols["cf"] = "smef"
    ie_cols["name"] = name
    ie_cols["ie"] = ie
    ie_cols["industry"] = industry
    ie_cols["position"] = position
    ie_cols["work"] = work_auth

    store_smef.append(ie_cols.copy())
    ie_cols.clear()

ie_companies = list()
for i in ie_data:
    name = i["name"]
    # majors = i["majors"]
    # majors = list(filter(lambda x: x["_id"] == 260, majors))
    # if len(majors) > 0:
    #     ie = True
    # else:
    #     ie = False
    work_auth = i["work_authorization"]
    work_auth = [i["_label"] for i in work_auth]
    work_auth = ', '.join(work_auth)
    industry = i["industry"]
    industry = [i["_label"] for i in industry]
    industry = ", ".join(industry)
    position = i["position_types"]
    position = [i["_label"] for i in position]
    position = ", ".join(position)

    ie_cols["cf"] = "ie"
    ie_cols["name"] = name
    ie_cols["ie"] = True
    ie_cols["industry"] = industry
    ie_cols["position"] = position
    ie_cols["work"] = work_auth

    store_ie.append(ie_cols.copy())
    ie_cols.clear()


df_ie = pd.DataFrame(store_ie)
df_smef = pd.DataFrame(store_smef)
df_expo = pd.DataFrame(store_expo)
order = ["name", "cf", "ie", "industry", "position", "work"]
df_expo_ie = df_expo.merge(df_ie, how="outer", on="name", suffixes=('_left', '_right'))
df_expo_ie_smef = df_expo_ie.merge(df_smef, how="outer", on="name")
df = df_expo_ie_smef
ie_cols = list(filter(lambda x: "ie" in x, list(df)))
for i in ie_cols:
    df[i] = df[i].apply(lambda x: False if type(x) is float else x)
df["IE"] = df['ie_left'] | df['ie_right'] | df['ie']

df.fillna("", inplace=True)

df['Career_Fairs'] = df['cf_left'] + ', ' + df['cf_right'] + ', ' + df['cf']

industry_cols = list(filter(lambda x: "industry" in x.lower(), list(df)))
work_cols = list(filter(lambda x: "work" in x.lower(), list(df)))
position_cols = list(filter(lambda x: "position" in x.lower(), list(df)))

df["Industry"] = df[industry_cols[0]] + ', ' + df[industry_cols[1]] + ', ' + df[industry_cols[2]]
df["Work"] = df[work_cols[0]] + ', ' + df[work_cols[1]] + ', ' + df[work_cols[2]]
df["Position"] = df[position_cols[0]] + ', ' + df[position_cols[1]] + ', ' + df[position_cols[2]]

drop_cols = ie_cols + industry_cols + work_cols + position_cols

df.drop(columns=["cf_left", "cf_right", "cf"], inplace=True)
df.drop(columns=drop_cols, inplace=True)
col_names = ["name", "Career_Fairs", "IE", "Industry", "Position", "Work"]
# col_names.pop(col_names.index("name"))
# col_names.pop(col_names.index("Career_Fairs"))
# col_names.pop(col_names.index("IE"))
# col_names.insert(0, "IE")
# col_names.insert(0, "Career_Fairs")
# col_names.insert(0, "name")
df = df[col_names]
df.to_excel("assets/companies/comp.xlsx", index=False)