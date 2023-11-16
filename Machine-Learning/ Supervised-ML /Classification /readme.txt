# Project Case-study
  ## Predicting housing prices
You work for a consultancy specialising in real estate: your clients include developers, agencies, and investors. Pricing is a central aspect to the business. Traditionally, it’s the domain of home appraisers to determine the value of a property, which must be executed in an unbiased way, following an official criteria to ensure that there is no bias towards neither the buyer nor the seller.

When the appraisal price is set, your clients need to decide whether they should buy the property or not. It all boils down to this simple question: is the “true value” of the property above or below the price set by the appraisal? Your consultancy wants to use data to be able to answer this question reliably and efficiently. It has acquired a dataset containing a historical register of housing prices in Ames, a small city in Iowa —the actual prices at which the properties were sold. For each house, it also contains around 80 different features, such as the area, the state of the property, whether it has a backyard or not, etc.

* You were tasked with creating a model that predicts the price of a house based on its characteristics.

# Project overview
The project will be divided into two major phases:

* Create a model to predict whether a house is expensive or not. 
* Create a model to predict the exact price of a house.

In the first phase, the model you build will have a categorical target: “Expensive” and “Not expensive”. Whenever an ML task involves a categorical target variable, it is called a classification task. In the second phase of the project, the target variable will be numerical (the exact prices of the houses in dollars): you will be dealing with a regression task.

This division of Supervised Machine Learning tasks between classification and regression is especially relevant when it comes to evaluating the model. In a classification task, you can either make a correct prediction or an incorrect one. In a regression task, you will most likely never predict the exact number, but you will be happy if you get close to it. When we discuss performance metrics (ways to determine how good is a model), we will come back to this.

## In each one of these two phases, you will follow a general approach to any Machine Learning project:
 * Understand the context.
 * Explore & clean the data.
 * Data pre-processing.
 * Modelling.
 * Error analysis.
 * Implement your solution.
 
