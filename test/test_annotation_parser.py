import unittest
import annotation_parser
import pandas as pd
import io

multipleAnnotations = """
Composer: Néstor Nápoles López
Title: A unit test in C

Time signature: 3/4

m1 b1 C: I b2 ii b3 iii
m2 b1 IV b2 Cad64 b3 V
m3 vi b2 V6 b3 viio65/i
m4 b1 I6 b3 V
m5 b1 c: i b2 iio b3 III
m6 b1 N6 b2 Cad64 b3 V
m7 b1 It6 b3 V
m8 b1 Fr43 b3 V
m9 b1 Ger65
m10 b1 iv
m11 b1 V b3 V
m12 b1 I
"""

multipleAnnotationsInitialDataFrame = """
a_offset,a_measure,a_duration,a_annotationNumber,a_romanNumeral,a_isOnset,a_pitchNames,a_bass,a_root,a_inversion,a_quality,a_pcset,a_localKey,a_tonicizedKey,a_degree1,a_degree2
0.0,1,1.0,0,I,True,"('C', 'E', 'G')",C,C,0,major triad,"(0, 4, 7)",C,None,1,None
1.0,1,1.0,1,ii,True,"('D', 'F', 'A')",D,D,0,minor triad,"(2, 5, 9)",C,None,2,None
2.0,1,1.0,2,iii,True,"('E', 'G', 'B')",E,E,0,minor triad,"(4, 7, 11)",C,None,3,None
3.0,2,1.0,3,IV,True,"('F', 'A', 'C')",F,F,0,major triad,"(0, 5, 9)",C,None,4,None
4.0,2,1.0,4,Cad,True,"('G', 'C', 'E')",G,C,2,major triad,"(0, 4, 7)",C,None,1,None
5.0,2,1.0,5,V,True,"('G', 'B', 'D')",G,G,0,major triad,"(2, 7, 11)",C,None,5,None
6.0,3,1.0,6,vi,True,"('A', 'C', 'E')",A,A,0,minor triad,"(0, 4, 9)",C,None,6,None
7.0,3,1.0,7,V,True,"('B', 'D', 'G')",B,G,1,major triad,"(2, 7, 11)",C,None,5,None
8.0,3,1.0,8,viio7/i,True,"('D', 'F', 'A-', 'B')",D,B,1,diminished seventh chord,"(2, 5, 8, 11)",C,c,#7,1
9.0,4,2.0,9,I,True,"('E', 'G', 'C')",E,C,1,major triad,"(0, 4, 7)",C,None,1,None
11.0,4,1.0,10,V,True,"('G', 'B', 'D')",G,G,0,major triad,"(2, 7, 11)",C,None,5,None
12.0,5,1.0,11,i,True,"('C', 'E-', 'G')",C,C,0,minor triad,"(0, 3, 7)",c,None,1,None
13.0,5,1.0,12,iio,True,"('D', 'F', 'A-')",D,D,0,diminished triad,"(2, 5, 8)",c,None,2,None
14.0,5,1.0,13,III,True,"('E-', 'G', 'B-')",E-,E-,0,major triad,"(3, 7, 10)",c,None,3,None
15.0,6,1.0,14,N,True,"('F', 'A-', 'D-')",F,D-,1,major triad,"(1, 5, 8)",c,None,-2,None
16.0,6,1.0,15,Cad,True,"('G', 'C', 'E-')",G,C,2,minor triad,"(0, 3, 7)",c,None,1,None
17.0,6,1.0,16,V,True,"('G', 'B', 'D')",G,G,0,major triad,"(2, 7, 11)",c,None,5,None
18.0,7,2.0,17,It,True,"('A-', 'C', 'F#')",A-,F#,1,Italian augmented sixth chord,"(0, 6, 8)",c,None,#4,None
20.0,7,1.0,18,V,True,"('G', 'B', 'D')",G,G,0,major triad,"(2, 7, 11)",c,None,5,None
21.0,8,2.0,19,Fr7,True,"('A-', 'C', 'D', 'F#')",A-,D,2,French augmented sixth chord,"(0, 2, 6, 8)",c,None,2,None
23.0,8,1.0,20,V,True,"('G', 'B', 'D')",G,G,0,major triad,"(2, 7, 11)",c,None,5,None
24.0,9,3.0,21,Ger7,True,"('A-', 'C', 'E-', 'F#')",A-,F#,1,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
27.0,10,3.0,22,iv,True,"('F', 'A-', 'C')",F,F,0,minor triad,"(0, 5, 8)",c,None,4,None
30.0,11,2.0,23,V,True,"('G', 'B', 'D')",G,G,0,major triad,"(2, 7, 11)",c,None,5,None
32.0,11,1.0,24,V,True,"('G', 'B', 'D')",G,G,0,major triad,"(2, 7, 11)",c,None,5,None
33.0,12,3.0,25,I,True,"('C', 'E', 'G')",C,C,0,major triad,"(0, 4, 7)",c,None,1,None
"""

multipleAnnotationsFixedTimeframe = """
a_offset,a_measure,a_duration,a_annotationNumber,a_romanNumeral,a_isOnset,a_pitchNames,a_bass,a_root,a_inversion,a_quality,a_pcset,a_localKey,a_tonicizedKey,a_degree1,a_degree2
0.0,1.0,1.0,0.0,I,True,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",C,None,1,None
0.25,1.0,1.0,0.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",C,None,1,None
0.5,1.0,1.0,0.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",C,None,1,None
0.75,1.0,1.0,0.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",C,None,1,None
1.0,1.0,1.0,1.0,ii,True,"('D', 'F', 'A')",D,D,0.0,minor triad,"(2, 5, 9)",C,None,2,None
1.25,1.0,1.0,1.0,ii,False,"('D', 'F', 'A')",D,D,0.0,minor triad,"(2, 5, 9)",C,None,2,None
1.5,1.0,1.0,1.0,ii,False,"('D', 'F', 'A')",D,D,0.0,minor triad,"(2, 5, 9)",C,None,2,None
1.75,1.0,1.0,1.0,ii,False,"('D', 'F', 'A')",D,D,0.0,minor triad,"(2, 5, 9)",C,None,2,None
2.0,1.0,1.0,2.0,iii,True,"('E', 'G', 'B')",E,E,0.0,minor triad,"(4, 7, 11)",C,None,3,None
2.25,1.0,1.0,2.0,iii,False,"('E', 'G', 'B')",E,E,0.0,minor triad,"(4, 7, 11)",C,None,3,None
2.5,1.0,1.0,2.0,iii,False,"('E', 'G', 'B')",E,E,0.0,minor triad,"(4, 7, 11)",C,None,3,None
2.75,1.0,1.0,2.0,iii,False,"('E', 'G', 'B')",E,E,0.0,minor triad,"(4, 7, 11)",C,None,3,None
3.0,2.0,1.0,3.0,IV,True,"('F', 'A', 'C')",F,F,0.0,major triad,"(0, 5, 9)",C,None,4,None
3.25,2.0,1.0,3.0,IV,False,"('F', 'A', 'C')",F,F,0.0,major triad,"(0, 5, 9)",C,None,4,None
3.5,2.0,1.0,3.0,IV,False,"('F', 'A', 'C')",F,F,0.0,major triad,"(0, 5, 9)",C,None,4,None
3.75,2.0,1.0,3.0,IV,False,"('F', 'A', 'C')",F,F,0.0,major triad,"(0, 5, 9)",C,None,4,None
4.0,2.0,1.0,4.0,Cad,True,"('G', 'C', 'E')",G,C,2.0,major triad,"(0, 4, 7)",C,None,1,None
4.25,2.0,1.0,4.0,Cad,False,"('G', 'C', 'E')",G,C,2.0,major triad,"(0, 4, 7)",C,None,1,None
4.5,2.0,1.0,4.0,Cad,False,"('G', 'C', 'E')",G,C,2.0,major triad,"(0, 4, 7)",C,None,1,None
4.75,2.0,1.0,4.0,Cad,False,"('G', 'C', 'E')",G,C,2.0,major triad,"(0, 4, 7)",C,None,1,None
5.0,2.0,1.0,5.0,V,True,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",C,None,5,None
5.25,2.0,1.0,5.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",C,None,5,None
5.5,2.0,1.0,5.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",C,None,5,None
5.75,2.0,1.0,5.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",C,None,5,None
6.0,3.0,1.0,6.0,vi,True,"('A', 'C', 'E')",A,A,0.0,minor triad,"(0, 4, 9)",C,None,6,None
6.25,3.0,1.0,6.0,vi,False,"('A', 'C', 'E')",A,A,0.0,minor triad,"(0, 4, 9)",C,None,6,None
6.5,3.0,1.0,6.0,vi,False,"('A', 'C', 'E')",A,A,0.0,minor triad,"(0, 4, 9)",C,None,6,None
6.75,3.0,1.0,6.0,vi,False,"('A', 'C', 'E')",A,A,0.0,minor triad,"(0, 4, 9)",C,None,6,None
7.0,3.0,1.0,7.0,V,True,"('B', 'D', 'G')",B,G,1.0,major triad,"(2, 7, 11)",C,None,5,None
7.25,3.0,1.0,7.0,V,False,"('B', 'D', 'G')",B,G,1.0,major triad,"(2, 7, 11)",C,None,5,None
7.5,3.0,1.0,7.0,V,False,"('B', 'D', 'G')",B,G,1.0,major triad,"(2, 7, 11)",C,None,5,None
7.75,3.0,1.0,7.0,V,False,"('B', 'D', 'G')",B,G,1.0,major triad,"(2, 7, 11)",C,None,5,None
8.0,3.0,1.0,8.0,viio7/i,True,"('D', 'F', 'A-', 'B')",D,B,1.0,diminished seventh chord,"(2, 5, 8, 11)",C,c,#7,1
8.25,3.0,1.0,8.0,viio7/i,False,"('D', 'F', 'A-', 'B')",D,B,1.0,diminished seventh chord,"(2, 5, 8, 11)",C,c,#7,1
8.5,3.0,1.0,8.0,viio7/i,False,"('D', 'F', 'A-', 'B')",D,B,1.0,diminished seventh chord,"(2, 5, 8, 11)",C,c,#7,1
8.75,3.0,1.0,8.0,viio7/i,False,"('D', 'F', 'A-', 'B')",D,B,1.0,diminished seventh chord,"(2, 5, 8, 11)",C,c,#7,1
9.0,4.0,2.0,9.0,I,True,"('E', 'G', 'C')",E,C,1.0,major triad,"(0, 4, 7)",C,None,1,None
9.25,4.0,2.0,9.0,I,False,"('E', 'G', 'C')",E,C,1.0,major triad,"(0, 4, 7)",C,None,1,None
9.5,4.0,2.0,9.0,I,False,"('E', 'G', 'C')",E,C,1.0,major triad,"(0, 4, 7)",C,None,1,None
9.75,4.0,2.0,9.0,I,False,"('E', 'G', 'C')",E,C,1.0,major triad,"(0, 4, 7)",C,None,1,None
10.0,4.0,2.0,9.0,I,False,"('E', 'G', 'C')",E,C,1.0,major triad,"(0, 4, 7)",C,None,1,None
10.25,4.0,2.0,9.0,I,False,"('E', 'G', 'C')",E,C,1.0,major triad,"(0, 4, 7)",C,None,1,None
10.5,4.0,2.0,9.0,I,False,"('E', 'G', 'C')",E,C,1.0,major triad,"(0, 4, 7)",C,None,1,None
10.75,4.0,2.0,9.0,I,False,"('E', 'G', 'C')",E,C,1.0,major triad,"(0, 4, 7)",C,None,1,None
11.0,4.0,1.0,10.0,V,True,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",C,None,5,None
11.25,4.0,1.0,10.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",C,None,5,None
11.5,4.0,1.0,10.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",C,None,5,None
11.75,4.0,1.0,10.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",C,None,5,None
12.0,5.0,1.0,11.0,i,True,"('C', 'E-', 'G')",C,C,0.0,minor triad,"(0, 3, 7)",c,None,1,None
12.25,5.0,1.0,11.0,i,False,"('C', 'E-', 'G')",C,C,0.0,minor triad,"(0, 3, 7)",c,None,1,None
12.5,5.0,1.0,11.0,i,False,"('C', 'E-', 'G')",C,C,0.0,minor triad,"(0, 3, 7)",c,None,1,None
12.75,5.0,1.0,11.0,i,False,"('C', 'E-', 'G')",C,C,0.0,minor triad,"(0, 3, 7)",c,None,1,None
13.0,5.0,1.0,12.0,iio,True,"('D', 'F', 'A-')",D,D,0.0,diminished triad,"(2, 5, 8)",c,None,2,None
13.25,5.0,1.0,12.0,iio,False,"('D', 'F', 'A-')",D,D,0.0,diminished triad,"(2, 5, 8)",c,None,2,None
13.5,5.0,1.0,12.0,iio,False,"('D', 'F', 'A-')",D,D,0.0,diminished triad,"(2, 5, 8)",c,None,2,None
13.75,5.0,1.0,12.0,iio,False,"('D', 'F', 'A-')",D,D,0.0,diminished triad,"(2, 5, 8)",c,None,2,None
14.0,5.0,1.0,13.0,III,True,"('E-', 'G', 'B-')",E-,E-,0.0,major triad,"(3, 7, 10)",c,None,3,None
14.25,5.0,1.0,13.0,III,False,"('E-', 'G', 'B-')",E-,E-,0.0,major triad,"(3, 7, 10)",c,None,3,None
14.5,5.0,1.0,13.0,III,False,"('E-', 'G', 'B-')",E-,E-,0.0,major triad,"(3, 7, 10)",c,None,3,None
14.75,5.0,1.0,13.0,III,False,"('E-', 'G', 'B-')",E-,E-,0.0,major triad,"(3, 7, 10)",c,None,3,None
15.0,6.0,1.0,14.0,N,True,"('F', 'A-', 'D-')",F,D-,1.0,major triad,"(1, 5, 8)",c,None,-2,None
15.25,6.0,1.0,14.0,N,False,"('F', 'A-', 'D-')",F,D-,1.0,major triad,"(1, 5, 8)",c,None,-2,None
15.5,6.0,1.0,14.0,N,False,"('F', 'A-', 'D-')",F,D-,1.0,major triad,"(1, 5, 8)",c,None,-2,None
15.75,6.0,1.0,14.0,N,False,"('F', 'A-', 'D-')",F,D-,1.0,major triad,"(1, 5, 8)",c,None,-2,None
16.0,6.0,1.0,15.0,Cad,True,"('G', 'C', 'E-')",G,C,2.0,minor triad,"(0, 3, 7)",c,None,1,None
16.25,6.0,1.0,15.0,Cad,False,"('G', 'C', 'E-')",G,C,2.0,minor triad,"(0, 3, 7)",c,None,1,None
16.5,6.0,1.0,15.0,Cad,False,"('G', 'C', 'E-')",G,C,2.0,minor triad,"(0, 3, 7)",c,None,1,None
16.75,6.0,1.0,15.0,Cad,False,"('G', 'C', 'E-')",G,C,2.0,minor triad,"(0, 3, 7)",c,None,1,None
17.0,6.0,1.0,16.0,V,True,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
17.25,6.0,1.0,16.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
17.5,6.0,1.0,16.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
17.75,6.0,1.0,16.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
18.0,7.0,2.0,17.0,It,True,"('A-', 'C', 'F#')",A-,F#,1.0,Italian augmented sixth chord,"(0, 6, 8)",c,None,#4,None
18.25,7.0,2.0,17.0,It,False,"('A-', 'C', 'F#')",A-,F#,1.0,Italian augmented sixth chord,"(0, 6, 8)",c,None,#4,None
18.5,7.0,2.0,17.0,It,False,"('A-', 'C', 'F#')",A-,F#,1.0,Italian augmented sixth chord,"(0, 6, 8)",c,None,#4,None
18.75,7.0,2.0,17.0,It,False,"('A-', 'C', 'F#')",A-,F#,1.0,Italian augmented sixth chord,"(0, 6, 8)",c,None,#4,None
19.0,7.0,2.0,17.0,It,False,"('A-', 'C', 'F#')",A-,F#,1.0,Italian augmented sixth chord,"(0, 6, 8)",c,None,#4,None
19.25,7.0,2.0,17.0,It,False,"('A-', 'C', 'F#')",A-,F#,1.0,Italian augmented sixth chord,"(0, 6, 8)",c,None,#4,None
19.5,7.0,2.0,17.0,It,False,"('A-', 'C', 'F#')",A-,F#,1.0,Italian augmented sixth chord,"(0, 6, 8)",c,None,#4,None
19.75,7.0,2.0,17.0,It,False,"('A-', 'C', 'F#')",A-,F#,1.0,Italian augmented sixth chord,"(0, 6, 8)",c,None,#4,None
20.0,7.0,1.0,18.0,V,True,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
20.25,7.0,1.0,18.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
20.5,7.0,1.0,18.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
20.75,7.0,1.0,18.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
21.0,8.0,2.0,19.0,Fr7,True,"('A-', 'C', 'D', 'F#')",A-,D,2.0,French augmented sixth chord,"(0, 2, 6, 8)",c,None,2,None
21.25,8.0,2.0,19.0,Fr7,False,"('A-', 'C', 'D', 'F#')",A-,D,2.0,French augmented sixth chord,"(0, 2, 6, 8)",c,None,2,None
21.5,8.0,2.0,19.0,Fr7,False,"('A-', 'C', 'D', 'F#')",A-,D,2.0,French augmented sixth chord,"(0, 2, 6, 8)",c,None,2,None
21.75,8.0,2.0,19.0,Fr7,False,"('A-', 'C', 'D', 'F#')",A-,D,2.0,French augmented sixth chord,"(0, 2, 6, 8)",c,None,2,None
22.0,8.0,2.0,19.0,Fr7,False,"('A-', 'C', 'D', 'F#')",A-,D,2.0,French augmented sixth chord,"(0, 2, 6, 8)",c,None,2,None
22.25,8.0,2.0,19.0,Fr7,False,"('A-', 'C', 'D', 'F#')",A-,D,2.0,French augmented sixth chord,"(0, 2, 6, 8)",c,None,2,None
22.5,8.0,2.0,19.0,Fr7,False,"('A-', 'C', 'D', 'F#')",A-,D,2.0,French augmented sixth chord,"(0, 2, 6, 8)",c,None,2,None
22.75,8.0,2.0,19.0,Fr7,False,"('A-', 'C', 'D', 'F#')",A-,D,2.0,French augmented sixth chord,"(0, 2, 6, 8)",c,None,2,None
23.0,8.0,1.0,20.0,V,True,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
23.25,8.0,1.0,20.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
23.5,8.0,1.0,20.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
23.75,8.0,1.0,20.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
24.0,9.0,3.0,21.0,Ger7,True,"('A-', 'C', 'E-', 'F#')",A-,F#,1.0,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
24.25,9.0,3.0,21.0,Ger7,False,"('A-', 'C', 'E-', 'F#')",A-,F#,1.0,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
24.5,9.0,3.0,21.0,Ger7,False,"('A-', 'C', 'E-', 'F#')",A-,F#,1.0,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
24.75,9.0,3.0,21.0,Ger7,False,"('A-', 'C', 'E-', 'F#')",A-,F#,1.0,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
25.0,9.0,3.0,21.0,Ger7,False,"('A-', 'C', 'E-', 'F#')",A-,F#,1.0,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
25.25,9.0,3.0,21.0,Ger7,False,"('A-', 'C', 'E-', 'F#')",A-,F#,1.0,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
25.5,9.0,3.0,21.0,Ger7,False,"('A-', 'C', 'E-', 'F#')",A-,F#,1.0,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
25.75,9.0,3.0,21.0,Ger7,False,"('A-', 'C', 'E-', 'F#')",A-,F#,1.0,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
26.0,9.0,3.0,21.0,Ger7,False,"('A-', 'C', 'E-', 'F#')",A-,F#,1.0,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
26.25,9.0,3.0,21.0,Ger7,False,"('A-', 'C', 'E-', 'F#')",A-,F#,1.0,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
26.5,9.0,3.0,21.0,Ger7,False,"('A-', 'C', 'E-', 'F#')",A-,F#,1.0,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
26.75,9.0,3.0,21.0,Ger7,False,"('A-', 'C', 'E-', 'F#')",A-,F#,1.0,German augmented sixth chord,"(0, 3, 6, 8)",c,None,#4,None
27.0,10.0,3.0,22.0,iv,True,"('F', 'A-', 'C')",F,F,0.0,minor triad,"(0, 5, 8)",c,None,4,None
27.25,10.0,3.0,22.0,iv,False,"('F', 'A-', 'C')",F,F,0.0,minor triad,"(0, 5, 8)",c,None,4,None
27.5,10.0,3.0,22.0,iv,False,"('F', 'A-', 'C')",F,F,0.0,minor triad,"(0, 5, 8)",c,None,4,None
27.75,10.0,3.0,22.0,iv,False,"('F', 'A-', 'C')",F,F,0.0,minor triad,"(0, 5, 8)",c,None,4,None
28.0,10.0,3.0,22.0,iv,False,"('F', 'A-', 'C')",F,F,0.0,minor triad,"(0, 5, 8)",c,None,4,None
28.25,10.0,3.0,22.0,iv,False,"('F', 'A-', 'C')",F,F,0.0,minor triad,"(0, 5, 8)",c,None,4,None
28.5,10.0,3.0,22.0,iv,False,"('F', 'A-', 'C')",F,F,0.0,minor triad,"(0, 5, 8)",c,None,4,None
28.75,10.0,3.0,22.0,iv,False,"('F', 'A-', 'C')",F,F,0.0,minor triad,"(0, 5, 8)",c,None,4,None
29.0,10.0,3.0,22.0,iv,False,"('F', 'A-', 'C')",F,F,0.0,minor triad,"(0, 5, 8)",c,None,4,None
29.25,10.0,3.0,22.0,iv,False,"('F', 'A-', 'C')",F,F,0.0,minor triad,"(0, 5, 8)",c,None,4,None
29.5,10.0,3.0,22.0,iv,False,"('F', 'A-', 'C')",F,F,0.0,minor triad,"(0, 5, 8)",c,None,4,None
29.75,10.0,3.0,22.0,iv,False,"('F', 'A-', 'C')",F,F,0.0,minor triad,"(0, 5, 8)",c,None,4,None
30.0,11.0,2.0,23.0,V,True,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
30.25,11.0,2.0,23.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
30.5,11.0,2.0,23.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
30.75,11.0,2.0,23.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
31.0,11.0,2.0,23.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
31.25,11.0,2.0,23.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
31.5,11.0,2.0,23.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
31.75,11.0,2.0,23.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
32.0,11.0,1.0,24.0,V,True,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
32.25,11.0,1.0,24.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
32.5,11.0,1.0,24.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
32.75,11.0,1.0,24.0,V,False,"('G', 'B', 'D')",G,G,0.0,major triad,"(2, 7, 11)",c,None,5,None
33.0,12.0,3.0,25.0,I,True,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",c,None,1,None
33.25,12.0,3.0,25.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",c,None,1,None
33.5,12.0,3.0,25.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",c,None,1,None
33.75,12.0,3.0,25.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",c,None,1,None
34.0,12.0,3.0,25.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",c,None,1,None
34.25,12.0,3.0,25.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",c,None,1,None
34.5,12.0,3.0,25.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",c,None,1,None
34.75,12.0,3.0,25.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",c,None,1,None
35.0,12.0,3.0,25.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",c,None,1,None
35.25,12.0,3.0,25.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",c,None,1,None
35.5,12.0,3.0,25.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",c,None,1,None
35.75,12.0,3.0,25.0,I,False,"('C', 'E', 'G')",C,C,0.0,major triad,"(0, 4, 7)",c,None,1,None
"""


def _load_dfgt(csvGT):
    csvGTF = io.StringIO(csvGT)
    dfGT = pd.read_csv(csvGTF)
    dfGT.set_index("a_offset", inplace=True)
    for col in annotation_parser.A_LISTTYPE_COLUMNS:
        dfGT[col] = dfGT[col].apply(eval)
    return dfGT


class TestAnnotationParser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_initial_dataframe(self):
        dfGT = _load_dfgt(multipleAnnotationsInitialDataFrame)
        s = annotation_parser._m21Parse(multipleAnnotations)
        df = annotation_parser._initialDataFrame(s)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_reindexed_dataframe(self):
        dfGT = _load_dfgt(multipleAnnotationsFixedTimeframe)
        s = annotation_parser._m21Parse(multipleAnnotations)
        df = annotation_parser._initialDataFrame(s)
        df = annotation_parser._reindexDataFrame(df)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())


if __name__ == "__main__":
    unittest.main()