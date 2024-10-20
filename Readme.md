# 2024 年秋 GDUT 云计算大作业 CC-LSTR

## 项目概述

CC-LSTR（Cloud Computer - Text Relevance Logistic Classifier）是使用 Apache Hadoop + Apache Spark 基于线性回归模型完成对语言关联度二分类分析。训练集采用 WIC ，精度约为53%，作为二分类模型力压OPT-6.7b三个百分点，并且运行速度不在一个量级，故某种意义上还挺成功的。

| 注意：线性回归模型根本不可能完成语言关联度二分类，因为语言类问题不太可能放到一个二维平面并取一个超平面，所以该工作仅供学习云计算，要精度可以自己研究研究如何利用 Spark 实现 Transformer。

## 食用方法

1. 部署 Apache Hadoop + Apache Spark 集群，详见 [Hadoop](https://github.com/Emoreday/CC-LSTR/tree/main/Hadoop) 文件夹。
2. 训练以及部署，详见 TSLR 文件夹。
3. 启动 WebUI 界面，时间关系暂时没打算写。
