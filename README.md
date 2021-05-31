# Car Assistant

### Project Motivation
> The touchscreen hype has recently hit the automotive industry. Many manufacturers are building cars with minimalist designs, features little more than a large touchscreen to manage many controls that traditionally found their place on buttons. This change can greatly increase the user satisfaction with interior design but has its downsides. While many cars offer autonomous and semi-autonomous features, these are not commonly standard. This means that many of the cars on the road will features these large screens but not driver safety aids. Most states have a law banning the use of cell phones while driving, a law that is seen as a bipartisan success (quite rare in the US). This begs the question: If my car's infotainment screen is basically a tablet, how different is that from using my phone? 
### Project Description
> This project is a virtual assistant designed to understand car related verbal interactions and minimize the number of distracted drivers. 
### Methods
> The core idea of the project is nested classification. The first step was to come up with a finite number of classes that encapsulated the different features that can be addressed in a car: Navigation, Music, Air Conditioning, and Inquiries about the car's condition. A factory pattern is used to call the proper processing function. 
Each of the car features are derivatives of a the abstract class Function, the hotwords member variable is a list of hotwords that are used to in the initial classification (choosing which feature the input string relates to). After this, the factory method is called and the returned object is used for further processing. 
 > ![Design Pattern](https://github.com/piyushmundhra/carAssistant/blob/main/Car%20Assistant%20(1).png)

The most demanding processing task is with Navigation related commands and inputs. Other functions tend to have straightforward inputs with very limited variation. Navigation provides a different challenge due to the variety of sentence structure which may require different processing. Some examples are:
* It feels hot -> Lowering the temperature
* I want it to feel warm -> Raising the temperature
> Above are examples of how similar input sentences can have the opposite "correct" output. This program tackles the problem using classification. Even within classification, there are multiple ways to approach building the model and classifier. If training data was available, I would have chosen to use a Neural Network with word2vec or one-hot encoding vectorization for inputs. This program uses regular expression parsing to try and identify the different cases input can fall under. In the first example, the input is a statement. In the second example, the input is an expressed desire. During the developement of this program, varied usage helped identify more input strucutres that could be added to the regular expresssion parsing language to increase the output accuracy for a greater variety of inputs. 
### Screenshots
 > ![Sample input/output](https://github.com/piyushmundhra/carAssistant/blob/main/Screen%20Shot%202021-05-31%20at%207.18.57%20AM.png)
