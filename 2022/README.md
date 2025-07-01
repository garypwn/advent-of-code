# AoC 2022

This is the first backlog year (from before I started participating in events) that I tackled.
I did some puzzles in November 2024 as a warmup for the 2024 event, and then some more in summer 2025 for fun.

## Journal

### Days 1-14

I did these before I started keeping journal entries for puzzles.

### [Day 15](day_15) - Beacons
_Solved Jun. 30, 2025_

We're looking for a beacon. We have some points,
and each one has an exclusion zone around it with a given manhattan distance.

#### Part 1
I took my new RangeSet utility for a spin, and it worked great!
Each beacon adds an interval of excluded points in the target row,
then I just take len(points) for the answer.

There was a slight hiccup: The question was _"how many positions cannot contain a beacon?"_
but my solution answered the question "how many positions cannot contain a beacon,
_excluding those already present?_" Basically, I was off by the number of beacons in the target row.
But it was an easy fix to subtract that number from my result.

Where N is the number of sensors in the input, I do O(N) insertions
into the RangeSet. Insertions into a RangeSet are worst-case O(N),
since it's backed by an array, and insertion may require shifting the elements.

So, the solution is O(N^2).

**TODO: Is it worth considering changing RangeSet to be backed by a binary tree?**
I think probably not. It could make insertion O(log(n)), but it would be a pain in the butt
to implement. And, even though it might perform better in an asymptotic case, realistically a
cpython powered array list will be way faster than a python powered data structure.

#### Part 2

Now for the real problem: the puzzle guarantees there is only one non-excluded spot for a beacon
between x,y = 0 and 2 million. Here's how I found that one spot:

**Key Observation:** Each sensor creates an exclusion boundary that looks like a diamond—four diagonal
lines that bound all the points that beacon excludes. Since there is exactly one viable point, it must be
sandwiched by four of these boundary lines. Or, it could be sandwiched by one or two such lines and the
edge of the arena.

I processed the sensors, and stored the bounding lines in four sets (two possible line slopes times two
boundary directions.) Then I found each sandwich with positive slope and compared it to each sandwich with
negative slope to find candidate points. At worst, that's O(N^2) candidate points, which is not great. But
realistically, there should be far, far less than O(N) sandwiches, depending on how the sensors and beacons
are distributed.

Then, I checked each candidate point against each sensor to see if it was inside an exclusion zone.
There should only ever be one result (per the problem specification), which is the solution.
All told, it works in O(N^3).

**Possible Bug:** Remember how I said the solution could be sandwiched against the arena boundary? Yeah,
I didn't bother checking it. Once I got the main sandwich logic working, I tried it on my input and
immediately got a correct solution. Depending on how puzzle inputs are generated, my solution might
fail. **Todo: add logic to fix this.**