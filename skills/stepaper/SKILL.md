---
name: stepaper
description: 读懂论文，再用 PPT 检验自己懂了 - the user's own method, run step by step with Durweg.
---

# 读懂论文，再用 PPT 检验自己懂了

Run it with durweg (skill run-workflow): `durweg start stepaper <name-of-this-run>`, then for each step `durweg begin`, do the step, write its file, and `durweg done`. Talk to the user in the language set in ~/Durweg/config.json.

## 1. language

**选择语言**

Do: 先问用户这次运行用什么语言（例如中文、英文、德语）。之后所有笔记、指标说明、PPT 和讲稿都用这种语言写，和用户交流也用这种语言。

Deliver: 这次运行使用的语言。

Write `steps/1-language.md` with a `## Result` section that holds what this step delivered.

The user decides here: write the result, `durweg propose`, show it to the user, and `durweg confirm` with their own words when they agree.

## 2. core-claim

**找到核心论点**

Do: 读摘要，用一两句话写出论文要解决的具体问题和它的核心论点。

Deliver: 核心论点笔记：论文要解决什么具体问题，主张什么。

Write `steps/2-core-claim.md` with a `## Result` section that holds what this step delivered.

The user decides here: write the result, `durweg propose`, show it to the user, and `durweg confirm` with their own words when they agree.

## 3. walkthrough

**一步一步读，每步追问**

Do: 按 原因 → 办法 → 为什么有用 → 怎么检验 → 结果 的顺序，和用户一起一步一步读：一次只讲一步（办法有几部分就分几次讲），讲完先问用户看懂了没有，请用户说自己的想法或反驳，回答用户的提问；用户说没看懂时，换一种更简单的讲法，不加公式、图或长解释。每一步记下要点、用户的提问与回答、用户的复述和见解；用户的见解若要靠后面的结果检验，标为待检验，到结果一步核对。最后写明追问改变了对核心论点的哪些理解。

Deliver: 逐步讨论笔记：每一步的要点、用户的提问与回答、用户的复述和见解，以及追问改变了什么。

Write `steps/3-walkthrough.md` with a `## Result` section that holds what this step delivered.

The user decides here: write the result, `durweg propose`, show it to the user, and `durweg confirm` with their own words when they agree.

## 4. metrics

**指标说明**

Do: 列出论文里出现的每个评价指标，每个只写两件事：它是用来干什么的；怎么看它的好坏（越大越好还是越小越好、取值范围、论文里的数字怎么读）。不写推导和公式细节，以用户能复述为准。

Deliver: 指标说明 markdown：每个指标一小段（干什么用、怎么看好坏）。

Write `steps/4-metrics.md` with a `## Result` section that holds what this step delivered.

The user decides here: write the result, `durweg propose`, show it to the user, and `durweg confirm` with their own words when they agree.

## 5. retell-judge

**复述与判断**

Do: 先请用户用自己的话把核心论点复述成一个对比（A 和 B 哪个更好），再请用户判断：论文的问题是否解决、证据有多强、保留是什么、自己的目的（看懂这篇论文）是否达到。按用户的话整理；Claude 想补充或反驳的地方单独标出，由用户决定是否保留。

Deliver: 用户的一句话复述（A 对 B）+ 判断与保留（附用户原话）。

Write `steps/5-retell-judge.md` with a `## Result` section that holds what this step delivered.

The user decides here: write the result, `durweg propose`, show it to the user, and `durweg confirm` with their own words when they agree.

## 6. outline

**列 PPT 大纲**

Do: 每页只回答一个问题，标题写成这一页的一句话结论；默认顺序：核心论点、原因、办法、为什么有用、怎么检验、结果（A 对 B，写清指标和数字）、追问与判断、复述与还想弄清的问题。

Deliver: PPT 大纲：每页的标题结论和要放的图或数字。

Write `steps/6-outline.md` with a `## Result` section that holds what this step delivered.

The user decides here: write the result, `durweg propose`, show it to the user, and `durweg confirm` with their own words when they agree.

## 7. slides

**做页面**

Do: 按确认的大纲做 PPT：从论文取关键图，每页文字少，不堆公式，结果页写清指标、对比对象和出处；讲稿写进每页备注。

Deliver: PPT 文件。

Write `steps/7-slides.md` with a `## Result` section that holds what this step delivered.

## 8. rehearse

**试讲检查**

Do: 按页试讲一遍，检查每页是否回答了它的问题、前后是否连成一条线、数字是否和论文一致，记下要改的地方并改好；请用户在 PowerPoint 里打开文件检查显示效果。

Deliver: 改好的 PPT + 试讲时发现并修改的问题清单。

Write `steps/8-rehearse.md` with a `## Result` section that holds what this step delivered.

The user decides here: write the result, `durweg propose`, show it to the user, and `durweg confirm` with their own words when they agree.
