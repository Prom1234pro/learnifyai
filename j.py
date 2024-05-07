import json

filename = 'j.json'
v = {}
def loadd():
    with open(filename) as f:
        v = json.load(f)
        return v


def save_active_sessions(content):
    with open(filename, 'w') as file:
        json.dump(content, file)

save_active_sessions({"asdf":{"asdf":"ASDF", "dfs":"wefdsa"}})
vf = loadd()
vf["argr"] = {"efs":"sdg"}
save_active_sessions(vf)
print(loadd())