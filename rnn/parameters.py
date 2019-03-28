import torch

UNIT = "word" # unit of tokenization (char, word)
RNN_TYPE = "LSTM"
NUM_DIRS = 2 # unidirectional: 1, bidirectional: 2
BATCH_SIZE = 128
EMBED = ["char", "word"] # embeddings (char, word)
EMBED_SIZE = 300
HIDDEN_SIZE = 500
DROPOUT = 0.5
NUM_HEADS = 8
DK = HIDDEN_SIZE // NUM_HEADS # dimension of key
DV = HIDDEN_SIZE // NUM_HEADS # dimension of value
LEARNING_RATE = 1e-4
VERBOSE = False
EVAL_EVERY = 10
SAVE_EVERY = 10

PAD = "<PAD>" # padding
SOS = "<SOS>" # start of sequence
EOS = "<EOS>" # end of sequence
UNK = "<UNK>" # unknown token

PAD_IDX = 0
SOS_IDX = 1
EOS_IDX = 2
UNK_IDX = 3

torch.manual_seed(1)
CUDA = torch.cuda.is_available()

KEEP_IDX = False # use the existing indices when preparing additional data
NUM_DIGITS = 4 # number of digits to print