import pandas as pd
import os
import sys

import torch
from torch import nn
from tqdm import tqdm

import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import BatchSampler, RandomSampler

import joblib
from core.config import MODEL_NAME, MODEL_PATH, MODEL_ABS_PATH

sys.path.append(MODEL_ABS_PATH)
from HGAT.models import HGAT
from HGAT.dataset import recipe_dataset
from HGAT.args import config


def load(load_wrapper=joblib.load):
    cur_path = os.path.dirname(os.path.abspath(__file__))
    args = config()
    path = '/recipe_Data/recipe_data/'
    path = cur_path + path

    recipe_ingredient = pd.read_csv(os.path.join(path, '레시피_재료_내용_raw.csv'))
    recipe_ingredient.dropna(subset=['재료_아이디'],inplace=True)

    train = pd.read_csv(os.path.join(path, 'train셋(73609개-220603_192931).csv'))
    test = pd.read_csv(os.path.join(path, 'test셋(4422개-220603_192931).csv'))

    dataset = recipe_dataset( train,test, recipe_ingredient ,args.user_dimension)
    users, recipes, ings = dataset.get_user_recipe_ing()

    if args.load_interaction:
        interaction = torch.load(cur_path + '/recipe_Data/data/interaction.pt').to(args.device)
    else:  
        data = pd.concat([train,test])
        user2idx = dataset.user2idx
        recipe2idx = dataset.recipe2idx
        interaction = torch.zeros(len(users), len(recipes)).to(args.device)

        for u in tqdm(data.유저_아이디.unique()):
            u_idx = user2idx[u]
            for r in data[data.유저_아이디==u].레시피_아이디.unique():
                r_idx = recipe2idx[r]
                interaction[u_idx][r_idx] = 1
        torch.save(interaction, cur_path + '/recipe_Data/data/interaction.pt') 

    model = HGAT(
            user_dim = args.user_dimension, 
            dim_list = [args.recipe_dimension], 
            n_hidden_unit = args.hidden_unit, 
            r_hidden_unit = args.hidden_unit, 
            nclass = len(recipes), 
            n_dropout = args.drop_out, 
            r_dropout = args.drop_out, 
            alpha = args.alpha, 
            nheads = args.n_heads,
            device = args.device
            )     
    
    model.load_state_dict(torch.load(cur_path + '/recipe_Data/model_save/best_model.pt'))
    joblib.dump(model, f"{MODEL_PATH}/{MODEL_NAME}")
    model = load_wrapper(f"{MODEL_PATH}/{MODEL_NAME}")
    
    user_emb = dataset.user_embedding.weight.to(args.device)
    recipe_emb = dataset.recipe_embedding.weight.to(args.device)
    ing_emb = dataset.ing_embedding.weight.to(args.device)

    return model, user_emb, recipe_emb, ing_emb, interaction

if __name__=="__main__":
    load()
    print("load completed!")