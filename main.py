import os

import numpy as np
import pandas as pd

from time import perf_counter
from datetime import timedelta
from string import ascii_uppercase


hpb_type_dict = {
    
    0: "Fighting",
    1: "Flying",
    2: "Poison",
    3: "Ground",
    4: "Rock",
    5: "Bug",
    6: "Ghost",
    7: "Steel",
    8: "Fire",
    9: "Water",
    10: "Grass",
    11: "Electric",
    12: "Psychic",
    13: "Ice",
    14: "Dragon",
    15: "Dark"
    
}

genders_male_th = {
    
    "0:1": 0,
    "1:7": 2,
    "1:3": 4,
    "1:1": 8,
    "3:1": 12,
    "1:0": 16

}

def get_data_base(filename="gen2DVs.csv", quiete=True):

    if filename in os.listdir():

        return pd.read_csv(filename)

    t0 = perf_counter()

    df = pd.DataFrame(columns=["DVs"])

    df["DVs"] = ["0"*(16 - len(bin(i)[2:])) + bin(i)[2:] for i in np.arange(2**16)]

    df["Attackb"] = df["DVs"].str[:4]
    df["Defenseb"] = df["DVs"].str[4:4*2]
    df["Speedb"] = df["DVs"].str[4*2:4*3]
    df["Specialb"] = df["DVs"].str[4*3:4*4]

    df["Attack"] = ("0b" + df["Attackb"]).apply(lambda x: int(x, 2))
    df["Defense"] = ("0b" + df["Defenseb"]).apply(lambda x: int(x, 2))
    df["Speed"] = ("0b" + df["Speedb"]).apply(lambda x: int(x, 2))
    df["Special"] = ("0b" + df["Specialb"]).apply(lambda x: int(x, 2))

    df["HPb"] = ((df["Attack"] % 2).astype(str) + 
                (df["Defense"] % 2).astype(str) + 
                (df["Speed"] % 2).astype(str) + 
                (df["Special"] % 2).astype(str))
                
    df["HP"] = ("0b" + df["HPb"]).apply(lambda x: int(x, 2))

    df["Letter"] = ('0b' + 
                    df["Attackb"].str[1:-1] + 
                    df["Defenseb"].str[1:-1] + 
                    df["Speedb"].str[1:-1] + 
                    df["Specialb"].str[1:-1]).apply(lambda x: ascii_uppercase[int(x, 2) // 10])

    df["X"] = ("0b" + 
               (("0b" + df["Attackb"]).apply(lambda x: "1" if int(x, 2) > 7 else "0") + 
                ("0b" + df["Defenseb"]).apply(lambda x: "1" if int(x, 2) > 7 else "0") + 
                ("0b" + df["Speedb"]).apply(lambda x: "1" if int(x, 2) > 7 else "0") + 
                ("0b" + df["Specialb"]).apply(lambda x: "1" if int(x, 2) > 7 else "0"))
                ).apply(lambda x: int(x, 2))
    
    df["Y"] = np.clip(df["Special"], 0, 3)

    df["HPb_BP"] = (5 * df["X"] + df["Y"]) // 2 + 31

    df["HPb_Type"] = ("0b" + 
                     (df["Attackb"].str[-2:] + df["Defenseb"].str[-2:])
                     ).apply(lambda x: hpb_type_dict[int(x, 2)])

    df["Shiny"] = (df["Attackb"].isin(["0010", "0011", "0110", "0111", "1010", "1011", "1110", "1111"]) & 
                   (df["Defenseb"] == "1010") & 
                   (df["Speedb"] == "1010") & 
                   (df["Specialb"] == "1010"))

    for ratio, th in genders_male_th.items():
        
        df[ratio] = df["Attack"].apply(lambda x: "♂" if x >= th else "♀")

    tf = perf_counter()

    if not quiete:

        print(f"Elapsed Time: {timedelta(seconds=tf-t0)}")

    df.to_csv(filename)

    return df

if __name__ == "__main__":

    tabla = get_data_base(quiete=False)
