import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(1)
CUDA = torch.cuda.is_available()

class cnn(nn.Module):
    def __init__(self, vocab_size, num_labels):
        super().__init__()

        # architecture
        self.embed = nn.Embedding(vocab_size, EMBED_SIZE, padding_idx = PAD_IDX)
        self.conv = nn.ModuleList([nn.Conv2d(
            in_channels = 1,
            out_channels = NUM_FEATURE_MAPS,
            kernel_size = (i, EMBED_SIZE)
        ) for i in KERNEL_SIZES])
        self.dropout = nn.Dropout(DROPOUT)
        self.fc = nn.Linear(len(KERNEL_SIZES) * NUM_FEATURE_MAPS, num_labels)
        self.softmax = nn.LogSoftmax(1)

        if CUDA:
            self = self.cuda()

    def forward(self, x):
        x = self.embed(x) # [B, L, H]
        x = x.unsqueeze(1) # [B, in_channels (Ci), L, H]
        h = [conv(x) for conv in self.conv] # [B, out_channels (Co), L, 1] * num_kernels (K)
        h = [F.relu(k).squeeze(3) for k in h] # [B, Co, L] * K
        h = [F.max_pool1d(k, k.size(2)).squeeze(2) for k in h] # [B, Co] * K
        h = torch.cat(h, 1) # [B, Co * K]
        h = self.dropout(h)
        h = self.fc(h) # fully connected layer
        y = self.softmax(h)
        return y

def LongTensor(*args):
    x = torch.LongTensor(*args)
    return x.cuda() if CUDA else x
