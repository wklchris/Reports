import os
import numpy as np
import pandas as pd

def label_correcting_algo(dt, ori_node, des_node, do_return=False):
    """
    Find the shortest path from Origin to Destination under a constant-link-costs network.
    
    Args:
        dt: Network representation. At least 3 columns:
              "start": start nodes of links
              "end": end nodes of links
              "cost": constant costs of links
        ori_node: Origin node.
        des_node: Destination node.
        do_return: Boolean. 
            If True, Return a dataframe as described below.
            If False, Return the shortest path string instead.
        
    Returns:
        A dataframe of two columns:
            "Front-Node": The node visited before current node on the shortest path.
            "Distance": Total distance from origin to current node.
    """
    # Convert all labels to string
    ori = str(ori_node)
    des = str(des_node)
    dt[["start", "end"]] = dt[["start", "end"]].astype(str) 
    
    # Initialization
    nodes = set(dt.loc[:,"start"].unique()) | set(dt.loc[:,"end"].unique())
    dist = {}.fromkeys(nodes, np.inf)
    dist[ori] = 0
    points = {}.fromkeys(nodes, ori)
    iter_set = {ori}
    
    # Main Algo
    while iter_set:
        i = iter_set.pop()  # Randomly pop out a node i
        A_i = dt[dt.start == i]
        for row in A_i.index: 
            j = A_i.loc[:, "end"][row]
            c_ij = A_i.loc[:, "cost"][row]
            if dist[j] > dist[i] + c_ij:
                dist[j] = dist[i] + c_ij
                points[j] = i
                iter_set = iter_set | set([j])  # Union
    
    # Print & Return the Answer
    x = pd.concat([pd.Series(points), pd.Series(dist)], axis=1)
    x.columns = ["Front-node", "Distance"]

    current_node = des
    front_node = ""
    sp = des
    while front_node != ori:
        front_node = str(x.loc[current_node, "Front-node"])
        sp = "{} -> {}".format(front_node, sp)
        current_node = front_node
    
    sp = "From node {} to node {}, total Distance: {}\n{}\n".format(ori, des, x.loc[des, "Distance"], sp)
    if do_return:
        print(sp)
        return x
    else:
        return sp

dt_raw = pd.read_csv(r"{}/data/Label-correcting-test.csv".format(os.getcwd()))

# Delete unnecessary variables (columns)
dt_test = dt_raw.loc[:,["start", "end", "Free Flow Travel Time (min)"]]
dt_test.rename(columns={"Free Flow Travel Time (min)": "cost"}, inplace=True)

test = label_correcting_algo(dt_test, "a", "j")

# Apply to a complex network
dt_raw = pd.read_csv(r"{}/data/Label-correcting-data.csv".format(os.getcwd()))
dt_app = dt_raw.loc[:,["start", "end", "Free Flow Travel Time (min)"]]
dt_app.rename(columns={"Free Flow Travel Time (min)": "cost"}, inplace=True)

app= []
app.append(label_correcting_algo(dt_app, 1, 411))
app.append(label_correcting_algo(dt_app, 1, 300))
app.append(label_correcting_algo(dt_app, 2, 411))
app.append(label_correcting_algo(dt_app, 2, 300))

print("\n".join(app))
