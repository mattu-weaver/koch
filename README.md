# Island coastlines
The application uses Pygame to draw pseudo-random islands with varying levels of precision. The basic process is as follows:
- Start with an equilateral triangle
- Perform x iterations as follows:
  -  Divide each side into three equal parts.
  -  Draw an equilateral triangle that has the middle segment from step 1 as its base and points outward.
  -  Remove the line segment that is the base of the triangle from step 2.
-  Store each point in 2-dimensional space.
