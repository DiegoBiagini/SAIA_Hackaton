
from pathlib import Path
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import json
import torch
from model.model import TSPrediction

def load_model():
    path = Path("model/weights.tar")
    if not path.is_file():
        raise FileNotFoundError

    if torch.cuda.is_available():
        checkpoint = torch.load(path)
    else: 
        checkpoint = torch.load(path, map_location=torch.device('cpu'))
    model = TSPrediction(checkpoint["outsize"])
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model

def main():
    # Load the model
    model = load_model()
    # Load what the user currently has
    user_path = Path("user_data/history.csv")
    user_df = pd.read_csv(user_path)
    last_row = user_df.iloc[-1].fillna(0).to_numpy()[1:-1]

    # Load history for each other user
    user_history = {}
    others_path = Path("user_data/other_users")

    valid_files = [p for p in Path(others_path).glob('*.csv')]
    for file in valid_files:
        filename = file.stem
        df = pd.read_csv(file)
        df.drop("date", axis=1, inplace=True)
        #df.reset_index(drop=True, inplace=True) Why doesnt this work,...
        user_history[filename] = df.fillna(0).to_numpy()[:, 1:]
    
    user_future = {}
    for user in user_history.keys():
        # PREDICT
        np_in = user_history[user]
        tensor_in = torch.unsqueeze(torch.as_tensor(np_in), 0).float()
        with torch.no_grad():
            future = model(tensor_in).detach().numpy()

        user_future[user] = future

    user_similarity = []
    for user in user_future.keys():

        similarity = float(cosine_similarity(last_row.reshape(1,-1), user_future[user].reshape(1,-1)))
        entry = {"user_id":user, "similarity":similarity}
        user_similarity.append(entry)
    
    # Decide whether the current user should share
    can_share = True

    json_out = {"can_share":can_share, "users":user_similarity}
    out_path = Path("sharing.json")
    with open(out_path, "w") as f:
        json.dump(json_out, f)

if __name__ == "__main__":
    main()