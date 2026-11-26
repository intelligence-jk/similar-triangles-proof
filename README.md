# TRIAD: Triangle Ratios, Investigated And Derived

Formerly `similar-triangles-proof`.

Give two triangles, get back which similarity test applies (AA, SAS or SSS) and the proof written out line by line, with exact fractions. It can also find a missing side.

## What it solves
Writing a similarity proof is a fixed routine: match the vertices in order, pick the test the facts allow, show each ratio or angle, and state the conclusion with the test named. Students lose marks by comparing the wrong sides or forgetting that the angle in SAS must sit between the two sides. This tool does the routine for any numbers and says plainly when the facts do not show similarity. Pure Python 3.10+, standard library only, exact `Fraction` arithmetic.

## Example
Triangle ABC has sides b = 4 and c = 6 and angle A = 40 degrees. Triangle PQR has q = 8, r = 12 and angle P = 40 degrees (A matches P, B matches Q, C matches R).
```bash
python -m similarproof "b=4,c=6,A=40" "b=8,c=12,A=40"
```
```
To show: triangle ABC is similar to triangle PQR with ABC matched to PQR.
Sides around A: 8/4 = 2 and 12/6 = 2.
The ratios are equal and the angle between them is the same (40 degrees).
Hence triangle ABC is similar to triangle PQR (SAS).
```
Finding a side:
```bash
python -m similarproof "A=50,B=60,a=3,b=4" "A=50,B=60,a=9/2" --find b
```
```
To show: triangle ABC is similar to triangle PQR with ABC matched to PQR.
Angle A = 50 and angle P = 50, so angle A = angle P.
Angle B = 60 and angle Q = 60, so angle B = angle Q.
Two angles of one triangle equal two angles of the other, so the third angles are equal too.
Hence triangle ABC is similar to triangle PQR (AA).
Side b of PQR = 6
```

## The maths behind it
Triangles are similar when their angles are equal one by one, which forces every pair of matching sides to have the same ratio k. The three tests are the minimum facts that give this. AA: two equal angles make the third equal because the angles sum to 180. SSS: three equal ratios. SAS: two equal ratios with the equal angle between those two sides (at vertex A the sides around it are b and c). In the example the ratios are 8/4 = 12/6 = 2 and the angle A = 40 is between b and c, so k = 2. For the missing side, similarity gives (side b of PQR)/b = (side a of PQR)/a, so q = 4 x (9/2) / 3 = 6. Everything is computed with exact fractions, so equal ratios are tested for exact equality, never "close enough". Inputs that are not triangles (sides 1, 1, 2, or two angles summing to 180 or more) are refused.

## Install and run
```bash
python -m pip install -e .
python -m similarproof "a=3,b=4,c=5" "a=6,b=8,c=10"
python -m pytest
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
