---
title: "[2608.14071] Scaling Domain Data Repetition in LLM Pretraining"
type: url
captured: 2026-08-17T12:44:05.102976+00:00
source: android-share
url: "https://arxiv.org/abs/2608.14071"
content_hash: "sha256:297a831c5d490c0552be42256ba1ae1cdb0224c80b787be98f42fe4f047a487d"
tags: []
status: ingested
---

https://arxiv.org/abs/2608.14071

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-08-17T12:44:19+00:00
- source_url: https://arxiv.org/abs/2608.14071
- resolved_url: https://arxiv.org/pdf/2608.14071.pdf
- content_type: application/pdf
- image_urls: []

## Fetched Content
| Scaling | Domain | Data | Repetition | in LLM | Pretraining |
| ------- | ------ | ---- | ---------- | ------ | ----------- |
Jingwei Li1,‡, Xinran Gu1, Rui Dai1, Xintong Hao2,†, Chengyin Xu2, Yan Wu2, Shuran
|     |            | Zheng1,              | Jingzhao       | Zhang1,∗             |        |
| --- | ---------- | -------------------- | -------------- | -------------------- | ------ |
|     |            | 1TsinghuaUniversity, |                | 2ByteDanceSeed       |        |
|     | ‡Work done | at ByteDance         | Seed, †Project | Lead, ∗Corresponding | Author |
Abstract
As large language models scale, their training-token budgets must also increase to maintain an
6202 guA 41  ]IA.sc[  1v17041.8062:viXra
appropriate tokens-per-parameter ratio (TPP). However, high-quality domain data is much harder
to scale than general web data. As model size and the training-token budget increase, its fraction
in the training mixture tends to decrease. Repeating the available high-quality data provides an
effective way to counteract this dilution, but excessive repetition may lead to overfitting. We study
this trade-off under practical LLM scaling, wherethe training-token budget grows proportionally
with model size. For a fixed domain, we first find that, surprisingly at a fixed TPP, the optimal
repetition count mildly increases with model size. Across different domains, we find that the
optimal repetition count is strongly negatively correlated with the final validation loss of a domain:
domains with lower loss can generally benefit from more repetitions. In contrast, the amount of
unique domain data is only weakly related to the optimal repetition count. These findings suggest
that repetition counts tuned on smaller proxy models with the same TPP can provide a practical
| estimate | for larger models. |                                         |     |     |     |
| -------- | ------------------ | --------------------------------------- | --- | --- | --- |
| Date:    | August 17, 2026    |                                         |     |     |     |
|          | Jingzhao           | Zhang at jingzhaoz@mail.tsinghua.edu.cn |     |     |     |
Correspondence:
1 Introduction
Large language models (LLMs) are often pretrained on mixtures of diverse domains, including general web
text, code, mathematics, scientific corpora, and multilingual content [7, 8, 33, 34]. As model size increases,
compute-optimal training also requires an increasing number of training tokens [13, 16]. This creates an
asymmetric data-scaling problem: broad general web data [20, 29, 30] can often be scaled relatively easily,
whereashigh-qualitydomain-specificdata[11,21,28]ismuchhardertoscaleatthesamerate. However,ifthe
amount of such data remains fixed, its mixing ratio decreases as the total training budget grows. Recent work
shows that under data mixing, knowledge-dense domains may only be learned once their mixing ratio exceeds
a critical threshold; below this threshold, additional training can still fail to acquire the target knowledge [10].
Therefore, maintaining a sufficient fraction of high-quality domain data is important when scaling data.
Prior work has extensively studied data repetition, where examples from a finite dataset are reused multiple
timesduringtraining[26,27,31,35]. Forhigh-qualitydomaindata,repetitionoffersadirectwaytocounteract
data dilution, but may also increase the risk of overfitting [2, 12, 18, 37]. We therefore need to study the
trade-off between the domain-learning gains from repeated high-quality data and the risk of overfitting, and
| to identify | the optimal number | of repetitions | for different | domains. |     |
| ----------- | ------------------ | -------------- | ------------- | -------- | --- |
1

Figure1 Datarepetitionundertwomodel-scalingsetups. Left: Whenthetraining-datasizeisfixedindependently
of model size, the optimal repetition count decreases with model size. Right: When the tokens-per-parameter ratio
TPP is fixed, the optimal repetition count increases with model size. The fixed-TPP setting better reflects practical
| LLM scaling | and | is the focus | of  | our study. |     |     |     |     |
| ----------- | --- | ------------ | --- | ---------- | --- | --- | --- | --- |
A first line of work studies data repetition in the single-dataset setting [26, 27, 37]. More recent work extends
this question to mixtures of general and domain-specific data, showing that general data can regularize
repeated domain data and developing scaling laws that account for repetition under data mixing [4, 23, 31].
Across these settings, the conclusion is that larger models are more susceptible to overfitting from repeated
data, suggesting that repetition should be minimized when training large LLMs. We confirm this with our
| experiments | shown | on  | the left | in Figure 1. |     |     |     |     |
| ----------- | ----- | --- | -------- | ------------ | --- | --- | --- | --- |
However, we also note that existing cross-scale comparisons typically hold the training-data size fixed rather
than preserving the tokens-per-parameter ratio [4, 27, 37], D/N, where is the total number of
|     |     |     |     |     |     | TPP := D |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- |
training tokens and N is the model size. This distinction leads to different conclusions about repetition. As
illustrated in Figure 1, when is fixed, increasing the model size exposes a larger model to the same repeated
D
dataset, causing overfitting to occur earlier and the optimal repetition count to approach one. In contrast,
when the training-token budget grows with model size using a fixed TPP [13, 14], the optimal repetition count
| surprisingly | increases | with | model | size. |     |     |     |     |
| ------------ | --------- | ---- | ----- | ----- | --- | --- | --- | --- |
To study repetition under this scaling regime, we consider four high-quality domains: code, math, Wikipedia
and medical data. For each domain, we vary its amount of unique data and repetition count while keeping
the total training-token budget fixed for each model size. This setup allows us to isolate how data repetition
| interacts | with domain |     | properties, | unique-data | size, and model | scale. |     |     |
| --------- | ----------- | --- | ----------- | ----------- | --------------- | ------ | --- | --- |
| Our main  | findings    | are | as follows. |             |                 |        |     |     |
•
Theoptimalrepetitioncountisstronglynegativelycorrelatedwiththefinalvalidationlossofadomain.
Domains with lower validation loss can generally tolerate and benefit from more repetitions, whereas
| domains | with | higher | validation | loss overfit | earlier. |     |     |     |
| ------- | ---- | ------ | ---------- | ------------ | -------- | --- | --- | --- |
• Atafixedtokens-per-parameterratioTPP,theoptimalrepetitioncountincreaseswithmodelsize. This
trend is opposite to that observed when the data budget is fixed across model sizes. It also supports
conservative transfer from smaller proxy models: a repetition count that does not cause overfitting in a
smaller model is unlikely to cause overfitting in a larger model trained at the same TPP.
| •   |     |     |     |     |     |     | Across | the tested |
| --- | --- | --- | --- | --- | --- | --- | ------ | ---------- |
The optimal repetition count is largely insensitive to the amount of unique data.
fractions of unique high-quality tokens, the repetition count that minimizes validation loss remains
nearly unchanged. Therefore, when estimating the optimal repetition count on a smaller proxy model,
it is not necessary to use a specific unique high-quality token fraction; any representative fraction within
| the | tested | range | can be | used. |     |     |     |     |
| --- | ------ | ----- | ------ | ----- | --- | --- | --- | --- |
Together, these results provide a practical approach for configuring the optimal repetition counts for high2

quality domains. Repetition counts can first be swept on a smaller proxy model with the same TPP for an
arbitrary fraction of unique high-quality tokens, and the result can be used to select relatively safe repetition
counts for the target model.
2 Related Work
Early studies mainly examine multi-epoch training on a single
DataRepetitioninSingle-DatasetTraining.
dataset. One line of work extends the Chinchilla scaling law [13] and develops scaling laws for repeated data.
[27]modelthevalidationlossunderrepetitionusingexponentialdecayandshowthatafewepochsofrepetition
can perform similarly to fresh data, while heavier reuse yields diminishing returns. [26] further extend this
formulation by modeling the subsequent increase in validation loss with an additive overfitting penalty,
achieving more accurate predictions. Another line of work studies the factors that determine repetitioninduced degradation. [37] identify dataset size, model size, and training objective as key factors, while [3]
show that repetition can improve generalization on some synthetic mathematical tasks. [38] theoretically
prove that larger datasets can generally support more reuse. Beyond exact duplication, [17] find that semantic
duplication can also cause overfitting, and [35] show that sparse models benefit from more repeated epochs
thandensemodels. However,thesestudiesmainlyrepeatanentiredataset,whereaspracticalLLMpretraining
often repeats only selected domains within data mixtures.
Morerecentworkstudiesrepetitionwithinpretrainingmixtures,where
DataRepetitioninPretrainingMixtures.
a limited subset is reused while the remaining data remain unique. [12] study a setting in which 10% of the
training tokens are drawn from a repeatedly reused subset and the remaining 90% are unique. They find that
repetitioncancausenon-monotonicdegradation,withintermediaterepetitionlevelsbeingparticularlyharmful.
Extending this analysis, [4] jointly vary the subset size and repetition count, showing that a moderately sized
subset repeated a moderate number of times can be more harmful than either a larger subset repeated fewer
timesorasmallersubsetrepeatedmoretimes. [31]studymixturepretrainingwithlimitedtarget-domaindata
and abundant generic data. They show that generic data mitigates overfitting from repeated target-domain
data and that the optimal repetition count depends on the amount of target data, compute budget, and
model scale. However, existing cross-scale studies do not preserve the tokens-per-parameter ratio. We instead
study repetition under a fixed TPP=D/N, such that the training-token budget grows proportionally with
model size.
Data mixture optimization studies how to allocate a fixed training
Data Mixture Optimization for LLMs.
budget across domains by modeling their relative value and interactions. Existing methods estimate domain
weights using proxy training, predictive models, or scaling laws, and transfer the resulting mixture to larger
models [6, 9, 15, 25, 32, 36, 39]. These methods generally assume sufficient unique data in each domain and
therefore do not model repetition. Recent work [23, 31] relaxes this assumption by deriving repetition-aware
mixture scaling laws that jointly characterize domain allocation and data reuse.
3 Setup
We study data repetition under different model sizes. Let N ={N ,...,N } denote the model sizes. For a
1 K
model of size N ∈N, we set its total training-token budget to
D =TPP·N,
N
where TPP denotes the number of training tokens per parameter and is set to a constant greater than 100
in our experiments. Therefore, all training runs with the same model size use exactly the same number
of training tokens, while larger models receive proportionally larger token budgets. We focus on different
high-quality domains. Let
D ={Code,Math,Wiki,Medical}
HQ
denote the set of high-quality domains. For each high-quality domain d ∈ D , we sweep over different
HQ
combinations of unique-data fractions and repetition counts.
3

Figure 2 Overview of our experimental framework. We train models of different sizes at a fixed tokens-perparameter ratio and vary the amount and repetition count of high-quality domain data in the training mixture. We
| evaluate both | in-domain      | validation | loss and     | out-of-domain | performance. |     |     |
| ------------- | -------------- | ---------- | ------------ | ------------- | ------------ | --- | --- |
| Next, we      | set the number | of unique  | high-quality |               | tokens       | as  |     |
U
N,α
|     |     |     |     |     |      |  |  |
| --- | --- | --- | --- | --- | ---- | -------- | -------- |
|     |     |     |     |     |      | 1 1      | 1        |
|     |     |     | U   | =αD | , α∈ | , ,      | ,        |
|     |     |     | N,α | N   |      |          |          |
|     |     |     |     |     |      | 40 20 10 |          |
and the repetition count as e∈{1,2,3,4,5,6,7}. In other words, for a configuration (d,N,α,e), we first select
a fixed subset from domain d containing U unique tokens. This subset is then repeated e times. Hence,
N,α
| the total | number of high-quality |     | tokens during | training | is  |        |     |
| --------- | ---------------------- | --- | ------------- | -------- | --- | ------ | --- |
|           |                        |     |               | H        | =eU | =eαD . |     |
|           |                        |     |               | N,α,e    | N,α | N      |     |
The remaining token budget is filled with non-repeated web data, whose token count is
|     |     |     | W     | =D  | −H    | =(1−eα)D | .   |
| --- | --- | --- | ----- | --- | ----- | -------- | --- |
|     |     |     | N,α,e | N   | N,α,e |          | N   |
All configurations satisfy eα ≤ 1, and thus W ≥ 0. Importantly, α controls the amount of unique
N,α,e
high-quality data, whereas controls how often this fixed subset is revisited. Their product determines
e eα
the final proportion of high-quality token presentations in the training stream. The total budget D remains
N
unchanged across recipes for a fixed N; only its composition between the target high-quality domain and the
web corpus changes. We do not mix multiple high-quality domains in the same run.
Let θ denote the model obtained from configuration (d,N,α,e). The complete experiment grid for each
d,N,α,e
| domain | and the full | set of | experiments | are |     |     |     |
| ------ | ------------ | ------ | ----------- | --- | --- | --- | --- |
| G      | d            |        |             | G   |     |     |     |

|     |     |     | G =N | ×A×E, | G = | ({d}×G | ).  |
| --- | --- | --- | ---- | ----- | --- | ------ | --- |
|     |     |     | d    |       |     |        | d   |
d∈DHQ
We evaluate each trained model using both in-distribution and out-of-distribution validation losses. For a
| validation | corpus V, we | define | the token-averaged |     | negative | log-likelihood | as  |
| ---------- | ------------ | ------ | ------------------ | --- | -------- | -------------- | --- |
|x|
1
|     |     |     | L(θ;V)=− |     |     | logp (x | |x ), |
| --- | --- | --- | -------- | --- | --- | ------- | ----- |
|     |     |     |          | M   |     | θ t     | <t    |
V
x∈Vt=1
4

|         |                                            |     |     |     |     | Left: different | high-quality | domains exhibit | substantially |
| ------- | ------------------------------------------ | --- | --- | --- | --- | --------------- | ------------ | --------------- | ------------- |
| Figure3 | Factorsaffectingtheoptimalrepetitioncount. |     |     |     |     |                 |              |                 |               |
different optimal repetition counts. Middle: for the Math domain, the optimal repetition count increases with model
size under a fixed TPP. Right: for the Math domain, varying α mainly shifts the validation loss but has little effect on
the optimal repetition count. Overall, the domain has the strongest effect on the optimal repetition count, followed by
| model size, | while | α has little | effect. |     |     |     |     |     |     |
| ----------- | ----- | ------------ | ------- | --- | --- | --- | --- | --- | --- |

where x = (x ,...,x ) is a token sequence and M = |x| is the total number of validation tokens.
|           | 1         | |x|    |        |                 | V       | x∈V          |     |     |     |
| --------- | --------- | ------ | ------ | --------------- | ------- | ------------ | --- | --- | --- |
| For a run | targeting | domain | d, the | in-distribution | metric  | is           |     |     |     |
|           |           |        |        | L(d)(N,α,e)=L   |  | ;VIID |     |     |     |
|           |           |        |        |                 | θ       |              | ,   |     |     |
|           |           |        |        | IID             |         | d,N,α,e      | d   |     |     |
where VIID is the held-out validation set from the same high-quality domain. We additionally report
d
|     |     |     |     |                |  | ;VOOD |     |     |     |
| --- | --- | --- | --- | -------------- | ------- | ------------ | --- | --- | --- |
|     |     |     |     | L(d) (N,α,e)=L | θ       |              | ,   |     |     |
|     |     |     |     | OOD            |         | d,N,α,e      |     |     |     |
where VOOD is a pretraining validation set used to measure performance outside the repeated target domain.
| Our setup  | is illustrated | in     | Figure  | 2.         |       |     |     |     |     |
| ---------- | -------------- | ------ | ------- | ---------- | ----- | --- | --- | --- | --- |
| 4 Analysis |                | of the | Optimal | Repetition | Count |     |     |     |     |
In this section, we summarize the empirical factors associated with the optimal repetition count and provide
a theoretical explanation. Empirically, the optimal repetition count depends mildly on model size, is largely
insensitive to the fraction of unique high-quality data, and is strongly negatively correlated with the minimum
validation loss. We then use a theoretical model to explain these observations through the trade-off between
| knowledge   | acquisition | and        | noise  | fitting.         |     |         |     |     |     |
| ----------- | ----------- | ---------- | ------ | ---------------- | --- | ------- | --- | --- | --- |
| 4.1 Optimal |             | Repetition | Counts | for High-Quality |     | Domains |     |     |     |
Recall that for each model size N, we train with a token budget and record the validation
|     |     |     |     |     |     |     | D =TPP·N |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- |
N
loss at the end of training. We vary the fraction of unique high-quality data, denoted by α, and its repetition
count, denoted by e, while keeping the total number of training tokens fixed. We use these experiments to
study how the optimal repetition count depends on α, model size, and data domain.
Figure 3 compares the effects of data domain, model size, and the fraction of unique high-quality data on
α
the optimal repetition count. The left panel shows a strong domain dependence. Math reaches its minimum
at around 5 repetitions, while Wiki, Code, and Medical reach their minima earlier, indicating that the optimal
repetition count varies substantially across domains. The middle panel shows the effect of model size on
the Math domain at a fixed α. As model size increases, the optimal repetition count shifts toward larger
values, suggesting a moderate dependence on model scale. The right panel shows the effect of α on the Math
domain at a fixed model size. Although increasing consistently reduces the validation loss, the location of
α
the minimum remains nearly unchanged, indicating that α has little effect on the optimal repetition count.
Overall, the optimal repetition count mainly depends on the data domain and model size, but is largely
insensitive to α. The full results across all domains, model sizes, and values of α are provided in Appendix B.
To quantify the above observations, we estimate the optimal repetition count for each combination of domain
d, model size N, and the fraction of unique high-quality data α, and then quantitatively characterize its
5

Figure4 Factorsassociatedwiththeestimatedoptimalrepetitioncount. For each combination of high-quality
domain, model size, and unique data fraction, we fit a quadratic function to the final validation loss as a function of
repetition count and use the minimum of the fitted curve as the estimated optimum. From left to right, we plot the
estimated optimal repetition count against the minimum validation loss, model size, and unique high-quality data
fraction. ThecorrespondingPearsoncorrelationsare−0.944,0.400,and0.018,respectively. Colorsdenotehigh-quality
domains, marker shapes denote model sizes, and marker sizes denote unique data fractions where applicable.
dependence on these factors. Specifically, we fit a quadratic function to the final validation loss as a function
of repetition count:
Ld,N,α (e)=a
d,N,α
e2+b
d,N,α
e+c
d,N,α
.
We use the minimum of the fitted curve as the estimated optimal repetition count,
b
e∗ =− d,N,α .
d,N,α 2a
d,N,α
This continuous estimate reduces the effect of the discrete repetition grid, allowing clearer analysis of the
correlations between the optimal repetition count and different factors.
Sincedifferentdomainsexhibitsubstantiallydifferentvalidation-losslevels, wefurthercharacterizethedomain
effectthroughvalidationloss. Specifically, insteadoftreatingthedomainonlyasacategoricalvariable, weuse
the minimum validation loss achieved within each domain setting as a continuous proxy for its domain-specific
characteristics, and quantitatively examine how it relates to the optimal repetition count.
Figure 4 compares the estimated optimal repetition count with the minimum validation loss, model size,
and unique high-quality data fraction. The optimal repetition count has a strong negative correlation with
the minimum validation loss, with a Pearson correlation of −0.944. Across the domains considered in our
experiments, settings with higher validation loss tend to prefer fewer repetitions, whereas settings with lower
validation loss tend to have larger optimal repetition counts. Model size has a weaker positive correlation of
0.400, consistent with the observation that larger models tend to prefer slightly more repetitions under a fixed
tokens-per-parameter ratio. By comparison, the correlation with the unique high-quality data fraction is only
0.018, indicating that the optimal repetition count is nearly insensitive to the amount of unique data over the
range considered.
Overall, the optimal repetition count is mainly determined by the high-quality domain loss, with a smaller
dependence on model size and little observable dependence on the unique high-quality data fraction.
These findings suggest a practical procedure for selecting the repetition count for large-scale training: we
first train a smaller proxy model with the same tokens-per-parameter ratio as the target model, using any
suitable value of α. For each high-quality domain, the validation loss provides a useful indication of the range
of repetition counts worth considering. This value can then serve as a conservative estimate for the target
model, since our experiments show that a repetition count that does not cause overfitting on the proxy model
also remains safe for a larger model under the same tokens-per-parameter ratio.
6

| 4.2 Theoretical |     | Analysis |     |     |     |     |     |     |     |     |     |     |
| --------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
In this section, we analyze the experimental observations above from a theoretical perspective. To capture
the experimental setup, we consider a one-hot linear regression problem in R∞. Let {e } be the standard
k k≥1
basis, where each coordinate k represents a knowledge unit, and its frequency follows a power law. Specifically,
| following | [38], let the | input | distribution |     | be P(x |     | where   |     |           |     |           | and    |
| --------- | ------------- | ----- | ------------ | --- | ------ | --- | ------- | --- | --------- | --- | --------- | ------ |
|           |               |       |              |     |        | = e | ) = p , | p   | = c k−α,c |     | = ζ(α)−1, | α > 1. |
|           |               |       |              |     |        |     | k k     | k   | α         | α   |           |        |
Further, let θ∗ be the target linear predictor, where θ∗ specifies the response associated with knowledge unit
| k. We make | the following |     | assumption: |     |     |     |     |     |     |     |     |     |
| ---------- | ------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Assumption 4.1 (SourceCondition). Weassumethatθ∗ satisfiesapriorthatE[(θ∗)2p ]=k−β,β ∈(1,+∞).
|     |     |     |     |     |     |     |     |     |     | k   | k   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Source condition assumptions are widely used in theoretical work such as [19, 22]. The total weighted signal
|           |                | ∞ |     |         | ∞ |     |     |     |     |     |     |     |
| --------- | -------------- | --------- | --- | ------- | --------- | --- | --- | --- | --- | --- | --- | --- |
| energy is | finite because |           | E[p | (θ∗)2]= |           | k−β | <∞. |     |     |     |     |     |
|           |                |           | k=1 | k k     | k=1       |     |     |     |     |     |     |     |
Next, we define the learning setup. Given a training-token budget and model size N, let :R∞ →RN
|     |     |     |     |     |     |     |     | D   |     |     |     | S   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
N
be the projection onto the first N coordinates. Due to the limited model capacity, we can only observe S x
N
instead of observing the intact [5, 19]. Therefore, we observe the dataset )}D with the
|     |     |     | x   |     |     |     |     |     | D   | = {(S | N x i ,y i | ,   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ---------- | --- |
i=1
| following | data distribution |     | and loss, |       |        |     |              |     |     |     |     |     |
| --------- | ----------------- | --- | --------- | ----- | ------ | --- | ------------ | --- | --- | --- | --- | --- |
|           |                   |     | i id      |       |        |     | i id         |     |     |     |     |     |
|           |                   | x   | ∼ p,      | y =⟨x | ,θ∗⟩+ε | ,   | ε ∼ N(0,σ2), |     | σ2  | >0, |     |     |
|           |                   | i   |           | i     | i      | i   | i            |     |     |     |     |     |
D
1
|     |     |     |     | L   | (θ)= |     | (⟨S x ,θ⟩−y | )2, | θ ∈RN. |     |     |     |
| --- | --- | --- | --- | --- | ---- | --- | ----------- | --- | ------ | --- | --- | --- |
|     |     |     |     | N   |      |     | N i         | i   |        |     |     |     |
2D
i=1
To fit the linear regression model, we initialize at and run full-batch gradient descent:
θ 0 =0
|     |     | θ   | =θ  | −η∇L | (θ ), |     | r =0,1,2,..., |     | 0<η <1. |     |     |     |
| --- | --- | --- | --- | ---- | ----- | --- | ------------- | --- | ------- | --- | --- | --- |
|     |     |     | r+1 | r    | N r   |     |               |     |         |     |     |     |
To evaluate the performance, we define population risk and the total expected risk. For θ ∈RN, define the
| population | excess risk |     |     |           |     |           |               |           |     |     |     |     |
| ---------- | ----------- | --- | --- | --------- | --- | --------- | ------------- | --------- | --- | --- | --- | --- |
|            |             |     |     |           | 1   |  |               |  |     |     |     |     |
|            |             |     |     |           | E   |           | x,θ⟩−⟨x,θ∗⟩)2 |           |     |     |     |     |
|            |             |     |     | R N (θ):= |     | x (⟨S     | N             |           | .   |     |     |     |
2
To investigate the expected population risk with respect to r, we write R (r;β,σ):=E [R (θ )], and
|            |                  |     |                         |          |      |     |     |          | D,N |     | θ∗,D,ε | N r |
| ---------- | ---------------- | --- | ----------------------- | -------- | ---- | --- | --- | -------- | --- | --- | ------ | --- |
| define the | earliest optimal |     | integer                 | stopping | time | by  |     |          |     |     |        |     |
|            |                  |     | r∗(D,N;β,σ):=minargminR |          |      |     |     | (r;β,σ). |     |     |        |     |
D,N
r∈Z
≥0
| When | and are | fixed, we | simply | write | r∗(D,N). |     |     |     |     |     |     |     |
| ---- | ------- | --------- | ------ | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
| β    | σ       |           |        |       |          |     |     |     |     |     |     |     |
Condition on the number of observations of each knowledge unit gives the exact decomposition:
N
|     |     |          |     |     |  k−β                 |           |  k−βE |           | (1−ηm/D)2r         |     |           |     |
| --- | --- | -------- | --- | --- | ---------------------------- | --------- | ------------- | --------- | ------------------ | --- | --------- | --- |
|     | 2R  | (r;β,σ)= |     |     |                              |           | +             |           |                    |     |           |     |
|     |     | D,N      |     |     |                              |           |               | m∼B(D,pk) |                    |     |           |     |
|     |     |          |     |     | k>N                          |           | k=1           |           |                    |     |           |     |
|     |     |          |     |     |   |  |      |           |  |     |  |     |
knowledge-acquisitionerror
unrepresentedknowledge
|     |     |     |     |     | N   |     |     | (1−(1−ηm/D)r)2 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | --- | --- | --- |

|     |     |     |     | +σ2 | p E |           | 1     | ·   |     |     | ,   |     |
| --- | --- | --- | --- | --- | --- | --------- | ----- | --- | --- | --- | --- | --- |
|     |     |     |     |     | k   | m∼B(D,pk) | {m>0} |     | m   |     |     |     |
k=1
|     |     |     |     |  |     |     |  |     |     |     |  |     |
| --- | --- | --- | --- | --------- | --- | --- | ------------------ | --- | --- | --- | --------- | --- |
noise-fittingerror
whereB(D,p )denotestheBinomialdistribution. Repeatedoptimizationdecreasestheknowledge-acquisition
k
error but increases the noise-fitting error, and the optimal repetition count is the point at which the latter
| marginal | effect begins | to dominate. |     |     |     |     |     |     |     |     |     |     |
| -------- | ------------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Theorem 4.2 (Noise decay). For fixed token size D and model size N, let 0<σ2 ≤σ2. Then
|           |           |     |     |            |     |              |     |      |     | 1   | 2   |     |
| --------- | --------- | --- | --- | ---------- | --- | ------------ | --- | ---- | --- | --- | --- | --- |
|           |           |     |     | r∗(D,N;β,σ |     | )≤r∗(D,N;β,σ |     |      |     |     |     |     |
|           |           |     |     |            |     | 2            |     | 1 ). |     |     |     |     |
| Moreover, | as σ2 →0, |     |     |            |     |              |     |      |     |     |     |     |
log(1/σ2)
r∗(D,N;β,σ)=
+O(1).
−log(1−η/D)
7

Findings: A smaller σ2 reduces the noise-fitting term without changing the knowledge-acquisition term, so
the benefit of fitting the signal dominates for more iterations; overfitting still occurs, but its onset is delayed.
Theorem 4.2 formalizes this mechanism and explains the negative relationship between validation loss and the
| optimal repetition | count     | in Figure | 4.               |                   |            |               |        |
| ------------------ | --------- | --------- | ---------------- | ----------------- | ---------- | ------------- | ------ |
|                    | (Stopping | time      | and model size). |                   |            | σ2            |        |
| Theorem            | 4.3       |           |                  | Suppose β >α.     | For fixed  | D, β, and >0, | define |
|                    |           |           |                  |  D(2−η/D) |  1 |               |        |
|                    |           |           | (D,σ2)=          |                   | β−α        |               |        |
|                    |           |           | N                |                   | .          |               |        |
|                    |           |           | 0                | c ησ2             |            |               |        |
α
Then
|     |     |     | r∗(D,N +1)≤r∗(D,N), |     | (D,σ2). |     |     |
| --- | --- | --- | ------------------- | --- | ------- | --- | --- |
N >N 0
| The crossover | scale satisfies |     |     |                  |          |     |     |
| ------------- | --------------- | --- | --- | ---------------- | -------- | --- | --- |
|               |                 |     |     |  |  |     |     |
1/(β−α)
D
|     |     |     | N (D,σ2)=Θ |     | .   |     |     |
| --- | --- | --- | ---------- | --- | --- | --- | --- |
|     |     |     | 0          | σ2  |     |     |     |
Findings: Under a fixed token budget, increasing N extends the model toward rarer and weaker knowledge
units without providing additional observations, causing the noise-fitting effect to dominate earlier once the
model passes the explicit crossover scale in Theorem 4.3, as illustrated in the left panel of Figure 1.
Theorem 4.4 (Stoppingtimeunderlineardata–modelscaling). Suppose β >α. For fixed σ2 >0 and C >0,
0
suppose that
D
|     |     |     |     | −→C . |     |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- |
N 0
| Then, as D,N | →∞, |     |           |          |          |     |     |
| ------------ | --- | --- | --------- | -------- | -------- | --- | --- |
|              |     |     |           |  |  |     |     |
|              |     |     | r∗(D,N)=Θ | Dα/β     | .        |     |     |
Findings: Under fixed tokens-per-parameter scaling, however, the data budget grows together with model
size, allowing the reduction in knowledge-acquisition error to dominate for longer; Theorem 4.4 quantifies the
resulting increase in the optimal repetition count shown in the right panel of Figure 1.
| All proofs   | are deferred | to Appendix | D.  |     |     |     |     |
| ------------ | ------------ | ----------- | --- | --- | --- | --- | --- |
| 5 Additional | Analyses     |             |     |     |     |     |     |
In this section, we present additional analyses of data repetition. Section 5.1 compares repeated and unique
high-quality tokens at a fixed total domain fraction and shows that the effect of repetition is strongly domain
dependent. Section 5.2 examines OOD pretraining performance and finds that replacing unique high-quality
tokens with repeated tokens has only a limited effect when the total high-quality and web-data fractions
are fixed. Finally, Section 5.3 examines whether the optimal repetition count depends on the learning-rate
schedule.
| 5.1 Unique | versus | Repeated | Tokens | at a Fixed Domain | Fraction |     |     |
| ---------- | ------ | -------- | ------ | ----------------- | -------- | --- | --- |
In the previous section, we fix the amount of unique high-quality data and vary its repetition count. We now
consider the complementary setup studied by [27], wherethe total number of training tokens from a dataset is
fixed and repeated tokens are directly compared with the same number of unique data. Their results suggest
that, for up to roughly four repetitions, repeated data can achieve performance close to that of an equivalent
amount of unique data. However, this analysis does not distinguish how this trade-off varies across data
domains.
We therefore study the same question separately for different high-quality domains. Let α denote the fraction
of unique high-quality data and its repetition count. The total fraction of high-quality tokens consumed
e
| during training | is  |     |     |     |     |     |     |
| --------------- | --- | --- | --- | --- | --- | --- | --- |
ρ=αe.
8

Figure5 Finalvalidationlossatfixedtotalhigh-qualitydatafractions. Top: Math. Bottom: Wiki. We fix the
total high-quality-data fraction and vary the repetition count, such that more repetition corresponds to fewer unique
high-quality tokens. More unique data consistently yields lower validation loss in both domains. However, Math is
relatively robust to repetition, whereas Wiki degrades sharply when the repetition count increases beyond 2.
For a fixed ρ, increasing e requires decreasing the amount of unique data according to α=ρ/e. This setup
allows us to directly ask whether repeating a smaller unique dataset e times can match the performance of
using e times as much unique data once, under the same total high-quality token budget.
Figure 5 shows the results for Math and Wiki. We find that the result depends strongly on the domain.
For Math, increasing the repetition count from 1 to 4 causes only a small increase in validation loss. Thus,
repeated Math data can largely substitute for additional unique Math data, consistent with the observation of
[27]. In contrast, Wiki exhibits a clear degradation as repetition increases. While repeating the data twice
incurs only a modest loss increase, heavier repetition leads to substantially worse validation loss, indicating
that repeated Wiki tokens cannot effectively replace the corresponding amount of unique data.
These results show that the effectiveness of repeated data under a fixed token budget is domain dependent,
rather than being characterized by a universal repetition threshold. Additional results in Appendix C show
the same contrast across the remaining domains. Both Code and Medical show increasing validation loss as
more unique data is replaced by repeated data, although the magnitude of degradation varies across domains.
5.2 Effect of Repetition on OOD Pretraining Performance
Next, we study whether repetition within a high-quality domain affects pretraining performance outside that
domain. To isolate the effect of repetition, it is important to control the amount of web data used during
training. If we instead fix the amount of unique high-quality data and increase its repetition count, the total
amount of high-quality data increases accordingly, leaving fewer training tokens for web data. Any change in
OOD performance would then confound the effect of repetition with the change in web data.
We therefore adopt the fixed-domain-fraction setup from Section 5.1. Specifically, we fix the total fraction
of high-quality Math tokens, and hence also the amount of web data, while varying the repetition count by
changing the amount of unique high-quality data. This allows us to isolate how replacing unique high-quality
tokens with repeated tokens affects performance outside the repeated domain.
We evaluate the trained models on two OOD pretraining validation sets, ArXiv and News. Figure 6 reports
the results. In contrast to the clear domain-dependent degradation observed on in-domain validation sets,
the OOD validation loss remains largely stable as the repetition count changes. Across model sizes and total
high-quality data fractions, the differences between configurations using 1, 2, or 4 repetitions are generally
small.
9

|         |                                                         |     |     |     |     | Top: ArXiv. | Bottom: News. | Each |
| ------- | ------------------------------------------------------- | --- | --- | --- | --- | ----------- | ------------- | ---- |
| Figure6 | OODvalidationlossatfixedtotalhigh-qualitydatafractions. |     |     |     |     |             |               |      |
line fixes the total fraction of high-quality tokens, while the annotations indicate the corresponding repetition counts.
Unlike the in-domain validation loss, the OOD loss changes only slightly as unique tokens are replaced with repeated
| tokens and | shows no consistent | monotonic |     | relationship with the | repetition count. |     |     |     |
| ---------- | ------------------- | --------- | --- | --------------------- | ----------------- | --- | --- | --- |
These results suggest that, when the total fractions of high-quality and web tokens are fixed, replacing unique
high-qualitytokenswithrepeatedtokensmainlyaffectsperformancewithintherepeateddomain, whilehaving
| limited effect | on OOD     | pretraining   | performance. |           |     |     |     |     |
| -------------- | ---------- | ------------- | ------------ | --------- | --- | --- | --- | --- |
| 5.3 Effect     | of Various | Learning-Rate |              | Schedules |     |     |     |     |
Finally, we examine whether the optimal repetition count depends on the learning-rate schedule. We compare
a warmup-stable-decay (WSD) schedule with the decay phase starting at 0%, 25%, 50%, or 75% of training,
as well as a constant learning rate. For each schedule, we vary the fraction of unique high-quality data and
| the repetition | count while | keeping | all other | training settings | unchanged. |     |     |     |
| -------------- | ----------- | ------- | --------- | ----------------- | ---------- | --- | --- | --- |
As shown in Figure 7, the learning-rate schedule has a clear effect on the optimal repetition count. Earlier
decay causes the validation loss to increase after fewer repetitions, whereas delaying the decay shifts this
increase to a larger repetition count. With a constant learning rate, the model tolerates the largest number of
| repetitions | before degradation | occurs. |     |     |     |     |     |     |
| ----------- | ------------------ | ------- | --- | --- | --- | --- | --- | --- |
A possible explanation is that repeated samples seen during the low-learning-rate stage can be fitted more
closely, increasing the tendency to memorize sample-specific patterns. Delaying the decay keeps training at
a relatively high learning rate for longer, which may reduce this effect through stronger optimization noise
and implicit regularization. Overall, although excessive repetition eventually degrades performance across
all schedules, the learning-rate schedule determines how much repetition the model can tolerate before this
| degradation  | begins. |        |            |     |     |     |     |     |
| ------------ | ------- | ------ | ---------- | --- | --- | --- | --- | --- |
| 6 Conclusion | and     | Future | Directions |     |     |     |     |     |
In this work, we study domain data repetition across model scales while keeping the tokens-per-parameter
ratio fixed. We find that the optimal repetition count is strongly negatively correlated with the minimum
validation loss of the repeated domain: domains with lower validation loss generally support more repetitions.
At a fixed tokens-per-parameter ratio, the optimal repetition count increases mildly with model size, while
remaining nearly insensitive to the fraction of unique high-quality tokens over the range considered. These
observations suggest that repetition counts selected on smaller proxy models with the same TPP can provide
conservative estimates for larger models. Our theoretical analysis further provides an explanation for the
| observed | dependence on | validation | loss | and model scale. |     |     |     |     |
| -------- | ------------- | ---------- | ---- | ---------------- | --- | --- | --- | --- |
10

Figure7 Effectofthelearning-ratescheduleontheoptimalrepetitioncount. From left to right: WSD with
decay starting at 0%, 25%, 50%, and 75% of training, followed by a constant learning rate. Earlier decay leads to
degradation after fewer repetitions, while delaying or removing the decay allows more repetitions.
Our current setup repeats only one high-quality dataset in each training run. Future work should consider
mixtures in which multiple domains are repeated simultaneously and study their interactions. Another
direction is to develop a quantitative scaling rule that predicts the optimal repetition count of a large model
from small-model results, enabling more accurate and efficient data-recipe selection.
11

References
[1] Xiao Bi, Deli Chen, Guanting Chen, Shanhuang Chen, Damai Dai, Chengqi Deng, Honghui Ding, Kai Dong,
Qiushi Du, Zhe Fu, et al. Deepseek llm: Scaling open-source language models with longtermism. arXiv preprint
| arXiv:2401.02954, | 2024. |     |     |     |
| ----------------- | ----- | --- | --- | --- |
[2] Nicholas Carlini, Daphne Ippolito, Matthew Jagielski, Katherine Lee, Florian Tramer, and Chiyuan Zhang.
Quantifyingmemorizationacrossneurallanguagemodels. InTheEleventhInternationalConferenceonLearning
| Representations, | 2022. |     |     |     |
| ---------------- | ----- | --- | --- | --- |
[3] FrançoisChartonandJuliaKempe.Emergentpropertieswithrepeatedexamples.arXivpreprintarXiv:2410.07041,
2024.
[4] Jessica Chudnovsky, Joshua Kazdan, Noam Levi, Rylan Schaeffer, Yegor Denisov-Blanch, Bo He, Mehmet
Donmez, Sanmi Koyejo, and David Donoho. Internal data repetition destroys language models. arXiv preprint
| arXiv:2606.24998, | 2026. |     |     |     |
| ----------------- | ----- | --- | --- | --- |
[5] Rui Dai and Shuran Zheng. Explaining data mixing scaling laws. In Forty-third International Conference on
| Machine | Learning, 2026.| URL https://openreview.net/forum?id=joReaAnwnH.|     |     |
| ------- | --------------- | ----------------------------------------------- | --- | --- |
[6] Shizhe Diao, Yu Yang, Yonggan Fu, Xin Dong, Dan Su, Markus Kliegl, Zijia Chen, Peter Belcak, Yoshi Suhara,
Hongxu Yin, et al. Climb: Clustering-based iterative data mixture bootstrapping for language model pre-training.
| arXiv preprint | arXiv:2504.13161, | 2025. |     |     |
| -------------- | ----------------- | ----- | --- | --- |
[7] Sumanth Doddapaneni, Gowtham Ramesh, Mitesh Khapra, Anoop Kunchukuttan, and Pratyush Kumar. A
primer on pretrained multilingual language models. ACM Computing Surveys, 57(9):1–39, 2025.
[8] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman,
Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models. arXiv e-prints, pages
| arXiv–2407, | 2024. |     |     |     |
| ----------- | ----- | --- | --- | --- |
[9] Simin Fan, Matteo Pagliardini, and Martin Jaggi. Doge: Domain reweighting with generalization estimation. In
| International | Conference | on Machine | Learning, pages 12895–12915. | PMLR, 2024. |
| ------------- | ---------- | ---------- | ---------------------------- | ----------- |
[10] XinranGu,KaifengLyu,JiazhengLi,andJingzhaoZhang. Datamixingcaninducephasetransitionsinknowledge
| acquisition. | arXiv preprint | arXiv:2505.18091, | 2025. |     |
| ------------ | -------------- | ----------------- | ----- | --- |
[11] Mandy Guo, Zihang Dai, Denny Vrandečić, and Rami Al-Rfou. Wiki-40b: Multilingual language model dataset.
In Proceedings of the Twelfth Language Resources and Evaluation Conference, pages 2440–2452, 2020.
[12] Danny Hernandez, Tom Brown, Tom Conerly, Nova DasSarma, Dawn Drain, Sheer El-Showk, Nelson Elhage, Zac
Hatfield-Dodds, Tom Henighan, Tristan Hume, et al. Scaling laws and interpretability of learning from repeated
| data. arXiv | preprint arXiv:2205.10487, |     | 2022. |     |
| ----------- | -------------------------- | --- | ----- | --- |
[13] Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego
deLasCasas,LisaAnneHendricks,JohannesWelbl,AidanClark,etal. Trainingcompute-optimallargelanguage
models. In Proceedings of the 36th International Conference on Neural Information Processing Systems, pages
| 30016–30030, | 2022. |     |     |     |
| ------------ | ----- | --- | --- | --- |
[14] DayalSinghKalraandMaissamBarkeshli. Quantifyinghyperparametertransferandtheimportanceofembedding
layer learning rate. arXiv preprint arXiv:2605.21486, 2026. doi: 10.48550/arXiv.2605.21486.
[15] Feiyang Kang, Yifan Sun, Bingbing Wen, Si Chen, Dawn Song, Rafid Mahmood, and Ruoxi Jia. Autoscale:
Scale-aware data mixing for pre-training llms. arXiv preprint arXiv:2407.20177, 2024.
[16] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec
Radford,JeffreyWu,andDarioAmodei.Scalinglawsforneurallanguagemodels.arXivpreprintarXiv:2001.08361,
2020.
[17] Joshua Kazdan, Noam Levi, Rylan Schaeffer, Jessica Chudnovsky, Abhay Puri, Bo He, Mehmet Donmez, Sanmi
Koyejo, and David Donoho. Scale dependent data duplication. arXiv preprint arXiv:2603.06603, 2026.
[18] Katherine Lee, Daphne Ippolito, Andrew Nystrom, Chiyuan Zhang, Douglas Eck, Chris Callison-Burch, and
Nicholas Carlini. Deduplicating training data makes language models better. In Proceedings of the 60th Annual
Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 8424–8445, 2022.
12

[19] Binghui Li, Fengling Chen, Zixun Huang, Lean Wang, and Lei Wu. Functional scaling laws in kernel regression:
Loss dynamics and learning rate schedules. In The Thirty-ninth Annual Conference on Neural Information
| Processing | Systems, | 2025.| URL https://openreview.net/forum?id=dpllevHMbc.|     |     |     |     |
| ---------- | -------- | ----- | ----------------------------------------------- | --- | --- | --- | --- |
[20] Jeffrey Li, Alex Fang, Georgios Smyrnis, Maor Ivgi, Matt Jordan, Samir Gadre, Hritik Bansal, Etash Guha,
Sedrick Keh, Kushal Arora, et al. Datacomp-lm: In search of the next generation of training sets for language
models. Advances in Neural Information Processing Systems, 37:14200–14282, 2024.
[21] R Li, LB Allal, Y Zi, N Muennighoff, D Kocetkov, C Mou, M Marone, C Akiki, J Li, J Chim, et al. Starcoder:
| May the | source | be with you! | Transactions | on  | machine | learning research, | 2023. |
| ------- | ------ | ------------ | ------------ | --- | ------- | ------------------ | ----- |
[22] Licong Lin, Jingfeng Wu, Sham M. Kakade, Peter Bartlett, and Jason D. Lee. Scaling laws in linear regression:
Compute, parameters, and data. In The Thirty-eighth Annual Conference on Neural Information Processing
| Systems, | 2024.| URL https://openreview.net/forum?id=PH7sdEanXP.|     |     |     |     |     |
| -------- | ----- | ----------------------------------------------- | --- | --- | --- | --- | --- |
[23] Fengze Liu, Weidong Zhou, Binbin Liu, Ping Guo, Zijun Wang, Bingni Zhang, Yifan Zhang, Yifeng Yu, Xiaohuan
Zhou, and Taifeng Wang. Infolaw: Information scaling laws for large language models with quality-weighted
| mixture | data and | repetition. | arXiv | preprint | arXiv:2605.02364, | 2026. |     |
| ------- | -------- | ----------- | ----- | -------- | ----------------- | ----- | --- |
[24] Jingyuan Liu, Jianlin Su, Xingcheng Yao, Zhejun Jiang, Guokun Lai, Yulun Du, Yidao Qin, Weixin Xu, Enzhe
Lu, Junjie Yan, et al. Muon is scalable for llm training. arXiv preprint arXiv:2502.16982, 2025.
[25] Qian Liu, Xiaosen Zheng, Niklas Muennighoff, Guangtao Zeng, Longxu Dou, Tianyu Pang, Jing Jiang, and
Min Lin. Regmix: Data mixture as regression for language model pre-training. In The Thirteenth International
| Conference | on Learning | Representations, |     | 2024. |     |     |     |
| ---------- | ----------- | ---------------- | --- | ----- | --- | --- | --- |
[26] Justin Lovelace, Christian Belardi, Srivatsa Kundurthy, Shriya Sudhakar, and Kilian Q Weinberger. Prescriptive
| scaling laws | for | data constrained | training. | arXiv | preprint | arXiv:2605.01640, | 2026. |
| ------------ | --- | ---------------- | --------- | ----- | -------- | ----------------- | ----- |
[27] Niklas Muennighoff, Alexander Rush, Boaz Barak, Teven Le Scao, Nouamane Tazi, Aleksandra Piktus, Sampo
Pyysalo, Thomas Wolf, and Colin A Raffel. Scaling data-constrained language models. Advances in Neural
| Information | Processing | Systems, | 36:50358–50376, |     | 2023. |     |     |
| ----------- | ---------- | -------- | --------------- | --- | ----- | --- | --- |
[28] Keiran Paster, Marco Dos Santos, Zhangir Azerbayev, and Jimmy Ba. Openwebmath: An open dataset of
high-quality mathematical web text. In International Conference on Learning Representations, volume 2024,
| pages 20357–20379, |     | 2024. |     |     |     |     |     |
| ------------------ | --- | ----- | --- | --- | --- | --- | --- |
[29] GuilhermePenedo,HynekKydlíček,AntonLozhkov,MargaretMitchell,ColinRaffel,LeandroVonWerra,Thomas
Wolf, et al. The fineweb datasets: Decanting the web for the finest text data at scale. Advances in Neural
| Information | Processing | Systems, | 37:30811–30849, |     | 2024. |     |     |
| ----------- | ---------- | -------- | --------------- | --- | ----- | --- | --- |
[30] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei
Li, and Peter J Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. Journal of
| machine | learning | research, | 21(140):1–67, | 2020. |     |     |     |
| ------- | -------- | --------- | ------------- | ----- | --- | --- | --- |
[31] Anastasiia Sedova, Skyler Seto, Natalie Schluter, and Pierre Ablin. Scaling laws for mixture pretraining under
| data constraints. |     | arXiv preprint | arXiv:2605.12715, |     | 2026. |     |     |
| ----------------- | --- | -------------- | ----------------- | --- | ----- | --- | --- |
[32] Mustafa Shukor, Louis Bethune, Dan Busbridge, David Grangier, Enrico Fini, Alaaeldin El-Nouby, and Pierre
Ablin. Scaling laws for optimal data mixtures. arXiv preprint arXiv:2507.09404, 2025.
[33] Ross Taylor, Marcin Kardas, Guillem Cucurull, Thomas Scialom, Anthony Hartshorn, Elvis Saravia, Andrew
Poulton, Viktor Kerkez, and Robert Stojnic. Galactica: A large language model for science. arXiv preprint
| arXiv:2211.09085, |     | 2022. |     |     |     |     |     |
| ----------------- | --- | ----- | --- | --- | --- | --- | --- |
[34] GeminiTeam,RohanAnil,SebastianBorgeaud,Jean-BaptisteAlayrac,JiahuiYu,RaduSoricut,JohanSchalkwyk,
Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. arXiv
| preprint | arXiv:2312.11805, |     | 2023. |     |     |     |     |
| -------- | ----------------- | --- | ----- | --- | --- | --- | --- |
[35] BoqianWu,QiaoXiao,PatrikOkanovic,TomaszSternal,MauricevanKeulen,MykolaPechenizkiy,ElenaMocanu,
Torsten Hoefler, and Decebal Constantin Mocanu. When data is scarce: Scaling sparse language models with
| repeated | training. | arXiv | preprint arXiv:2606.01155, |     | 2026. |     |     |
| -------- | --------- | ----- | -------------------------- | --- | ----- | --- | --- |
[36] SangMichaelXie,HieuPham,XuanyiDong,NanDu,HanxiaoLiu,YifengLu,PercySLiang,QuocVLe,Tengyu
Ma, and Adams Wei Yu. Doremi: Optimizing data mixtures speeds up language model pretraining. Advances in
| Neural Information |     | Processing | Systems, | 36:69798–69818, |     | 2023. |     |
| ------------------ | --- | ---------- | -------- | --------------- | --- | ----- | --- |
13

[37] Fuzhao Xue, Yao Fu, Wangchunshu Zhou, Zangwei Zheng, and Yang You. To repeat or not to repeat: Insights
from scaling llm under token-crisis. Advances in Neural Information Processing Systems, 36:59304–59322, 2023.
[38] Tingkai Yan, Haodong Wen, Binghui Li, Kairong Luo, Wenguang Chen, and KaifengLyu. Larger datasets can be
repeatedmore: Atheoreticalanalysisofmulti-epochscalinginlinearregression. arXivpreprintarXiv:2511.13421,
2025.
[39] Jiasheng Ye, Peiju Liu, Tianxiang Sun, Jun Zhan, Yunhua Zhou, and Xipeng Qiu. Data mixing laws: Optimizing
data mixtures by predicting language modeling performance. In The Thirteenth International Conference on
Learning Representations, 2025.
14

Appendix
| A   | General | Implementation |     |     | Details |     |     |
| --- | ------- | -------------- | --- | --- | ------- | --- | --- |
In this section, we describe the datasets and training hyperparameters used in our experiments.
| A.1 | Details | of  | Datasets |     |     |     |     |
| --- | ------- | --- | -------- | --- | --- | --- | --- |
Our pretraining corpus consists of general web data and several high-quality domain-specific datasets. The
general web data contains content from diverse sources, covering a broad range of topics and writing styles.
| The | high-quality | data | includes | four | domains: |     |     |
| --- | ------------ | ---- | -------- | ---- | -------- | --- | --- |
• A multilingual programming corpus covering a range of programming languages and
|     | Code                 | data. |     |            |     |     |     |
| --- | -------------------- | ----- | --- | ---------- | --- | --- | --- |
|     | software-development |       |     | scenarios. |     |     |     |
• A bilingual mathematical corpus containing educational materials, mathematical problems,
Mathdata.
|     | and | step-by-step | solutions | across | different | difficulty | levels. |
| --- | --- | ------------ | --------- | ------ | --------- | ---------- | ------- |
• Encyclopedic text covering diverse concepts, entities, and factual knowledge.
Wikidata.
• Medicaldata. A collection of medical and health-related content covering biomedical knowledge, clinical
|     | topics, | and health | education. |                 |     |     |     |
| --- | ------- | ---------- | ---------- | --------------- | --- | --- | --- |
| A.2 | Details | of         | Training   | Hyperparameters |     |     |     |
The total training-token budget was scaled proportionally with model size under a fixed tokens-per-parameter
ratio. Following [1], we set the learning rate and global batch size for different model sizes according to
power-law functions of the model size. The learning rate was linearly warmed up for the first 200 optimization
steps and was then held constant for the remainder of training. We used an attention dropout rate of 0.1.
| Optimization |               | used | the Muon | optimizer  | [24],   | a variant  | of AdamW. |
| ------------ | ------------- | ---- | -------- | ---------- | ------- | ---------- | --------- |
| B            | Additional    |      | Results  | on         | Section | 4.1        |           |
| In           | this section, | we   | present  | additional | results | of Section | 4.1.      |
Figures 8, 9, 10, and 11 present the complete results for Math, Wiki, Code, and Medical. Among the four
domains, Math supports the most repetition, with an optimal repetition count of about 5–6, followed by Code
and Wiki, while Medical has the lowest optimal repetition count of about 3–4. For each domain, the optimal
repetition count increases with model size. In contrast, for a fixed model size, the optimal repetition count
remains nearly unchanged across different values of α. Overall, all experimental results are consistent with
| the | observations | in  | the main | text. |     |     |     |
| --- | ------------ | --- | -------- | ----- | --- | --- | --- |
Figure8 FinalvalidationlossacrossrepetitioncountsforMath. Each panel corresponds to a different model
size, and each curve represents a different fraction of unique high-quality data. All configurations are trained for the
full token budget associated with the corresponding model size. The validation loss is generally minimized between 5
and 6 repetitions. Increasing the unique data fraction reduces the absolute validation loss but has little effect on the
| optimal | repetition | count, | which | increases | only | mildly with | model size. |
| ------- | ---------- | ------ | ----- | --------- | ---- | ----------- | ----------- |
15

Figure9 FinalvalidationlossacrossrepetitioncountsforWikipedia. Compared with Math, Wikipedia reaches
its minimum validation loss earlier, typically after 3 to 4 repetitions, while showing the same stability across unique
| data fractions | and | mild increase |     | with model | size. |     |
| -------------- | --- | ------------- | --- | ---------- | ----- | --- |
Figure10 FinalvalidationlossacrossrepetitioncountsforCode. Code generally reaches its minimum validation
loss after 4 to 5 repetitions. The optimal repetition count remains stable across unique data fractions and increases
| mildly with | model | size. |     |     |     |     |
| ----------- | ----- | ----- | --- | --- | --- | --- |
Figure 11 Final validation loss across repetition counts for Medical. Medical generally reaches its minimum
validation loss after 3 to 4 repetitions. As in the other domains, the optimal repetition count is largely insensitive to
| the unique       | data | fraction   | and increases | only       | mildly with        | model size. |
| ---------------- | ---- | ---------- | ------------- | ---------- | ------------------ | ----------- |
| C Additional     |      | Results    |               | on Section | 5.1                |             |
| In this section, |      | we present | additional    |            | results of Section | 5.1.        |
Figure 12 shows the results under the same fixed-token-budget setup as in the main text. For each curve, the
total fraction of high-quality training tokens is fixed, while increasing the repetition count reduces the amount
of unique high-quality data. This directly compares repeated data with an equivalent number of fresh unique
tokens.
The results further show that the effectiveness of repetition differs across domains. Code and Medical behave
similarly to Wikipedia, with validation loss increasing more noticeably as more unique data is replaced by
repeated data. These results further support that whether repeated data can match fresh data under a fixed
| token budget | depends |     | strongly | on the | data domain. |     |
| ------------ | ------- | --- | -------- | ------ | ------------ | --- |
16

Figure12 Additionalresultsatfixedtotalhigh-qualitydatafractions. Top: Code. Bottom: Medical. Code and
Medical behave similarly to Wikipedia and shows a clearer degradation as more unique data is replaced by repeated
data.
D Proofs
| In this section, |     | we provide | the proofs |     | for the | results | in Section | 4.2. |     |     |     |     |     |
| ---------------- | --- | ---------- | ---------- | --- | ------- | ------- | ---------- | ---- | --- | --- | --- | --- | --- |
| D.1 Proof        | of  | Theorem    | 4.2        |     |         |         |            |      |     |     |     |     |     |
Proof of Theorem 4.2. For coordinate k, condition on the count M = m of samples x = e , where M ∼
|     |     |     |     |     |     |     |     |     | k   |     | i   | k   | k   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Binomial(D,p ) with probability π . The exact averaged population risk is
|     | k   |     |          | k,m      |     |          |          |          |      |       |          |     |     |
| --- | --- | --- | -------- | -------- | --- | -------- | -------- | -------- | ---- | ----- | -------- | --- | --- |
|     |     |     |          |          |     | N        | D        |  |      | σ2    |  |     |     |
|     |     |     |          |  |     |  |  |          |      |       |          |     |     |
|     |     | 2R  | (r;β,σ)= |          | k−β | +        | π        | k−βa2r+p |      | (1−ar | )2 ,     |     |     |
|     |     | D,N |          |          |     |          | k,m      |          | m km |       | m        |     |     |
|     |     |     |          | k>N      |     | k=1m=0   |          |          |      |       |          |     |     |
where =1−ηm/D, and the variance term is defined to be when m=0.
| a m |     |     |     |     |     |     |     | 0   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Let F(r):=2R (r;β,σ ) and G(r):=2R (r;β,σ ). Increasing the noise variance from σ2 to σ2 gives
|                 |     | D,N   | 1   |              |     | D,N      | 2        |          |     |     |     | 1   | 2   |
| --------------- | --- | ----- | --- | ------------ | --- | -------- | -------- | -------- | --- | --- | --- | --- | --- |
| G(r)=F(r)+∆(r), |     | where |     |              |     |          |          |          |     |     |     |     |     |
|                 |     |       |     |              |     |          | N D      |          |     |     |     |     |     |
|                 |     |       |     |              |     |  |  | p k(1−ar |     |     |     |     |     |
|                 |     |       |     | ∆(r)=(σ2−σ2) |     |          | π        |          | )2. |     |     |     |     |
|                 |     |       |     |              | 2   | 1        |          | k,mm     | m   |     |     |     |     |
k=1m=1
The function ∆(r) is non-decreasing in r, and it is strictly increasing when σ2 > σ2. Let r and r be
|     |     |     |     |     |     |     |     |     |     | 2   | 1   | F   | G   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
the earliest minimizers of F and G, respectively. Suppose that r > r . By the optimality of r and the
|              |     |     |     |       |       |     |       | G     | F     |     |     | F   |     |
| ------------ | --- | --- | --- | ----- | ----- | --- | ----- | ----- | ----- | --- | --- | --- | --- |
| monotonicity | of  | ∆,  |     |       |       |     |       |       |       |     |     |     |     |
|              |     |     | G(r | )=F(r | )+∆(r |     | )≥F(r | )+∆(r | )=G(r | ).  |     |     |     |
|              |     |     | G   |       | G     | G   |       | F     | F     | F   |     |     |     |
If the inequality is strict, it contradicts the optimality of r . If equality holds, it contradicts r being the
|                     |     |            |     |     |     |     |     | G   |     |     |     | G   |     |
| ------------------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| earliest minimizer. |     | Therefore, |     |     | .   |     |     |     |     |     |     |     |     |
r ≤r
|             |            |     | G           | F     |       |                       |          |     |     |     |     |     |     |
| ----------- | ---------- | --- | ----------- | ----- | ----- | --------------------- | -------- | --- | --- | --- | --- | --- | --- |
| It remains  | to derive  | the | small-noise | rate. | Write | τ =σ2                 | and      |     |     |     |     |     |     |
|             |            |     |             |       | H     | (r):=2R               | (r;β,σ). |     |     |     |     |     |     |
|             |            |     |             |       | τ     |                       | D,N      |     |     |     |     |     |     |
| Its forward | difference | is  |             |       |       |                       |          |     |     |     |     |     |     |
|             |            |     |             |       |       |  N  D |          |     |     |     |     |     |     |
)ar
|     |     | H   | τ (r+1)−H | τ (r)= |     |     | π k,m (1−a | m   |     |     |     |     |     |
| --- | --- | --- | --------- | ------ | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
m
k=1m=1
|     |     |     |     |     |     |  | τ     |  |        | τ  |  |     |     |
| --- | --- | --- | --- | --- | --- | --------- | ----- | -------- | ------ | ---------- | --------- | --- | --- |
|     |     |     |     |     |     | · 2p      | −(1+a | )        | k−β +p | ar         | .         |     |     |
|     |     |     |     |     |     |           | km    | m        |        | km         | m         |     |     |
17

Let a=a =1−η/D. The contribution from m=1 can be written as Aτar−B a2r, where
1 τ
N N

A=2(1−a) π p >0, B =(1−a)(1+a) π (k−β +p τ)>0.
k,1 k τ k,1 k
k=1 k=1
IfD ≥2,leta =1−2η/D <a;ifD =1,theremainderbelowisidenticallyzero. ToevaluateH (r+1)−H (r),
2 τ τ
we split it as follows:
N D
   τ  τ
H (r+1)−H (r)=Aτar−B a2r+ π (1−a )ar · 2p −(1+a ) k−β +p ar .
τ τ τ k,mmmkmmkmmk=1m=2

:=Eτ(r)
Since D and N are fixed, the contribution E (r) from m ≥ 2 satisfies, uniformly for 0 < τ ≤ 1, |E (r)| ≤
τ τ
C  τar+a2r for a constant C independent of r and τ.
2 2
By the optimality of r ,
τ
H (r +1)−H (r )≥0, H (r )−H (r −1)≤0.
τ τ τ τ τ τ τ τ
Suppose first that D ≥ 2, and write ρ = a
2
/a < 1. Setting x = arτ in the first inequality gives
 B
τ
−Cρ2rτ  x≤(A+Cρrτ)τ.Sincer
τ
→∞andB
τ
→B
0
>0,itfollowsthatarτ ≤C
1
τ,forallsufficiently
small τ. Similarly, setting y = arτ−1 in the second inequality gives  A−Cρrτ−1 τ ≤  B
τ
+Cρ2(rτ−1) y,
and hence arτ ≥ C
2
τ for a constant C
2
> 0 independent of τ. When D = 1, the same two bounds follow
directly because E
τ
(r)=0. Therefore, arτ =Θ(τ). Taking logarithms and recalling that τ =σ2 yields
log(1/σ2)
r∗(D,N;β,σ)= +O(1).
−log(1−η/D)
D.2 Proof of Theorem 4.3
Proof of Theorem 4.3. Let ∆ (r):=2R (r)−2R (r) and set j =N +1. The exact risk increment
N D,N+1 D,N
is ∆ (r)= D π h (r), where h (r)=j−β(a2r−1)+c j−ασ2(1−ar )2. The forward difference is
N m=1 j,m j,m j,m m α m m
h (r+1)−h (r)=(1−a )ar
j,m j,m m m
 σ2  σ2
· 2c j−α −(1+a ) j−β +c j−α ar .
α m m α m m
The bracketed term is minimized at r =0. Thus, h (r+1)−h (r)≥0 for all r ≥0 provided that
j,m j,m
σ2
c j−α (1−a )≥j−β(1+a ).
α m m m
Using 1−a =ηm/D and 1+a ≤2−η/D for m≥1, a sufficient condition ismmD(2−η/D)
jβ−α ≥ .
c ησ2
α
When N >N (D,σ2), this condition holds for j =N +1, implying that ∆ (r) is non-decreasing in r.
0 N
Let F(r):=2R (r) and G(r):=2R (r)=F(r)+∆ (r), with respective earliest minimizers r and
D,N D,N+1 N F
r . Suppose that r >r . By the optimality of r and the monotonicity of ∆ ,
GGFFNG(r )=F(r )+∆ (r )≥F(r )+∆ (r )=G(r ).
GGNGFNFF
18

As in the previous proof, a strict inequality contradicts the optimality of r , while equality contradicts the
G
| earliest-minimizer |           | convention. |         | Therefore, |          | r ≤r | .             |                 |     |     |     |     |     |
| ------------------ | --------- | ----------- | ------- | ---------- | -------- | ---- | ------------- | --------------- | --- | --- | --- | --- | --- |
|                    |           |             |         |            |          | G    | F             |                 |     |     |     |     |     |
| The stated         | crossover | order       | follows |            | directly | from |               |                 |     |     |     |     |     |
|                    |           |             |         |            |          |      |  2D−η | 1/(β−α) |     |     |     |     |     |
(D,σ2)=
|     |     |     |     |     | N 0 |     |     |     | .   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     | c   | ησ2 |     |     |     |     |     |
α
| D.3 Proof | of  | Theorem |     | 4.4 |     |     |     |     |     |     |     |     |     |
| --------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Proof of Theorem 4.4. For coordinate k, let M ∼Binomial(D,p ) and a =1−ηm/D. From the exact risk
|          |         |     |     |     |     | k   |     |     | k   | m   |     |     |     |
| -------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| formula, | we have |     |     |     |     |     |     |     |     |     |     |     |     |
N
|     |     |             |     |     |      | η   |  k−βE |        |     |  |     |     |     |
| --- | --- | ----------- | --- | --- | ---- | --- | -------------------- | ------ | --- | ------- | --- | --- | --- |
|     |     | 2R (r+1)−2R |     |     | (r)= | −   |                      | M (1+a |     | )a2r    |     |     |     |
|     |     | D,N         |     | D,N |      | D   |                      | k      | Mk  | Mk      |     |     |     |
k=1
|     |     |     |     |     |     |  |     |  |     |  |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | ------------------ | --- | --------- | --- | --- | --- |
SD(r)
N
|     |     |     |     |     |     | ησ2 |  |                     |       |       |           |           |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------------------- | ----- | ----- | --------- | --------- | --- |
|     |     |     |     |     |     | +   | p        | E 2ar | −(1+a | )a2r  |  1 |  . |     |
|     |     |     |     |     |     |     |          | k Mk                |       | Mk Mk | {Mk≥1}    |           |     |
D
k=1
|     |     |     |     |     |     |  |     |     |  |     |     |  |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | ------------------ | --- | --- | --------- | --- |
VD(r)
Both S (r) and V (r) are nonnegative. The first term is the marginal signal benefit, whereas the second is
|              | D        | D   |          |     |          |          |     |     |     |     |     |     |     |
| ------------ | -------- | --- | -------- | --- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- |
| the marginal | variance |     | penalty. |     |          |          |     |     |     |     |     |     |     |
|              |          |     |          |     |  |  |     |     |     |     |     |     |     |
Wefirstconsider1≪r ≤D. Byexp η r m  −η rm ,E[zMk]=(1−p and E[M
|     |     |     |     |     | −   |         | ≤ar ≤exp |     |     |     | +p  | z)D | zMk]= |
| --- | --- | --- | --- | --- | --- | ------- | -------- | --- | --- | --- | --- | --- | ----- |
|     |     |     |     |     | D   | (1 − η) | m        |     | D   |     | k   | k   | k     |
Dp z(1−p +p z)D−1 the dominant coordinates satisfy p r ≍1, or equivalently k ≍r1/α. Standard sum–
| k        | k          | k    |        |           |     |         |        | k   |     |     |     |     |     |
| -------- | ---------- | ---- | ------ | --------- | --- | ------- | ------ | --- | --- | --- | --- | --- | --- |
| integral | comparison | then | gives, | uniformly |     | in this | range, |     |     |     |     |     |     |
N

|     |     |     |     | S (r)≍ |     | k−(α+β)exp(−crk−α)≍r |     |     |     | 1−α −β , |     |     |     |
| --- | --- | --- | --- | ------ | --- | -------------------- | --- | --- | --- | -------- | --- | --- | --- |
|     |     |     |     | D      |     |                      |     |     |     | α        |     |     |     |
k=1
and
|     |     |     |      | 2          | N              |     |     |               |     | 2         |       |     |     |
| --- | --- | --- | ---- | ---------- | -------------- | --- | --- | ------------- | --- | --------- | ----- | --- | --- |
|     |     |     |      | σ  |                |     |     |        |     |  σ | 1− α  |     |     |
|     |     | V   | (r)≍ |            | k−αexp(−crk−α) |     |     | 1−exp(−crk−α) |     | ≍         | r α . |     |     |
|     |     |     | D    | D          |                |     |     |               |     | D         |       |     |     |
k=1
Here and below, the positive constants denoted by c may differ from line to line. Since D/N →C and r ≤D,
0
truncatingthesumsatN doesnotchangetheseorders. Therefore, SD(r) Dr−β/α.Thesameestimateswith
≍
|     |     |     |     |     |     |     |     |     | VD(r) | σ2  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
one-sided constants also cover bounded r. Hence, there exist constants <C′ <∞, independent of D,
0<c 0
0
such that, for all sufficiently large D, S (r)>V (r),0≤r ≤c Dα/β, and S (r)<V (r),C′Dα/β ≤r ≤D.
|     |     |     |     |     | D   |     | D   | 0   |     | D   | D   | 0   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
It remains to exclude a later decrease when D. Let 1−η/D. Restricting the variance sum to
|     |     |     |     |     |     | r   | ≥   | a 1 = |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
coordinates with p ≤ D−1 and to the event M = 1 gives V (r) ≥ cσ2ar D1− 2α. Using a ≤ am and the
|     |     | k   |     |     |     |     | k         | D   |     | 1 α |        | m 1 |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | ------ | --- | --- |
|     |     |     |     |     |     |     | 1 − α − β |     |     |     | 1 − β/ | α   |     |
binomialidentitiesabovegivesS (r ) ≤ C a 2 r D . Consequently, S D ( r ) ≤ CarD = o(1 ), wherethe
|     |     |     |     | D   |     | 1   | α   |     |     | V ( r ) | 1 σ 2 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | ----- | --- | --- |
lastequalityfollowsfrom . Thus, theexactriskisincreasingforDeverywheniss uffi ciently
|     |     |     | β   | > α |     |     |     |     |     | r   | ≥ D | D   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
large.
We have shown that the exact risk is decreasing up to Dα/β and increasing after C′Dα/β. Therefore, its
c 0
0
| earliest | global | minimizer | satisfies |     |        |                  |     |     |     |     |     |     |     |
| -------- | ------ | --------- | --------- | --- | ------ | ---------------- | --- | --- | --- | --- | --- | --- | --- |
|          |        |           |           |     | c Dα/β | ≤r∗(D,N)≤C′Dα/β, |     |     |     |     |     |     |     |
|          |        |           |           |     | 0      |                  |     | 0   |     |     |     |     |     |
which proves
|     |     |     |     |     |     |           |     |   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | ----------------- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | r∗(D,N)=Θ |     | Dα/β              |     |     |     |     |     |
.
19
<!-- fetched-content:end -->
