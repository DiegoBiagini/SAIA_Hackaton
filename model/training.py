
from pathlib import Path
from dataset import MBADataset
from model import TSPrediction
import torch
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence

BATCH_SIZE = 16
def batch_collate(data):
    X = [data[i][0] for i in range(BATCH_SIZE)]
    target = [data[i][1] for i in range(BATCH_SIZE)]
    X = pad_sequence(X, batch_first=True)

    return (X, torch.stack(target))



def train_model(model, ds, n_epochs, device):
    model.to(device)

    train_checkpointing = True
    optimizer = torch.optim.AdamW(params=model.parameters(), lr=10e-4, weight_decay=1e-5)
    loss_fn = torch.nn.SmoothL1Loss()

    for epoch in range(0, n_epochs+1):
        print("Epoch:", epoch)

        batched_ds = DataLoader(ds, batch_size=BATCH_SIZE, shuffle=True, collate_fn=batch_collate)
        
        model.train()
        epoch_losses = []
        for batch, batch_data in enumerate(batched_ds):

            
            X = batch_data[0].to(device)
            y = batch_data[1].to(device)

            # Forward and backward pass
            optimizer.zero_grad(set_to_none=True)

            logits = model(X)
            loss = loss_fn(logits, y)

            loss.backward()
            optimizer.step()
            
            loss = loss.item()
            
            epoch_losses += [loss]
            
            if device == 'cuda':
                torch.cuda.empty_cache() 
            
            # Stop early, no time to train
            if batch == 150:
                current = batch * X.shape[0]

                print(f"loss: {loss:>7f} [{current:>5d}/{len(ds):>5d}]")
                break
        
        train_loss = torch.mean(torch.as_tensor(epoch_losses))
        print(f"Train loss:{train_loss:>7f}")


        # Save train state (model params, optimizer state, epoch) only for the last epoch
        if train_checkpointing:

            epoch_train_state_path = ("model/weights.tar")
            torch.save({
                #'epoch': epoch,
                'model_state_dict': model.state_dict(),
                #'optimizer_state_dict': optimizer.state_dict(),
                'outsize' : model.out_size,
            }, epoch_train_state_path)
            print("Checkpointed train state in :", epoch_train_state_path)



def end_to_end_training(device):
    orders = Path("dataset/orders.csv")
    products = Path("dataset/products.csv")
    all_order_products = Path("dataset/all_order_products.csv")

    ds = MBADataset(products, orders, all_order_products)


    model = TSPrediction(ds.n_products)

    train_model(model, ds, 5, device)

if __name__ == "__main__":
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    end_to_end_training(device)