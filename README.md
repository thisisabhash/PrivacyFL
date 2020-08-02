## Federated Learning: What, Why & How?

**This is a fork of the repository at https://github.com/vaikkunth/PrivacyFL and contains changes made for the project in my course CS839 - Data Management for Machine Learning at UW-Madison. I am truly grateful to the authors to have provided us a cool framework to experiment with Federated Learning.**

This is a survey based project for CS839 - Data Management for Machine Learning at UW-Madison. We extended the experiments made in the original code for MNIST dataset to a skin segmentation dataset for UCI Machine Learning Repository at http://archive.ics.uci.edu/ml/datasets/Skin+Segmentation.

The steps to run the code are the same as in the original repository. The skin dataset is already downloaded and included in the `src` folder.
In case, a file not found error is observed, please make sure that the file `Skin_NonSkin.txt` is in the same folder as the source code.

Citation:
Rajen Bhatt, Abhinav Dhall, 'Skin Segmentation Dataset', UCI Machine Learning Repository

*Abstract*


Federated learning is emerging as a new technique enabling distributed clients to collaborate over a shared Machine Learning model while keeping their data localized, by sharing trained weights instead. Implementing and analyzing a federated learning setup still remains a challenge, with mul- tiple parameters and configurations. In this paper, we aim to do a two-part study. First, we aim to do a bird’s eye view of the federated learning land- scape, and its main challenges. Second, we aim to extend a federated learning simulation system, towards a highly scalable cluster-based environ- ment, to help get a better sense of its advantages in particular machine learning applications.
