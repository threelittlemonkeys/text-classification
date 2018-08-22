import torch
import torch.nn as nn
import torch.nn.functional as F

BATCH_SIZE = 128
EMBED_SIZE = 300
HIDDEN_SIZE = 1000
NUM_LAYERS = 2
DROPOUT = 0.5
BIDIRECTIONAL = True
NUM_DIRS = 2 if BIDIRECTIONAL else 1
VERBOSE = True
SAVE_EVERY = 10

PAD = "<PAD>" # padding
UNK = "<UNK>" # unknown token

PAD_IDX = 0
UNK_IDX = 1

torch.manual_seed(1)
CUDA = torch.cuda.is_available()

class rnn(nn.Module):
    def __init__(self, vocab_size, num_labels):
        super().__init__()

        # architecture
        self.embed = nn.Embedding(vocab_size, EMBED_SIZE, padding_idx = PAD_IDX)
        self.rnn = nn.GRU( # LSTM or GRU
            input_size = EMBED_SIZE,
            hidden_size = HIDDEN_SIZE // NUM_DIRS,
            num_layers = NUM_LAYERS,
            bias = True,
            batch_first = True,
            dropout = DROPOUT,
            bidirectional = BIDIRECTIONAL
        )
        self.attn = attn()
        self.dropout = nn.Dropout(DROPOUT)
        self.out = nn.Linear(HIDDEN_SIZE, num_labels)
        self.softmax = nn.LogSoftmax(1)

        if CUDA:
            self = self.cuda()

    def init_hidden(self, rnn_type): # initialize hidden states
        h = zeros(NUM_LAYERS * NUM_DIRS, BATCH_SIZE, HIDDEN_SIZE // NUM_DIRS) # hidden states
        if rnn_type == "LSTM":
            c = zeros(NUM_LAYERS * NUM_DIRS, BATCH_SIZE, HIDDEN_SIZE // NUM_DIRS) # cell states
            return (h, c)
        return h

    def forward(self, x, mask):
        self.hidden = self.init_hidden("GRU") # LSTM or GRU
        x = self.embed(x)
        x = nn.utils.rnn.pack_padded_sequence(x, mask[1], batch_first = True)
        h, _ = self.rnn(x, self.hidden)
        h, _ = nn.utils.rnn.pad_packed_sequence(h, batch_first = True)
        if self.attn:
            h = self.attn(h, mask[0])
        else:
            h = h.gather(1, mask[1].view(-1, 1, 1).expand(-1, -1, h.size(2)) - 1)
        h = self.dropout(h)
        h = self.out(h).squeeze(1)
        h = self.softmax(h)
        return h

class attn(nn.Module): # attention layer
    def __init__(self):
        super().__init__()

        # architecture
        self.Wa = nn.Linear(HIDDEN_SIZE, 1)

    def align(self, h, mask):
        a = self.Wa(h)
        a = a.masked_fill(mask.unsqueeze(2), -10000) # masking in log space
        a = F.softmax(a, 1) # [B, L, 1]
        return a # alignment weights

    def forward(self, h, mask):
        a = self.align(h, mask) # alignment vector
        v = (a * h).sum(1) # representation vector
        return v

def Tensor(*args):
    x = torch.Tensor(*args)
    return x.cuda() if CUDA else x

def LongTensor(*args):
    x = torch.LongTensor(*args)
    return x.cuda() if CUDA else x

def zeros(*args):
    x = torch.zeros(*args)
    return x.cuda() if CUDA else x

def scalar(x):
    return x.view(-1).data.tolist()[0]

def argmax(x):
    return scalar(torch.max(x, 0)[1]) # for 1D tensor

def maskset(x):
    mask = x.data.eq(PAD_IDX)
    return (mask, x.size(1) - mask.sum(1)) # set of mask and lengths
