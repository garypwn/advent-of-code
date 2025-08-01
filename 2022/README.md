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

You have some valves. You have 30 minutes to open the valves in the order that releases the most
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

#### Part 2

Oh boy. I had about six versions of this solution and none were fast enough for me.
First, I tried adapting my p1 solution to work with the extra agent. Unfortunately, the pareto
front gains an extra dimension for each agent added, and state space gains two dimensions.
The resulting solution would have needed dozens of GB of memory to work.

My second attempt was a dynamic programming based solution, and it worked. I rewrote my p1 solution
to use it as well, and it was faster. It does a sort of dfs, but at each step, it estimates the
upper bound for what the best value from the best path could be, and if that upper bound is worse
than what we've already seen for that state, it culls that branch.

This solution worked, but it took like 8 seconds. At this point I checked the subreddit and
saw a user claiming to have a solution _in python_ that took 0.8 seconds.This is where my descent
into insanity began.

I tried replacing the sets that I was using to represent visited node sets with
bitmasks. I whipped up a class that abstracted bitmasks behind something that behaved
like a set. It didn't give a significant speedup, I think because of all the extra stack frames
involved with the abstraction. Though I expect it to be useful for future problems with a bigger
state space.

So I finally dove into the solution of mister 0.8 seconds. This solution uses dfs to exhaustively
check every path that an agent could take. I copy-pasted it and it took way more than 0.8s. Maybe
if I ran it on my gaming system using pypy I could get those kinds of numbers.

It takes all path-value pairs, sorts them, and then iterates over non-overlapping pairs of
paths that the agents could independently take looking for the best. It has a couple of stop early
conditions to speed things up.

Overall, there's still some improvements that could be made, but I'm satisfied with this solution.

### [Day 17](day_17) - Tetris

This is a falling block puzzle, like the game Tetris. The puzzle input is a sequence of left/right
wind directions that will nudge the falling rocks. The objective is to figure out how tall the tower
will get after some number of rocks have fallen.

#### Part 1

We only need to drop 2022 rocks, so this was really just a matter of implementing the tetris game.
I chose to represent the grid using a set of (x,y) points instead of a 2d array. I think this approach
is better for the majority of Advent of Code puzzles that work on a 2d grid.

#### Part 2

For part 2, we need to drop 1 trillion rocks, so it's obviously not going to be feasible to simulate
them all. This is a fairly common Advent of Code part 2, and the solution usually involves finding a
cycle or pattern of some sort.

Since this sort of thing has shown up in AoC a few times, I decided to make a generic cycle finder
utility. The cycle finder is pretty simple. You send it values, and when it finds a pattern it will
give you a Cycle object that you can index or sum however you please.

The implementation checks for a cycle every time you send it a value, and checking for a cycle is
at worst O(N^2) if you have a bunch of very similar patterns that don't quite repeat. So yeah, for
something like this where finding a cycle involves dropping 2000 rocks or so, it's slow as hell.
For this puzzle I passed in the difference between the new height and the old height of the tower
each time I dropped a rock. It took like 8 seconds.

So I expanded the cycle checker so that in addition to passing in a value, you can pass it some
extra context, which I called a "state." A state doesn't necessarily need to be the actual puzzle
state, which could be huge. It just has to be something unique enough that if it shows up three times
then it guarantees you've found a cycle.

For this puzzle, the state that I passed to the cycle checker was the id of the shape that was just
dropped, the relative height of each of the 7 columns before and after the rock was dropped, and the
next three upcoming gusts of wind. I tried using less information, but it caused false positives which
slowed down the cycle checker. In the end, it took 170ms. Much better.

### [Day 18](day_18) - Cubes

There is a mass of cubes and we need to find the surface area.

#### Part 1

Each cube has six faces, and it's easy enough to iterate over them all.
I kept track of how many times each face showed up as I iterated over the cubes. Faces that showed up
more than once must be from cubes that are touching each other. Faces that showed up exactly once are
part of a surface.

#### Part 2

Now we need to exclude faces that are part of "bubbles." I modified my part 1 solution to record the
direction of each face. Faces are stored as (cube, cube) pairs, such that cube[0] is in the mass of
cubes and cube[1] is not.

Then I shoved all the faces into a NetworkX graph. Two nodes have an edge if their corresponding faces
are adjacent to each other. I realized that if two cubes were diagonal to each other, they would have two pairs of
adjacent faces that might not be parts of the same surface. So, I gave priority to adjacent faces with the
lowest angle between them.

Then, after constructing my graph, I just use `nx.connected_components` to list all the contiguous surfaces.
Then I made the assumption that the surface with the highest area was the correct solution, which worked for
my input.

In retrospect, about 42% of my faces were in a bubble, comparing my part 1 and part 2 solutions, so it's
possible I just got lucky and my solution might not work for some puzzle inputs.

Anyhow, after comparing my solution with those on the subreddit, I found out that all that hard work I did
could be easily done with NetworkX is like 5 lines of code. You can use `nx.grid_graph` to make a graph
of the "world", then you can remove all the cubes listed in the puzzle input to get a graph representing
all the voids. Then you can use `nx.connected_components` to isolate a surface, and you can even pass in
a point outside the playing field to ensure that you don't get a surface inside the bubble. Then you can
just use `nx.edge_boundary` to figure out how many faces are in the surface.

So what did I learn? I need to spend more time looking at the docs. I really should have known that
NetworkX can just solve the entire puzzle for me.
