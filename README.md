# 590PR Final_Project
Fork from here to create your final project repository.

Two things are different than all the previous assignments in 590PR regarding the permissions settings:

1. Please KEEP the "All_Students" team to have Read access.  
2. Whenever you choose to, you are welcome to change your Final Project repository to public.  This will enable you to list it in your resume, website, or other portfolio.

DELETE these lines from TEMPLATE up.

TEMPLATE for your report to fill out:

# Title: 
Monarch Butterfly Monte Carlo (MBMC) simulation

## Team Member(s):
Joshua Allen

# Monte Carlo Simulation Scenario & Purpose:
(be sure to read the instructions given in course Moodle)

## Simulation's variables of uncertainty
First off, let me preface this by saying that a lot remains unknown about the habits of monarch butterflies,
so I'm forced to make some guesses and assumptions about the parameters of this simulation. As more data comes to light,
the simulation could be improved to better reflect reality. I'm assuming a degree of random movement for the butterfly, 
though it will have goals (seek food, shelter, and a northly direction), which of course isn't 100% accurate. The insect
is no doubt following scent trails and air currents as it moves in apparently random fashion, but since those parameters
are subject to effectively random (i.e., highly nonlinear) motions, we can treat the butterfly movement as having a
heavy random component to its motion. The average farm size in Illinois is about 1.5 square km, according to the most
recent data I could find. A monarch can travel 50 km a day on average. Some have been tagged and found moving even
farther than that. What is unknown, to me, is if that motion represents their linear movement (50 km from start to
finish), or the actual distance it covers. You can imagine a butterfly zig-zagging across a field covering several km
of actual distance, but only traversing a few hundred meters as the crow flies.

I'll assume the researchers meant that it can get 50km from it's starting position, meaning thay they could potentially 
cross over 33-34 different farms in a single day. But the buffer zone regulations really only cover areas between crop 
fields and non-crop areas. And many farms in Illinois are adjacent. My model will attempt to cover ar area of 50km to 
try to simulate one day in the life of a monarch. I'll assume uniform 1.5 km fields with buffers in between to separate
farms, at least for my premade fields. Since the buffers are around 15 meters, this means each cell of my grid should
represent about 15 meters. So one day in the life of a monarch will require a grid size of around 3,333 units on the 
long edge. The fields, I think can be effectively modeled at a smaller width, since the monarch will be trying to move 
strictly north when it can I'll ignore towns, roads, and the other things that real life reflects in order to simplify 
the example.

I want to set up at least experiments. One on some reasonable land layouts as they might actually exsist now to test if those 
are ideal for Monarchs, one with randomly generated fields within certain parameters to see if a simulation can converge
on an ideal field layout. And a third with sort of a mix of semi-planned layouts to see if there is an ideal that might
reflect a reality with more constraints then "plant butterfly food anywhere"

The butterfly's variables will be the exact position it enters the field. It will be along and edge, but chosen at 
random and the amount of food the butterfly enters the field already carrying. There will also be a random element
to the butterfly's movement. Once the butterfly's food falls below the 50% threshold, it will begin to look for food.
When it falls below 25%, the butterfly becomes more and more at risk for dying. Beyond that it's general goal is 
to move north. Rarely (high wind, rain, night) it will seek shelter. Each of these will have a random chance of
moving in a random direction (scent trails and wind gusts)

The butterfly will fly until it exits the test site to the north or dies. I'll run this simulation many times to sample
the trend in how well the butterfly does, using a standard field to gauge success against.

## Hypothesis or hypotheses before running the simulation:
My hypothesis is that the current rules regarding buffer zones, that they need only be on edges of non-crop land, will
provide insufficient shelter and nutrition and the butterfly mortality rate will be higher. I believe adding more 
buffers between fields would create an environment that is more hospitable and that this could be done without
sacrificing too much crop land

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)

## Instructions on how to use the program:

## All Sources Used:
Buffer zone source: [usda organic farming](https://www.ams.usda.gov/sites/default/files/media/6%20Buffer%20Zones%20FINAL%20RGK%20V2.pdf)
They give a buffer zone of 50 feet, which is right around 15 meters. So my unit of distance for a cell will be 15 meters


How far do monarchs travel in a day? They quote 25-30 miles. I rounded up
to 50 km to be my standard distance. [monarch lab FAQ](https://monarchlab.org/biology-and-research/ask-the-expert/faq)

The average farm size in Illinois in 2018 was 358 acres [average farm size](https://farmdocdaily.illinois.edu/2013/08/trends-illinois-farmland-parcel-size.html),
which translates to about 1.4 square kilometers, so I'll base it on 1.5 km to make it easier.




