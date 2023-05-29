import torch
import torch.nn as nn
import torch.nn.functional as F
from final_layers import NodeAttentionLayer, RelationAttentionLayer
import time

class HGAT(nn.Module):
    def __init__(self, n_user, n_recipe, n_ing ,u_dim, r_dim, i_dim, out_features, drop_out, n_heads, user_relation_matrix, recipe_relation_matrix, device):
        super(HGAT, self).__init__()
        self.n_user = n_user
        self.n_recipe = n_recipe
        self.n_ing = n_ing

        self.u_dim = u_dim
        self.r_dim = r_dim
        self.i_dim = i_dim
        self.out_features = out_features

        self.device= device
        self.drop_out = drop_out
        self.n_heads = n_heads
        
        self.user_recipe_matrix = user_relation_matrix[0]
        self.recipe_user_matrix = recipe_relation_matrix[0]
        self.recipe_recipe_matrix = recipe_relation_matrix[1]
        self.recipe_ing_matrix = recipe_relation_matrix[2]                

        self.user_embedding = nn.Embedding(n_user, u_dim)
        self.recipe_embedding = torch.load('/opt/ml/recipe/HGAT/sentence_emb/sentence_5900_emb_multilingual-cased-v1.pt')
        self.ing_embedding = torch.load('/opt/ml/recipe/HGAT/ingredient_emb/ing_emb.pt')        
        
        self.user_node_level_attentions = []
        self.recipe_node_level_attentions = []

        self.device= device
        
        self.user_node_level_attentions.append([NodeAttentionLayer(self.u_dim, self.r_dim, self.drop_out, self.u_dim,concat=True, device = self.device) for _ in range(self.n_heads)])
        
        self.recipe_node_level_attentions.append([NodeAttentionLayer(self.r_dim, self.u_dim, self.drop_out, self.r_dim, concat=True, device = self.device) for _ in range(self.n_heads)])
        self.recipe_node_level_attentions.append([NodeAttentionLayer(self.r_dim, self.r_dim, self.drop_out, self.r_dim, concat=True, device = self.device) for _ in range(self.n_heads)])
        self.recipe_node_level_attentions.append([NodeAttentionLayer(self.r_dim, self.i_dim, self.drop_out, self.r_dim, concat=True, device = self.device) for _ in range(self.n_heads)])
        
        self.relation_level_attentions = RelationAttentionLayer(self.r_dim, self.out_features, device=self.device)

        self.W_u = nn.Linear(self.n_heads * u_dim, self.out_features).to(self.device)
        self.W_r = nn.Linear(self.n_heads * r_dim, self.out_features).to(self.device)        
        nn.init.xavier_uniform_(self.W_u.weight.data, gain=1.414)
        nn.init.xavier_uniform_(self.W_r.weight.data, gain=1.414)


    def forward(self, user, item_seq):        
        start_time = time.time()
        print(start_time)
        user_rel =[]
        H_U = torch.zeros((len(user), 1, self.out_features)).to(self.device)
        for n,u in enumerate(user):
            h_user = self.user_embedding(torch.tensor([u])).to(self.device)
            user_recipes = self.user_recipe_matrix[u]
            user_recipes = self.recipe_embedding[user_recipes].to(self.device)
            h_u_r = torch.cat([ node_att(h_user, user_recipes) for node_att in self.user_node_level_attentions[0]], dim=1 )             
            h_u = self.W_u(h_u_r)
            H_U[n] = h_u
        
        print('H_U :', start_time - time.time())

        H_R_U = torch.zeros((self.recipe_embedding.shape[0], 1, self.out_features)).to(self.device)
        H_R_R = torch.zeros((self.recipe_embedding.shape[0], 1, self.out_features)).to(self.device)
        H_R_I = torch.zeros((self.recipe_embedding.shape[0], 1, self.out_features)).to(self.device)
        for n,(u,r,i) in enumerate(zip(self.recipe_user_matrix, self.recipe_recipe_matrix, self.recipe_ing_matrix)):  
            h_recipe = self.recipe_embedding[n].to(self.device)                                        
            if not i:i=[0]
            h_r_u = torch.cat([att( h_recipe, self.user_embedding( torch.tensor(u).to(torch.int64) ).view(len(u), 1, self.u_dim).to(self.device) ) for att in self.recipe_node_level_attentions[0]], dim=1)
            h_r_r = torch.cat([att( h_recipe, self.recipe_embedding[torch.tensor(r)].view(len(r),1,self.r_dim).to(self.device) ) for att in self.recipe_node_level_attentions[1]], dim=1)
            h_r_i = torch.cat([att( h_recipe, self.ing_embedding[torch.tensor(i)].view(len(i),1,self.i_dim).to(self.device) ) for att in self.recipe_node_level_attentions[2]], dim=1)  
            
            h_r_u = self.W_r(h_r_u)
            h_r_r = self.W_r(h_r_r)
            h_r_i = self.W_r(h_r_i)
            # h_recipe = F.dropout(h_recipe, self.se_dropout) ?

            H_R_U[n] = h_r_u
            H_R_R[n] = h_r_r
            H_R_I[n] = h_r_i

        print('H_R :', start_time - time.time())

        recipe_rel = [H_R_U, H_R_R, H_R_I]
        
        H_R = self.relation_level_attentions(recipe_rel) 
        
        prediction = torch.inner(H_U, H_R)

        return prediction