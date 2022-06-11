import torch
from torch.utils.data import Dataset
import pandas as pd


class MBADataset(Dataset):

    def __init__(self, products, orders, product_order):

        self.products_df = pd.read_csv(products)
        self.orders_df = pd.read_csv(orders)
        self.product_order_df =pd.read_csv(product_order)

        self.n_customers = len(self.orders_df["user_id"].unique())
        self.n_products = len(self.products_df["product_id"].unique())
    
    def __len__(self):
        return self.n_customers

    def __getitem__(self, idx):
        actual_idx = idx+1
        # Get all orders for the customer
        user_orders = self.orders_df[self.orders_df["user_id"] == actual_idx]


        orders_rows = self.product_order_df[self.product_order_df["order_id"].isin(user_orders["order_id"])]

        grouped_orders = orders_rows.groupby("order_id")

        orders_tensors = []
        for g, gd in grouped_orders:
            product_ids = [ p-1 for p in list(gd["product_id"])]
            coordinates = torch.stack([torch.zeros((len(product_ids))),torch.as_tensor(product_ids)])
            sparse_tensor = torch.sparse_coo_tensor(coordinates, torch.ones((len(product_ids))), (1,self.n_products))
            orders_tensors.append(sparse_tensor)

        target_tensor = torch.squeeze(orders_tensors[-1].to_dense())
        x = torch.squeeze(torch.stack(orders_tensors[:-1]).to_dense()).view(-1,self.n_products)
        return x, target_tensor

