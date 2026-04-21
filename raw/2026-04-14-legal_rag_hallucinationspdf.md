---
title: "Legal_RAG_Hallucinations.pdf"
type: url
captured: 2026-04-14T00:22:46.570305+00:00
source: android-share
url: "https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf"
content_hash: "sha256:553c5174c7d93ee426f70af57f130ffbb8bd20d85d0eea05b37210dcfaa2e25c"
tags: []
status: ingested
---

https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:45:01+00:00
- source_url: https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf
- resolved_url: https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf
- content_type: application/pdf
- image_urls: []

## Fetched Content
Journal of Empirical Legal Studies

ORIGINAL ARTICLE OPEN ACCESS

Hallucination- Free? Assessing the Reliability of Leading AI
Legal Research Tools
Varun Magesh1  |  Faiz Surani1  |  Matthew Dahl2  |  Mirac Suzgun3  |  Christopher D. Manning4  |  Daniel E. Ho5

1Regulation, Evaluation, and Governance Lab, Stanford University, Stanford, California, USA  |  2Yale University, New Haven, Connecticut,
USA  |  3Department of Computer Science, Stanford Law School, Regulation, Evaluation, and Governance Lab, Stanford University, Stanford, California,
USA  |  4Department of Linguistics, Department of Computer Science, Stanford Artificial Intelligence Laboratory, Stanford Institute for Human- Centered
AI, Regulation, Evaluation, and Governance Lab, Stanford University, Stanford, California, USA  |  5Stanford Law School, Department of Political Science,
Department of Computer Science, Stanford Institute for Human- Centered AI, Stanford Institute for Economic Policy Research, Regulation, Evaluation, and
Governance Lab, Stanford University, Stanford, California, USA

Correspondence: Daniel E. Ho (deho@stanford.edu)

Accepted: 14 March 2025

ABSTRACT
Legal practice has witnessed a sharp rise in products incorporating artificial intelligence (AI). Such tools are designed to assist
with  a  wide  range  of  core  legal  tasks,  from  search  and  summarization  of  caselaw  to  document  drafting.  However,  the  large
language models used in these tools are prone to “hallucinate,” or make up false information, making their use risky in high-
stakes domains. Recently, certain legal research providers have touted methods such as retrieval- augmented generation (RAG) as
“eliminating” or “avoid[ing]” hallucinations, or guaranteeing “hallucination- free” legal citations. Because of the closed nature of
these systems, systematically assessing these claims is challenging. In this article, we design and report on the first preregistered
empirical evaluation of AI- driven legal research tools. We demonstrate that the providers' claims are overstated. While halluci-
nations are reduced relative to general- purpose chatbots (GPT- 4), we find that the AI research tools made by LexisNexis (Lexis+
AI) and Thomson Reuters (Westlaw AI- Assisted Research and Ask Practical Law AI) each hallucinate between 17% and 33% of
the time. We also document substantial differences between systems in responsiveness and accuracy. Our article makes four key
contributions. It is the first to assess and report the performance of RAG- based proprietary legal AI tools. Second, it introduces
a comprehensive, preregistered dataset for identifying and understanding vulnerabilities in these systems. Third, it proposes a
clear typology for differentiating between hallucinations and accurate legal responses. Last, it provides evidence to inform the
responsibilities of legal professionals in supervising and verifying AI outputs, which remains a central open question for the
responsible integration of AI into law.

1   |   Introduction

In the legal profession, the recent integration of large language
models  (LLMs)  into  research  and  writing  tools  presents  both
unprecedented  opportunities  and  significant  challenges  (Kite-
Jackson 2023). These systems promise to perform complex legal
tasks,  but  their  adoption  remains  hindered  by  a  critical  flaw:
their tendency to generate incorrect or misleading information,

a  phenomenon  generally  known  as  “hallucination”  (Dahl
et al. 2024).

As some lawyers have learned the hard way, hallucinations are
not merely a theoretical concern (Weiser and Bromwich 2023).
In  one  highly  publicized  case,  a  New  York  lawyer  faced  sanc-
tions  for  citing  ChatGPT- invented  fictional  cases  in  a  legal
brief  (Weiser  2023);  many  similar  incidents  have  since  been

Varun Magesh and Faiz Surani contributed equally to this work.

This is an open access article under the terms of the Creative Commons Attribution-NonCommercial License, which permits use, distribution and reproduction in any medium, provided the

original work is properly cited and is not used for commercial purposes.

© 2025 The Author(s). Journal of Empirical Legal Studies published by Cornell Law School and Wiley Periodicals LLC.

Journal of Empirical Legal Studies, 2025; 0:1–27
https://doi.org/10.1111/jels.12413

1 of 27

documented (Weiser and Bromwich 2023). In his 2023 annual
report on the judiciary, Chief Justice John Roberts specifically
noted the risk of “hallucinations” as a barrier to the use of AI in
legal practice (Roberts 2023).

legal

Recently,  however,
technology  providers  such  as
LexisNexis and Thomson Reuters (parent company of Westlaw)
have  claimed  to  mitigate,  if  not  entirely  solve,  hallucination
risk (Casetext 2023; LexisNexis 2023b; Thomson Reuters 2023,
inter alia). They say their use of sophisticated techniques such

FIGURE  1    |    Comparison  of  hallucinated  and  incomplete  answers
across generative legal research tools. Hallucinated responses are those
that include false statements or falsely assert a source supports a state-
ment. Incomplete responses are those that either fail to address the us-
er's query (e.g., by refusing to answer or providing accurate but unre-
sponsive information) or fail to provide citations for otherwise factual
claims.

as retrieval- augmented  generation (RAG) largely prevents hal-
lucination in legal research tasks.1 (We provide details on RAG
systems in Section 3.1 below.)

However, none of these bold proclamations have been accompa-
nied by empirical evidence. Moreover, the term “hallucination”
itself  is  often  left  undefined  in  marketing  materials,  leading  to
confusion about which risks these tools genuinely mitigate. This
study seeks to address these gaps by evaluating the performance
of  AI- driven  legal  research  tools  offered  by  LexisNexis  (Lexis+
AI)  and  Thomson  Reuters  (Westlaw  AI- Assisted  Research  and
Ask Practical Law AI) and, for comparison, GPT- 4.

Our  findings,  summarized  in  Figure  1,  reveal  a  more  nuanced
reality  than  the  one  presented  by  these  providers:  while  RAG
appears to improve the performance of language models in an-
swering legal queries, the hallucination problem persists at sig-
nificant levels. To offer one simple example, shown in the top left
panel of Figure 2, the Westlaw system claims that a paragraph in
the  Federal  Rules  of  Bankruptcy  Procedure  (FRBP)  states  that
deadlines  are  jurisdictional.  But  no  such  paragraph  exists,  and
the underlying claim is itself unlikely to be true in light of the
Supreme Court's holding in Kontrick v. Ryan, 540 U.S. 443, 447–
48  &  448  n.3  (2004),  which  held  that  FRBP  deadlines  under  a
related provision were not jurisdictional.2

We also document substantial variation in system performance.
LexisNexis's  Lexis+  AI  is  the  highest- performing  system  we
test,  answering  65%  of  our  queries  accurately.  Westlaw's  AI-
Assisted  Research  is  accurate  42%  of  the  time,  but  halluci-
nates nearly twice as often as the other legal tools we test. And
Thomson  Reuters's  Ask  Practical  Law  AI  provides  incomplete
answers (refusals or ungrounded responses; see Section 4.3) on
more than 60% of our queries, the highest rate among the sys-
tems we tested.

FIGURE 2    |    Top left: Example of a hallucinated response by Westlaw's AI- Assisted Research product. The system makes up a statement in the
Federal Rules of Bankruptcy Procedure that does not exist. Top right: Example of a hallucinated response by LexisNexis's Lexis+ AI. Casey and its
undue burden standard were overruled by the Supreme Court in Dobbs v. Jackson Women's Health Organization, 597 U.S. 215 (2022); the correct an-
swer is rational basis review. Bottom left: Example of a hallucinated response by Thomson Reuters's Ask Practical Law AI. The system fails to correct
the user's mistaken premise—in reality, Justice Ginsburg joined the Court's landmark decision legalizing same- sex marriage—and instead provides
additional false information about the case. Bottom right: Example of a hallucinated response from GPT- 4, which generates a statutory provision that
does not exist.

2 of 27

Journal of Empirical Legal Studies, 2025

 17401461, 0, Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/jels.12413, Wiley Online Library on [23/04/2025]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseOur article makes four key contributions. First, we conduct the
first  systematic  assessment  of  leading  AI  tools  for  real- world
legal research tasks. Second, we manually construct a preregis-
tered dataset of over 200 legal queries for identifying and under-
standing  vulnerabilities  in  legal  AI  tools. We  run  these  queries
on LexisNexis (Lexis+ AI), Thomson Reuters (Ask Practical Law
AI), Westlaw  (AI- Assisted  Research),  and  GPT- 4  and  manually
review their outputs for accuracy and fidelity to authority. Third,
we offer a detailed typology to refine the understanding of “hal-
lucinations,”  which  enables  us  to  rigorously  assess  the  claims
made by AI service providers. Last, we not only uncover limita-
tions of current technologies, but also characterize the reasons
that  they  fail. These  results  inform  the  responsibilities  of  legal
professionals in supervising and verifying AI outputs, which re-
mains  an  important  open  question  for  the  responsible  integra-
tion of AI into law.

The rest of this work is organized as follows. Section 2 provides
an  overview  of  the  rise  of  AI  in  law  and  discusses  the  central
challenge of hallucinations. Section 3 describes the potential and
limitations  of  RAG  systems  to  reduce  hallucinations.  Section  4
proposes a framework for evaluating hallucinations in a legal RAG
system. Because legal research commonly requires the inclusion
of citations, we define a hallucination as a response that contains
either incorrect information or a false assertion that a source sup-
ports a proposition. Section 5 details our methodology to evaluate
the performance of AI- based legal research tools (legal AI tools).
Section 6 presents our results. We find that legal RAG can reduce
hallucinations  compared  to  general- purpose  AI  systems  (here,
GPT- 4),  but  hallucinations  remain  substantial,  wide- ranging,
and  potentially  insidious.  Section  7  discusses  the  limitations  of
our  study  and  the  challenges  of  evaluating  proprietary  legal  AI
systems, which have far more restrictive conditions of use than
AI  systems  available  in  other  domains.  Section  8  discusses  the
implications for legal practice and legal AI companies. Section 9
concludes with implications of our findings for legal practice.

The adoption of AI tools presents additional risks, different from
those encountered in previous evolutions of legal research. Legal
AI tools present unprecedented ethical challenges for lawyers,
including concerns about client confidentiality, data protection,
the  introduction  of  new  forms  of  bias,  and  lawyers'  ultimate
duty of supervision over their work product (Avery et al. 2023;
Cyphert  2021;  Walters  2019;  Yamane  2020).  Recognizing  this,
the bar associations of California (2023), New York (2024), and
Florida  (2024)  have  all  recently  published  guidance  on  how
AI  should  be  safely  and  ethically  integrated  into  their  mem-
bers' legal practices. Courts have weighed in as well: as of May
2024, more than 25 federal judges have issued standing orders
instructing attorneys to disclose or limit the use of AI in their
courtrooms (Law360 2024).

In  order  for  these  guidelines  to  be  effective,  however,  lawyers
need to first understand what exactly an AI tool is, how it works,
and the ways in which it might expose them to liability. Do dif-
ferent tools have different error rates—and what kinds of errors
are likely to manifest? What training do lawyers need in order to
spot these errors—and can they do anything as users to mitigate
them? Are there particular tasks that current AI tools are par-
ticularly  adept  at—and  are  there  any  that  lawyers  should  stay
away from?

This  paper  moves  beyond  previous  work  on  general- purpose
AI  tools  (Choi  et  al.  2024;  Dahl  et  al.  2024;  Schwarcz  and
Choi  2023)  by  answering  these  questions  specifically  for  legal
AI tools—namely, the tools that have been carefully developed
by  leading  legal  technology  companies  and  that  are  currently
being marketed to lawyers as avoiding many of the risks known
to exist in off- the- shelf offerings. In doing so, we aim to provide
the concrete empirical information that lawyers need in order to
assess the ethical and practical dangers of relying on these new
commercial AI products.

2   |   Background

2.1   |   The Rise and Risks of Legal AI

Lawyers  are  increasingly  using  AI  to  augment  their  legal  prac-
tice, and with good reason: from drafting contracts to analyzing
discovery  productions  to  conducting  legal  research,  these  tools
promise significant efficiency gains over traditional methods. As
of January 2024, at least 41 of the top 100 largest law firms in the
United States have begun to use some form of AI in their practice
(Henry  2024);  among  a  broader  sample  of  384  firms,  35%  now
report working with at least one generative AI provider (Collens
et al. 2024). And in a recent survey of 1200 lawyers practicing in
the United Kingdom, 14% say that they are using generative AI
tools weekly or more often (Greenhill 2024).

2.2   |   The Hallucination Problem

We focus on one problem of AI that has received considerable at-
tention in the legal community: “hallucination,” or the tendency
of  AI  tools  to  produce  outputs  that  are  demonstrably  false.3  In
multiple  high- profile  cases,  lawyers  have  been  reprimanded  for
submitting  filings  to  courts  citing  nonexistent  case  law  halluci-
nated by an AI service (Weiser 2023; Weiser and Bromwich 2023).
Previous work has found that general- purpose LLMs hallucinate
on legal queries on average between 58% and 82% of the time (Dahl
et al. 2024). Yet this prior work did not examine tools specifically
developed for the legal setting, such as tools that use LLMs with
auxiliary legal databases and RAG. And because these tools are
placed prominently before lawyers on leading legal research plat-
forms (i.e., LexisNexis and Thomson Reuters/Westlaw), a system-
atic examination is sorely needed.

The  scale  of  adoption  suggests  a  potential  transformation  of
legal research, not unlike the adoption of online legal research
databases beginning in the 1970s (Berring 1986). Prior work in
that context, for instance, showed that online (vs. print) materi-
als led to distinct research strategies (Krieger and Kuh 2014) and
that legal research databases surfaced substantively different re-
sults from one another (Mart 2018).

In  this  article,  we  focus  on  factual  hallucinations.  In  the  legal
setting, there are three primary ways that a model can be said to
hallucinate: it can be unfaithful to its training data, unfaithful
to its prompt input, or unfaithful to the true facts of the world
(Dahl et al. 2024). Because we are interested in legal research
tools that are meant to help lawyers understand legal facts, we
focus on the third category: factual hallucinations.4 However, in

3 of 27

 17401461, 0, Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/jels.12413, Wiley Online Library on [23/04/2025]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseFIGURE 3    |    Schematic diagram of a retrieval- augmented generation (RAG) system. Given a user query (left), the typical process consists of two
steps: (1) retrieval (middle), where the query is embedded with natural language processing and a retrieval system takes embeddings and retrieves
the relevant documents (e.g., Supreme Court cases); and (2) generation (right), where the retrieved texts are fed to the language model to generate
the response to the user query. Any of the subsidiary steps may introduce errors and hallucinations into the generated response. (Icons are credited
to FlatIcon.)

Section 4.3 below, we also expand on this definition by decom-
posing  factual  hallucinations  into  two  dimensions: correctness
and  groundedness.  We  hope  that  this  distinction  will  provide
useful guidance for users seeking to understand the precise way
that these tools can be helpful or harmful.

3   |   Retrieval- Augmented Generation (RAG)

3.1   |   The Promise of RAG

Across  many  domains,  the  fairly  new  technique  of  retrieval-
augmented generation (RAG) is being seen and heavily promoted
as  the  key  technology  for  making  LLMs  effective  in  domain-
specific contexts. It allows general LLMs to make effective use of
company-  or domain- specific data and to produce more detailed
and  accurate  answers  by  drawing  directly  from  retrieved  text.
In  particular,  RAG  is  commonly  touted  as  the  solution  for  legal
hallucinations. In a February 2024 interview, a Thomson Reuters
executive  asserted  that,  within  Westlaw  AI- Assisted  Research,
RAG  “dramatically  reduces  hallucinations  to  nearly  zero”
(Ambrogi 2024). Similarly, LexisNexis has said that RAG enables
it to “deliver accurate and authoritative answers that are grounded
in the closed universe of authoritative content” (Wellen 2024a).5

As depicted in Figure 3, RAG comprises two primary steps to
transform a query into a response: (1) retrieval and (2) genera-
tion (Gao et al. 2024; Lewis et al. 2020). Retrieval is the process
of  selecting  relevant  documents  from  a  large  universe  of  doc-
uments.  This  process  is  familiar  to  anyone  who  uses  a  search
engine: using keywords, user information, and other context, a
search engine quickly identifies a handful of relevant web pages
out of the millions available on the internet. Retrieval systems
can be simple, like a keyword search, or complex, involving ma-
chine learning techniques to capture the semantic meaning of a
query (such as neural text embeddings).

generate a response. Many RAG systems involve additional pre-
and  post- processing  of  their  inputs  and  outputs  (e.g.,  filtering
and extraction depicted in the middle panel of Figure 3), but re-
trieval and generation are the hallmarks of a RAG pipeline.

The advantage of RAG is obvious: including retrieved information
in the prompt allows the model to respond in an “open- book” set-
ting rather than in “closed- book” one. The LLM can use the infor-
mation in the retrieved documents to inform its response, rather
than its hazy internal knowledge. Instead of generating text that
conforms to the general trends of a highly compressed represen-
tation of its training data, the LLM can rely on the full text of the
relevant information that is injected directly into its prompt.

For  example,  suppose  that  an  LLM  is  asked  to  state  the  year
that Brown v. Board of Education was decided. In a closed- book
setting, the LLM, without access to an external knowledge base,
would generate an answer purely based on its internal knowl-
edge learned during training—but a more obscure case might
have little or no information present in the training data, and
the  model  could  generate  a  realistic- sounding  year  that  may
or may not be accurate. In a RAG system, by contrast, the re-
triever would first look up the case name in a legal database, re-
trieve the relevant metadata, and then provide that to the LLM,
which  would  use  the  result  to  provide  the  user  a  response  to
their query.

On paper, RAG has the potential to substantially mitigate many
of the kinds of legal hallucinations that are known to afflict off-
the- shelf LLMs (Dahl et al. 2024)—the technique performs well
in many general question- answering situations (Guu et al. 2020a;
Lewis et al. 2020; Siriwardhana et al. 2023). However, as we show
in the next section, RAG systems are no panacea.

3.2   |   Limitations of RAG

With the retrieved documents in hand, the second step of gener-
ation involves providing those documents to a LLM along with
the  text  of  the  original  query,  allowing  the  LLM  to  use  both  to

There are several reasons that RAG is unlikely to fully solve the
hallucination problem (Barnett et al. 2024). Here, we highlight
some that are unique to the legal domain.

4 of 27

Journal of Empirical Legal Studies, 2025

 17401461, 0, Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/jels.12413, Wiley Online Library on [23/04/2025]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseFirst,  retrieval  is  particularly  challenging  in  law.  Many  popu-
lar  LLM  benchmarking  datasets  (Rajpurkar  et  al.  2016;  Yang
et  al.  2018)  contain  questions  with  clear,  unambiguous  refer-
ences  that  address  the  question  in  the  source  database.  Legal
queries, however, often do not admit a single, clear- cut answer
(Mik 2024). In a common law system, case law is created over
time by judges writing opinions; this precedent then builds on
precedent in the way that a chain novel might be written in seri-
atim (Dworkin 1986). By construction, these legal opinions are
not  atomic  facts;  indeed,  on  some  views,  the  law  is  an  “essen-
tially contested” concept (Waldron 2002). Thus, deciding what
to retrieve can be challenging in a legal setting. At best, a RAG
system must be able to locate information from multiple sources
across time and place in order to properly answer a query. And
at worst, there may be no set of available documents that defin-
itively answers the query, if the question presented is novel or
indeterminate.

Second, document relevance in the legal context is not based on
text alone. Most retrieval systems identify relevant documents
based on some kind of text similarity (Karpukhin et al. 2020).
But  the  retrieval  of  documents  that  only  seem  textually  rel-
evant—and  are  ultimately  irrelevant,  or  “distracting”—neg-
atively  affects  performance  on  general  question- answering
tasks (J. Chen et al. 2024; Cuconasu et al. 2024). Problems of
this type are likely to compound in the legal domain. In differ-
ent jurisdictions and in different time periods, the applicable
rule  or  the  relevant  jurisprudence  may  differ.  Even  similar-
sounding text in the correct time and place may not apply if
special conditions are not met. The problem may be worse if
a rule that applies in a special condition conflicts with a more
broadly applicable rule. The LLM may have been trained on a
much  greater  volume  of  text  supporting  the  broadly  applica-
ble rule and may be more faithful to its training data than to
the retrieval context. Consequently, designing a high- quality
research  tool  that  deals  with  this  problem  requires  careful
attention  to  non- textual  elements  of  retrieval  and  the  defer-
ence  of  the  model  to  different  sources  of  information.  These
challenges  are  familiar  to  lawyers  using  “natural  language”
searches, as opposed to more deterministic Boolean searches,
on legal research platforms.

Third,  the  generation  of  meaningful  legal  text  is  also  far  from
straightforward.  Legal  documents  are  generally  written  for
other lawyers immersed in the same issue, and they rely on an
immense amount of background knowledge to properly under-
stand and apply. A helpful generative legal research tool would
have  to  do  far  more  than  simple  document  summarization;  it
would need to synthesize facts, holdings, and rules from differ-
ent pieces of text while keeping the appropriate legal context in
mind. For example, consider this Lexis+ AI exchange:

While  the  retrieved  citation  offered  is  a  real  case  and  hence
“hallucination- free” in a narrow sense, it was not written by
Judge  Wilgarten,  a  fictional  judge  who  never  served  on  the
bench  (Miner  1989).6  And  while  the  generated  passages  are
based  on  the  actual  case,  the  second  sentence  contradicts
the  premise,  suggesting  Judge  Ellis  wrote  the  opinion,  but
the opinion was actually written by Judge Brinkema (and in-
volved a prior decision by Judge Ellis, which forms the basis
for the RAG response). Nor is the decision notable, as it was
an  unpublished  opinion  cited  only  once  outside  of  its  direct
history. Hallucinations are compounded by poor retrieval and
erroneous generation.

Conceptualizing the potential failure modes of legal RAG sys-
tems  requires  domain  expertise  in  both  computer  science  and
law. As is apparent once we examine the component parts of a
RAG system in Figure 3, each of the subsidiary steps (the em-
bedding, the design of lexical and semantic search, the number
of  documents  retrieved,  and  filtering  and  extraction)  involves
design  choices  that  can  affect  the  quality  of  output  (Barnett
et al. 2024), each with potentially subtle trade- offs (Belkin 2008).
In the next section, we devise a new task suite specifically de-
signed to probe the prevalence of RAG- resistant hallucinations,
complementing  existing  benchmarking  efforts  that  target  AI's
legal knowledge in general (Dahl et al. 2024) and its capacity for
legal reasoning (Guha et al. 2023).

4   |   Conceptualizing Legal Hallucinations

The binary notion of hallucination developed in Dahl et al. (2024)
does not fully capture the behavior of RAG systems, which are
intended  to  generate  information  that  is  both  accurate  and
grounded  in  retrieved  documents.  We  expand  the  framework
of legal hallucinations to two primary dimensions: correctness
and  groundedness.  Correctness  refers  to  the  factual  accuracy
of the tool's response (Section 4.1). Groundedness refers to the
relationship between the model's response and its cited sources
(Section 4.2).

Decomposing factual hallucinations in this way enables a more
nuanced  analysis  and  understanding  of  how  exactly  legal  AI
tools fail in practice. For example, a response could be correct
but improperly grounded. This might happen when retrieval re-
sults are poor or irrelevant, but the model happens to produce
the  correct  answer,  falsely  asserting  that  an  unrelated  source
supports its conclusion. This can mislead the user in potentially
dangerous ways.

4.1   |   Correctness

Prompt:  What  are  some  notable  opinions  written  by  Judge
Luther A. Wilgarten?

Lexis+  AI  Response:  One  of  the  notable  opinions  written  by
Judge  Luther  A.  Wilgarten  is  the  case  of  Luther  v.  Locke.  The
case citation is 2010 U.S. Dist. LEXIS 144868 and it was decided
in the Eastern District of Virginia on January 11, 2010. In this
case,  the  plaintiff  had  filed  a  Notice  of  Appeal  of  Judge  Ellis's
decision, but failed to properly prosecute the appeal. […]

We  say  that  a  response  is  correct  if  it  is  both  factually  correct
and relevant to the query. A response is incorrect if it contains
any  factually  inaccurate  information.  For  the  purposes  of  this
analysis,  we  label  an  answer  that  is  partially  correct—that  is,
one that contains correct information that does not fully address
the question—as correct. If a response is neither correct nor in-
correct, because the model simply declines to respond, we label
that as a refusal. See the top panel of Table 1 for examples of each
of these three codings of correctness.7

5 of 27

 17401461, 0, Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/jels.12413, Wiley Online Library on [23/04/2025]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseTABLE  1    |    A  summary  of  our  coding  criteria  for  correctness  and  groundedness,  along  with  hypothetical  responses  to  the  query  “Does  the
Constitution protect a right to same sex marriage?” that would fall under each of the categories. Groundedness is only applicable for correct responses.
The categories which qualify as a “hallucination” are bolded.

Description

Example

Correctness

Correct

Response is factually correct and relevant

Incorrect

Response contains factually inaccurate information

The right to same sex marriage is protected
under the U.S. Constitution. Obergefell
v. Hodges, 576 U.S. 644 (2015).

There is no right to same sex
marriage in the United States.

Model refuses to provide any answer
or provides an irrelevant answer

I'm sorry, but I cannot answer that
question. Please try a different query.

Refusal

Groundedness

Grounded

Key factual propositions make valid
references to relevant legal documents

Misgrounded

Key factual propositions are cited but the
source does not support the claim

Ungrounded

Key factual propositions are not cited

The right to same sex marriage is protected
under the U.S. Constitution. Obergefell
v. Hodges, 576 U.S. 644 (2015).

The right to same sex marriage is protected
under the U.S. Constitution. Miranda
v. Arizona, 384 U.S. 436 (1966).

The right to same sex marriage is
protected under the U.S. Constitution.

4.2   |   Groundedness

For correct responses, we additionally evaluate each response's
groundedness. A response is grounded if the key factual prop-
ositions  in  its  response  make  valid  references  to  relevant  legal
documents. A response is ungrounded if key factual propositions
are not cited. A response is misgrounded if key factual proposi-
tions are cited but misinterpret the source or reference an inap-
plicable  source.  See  the  bottom  panel  of  Table  1  for  examples
illustrating groundedness.

Note that our use of the term grounded deviates somewhat from
the notion in computer science. In the computer science litera-
ture, groundedness refers to adherence to the source documents
provided, regardless of the relevance or accuracy of the provided
documents (Agrawal et al. 2023). In this paper, by contrast, we
evaluate the quality of the retrieval system and the generation
model  together  in  the  legal  context.  Therefore,  when  we  say
grounded, we mean it in the legal sense—that is, responses that
are  correctly  grounded  in  actual  governing  caselaw.  If  the  re-
trieval system provides documents that are inappropriate to the
jurisdiction of interest, and the model cites them in its response,
we call that misgrounded, even though this might be a techni-
cally “grounded” response in the computer science sense.

4.3   |   Hallucination

We  now  adopt  a  precise  definition  of  a  hallucination  in  terms
of the above variables. A response is considered hallucinated if
it is either incorrect or misgrounded. In other words, if a model
makes a false statement or falsely asserts that a source supports
a statement, that constitutes a hallucination.

This definition provides technical clarity to the popular con-
cept  of  hallucination,  which  is  a  term  that  is  currently  being
used inconsistently by different industry actors. For example,
in  one  interview,  one  Thomson  Reuters  executive  appeared
to  refer  to  hallucinations  as  exclusively  instances  when  an
AI  system  fabricates  the  existence  of  a  case,  statute,  or  reg-
ulation,  distinct  from  more  general  problems  of  accuracy
(Ambrogi  2024).  Yet,  in  a  December  2023  press  release,  an-
other  Thomson  Reuters  executive  defined  hallucinations  dif-
ferently, as “responses that sound plausible but are completely
false” (Thomson Reuters 2023).

LexisNexis, by contrast, uses the term hallucination in yet a dif-
ferent way. LexisNexis claims that its AI tool provides “linked
hallucination- free legal citations” (LexisNexis 2023b), but, as we
demonstrate below, this claim can only be true in the most nar-
row sense of “hallucination,” in that their tool does indeed link
to real legal documents.8 If those linked sources are irrelevant,
or even contradict the AI tool's claims, the tool has, in our sense,
engaged  in  a  hallucination.  Failing  to  capture  that  dimension
of  hallucination  would  require  us  to  conclude  that  a  tool  that
links only to Brown v. Board of Education on every query (or pro-
vides  cases  for  fictional  judges  as  in  the  instance  of  Luther  A.
Wilgarten) has provided “hallucination- free” citations, a plainly
irrational result.

More concretely, consider the Casey example in Figure 2, where
the linked citation Planned Parenthood v. Reynolds is a real case
that has not been overturned.9 However, the model's answer re-
lies on Reynolds' description of Planned Parenthood v. Casey, a
case  that  has  been  overturned.  The  model's  response  is  incor-
rect,  and  its  citation  serves  only  to  mislead  the  user  about  the
reliability of its answer (Goddard et al. 2012).

6 of 27

Journal of Empirical Legal Studies, 2025

 17401461, 0, Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/jels.12413, Wiley Online Library on [23/04/2025]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseThese  errors  are  potentially  more  dangerous  than  fabricating
a  case  outright,  because  they  are  subtler  and  more  difficult  to
spot.10 Checking for these kinds of hallucinations requires users
to click through to cited references, read and understand the rel-
evant sources, assess their authority, and compare them to the
propositions the model seeks to support. Our definition reflects
this more complete understanding of “hallucination.”

4.4   |   Accuracy and Incompleteness

Alongside  hallucinations,  we  also  define  two  other  top- level
labels in terms of our correctness and groundedness variables:
accurate  responses,  which  are  those  that  are  both  correct  and
grounded,  and  incomplete  responses,  which  are  those  that  are
either refusals or ungrounded.

We  code  correct  but  ungrounded  responses  as  incomplete
because, unlike a misgrounded response, an ungrounded re-
sponse  does  not  actually  make  any  false  assertions.  Because
an  ungrounded  response  does  not  provide  key  information
(supporting  authorities)  that  the  user  needs,  it  is  marked
incomplete.

5   |   Methodology

5.1   |   AI- Driven Legal Research Tools

We  study  the  hallucination  rate  and  response  quality  of  three
available  RAG- based  AI  research  tools:  LexisNexis's  Lexis+
AI,  Thomson  Reuters's  Ask  Practical  Law  AI,  and  Westlaw's
AI- Assisted  Research.  As  nearly  every  practicing  U.S.  lawyer
knows, Thomson Reuters (the parent company of Westlaw) and
LexisNexis11 have historically enjoyed a virtual duopoly over the
legal research market (Arewa 2006) and continue to be two of the
largest incumbents now selling legal AI products (Ma et al. 2024).

Lexis+ AI functions as a standard chatbot interface, like ChatGPT,
with  a  text  area  for  the  user  to  enter  an  open- ended  inquiry.  In
contrast to traditional forms of legal search, “Boolean” connectors
and search functions like AND, OR, and W/n are neither required
nor supported. Instead, the user simply formulates their query in
natural language, and the model responds in kind. The user then
has the option to continue the chat by asking another question,
which the tool will respond to with the complete context of both
questions. Introduced in October 2023, Lexis+ AI states that it has
access  to  LexisNexis's  entire  repository  of  case  law,  codes,  rules,
constitution,  agency  decisions,  treatises,  and  practical  guidance,
all of which it presumably uses to craft its responses. While not
much  technical  detail  is  published,  it  is  known  that  Lexis+  AI
implements  a  proprietary  RAG  system  that  ensures  that  every
prompt “undergoes a minimum of five crucial checkpoints … to
produce the highest quality answer” (Wellen 2024b).12

Ask Practical Law AI, introduced in January 2024 and offered
on the Westlaw platform, is a more limited product, but it oper-
ates in a similar way. Like Lexis+ AI, Ask Practical Law AI also
functions as a chatbot, allowing the user to input their queries
in  natural  language  and  responding  to  them  in  the  same  for-
mat. However, instead of accessing all the primary sources that

Lexis+  AI  uses,  Ask  Practical  Law  AI  only  retrieves  informa-
tion from Thomson Reuters's database of “practical law” docu-
ments—“expert resources … that have been created and curated
by  more  than  650  bar- admitted  attorney  editors”  (Thomson
Reuters  2024b)  promising  “90,000+  total  resources  across  17
practice  areas”  (Thomson  Reuters  2024a).  Thomson  Reuters
markets this database for general legal research: “Practical Law
provides  trusted,  up- to- date  legal  know- how  across  all  major
practice areas to help attorneys deliver accurate answers quickly
and confidently.” Performing RAG on these materials, Thomson
Reuters claims, ensures that its system “only returns informa-
tion from [this] universe” (Thomson Reuters 2024b).

Westlaw's  AI- Assisted  Research  (AI- AR),  introduced  in
November 2023, is also a standard chatbot interface, promising
“answers to a far broader array of questions than what we could
anticipate with human power alone” (Thomson Reuters 2023).
The  RAG  system  retrieves  information  from  Westlaw's  data-
bases of cases, statutes, regulations, West Key Numbers, head-
notes,  and  KeyCite  markers  (Thomson  Reuters  2023).  While
not much technical detail is provided, AI- AR appears to rely on
OpenAI's GPT- 4 system (Ambrogi 2023). This system was built
out after a $650 million acquisition of Casetext, which had de-
veloped legal research systems on top of GPT- 4 (Ambrogi 2023).
RAG  is  prominently  touted  as  addressing  hallucinations:  one
Thomson Reuters official stated, “We avoid [hallucinations] by
relying on the trusted content within Westlaw and building in
checks and balances that ensure our  answers  are grounded  in
good law” (Thomson Reuters 2023). While AI- AR has been sold
to law firms, it has not been made available generally for educa-
tional and research purposes.13

Both AI- AR and Ask Practical Law AI are made available via the
Westlaw platform and are commonly referred to as AI products
within Westlaw.14 For shorthand, we will refer to Ask Practical
Law AI as a Thomson Reuters system and AI- AR as a Westlaw
system,  as  this  appears  to  track  the  internal  company  product
distinctions.

To provide a point of reference for the quality of these bespoke
legal research tools—and because AI- AR appears to be built on
top  of  GPT- 4—we  also  evaluate  the  hallucination  rate  and  re-
sponse quality of GPT- 4, a widely available LLM that has been
adopted  as  a  knowledge- work  assistant  (Collens  et  al.  2024;
Dell'Acqua  et  al.  2023).  GPT- 4's  responses  are  produced  in  a
“closed- book” setting; that is, produced without access to an ex-
ternal knowledge base.

5.2   |   Query Construction

We design a diverse set of legal queries to probe different aspects
of a legal RAG system's performance. We develop this benchmark
dataset to represent real- life legal research scenarios, without prior
knowledge of whether they would succeed or fail.

For ease of interpretation, we group our queries into four broad
categories:

1.  General  legal  research  questions:  common- law  doc-
trine questions, holding questions, or bar exam questions

7 of 27

 17401461, 0, Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/jels.12413, Wiley Online Library on [23/04/2025]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons Licensee
t
a
t
s

e
h
t

e
r
e
h
w

)
d
(
4
5
2
2
§

.

.

.

C
S
U
8
2
f
o
s
e
s
o
p
r
u
p
r
o
f

”
s
t
i
r
e
m

m
a
x
e

r
a
b
e
c
i
t
c
a
r
p
d
e
h
s
i
l
b
u
p
y
l
s
u
o
i
v
e
r
p

2.  Jurisdiction  or  time- specific  questions:  questions
about circuit splits, overturned cases, or new developments

3.  False premise questions: questions where the user has a

mistaken understanding of the law

4.  Factual recall questions: queries about facts of cases not
requiring interpretation, such as the author of an opinion
and matters of legal citation

Queries in the first category (n = 80) are the paradigmatic use case
for these tools, asking general questions of law. For instance, such
queries pose bar exam questions that have ground- truth answers,
but in contrast to assessments that focus only on the accuracy of
the multiple choice answer (e.g., Martínez 2024), we assess hallu-
cinations  in  the  fully  generated  response.  Queries  in  the  second
category (n = 70) probe for jurisdictional differences or developing
areas in the law, which represent precisely the kinds of active legal
questions requiring up- to- date legal research. Queries in the third
category (n = 22) probe for the tendency of LLMs to assume that
premises in the query are true, even when flatly false. The last cat-
egory (n = 30) probes the extent to which RAG systems are able to
overcome known vulnerabilities about how general LLMs encode
legal knowledge (Dahl et al. 2024).

Table  2  describes  these  categories  in  more  depth  and  provides
an  example  of  a  question  that  falls  within  each  category.  We
used 20 queries from LegalBench's Rule QA task verbatim (Guha
et al. 2023), and 20 BARBRI bar exam prep questions verbatim
(BARBRI Inc. 2013). Each of the 162 other queries were hand-
written or adapted for use in our benchmark. Appendix A pro-
vides a more granular list of the types of queries and descriptive
information.

Our  dataset  advances  AI  benchmarking  in  five  respects.  First,
it  is  expressly  designed  to  move  the  evaluation  of  AI  systems
from  standard  question- answer  settings  with  a  discrete  and
known  answer  (e.g.,  multiple  choice)  to  the  generative  (e.g.,
open- ended) setting (Li and Flanigan 2024; McIntosh et al. 2024;
Raji et al. 2021). Prior work has evaluated the amount of legal
information that LLMs can produce (Dahl et al. 2024), but this
kind of benchmark does not capture the practical benefits and
risks of everyday use cases. Legal practice is more than answer-
ing multiple choice questions. Of course, because these are not
simple queries, their design and evaluation is time- intensive—all
queries must be written based on external legal knowledge and
submitted  by  hand  through  the  providers'  web  interfaces,  and
evaluation  of  answers  requires  careful  assessment  of  the  tool's
legal analysis and citations, which can be voluminous.

Second, our queries are specifically tailored to RAG- based, open-
ended  legal  research  tools. This  differentiates  our  dataset  from
previously  released  legal  benchmarks,  like  LegalBench  (Guha
et  al.  2023).  Most  LegalBench  tasks  are  tailored  towards  legal
analysis of information given to the model in the prompt; tasks
like contract analysis or issue spotting. Our queries are written
specifically for RAG- based legal research tools; each query is an
open- ended legal question that requires legal analysis supported
by relevant legal documents that the model must retrieve. This
provides  a  more  realistic  representation  of  the  way  that  law-
yers  are  intended  to  use  these  tools.  Our  goal  with  our  dataset
is  to  move  beyond  anecdotal  accounts  and  offer  a  systematic

e
h
t
n
o
d
e
t
a
c
i
d
u
d
a
“
n
e
e
b
m
i
a
l
c

j

'

s
r
e
n
o
i
t
i
t
e
p
s
a
e
b
a
h
a
s
a
H

,
s
n
o
i
t
s
e
u
q
e
n

i
r
t
c
o
d
w
a
 l
-
n
o
m
m
o
C

y
r
e
u
q
e
l
p
m
a
x
E

n
o
i
t
p
i
r
c
s
e
D

.
c
r
e
P

%
6
9
3

.

t
n
u
o
C

0
8

h
c
r
a
e
s
e
r

l
a
g
e
l

l
a
r
e
n
e
G

y
r
o
g
e
t
a
C

.
s
e
i
r
e
u
q
e
l
p
m
a
s
d
n
a
,
s
n
o
i
t
p
i
r
c
s
e
d

,
s
e
i
r
e
u
q
f
o
)
.
c
r
e
P
(

s
e
g
a
t
n
e
c
r
e
p
d
n
a
s
t
n
u
o
c
h
t
i

w

,
t
e
s
a
t
a
d
y
r
e
u
q
e
h
t

f
o
s
e
i
r
o
g
e
t
a
c

l
e
v
e
 l
-
h
g
i

h
e
h
T

|

2
E
L
B
A
T

t
o
n
d
i
d
t
u
b
n
o
i
s
i
c
e
d
d
e
n

i
a
l
p
x
e
n
a
n

i

f
e
i
l
e
r
d
e
i

n
e
d
t
r
u
o
c

?

m
i
a
l
c

e
h
t

r
o
f

s
i
s
a
b
w
a
 l
-
l
a
r
e
d
e
f
a
e
g
d
e
l
w
o
n
k
c
a
y
l
s
s
e
r
p
x
e

s
n
o
i
t
s
e
u
q
g
n

i
d
l
o
h

,
s
n
o
i
t
s
e
u
q

s
e
i
t
i
l
i
b
a
s
i
D
h
t
i

w
s
n
a
c
i
r
e
m
A
e
h
t

s
e
o
d

,
t
i
u
c
r
i
C
h
t
x
i
S
e
h
t
n
I

d
e
n
r
u
t
r
e
v
o

,
s
t
i
l
p
s

t
i
u
c
r
i
c

t
u
o
b
a
s
n
o
i
t
s
e
u
Q

%
7
4
3

.

'

s
e
e
y
o
l
p
m
e
n
a
e
t
a
d
o
m
m
o
c
c
a
o
t

s
r
e
y
o
l
p
m
e

e
r
i
u
q
e
r

t
c
A

?
k
r
o
w
o
t
g
n

i
t
u
m
m
o
c

s
e
i
t
l
u
c
i
f
f
i
d
s
e
t
a
e
r
c

t
a
h
t
y
t
i
l
i
b
a
s
i
d

t
a
h
t
n
o
i
t
i
s
o
p
o
r
p
e
h
t

r
o
f

s
d
n
a
t
s

t
a
h
t

e
s
a
c
a
r
o
f
g
n

i
k
o
o
l

m

'
I

g
n

i
b
r
o
s
b
a
r
o
f

t
f
e
h
t
h
t
i

w
d
e
g
r
a
h
c

e
b
n
a
c
n
a
i
r
t
s
e
d
e
p
a

y
b
e
r
e
h
t

,
s
l
e
n
a
p
r
a
l
o
s
n
o
l
l
a
f

e
s
i
w
r
e
h
t
o
d
l

u
o
w

t
a
h
t

t
h
g
i
l

n
u
s

.
y
g
r
e
n
e

l
a
i
t
n
e
t
o
p
f
o
s
l
e
n
a
p
e
h
t

f
o
r
e
n
w
o
e
h
t
g
n

i
v
i
r
p
e
d

s
t
n
e
m
p
o
l
e
v
e
d
w
e
n
r
o

,
s
e
s
a
c

a
s
a
h
r
e
s
u
e
h
t

e
r
e
h
w
s
n
o
i
t
s
e
u
Q

w
a
l

e
h
t

f
o
g
n

i
d
n
a
t
s
r
e
d
n
u
n
e
k
a
t
s
i

m

%
9
0
1

.

0
7

2
2

c
i
f
i
c
e
p
 s
-
e
m

i
t

r
o
n
o
i
t
c
i
d
s
i
r
u
J

e
s
i

m
e
r
p
e
s
l
a
F

?
)
4
9
9
1

.
s
s
a
M

.

D

(
2
3
6

.

p
p
u
S

.

F
2
6
8

,
.
c
n
I

e
r
u
s
o
n
y
C

.
v

d
e
d
i
c
e
d
s
a
w
e
s
a
c
a
r
a
e
y
e
h
t

e
k
i
l

,

n
o
i
t
a
t
e
r
p
r
e
t
n

i

.

p
r
o
C
r
e
s
a
L
a
l
e
d
n
a
C
n

i

n
o
i

n

i
p
o
y
t
i
r
o
j
a
m
e
h
t

e
t
o
r
w
o
h
W

g
n

i
r
i
u
q
e
r

t
o
n
s
t
c
a
f

t
u
o
b
a
s
e
i
r
e
u
q
c
i
s
a
B

%
9

.

4
1

0
3

s
n
o
i
t
s
e
u
q
l
l
a
c
e
r

l
a
u
t
c
a
F

8 of 27

Journal of Empirical Legal Studies, 2025

 17401461, 0, Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/jels.12413, Wiley Online Library on [23/04/2025]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

investigation of the potential strengths and weaknesses of these
tools, responding to documented challenges in evaluating AI in
law (Guha et al. 2023; Kapoor et al. 2024).

Third, these queries are designed to represent the temporal and
jurisdictional  variation  (e.g.,  overruled  precedents  and  circuit
splits) that is often the subject of live legal research (Beim and
Rader 2019). We hypothesize that AI systems are not able to en-
code  this  type  of  multifaceted  and  dynamic  knowledge  at  the
moment, but these are precisely the kinds of inquiries requiring
legal research. Due to the nature of legal authority, attorneys will
inevitably have questions specific to their time, place, and facts,
and even the most experienced lawyers will need to ground their
understanding of the legal landscape when facing issues of first
impression.

Fourth,  the  queries  probe  for  “contrafactual  bias,”  or  the  ten-
dency  of  chat  systems  to  assume  the  veracity  of  a  premise
even  when  false  (Dahl  et  al.  2024).  Many  claim  that  AI  sys-
tems  will  help  to  address  longstanding  access  to  justice  issues
(Bommasani et al. 2022; Chien and Kim 2024; Chien et al. 2024;
Perlman  2023;  Tan  et  al.  2023),  but  contrafactual  bias  poses  a
particular risk for pro se litigants and lay parties.

Last, to guard against selection bias in our results (i.e., choosing
queries based on hallucination results), we modeled best prac-
tices with our dataset by preregistering our study and associated
queries with the Open Science Foundation prior to performing
our evaluation (Surani et al. 2024).15

5.3   |   Query Execution

For  Lexis+  AI,  Thomson  Reuters's  Ask  Practical  Law  AI,  and
Westlaw's AI- AR, we executed each query by copying and past-
ing  it  into  the  chat  window  of  each  product.16  For  GPT- 4,  we
prompted the LLM via the OpenAI API (model gpt- 4- turbo-
2024- 04- 09)  with  the  following  instruction,  appending  the
query afterwards:

You  are  a  helpful  assistant  that  answers  legal
questions. Do not hedge unless absolutely necessary,
and  be  sure  to  answer  questions  precisely  and  cite
caselaw for propositions.

This prompt aims to ensure comparability with legal AI tools,
particularly by prompting for legal citations and concrete factual
assertions.  We  recorded  the  complete  response  that  each  tool
gave, along with any references to case law or documents. The
dataset was preregistered on March 22, 2024 and all queries on
Lexis+ AI, Ask Practical Law AI, and GPT- 4 were run between
March 22 and April 22, 2024. Queries on Westlaw's AI- AR sys-
tem were run between May 23–27, 2024.

5.4   |   Inter- Rater Reliability

according  to  the  rubric  developed  in  Section  4.  As  noted
above,  efficiently  evaluating  AI- generated  text  remains  an
unsolved problem with inevitable trade- offs between internal
validity, external validity, replicability, and speed (Hashimoto
et al. 2019; Liu et al. 2016; Smith et al. 2022). These problems
are  particularl
<!-- fetched-content:end -->
