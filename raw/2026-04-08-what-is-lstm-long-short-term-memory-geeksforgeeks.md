---
title: "What is LSTM - Long Short Term Memory? - GeeksforGeeks"
type: url
captured: 2026-04-08T01:18:12.919628+00:00
source: android-share
url: "https://www.geeksforgeeks.org/deep-learning/deep-learning-introduction-to-long-short-term-memory/"
content_hash: "sha256:73fe1d731f603cd8001d2bf824aebd08961957a2c853f6b03186c4b76ac16189"
tags: []
status: ingested
---

https://www.geeksforgeeks.org/deep-learning/deep-learning-introduction-to-long-short-term-memory/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:38:23+00:00
- source_url: https://www.geeksforgeeks.org/deep-learning/deep-learning-introduction-to-long-short-term-memory/
- resolved_url: https://www.geeksforgeeks.org/deep-learning/deep-learning-introduction-to-long-short-term-memory/
- content_type: text/html; charset=utf-8
- image_urls: ["https://media.geeksforgeeks.org/wp-content/uploads/20250404172141987003/gate_of_lstm.webp", "https://media.geeksforgeeks.org/wp-content/uploads/20250404172543950041/output_gate.jpg", "https://media.geeksforgeeks.org/wp-content/uploads/20250404172507256364/forget_gate.jpg", "https://media.geeksforgeeks.org/wp-content/uploads/20250404172524079223/input_gate.jpg"]

## Fetched Content
Long Short-Term Memory (LSTM) is an improved version of
Recurrent Neural Network (RNN)
designed to capture long-term dependencies in sequential data. It uses a memory cell to store information over time, solving the limitations of traditional RNNs.
This makes it useful for:
- Handles Long Term Dependencies : Remembers information for longer sequences
- Memory Cell : Stores and updates important information over time
- Better than RNN : Overcomes short term memory limitations
- Applications : Used in language translation, speech recognition and time series forecasting
## Problem with Long-Term Dependencies in RNN
RNNs are designed to handle sequential data by using a hidden state that stores information from previous steps. However, they struggle to learn long-term dependencies. This happens due to:
- Vanishing Gradient : When training a model over time, the gradients which help the model learn can shrink as they pass through many steps. This makes it hard for the model to learn long-term patterns since earlier information becomes almost irrelevant.
- Exploding Gradient : Sometimes gradients can grow too large causing instability. This makes it difficult for the model to learn properly as the updates to the model become erratic and unpredictable.
## LSTM Architecture
LSTM architectures involves the memory cell which is controlled by three gates:
- Input gate : Controls what information is added to the memory cell.
- Forget gate : Determines what information is removed from the memory cell.
- Output gate : Controls what information is output from the memory cell.
This allows LSTM networks to selectively retain or discard information as it flows through the network which allows them to learn long-term dependencies. The network has a hidden state which is like its short-term memory. This memory is updated using the current input, the previous hidden state and the current state of the memory cell.
## Working of LSTM
LSTM consists of a repeating chain like structure with memory cells and gating mechanisms
LSTM Model
Information is retained by the cells and the memory manipulations are done by thegates
.
There are three gates:
### 1. Forget Gate
The forget gate decides which information to keep or remove from the cell state. It uses the current input
x_t
and previous output
h_{t-1}
applies weights and bias and passes the result through a sigmoid function that outputs values between 0 and 1. Values close to 0 remove information, while values close to 1 retain it.
The equation for the forget gate is:
f_t = \sigma \left( W_f \cdot [h_{t-1}, x_t] + b_f \right)
Where:
- W_f represents the weight matrix associated with the forget gate.
- [h_t-1, x_t] denotes the concatenation of the current input and the previous hidden state.
- b_f is the bias with the forget gate.
- \sigma is the sigmoid activation function.
Forget Gate
### 2. Input gate
The addition of useful information to the cell state is done by the input gate.
- First the information is regulated using the sigmoid function and filter the values to be remembered similar to the forget gate using inputs h_{t-1} and x_t .
- Then, a vector is created using tanh function that gives an output from -1 to +1 which contains all the possible values from h_{t-1} and x_t .
- At last the values of the vector and the regulated values are multiplied to obtain the useful information.
The equation for the input gate is:
i_t = \sigma \left( W_i \cdot [h_{t-1}, x_t] + b_i \right)
\hat{C}_t = \tanh \left( W_c \cdot [h_{t-1}, x_t] + b_c \right)
We multiply the previous state by
f_t
effectively filtering out the information we had decided to ignore earlier. Then we add
i_t \odot C_t
which represents the new candidate values scaled by how much we decided to update each state value.
C_t = f_t \odot C_{t-1} + i_t \odot \hat{C}_t
where
- \odot denotes element-wise multiplication
- tanh is activation function
Input Gate
### 3. Output gate
The output gate is responsible for deciding what part of the current cell state should be sent as the hidden state (output) for this time step. First, the gate uses a sigmoid function to determine which information from the current cell state will be output. This is done using the previous hidden state
h_{t - 1}
​ and the current input
x_t
​:
o_t = \sigma \left( W_o \cdot [h_{t-1}, x_t] + b_o \right)
Next, the current cell state
C_t
​ is passed through a tanh activation to scale its values between
-1
and
+1
. Finally, this transformed cell state is multiplied element-wise with
o_t
​ to produce the hidden state
h_t
:
h_t = o_t \odot \tanh(C_t)
Here:
- o_t ​ is the output gate activation.
- C_t ​ is the current cell state.
- \odot represents element-wise multiplication.
- \sigma is the sigmoid activation function.
This hidden state
h_t
​ is then passed to the next time step and can also be used for generating the output of the network.
Output Gate
## Applications
- Language Modeling : Used in tasks like machine translation and text summarization. RNNs learn dependencies between words in a sequence, helping generate grammatically correct and meaningful sentences.
- Speech Recognition : Used to convert spoken language into text. By learning temporal patterns in audio signals, RNNs can recognize words and map them accurately to text.
- Time Series Forecasting : Used for predicting stock prices, weather and energy consumption. They learn patterns in time series data to predict future events.
- Anomaly Detection : Used for detecting fraud or network intrusions. These networks can identify patterns in data that deviate drastically and flag them as potential anomalies.
- Recommender Systems : In recommendation tasks like suggesting movies, music and books. They learn user behavior patterns to provide personalized suggestions.
- Video Analysis : Applied in tasks like activity recognition and action classification. When combined with CNNs , RNNs help process sequential frames to understand motion and temporal patterns.
<!-- fetched-content:end -->
