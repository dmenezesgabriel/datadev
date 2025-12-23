# Transformers

Transformers architecture come from RNNs which:

- Introduced a feedback loop for propagating information forward
- Are useful for modeling sequential things for example a sequence of words (or tokens)

Then attention was introduced, creating a hidden state for each token and a concept of relationship between words arise. But RNNs are still sequential and can not parallelize it

So using _feed-forward neural networks (FFNNs)_ it was possible to do the processing in parallel that uses a mechanism called **self-attention**, each token carries it's relationship with the other tokens as attention weights and the position of where it is.

So once is possible to parallelize the training is possible to train the neural network in the entire content of the internet.

## Self-Attention

1. Each encoder or decoder has a list off embeddings (vectors) for each token (words are tokenized in a numerical representation). The space between the vectors represent how similar the tokens are to each other, so words with same meaning are closer in the multi dimensional space.
2. Self-attention produces a weighted average of all token embeddings.
3. This results in tokens being tied to other tokens that are important for its contexts, and a new embedding that captures its meaning in context.
4. Three matrices of weights are learned through back-propagation:

   - Query (wq)
   - Key (Wk)
   - Value (Wv)

5. Every token gets a query, key and value vector by multiplying its embedding against these matrices
6. Compute a score for each token by multiplying (dot product) its query with each key
7. Then softmax is applied to the scores to normalize them

## Masked Self-Attention

- A mask can be applied to prevent tokens from seeing next tokens (words)

## Applications

- Chat
- Question and answering
- Text classification
- Named entity recognition
- Summarization
- Translation
- Code generation
- Text generation
