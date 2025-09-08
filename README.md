# Havana Take Home Assignment
This repo outlines what I've done for Havana take home assignment.

## Code Review
This was self explanatory- my main changes involved refactoring the code so that we have similar layers of abstraction in a function, and a function does not expose too many granular details of its inner workings.

## Improvement Plan
This is where I feel that my thinking diverges from what was listed in the assignment prompt. I felt that the assignment prompt was looking for novel ways of implementing a better classifier. If I interpret this correctly, I disagree- I would first investigate the data and understand what is causing the misclassification.

Data first, modelling later.

As such, my notebook for this section illustrates my thought process and how I would tackle understanding the data. I have commented with plenty of markdown cells for this purpose.

## Implementation
Due to the lack of complexity in the suggested changes (again, I focused on data and not modelling), this section was rather simple. I implemented a sample automation processor that will take the categories that our classifier has high accuracy for and act on them.

## Total time breakdown
I spent the most time in part 2- perhaps the data science training in me wanted to spend more time looking at the data before deciding the next step.