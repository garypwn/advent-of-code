# AoC 2022

This is the first backlog year (from before I started participating in events) that I tackled.
I did some puzzles as a warmup in the November preceding the 2024 event,
and then I did some more in summer 2025 for fun.

## Journal

Here are my post-puzzle thoughts and opinions. I like to try answer the following questions:

- What is my opinion on the puzzle?
- How did I feel about my process for solving the puzzle?
- Am I satisfied with my solution?

### Days 1-14

I solved these puzzles before I started keeping journal entries.

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
fail.

**Update:** I handled the case of the solution being sandwiched into the corners or the edge.
It only runs if no normal sandwiches are found. It's also O(n^3) and in theory about as fast
as the typical case. It about doubled the amount of code for the part 2 solution, and I needed
two custom test cases to verify it worked.

#### Opinions

Conceptually, I think this puzzle was cool. Once the key observation for part 2 clicked, I knew
exactly what I needed to do, which was satisfying. The problem was that actually implementing it was
tedious. I am happy with my solution—it's fast (for python) and it's clean enough. Wrangling the
boundary directions without excessive code duplication wasn't too bad, but it's not very human-readable:

```python   
for slope, ss in zip((1, -1), intercepts):
    for d, s in zip((1, -1), ss):
        b = sy + d * dist - slope * sx  # the intercept
        s.add(b)
```

But it was annoying that handling the edge cases took so much code.

This is the sort of problem that would be a lot prettier described with pure math as opposed to
computer code. I'd been holding out on using an algebra solver for my AoC solutions, but I think
this solution would be much nicer and just as fast using Z3.

I think understanding the algebra is an important part of solving problems like this, and using
Z3 when you don't understand what's going on is against the spirit of the puzzle. But finding the
intersection of lines in the plane is baby-level shit, especially when those lines only ever have
slopes of 1 and -1.

Plus, learning how to use Z3 is far more valuable to me in terms of advancing my skills than
practicing ninth grade math. Using new tools is a good thing. If I wanted to be a purist, I'd
solve these puzzles in x86 assembly.

### [Day 16](day_16) - Pressure

You have some valves. You have 30 minutes to open the vales in the order that releases the most
pressure. It takes 1 minute to open a valve, and one minute to move to an adjacent location.

For this puzzle, I decided to switch from using igraph, which I'd been using from previous puzzles,
to NetworkX. I was seduced by the ability to directly index into a NetworkX graph, and how
well integrated naming and attaching objects to nodes and edges was.

#### Part 1

I was happy to see a graph problem that wasn't just another flavor of the Implement Dijkstra Again
puzzle. I had the great idea to turn the unweighted undirected graph given by the puzzle input into
a weighted complete graph (well, mostly complete. The starting valve AA only has outgoing edges).
This graph's weights would represent the amount of time it would take to travel to a valve (using the
shortest path) and open it. This allowed me to cull all the valves with zero pressure, reducing the size
of the network from 57 to 16, and essentially precompute all the pathfinding.

I spent a lot of time mulling over how to make this problem take anything but exponential time.
Ultimately it was not worth it. My solution is still exponential. But it's a much better kind of
exponential.

Using my condensed weighted network, I basically do DFS on all the possible paths, looking for the
highest output possible in 30 minutes. For each state (representing my current position and the
set of valves I've opened so far) I store all the pareto efficient ways I've reached it, in terms
of my output so far and the amount of the 30 minutes remaining, I don't bother exploring further.

Finally, once the solution was working, I noticed I was spending a lot of time indexing into my
graph, and a lot of time turning lists of edges into frozenset objects. So I just slapped on
@cache, took my 4x speedup, and called it a day. 