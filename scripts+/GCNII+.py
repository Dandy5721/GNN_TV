import argparse
import os.path as osp
import torch
import torch.nn.functional as F
import torch_geometric.transforms as T
from torch_geometric.datasets import Planetoid
from torch_geometric.logging import log
from torch_geometric.nn import GCN2Conv
import torchmetrics
from torch.nn import Linear
from torch_geometric.nn.conv.gcn_conv import gcn_norm
from utils import GTV

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='Citeseer')
parser.add_argument('--hidden_channels', type=int, default=128)
parser.add_argument('--list_number', type=int, default=16)
parser.add_argument('--lr', type=float, default=0.005)
parser.add_argument('--epochs', type=int, default=1500)
parser.add_argument('--use_gdc', action='store_true', help='Use GDC')
parser.add_argument('--wandb', action='store_true', help='Track experiment')
parser.add_argument('--use_conda', type=str, default='cuda:1')
parser.add_argument('--GTV_number', type=int, default=1)


args = parser.parse_args()

dataset = 'Cora'
path = osp.join(osp.dirname(osp.realpath(__file__)), '..', 'data', dataset)
transform = T.Compose([T.NormalizeFeatures(), T.ToSparseTensor()])
dataset = Planetoid(path, args.dataset, split='public', transform=transform)
data = dataset[0]
data.adj_t = gcn_norm(data.adj_t)

list_num=args.list_number
if list_num==16:
    list_cir = [2,1,1,1,1,1,1]
if list_num==32:
    list_cir = [4,4,4,3,3,3,3]
if list_num==64:
    list_cir = [8,8,8,8,8,8,8]
if list_num==128:
    list_cir = [18,17,17,17,17,17,17]


class Net(torch.nn.Module):
    def __init__(self, hidden_channels, num_layers, alpha, theta,
                 shared_weights=True, dropout=0.0):
        super().__init__()
        torch.manual_seed(12345)
        self.lins = torch.nn.ModuleList()
        self.lins.append(Linear(dataset.num_features, hidden_channels))
        self.lins.append(Linear(hidden_channels, dataset.num_classes))

        self.convs = torch.nn.ModuleList()
        for layer in range(num_layers):
            self.convs.append(GCN2Conv(hidden_channels, alpha, theta, layer + 1, shared_weights, normalize=False))

        self.dropout = dropout

    def forward(self, x, adj_t):
        GTV_number = args.GTV_number
        if GTV_number == 1:
        
            x = F.dropout(x, self.dropout, training=self.training)
            z = torch.zeros(x.shape[0]-1, (x.shape[-1]))
            z = z.to(x.device) 
            x, z = GTV(x,z) 
            x = x_0 = self.lins[0](x).relu()
            internal = (args.list_number)//8

            for conv in self.convs:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            # z=self.lins[0](z)
            # x, z = GTV(x,z)
                x = x.relu()

            x = F.dropout(x, self.dropout, training=self.training)
            x = self.lins[1](x)

        elif GTV_number ==2:
            x = F.dropout(x, self.dropout, training=self.training)
            z = torch.zeros(x.shape[0]-1, (x.shape[-1]))
            z = z.to(x.device) 
            x, z = GTV(x,z) 
            x = x_0 = self.lins[0](x).relu()
            internal = (args.list_number)//8

            for conv in self.convs[0:internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            z=self.lins[0](z)
            x, z = GTV(x,z)
            x = x.relu()
            for conv in self.convs[internal:2*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            # x, z = GTV(x,z)
                x = x.relu()

            for conv in self.convs[2*internal:]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            # x, z = GTV(x,z)
                x = x.relu()


            x = F.dropout(x, self.dropout, training=self.training)
            x = self.lins[1](x)

        elif GTV_number ==3:
            x = F.dropout(x, self.dropout, training=self.training)
            z = torch.zeros(x.shape[0]-1, (x.shape[-1]))
            z = z.to(x.device) 
            x, z = GTV(x,z) 
            x = x_0 = self.lins[0](x).relu()
            internal = (args.list_number)//8

            for conv in self.convs[0:internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            z=self.lins[0](z)
            x, z = GTV(x,z)
            x = x.relu()
            for conv in self.convs[internal:2*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[2*internal:]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            # x, z = GTV(x,z)
                x = x.relu()

            x = F.dropout(x, self.dropout, training=self.training)
            x = self.lins[1](x)    

        elif GTV_number ==4:
            x = F.dropout(x, self.dropout, training=self.training)
            z = torch.zeros(x.shape[0]-1, (x.shape[-1]))
            z = z.to(x.device) 
            x, z = GTV(x,z) 
            x = x_0 = self.lins[0](x).relu()
            internal = (args.list_number)//8

            for conv in self.convs[0:internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            z=self.lins[0](z)
            x, z = GTV(x,z)
            x = x.relu()
            for conv in self.convs[internal:2*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[2*internal:3*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[3*internal:]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            # x, z = GTV(x,z)
                x = x.relu()

            x = F.dropout(x, self.dropout, training=self.training)
            x = self.lins[1](x)        

        elif GTV_number ==5:
            x = F.dropout(x, self.dropout, training=self.training)
            z = torch.zeros(x.shape[0]-1, (x.shape[-1]))
            z = z.to(x.device) 
            x, z = GTV(x,z) 
            x = x_0 = self.lins[0](x).relu()
            internal = (args.list_number)//8

            for conv in self.convs[0:internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            z=self.lins[0](z)
            x, z = GTV(x,z)
            x = x.relu()
            for conv in self.convs[internal:2*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[2*internal:3*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[3*internal:4*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[4*internal:]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            # x, z = GTV(x,z)
                x = x.relu()

            x = F.dropout(x, self.dropout, training=self.training)
            x = self.lins[1](x)

        elif GTV_number ==6:
            x = F.dropout(x, self.dropout, training=self.training)
            z = torch.zeros(x.shape[0]-1, (x.shape[-1]))
            z = z.to(x.device) 
            x, z = GTV(x,z) 
            x = x_0 = self.lins[0](x).relu()
            internal = (args.list_number)//8

            for conv in self.convs[0:internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            z=self.lins[0](z)
            x, z = GTV(x,z)
            x = x.relu()
            for conv in self.convs[internal:2*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[2*internal:3*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[3*internal:4*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[4*internal:5*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[5*internal:]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
                x = x.relu()

            x = F.dropout(x, self.dropout, training=self.training)
            x = self.lins[1](x)

        elif GTV_number ==7:
            x = F.dropout(x, self.dropout, training=self.training)
            z = torch.zeros(x.shape[0]-1, (x.shape[-1]))
            z = z.to(x.device) 
            x, z = GTV(x,z) 
            x = x_0 = self.lins[0](x).relu()
            internal = (args.list_number)//8

            for conv in self.convs[0:internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            z=self.lins[0](z)
            x, z = GTV(x,z)
            x = x.relu()
            for conv in self.convs[internal:2*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[2*internal:3*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[3*internal:4*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[4*internal:5*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[5*internal:6*internal-1]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            x, z = GTV(x,z)
            x = x.relu()

            for conv in self.convs[6*internal:]:
                x = F.dropout(x, self.dropout, training=self.training)
                x = conv(x, x_0, adj_t)
            # x, z = GTV(x,z)
                x = x.relu()            

            x = F.dropout(x, self.dropout, training=self.training)
            x = self.lins[1](x)

        return x.log_softmax(dim=-1)

# args.cuda = not args.no_cuda and torch.cuda.is_available()
# device = torch.cuda.set_device(args.device_number)
connda = args.use_conda
device = torch.device(args.use_conda if torch.cuda.is_available() else 'cpu')
model = Net(hidden_channels=args.hidden_channels, num_layers=62, alpha=0.1, theta=0.5,
            shared_weights=True, dropout=0.6).to(device)
data = data.to(device)
optimizer = torch.optim.Adam([
    dict(params=model.convs.parameters(), weight_decay=0.01),
    dict(params=model.lins.parameters(), weight_decay=5e-4)
], lr=args.lr) 


def train():
    model.train()
    optimizer.zero_grad()
    out = model(data.x, data.adj_t)
    loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()
    return float(loss)


@torch.no_grad()
def test():
    model.eval()
    pred = model(data.x, data.adj_t).argmax(dim=-1)

    precision = torchmetrics.Precision(task="multiclass", average='weighted', num_classes=dataset.num_classes).to(device)
    pre = precision(pred[data.test_mask], data.y[data.test_mask])
    recall = torchmetrics.Recall(task="multiclass", average='weighted', num_classes=dataset.num_classes).to(device)
    rec = recall(pred[data.test_mask], data.y[data.test_mask])
    f1score = torchmetrics.F1Score(task="multiclass", average='weighted', num_classes=dataset.num_classes).to(device)
    f1 = f1score(pred[data.test_mask], data.y[data.test_mask])

    accs = []
    for mask in [data.train_mask, data.val_mask, data.test_mask]:
        accs.append(int((pred[mask] == data.y[mask]).sum()) / int(mask.sum()))
    return accs[0], accs[1], accs[2], pre, rec, f1


best_val_acc = final_test_acc = 0
for epoch in range(1, args.epochs + 1):
    loss = train()
    train_acc, val_acc, tmp_test_acc, tmp_test_precision, tmp_test_recall, tmp_test_f1 = test()
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        test_acc = tmp_test_acc
        test_precision = tmp_test_precision
        test_recall = tmp_test_recall
        test_f1 = tmp_test_f1
    log(Epoch=epoch, Loss=loss, Train=train_acc, Val=val_acc, Test=test_acc)
print(best_val_acc, test_acc, test_precision, test_recall, test_f1)