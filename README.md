# 590PR Final_Project

# Title: 
Monarch Butterfly Monte Carlo (MBMC) simulation

## Team Member(s):
Joshua Allen

# Monte Carlo Simulation Scenario & Purpose:
This simulation will simulate a field approximately 50 km long and monarch butterflies that will attempt to move north 
on it's migration. The fields will simulate several one-acre plots with buffer zones both required and some variations 
to try to model different scenarios to see if we can find an optimal field configuration for monarchs. The ultimate
goal is to both test the effectiveness of bare minimum agriculture rules and to see if there is an optimal arrangement 
that maximizes field production while still being good for the butterflies.

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

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  
## What are the management decisions one could make from your simulation's output, etc.)
These are the results of running the simulation on 8 fields of dimension 50km x 1.5 km. I used the 5 pregenerated fields
I had created based on trying to limit the dispersal of the food and shelter to the edges. The middle shelter field
(which has food on the east and west edges, and a line of trees in the middle) consistently performed the best after
running this simulation several times. The second best being the food-heavy version, which has the entire border 
surronded by food. This makes sense, to me, when you consider that the butterflies are migrating north to south, so
having a line of food in that direction to sustain them, combined with shelter in the middle (equidistant from both
food sources) gives the butterflies the optimal chance of finding what they need.

Dead percentage = 55.30%
Exit percentage = 44.70%
--- 11.827407360076904 seconds ---
Dead percentage = 9.20%
Exit percentage = 90.80%
--- 11.929078340530396 seconds ---
Dead percentage = 23.00%
Exit percentage = 77.00%
--- 9.871609687805176 seconds ---
Dead percentage = 6.60%
Exit percentage = 93.40%
--- 14.209017515182495 seconds ---
Dead percentage = 12.60%
Exit percentage = 87.40%
--- 10.8919095993042 seconds ---
Dead percentage = 53.70%
Exit percentage = 46.30%
--- 5.590059041976929 seconds ---
Dead percentage = 51.80%
Exit percentage = 48.20%
--- 4.703392505645752 seconds ---
Dead percentage = 52.80%
Exit percentage = 47.20%
--- 4.925860166549683 seconds ---
The best-performing field was middle_shelter

For that field the breakdown by percentage for the layout is
Percent food: 4.00%
Percent shelter: 1.00%
Percent crops: 95.00%

So, 95% of each acre is going toward crops, which the farmer needs to survive. I had two additonal questions: is there 
a field configuration that outperforms the middle-shelter config, and can we increase the crop area and still maintain 
a high survival rate of the species.

However, I was not able to complete those tests before the deadline. I will go ahead and post more updates as I continue
to improve the code, however.

## Instructions on how to use the program:
A test field can be created by making a list of lists and converting it to a field using the field object. Anything
that can be converted to a pandas DataFrame can be converted to a Field. The only extra requirement is that the entries
must be integer values of 1, 2, or 3. 1 = crop, 2 = food (milkweed and other flowers), 3 = shelter (trees). There are
also several functions to create the fields used in the test. These are all prefaced "create_" etc. There is also a 
built-in function in Field called random_field that can create a field given parameters of length, width, percent crop,
percent food, and percent shelter.

## All Sources Used:
Buffer zone source: [usda organic farming](https://www.ams.usda.gov/sites/default/files/media/6%20Buffer%20Zones%20FINAL%20RGK%20V2.pdf)
They give a buffer zone of 50 feet, which is right around 15 meters. So my unit of distance for a cell will be 15 meters


How far do monarchs travel in a day? They quote 25-30 miles. I rounded up
to 50 km to be my standard distance. [monarch lab FAQ](https://monarchlab.org/biology-and-research/ask-the-expert/faq)

The average farm size in Illinois in 2018 was 358 acres [average farm size](https://farmdocdaily.illinois.edu/2013/08/trends-illinois-farmland-parcel-size.html),
which translates to about 1.4 square kilometers, so I'll base it on 1.5 km to make it easier.

Stack overflow as noted in the code.




