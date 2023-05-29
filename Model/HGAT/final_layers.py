from turtle import home
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
# import GPUtil

class NodeAttentionLayer(nn.Module):    
    def __init__(self, o_dim, t_dim, drop_out, out_features, device, concat=True,):
        
        super(NodeAttentionLayer, self).__init__()
        self.o_dim = o_dim
        self.t_dim= t_dim
        self.out_features = out_features
        self.drop_out = drop_out
        self.concat = concat
        self.device = device
    
        self.W_i = nn.Linear(self.o_dim, self.out_features).to(self.device) # [T_n, Out]  linear transformation weight smatrix   
        self.W_j = nn.Linear(self.t_dim, self.out_features).to(self.device) # [T_n, Out]  linear transformation weight matrix
        
        self.W_ij = nn.Parameter(torch.zeros(size=( 1, 2 * self.out_features  ))).to(self.device)
        
        nn.init.xavier_uniform_(self.W_i.weight.data, 1.414)
        nn.init.xavier_uniform_(self.W_j.weight.data, 1.414)

        nn.init.xavier_uniform_(self.W_ij.data, gain=1.414)

        self.leakyrelu = nn.LeakyReLU(0.1)

    def forward(self, h_i, h_j):
        z_i = self.W_i(h_i)        
        
        N_i = h_i.shape[0]
        N_j = h_j.shape[0]

        Z_J = torch.zeros(N_j, self.o_dim).to(self.device)
        
        if N_j:
            e = torch.zeros(N_j,1)
            for n, j in enumerate(h_j):   
                z_j = self.W_j(j) 
                Z_J[n] = z_j                
                e[n] = self.leakyrelu( torch.mm(self.W_ij, torch.cat([ z_i, z_j ]).view(2*self.out_features,1) ) ).unsqueeze(0)  # 두 벡터 간의 score                
        else:
            e = torch.rand(N_j,1)

        alpha = F.softmax(e, dim=0).to(self.device)
        
        h_i_r = torch.mm(alpha.T, Z_J)
        # h_i_r = Z_J.view(N_j, self.o_dim) * alpha
        h_i_r = F.elu( h_i_r.sum(0))
        
        
        return h_i_r.unsqueeze(0)

    def __repr__(self):
        return self.__class__.__name__ + ' (' + str(self.t_in_features) + ' -> ' + str(self.out_features) + ')'

class RelationAttentionLayer(nn.Module):

    def __init__(self, r_dim, out_features, device):
        super(RelationAttentionLayer, self).__init__()  
                        
        self.device = device
        self.r_dim = r_dim
        self.out_features = out_features
        
        self.W = nn.Parameter(torch.zeros(size=(self.out_features , self.out_features )), requires_grad=True).to(self.device)
        nn.init.xavier_uniform_(self.W.data, gain=1.414)
        self.b = nn.Parameter(torch.zeros(size=( 1, self.out_features )), requires_grad=True).to(self.device)
        nn.init.xavier_uniform_(self.b.data, gain=1.414)
        self.q = nn.Parameter(torch.zeros(size=( 1, self.out_features )), requires_grad=True).to(self.device)
        nn.init.xavier_uniform_(self.q.data, gain=1.414)

        self.Tanh = nn.Tanh()
                
        
    def forward(self, rels ):
        w_ir = torch.zeros(rels[0].shape[0], 1).to(self.device)

        for h_ir in rels:
            h_ir = h_ir.view(h_ir.shape[0], h_ir.shape[2])
            h_ir = torch.mm(h_ir, self.W)
            h_ir = h_ir + self.b
            h_ir = self.Tanh(h_ir)
                        
            h_ir = torch.mm(h_ir, self.q.T)
            
            w_ir += h_ir
        
        B_ir = F.softmax(w_ir, dim=0)
        
        h_i = (B_ir * rels[0].squeeze(1)) + (B_ir * rels[1].squeeze(1)) + (B_ir * rels[2].squeeze(1))

        return h_i

    def __repr__(self):
        return self.__class__.__name__ + ' (' + str(self.in_features) + ' -> ' + str(self.out_features) + ')'

