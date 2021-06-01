# Car Assistant

## Project Description
> This project is a virtual assistant designed to understand car related verbal interactions and minimize the number of distracted drivers. 
## Project Motivation
> The touchscreen hype has recently hit the automotive industry. Many manufacturers are building cars with minimalist designs, features little more than a large touchscreen to manage many controls that traditionally found their place on buttons. This change can greatly increase the user satisfaction with interior design but has its downsides. While many cars offer autonomous and semi-autonomous features, these are not commonly standard. This means that many of the cars on the road will features these large screens but not driver safety aids. Most states have a law banning the use of cell phones while driving, a law that is seen as a bipartisan success (quite rare in the US). This begs the question: If my car's infotainment screen is basically a tablet, how different is that from using my phone? 
## Initial Research
> When first approaching this task, I made several mistakes that helped lead me to key resources. The first mistake was attempting to use graph similarity algorithms with WordNet synsets. While these tools are very useful for other classification tasks, graph similarity algorithms fail to compare the actual meaning of two words. In addition, some colloquial/informal uses of words may result in synsets not being exhaustive. This issue led me to SimLex-999 and SimVerb-3500. Both are reviewed, crowd-sourced datasets that quantify the similarty of a pair of given words. This was key in filling in the gaps left by only using synsets. 
## Methods
> The core idea of the project is nested classification. The first step was to come up with a finite number of classes that encapsulated the different features that can be addressed in a car: Navigation, Music, Air Conditioning, and Inquiries about the car's condition. A factory pattern is used to call the proper processing function. 
Each of the car features are derivatives of a the abstract class Function, the hotwords member variable is a list of hotwords that are used to in the initial classification (choosing which feature the input string relates to). After this, the factory method is called and the returned object is used for further processing. 
 <img src = https://github.com/piyushmundhra/carAssistant/blob/main/Car%20Assistant%20(2).png/>
 
> The initial classification is made by choosing the feature with the most number of matches: each feature has a list of associated hotwords as a member variable. The vectorizer returns the number of hotwords that found matches in the input sentence. The matches are found using three similarity metrics: SimLex-999, SimVerb-3500, and WordNet synsets. Matches are either 0 or 1. As mentioned before, this classifier can be improved using machine learning and a sufficiently large dataset (possible method: word2vec vectorization into a neural netowrk/MLP). After this classification, the program must process the input.

> The most demanding processing task is with Air Conditioning related commands and inputs. Other features tend to have straightforward inputs with very limited variation. Air Conditioning input processing provides a different challenge due to the variety of sentence structure which may require different processing. Some examples are:
* It feels hot -> Lowering the temperature
* I want it to feel warm -> Raising the temperature
> Above are examples of how similar input sentences can have the opposite "correct" output. This program tackles the problem using classification. Even within classification, there are multiple ways to approach building the model and classifier. If training data was available, I would have chosen to use a Neural Network with word2vec or one-hot encoding vectorization for inputs. This program uses regular expression parsing to try and identify the different cases input can fall under. In the first example, the input is a statement. In the second example, the input is an expressed desire. NLTK's Regexparser helps construct parse trees based on the user designed rules. The regular language type rule set allows different rules to interact with each other. In my case, this was important for a couple use cases. It meant that any subtree that was parsed as an statement could be used to identify a desire (getTargetAc() in assistantv2.py shows the full rule set). During the developement of this program, varied usage helped identify more input strucutres that could be added to the regular expresssion parsing language to increase the output accuracy for a greater variety of inputs. 
## Findings / What I Learned / Possible Improvements
* I found that rather than having a single classifier that directly processed inputs was much harder to develop/needed much more data to be accurate. The nested classifiers required more models to be designed and developed with each model being less complex. This lower complexity led to cleaner code, wider range of recognition, and higher customizability. 
* This project criminally does not feature ML. This is because this was built without any training data. Finding training data for this specific purpose was not possible at the time and so all the models were built by hand. For example, in the case of the Air Conditioning regex classifier, it meant understanding the sentence structure and POS tags of different types of inputs and trying to create an exhaustive language for AC related inputs. This shows that creating these models was anything but ML related. Different resources I will be researching and experimenting with to develop this assistant further are: 
** BERT, Universal Sentence Encoder Tensorflow client, word2vec/doc2vec, and RNNs. 
## Screenshots
 > ![Sample input/output](https://github.com/piyushmundhra/carAssistant/blob/main/Screen%20Shot%202021-05-31%20at%207.18.57%20AM.png)
* The above screenshot shows sample usage of the program. Every input is directly followed by an output on the next line and each input/output is separated by a newline. 
