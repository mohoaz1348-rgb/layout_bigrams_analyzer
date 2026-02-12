# ABA – All Bigrams Analyzer
## Why another analyzer?
  If you look at the results of a keyboard layout bigram analysis in any analyzer and add them together, the sum won't exceed 5%. Where are the results for the other bigrams? Are they really that unimportant?
  These analyzers also do not take into account a person's individual preferences for typing certain key combinations on one hand.
As a result, I found it difficult to evaluate the usability of any particular layout for myself. I should note that evaluating a layout based solely on bigram analysis is impossible, and my bigram analyzer doesn't claim to be a full-fledged layout analyzer—it's simply an additional utility that fills the gaps in modern analyzers.
## Possible algorithm for applying ABA
When choosing a layout, I proceed as follows: first, I select layouts that meet my requirements for redirects (especially bad ones); at this stage, significant selection occurs. I don't pay attention to the number of rolls, as these can be scissors or other awkward combinations. I simply look at the ratio of inward/outward rolls. There shouldn't be significantly more outward rolls than inward rolls.
I run the remaining layouts through my analyzer, which creates a comparison table. Since comfort is important to me, I choose the layouts with the fewest awkward combinations. If there are several such layouts, I look at the comfortable combinations and choose the one with the most.
## How ABA Works
Now I'll explain how all the bigrams of a language are analyzed for the layout. I use a standard keyboard for typing, so I'll use that as an example. The left- and right-hand keys are numbered sequentially:
Left arm:
| 1 | 2 | 3 | 4 | 5 |
 -----------------
 | 6 | 7 | 8 | 9 | 10|
 -----------------
   | 11| 12| 13| 14| 15|
Right arm:
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
     -----------------
 | 8 | 9 | 10| 11| 12| 13|
     -----------------
   | 14| 15| 16| 17| 18|
Then, for each key combination on one hand, I build a preference matrix (they are different for standard mode and Angle Mod)
Left arm (Angle Mod) for example:
**  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
-----------------------------------------------
01 -3  1 -2  1  1 -3 -3 -3  2  1 -3 -3  1  1 -2
02 -1 -1  2  2  0 -3 -1 -2  3  0 -2 -3  2  0 -2
03 -2  2 -1  2  0 -2  1 -1  3 -1 -3 -2  1  0 -3
04  1  2  2 -1 -1  1  1  1 -1 -2 -2 -3 -2 -2 -3
05  1  0  0 -1 -1  0  0  0 -1 -1 -2 -3 -3 -2 -3
06 -3  0 -2  1  1 -3  2 -2  2  2 -3 -3  2  2  0
07 -3 -1  3  2  1 -1 -1  3  3  2 -1 -2  3  3 -2
08 -3 -2 -1  1  0 -2  3 -1  3  0  0 -1  3  2 -2
09  2  3  3 -1 -1  2  3  3 -1 -1  0  0 -1 -1 -2
10  1  1 -1 -2 -1  2  1  0 -1 -1 -1 -1 -2 -1 -1 
11 -3 -2 -3 -2 -2 -3 -1  1  0 -1 -1  1  1  0 -3
12 -2 -3 -2 -3 -3 -3  2 -1  1 -2  1 -1  1 -1 -3
13  1  2  1 -2 -3  2  3  3 -1 -2  1  1 -1 -1 -3
14  1  1  0 -2 -2  2  3  2 -1 -1  0 -1 -1 -1 -2
15 -2 -2 -3 -3 -3  0 -1 -1 -2 -1 -3 -3 -3 -2 -2
- “-3” – the most inconvenient combinations
- “0” – neutral combinations
- “3” – the most convenient combinations
This is the most labor-intensive part, which can take a full day. But at least you'll know for sure that the analysis results reflect your preferences.
Then, based on these effort matrices, all the bigrams in the language are classified, the total frequency is calculated for each category (-3, -2, -1, 0, 1, 2, 3), and a final comparison table is created. The results are sorted by the "-3" column, as I believe that the comfort of a layout is primarily determined by the absence of awkward combinations.
en
LAYOUT(mode)        -3        -2        -1        0         1         2         3         alt       not_found 
grawerty(ang)       0.248     1.11      5.374     1.398     3.178     8.026     12.118    70.763    0.19      
canary(ang)         0.506     1.529     4.173     3.613     3.645     8.718     17.516    62.515    0.19      
graphite-ang(ang)   0.618     4.808     3.987     0.895     2.968     7.518     10.728    70.883    0.0       
workman(ang)        0.665     4.235     5.518     2.343     4.378     13.092    14.566    57.418    0.19      
comet(ang)          0.687     2.244     4.052     4.051     4.533     7.0       10.73     69.108    0.0       
workman(std)        0.688     5.251     5.661     2.39      4.19      12.223    14.394    57.418    0.19      
gallium-v2(std)     0.815     4.438     4.239     0.921     3.782     7.312     9.945     70.763    0.19      
northstar(ang)      0.962     2.244     4.156     1.276     3.163     9.451     10.2      70.763    0.19      
colemak(ang)        1.087     2.772     5.441     5.351     5.698     10.396    11.339    60.131    0.19      
colemak(std)        1.093     3.757     5.889     5.4       5.645     9.409     10.891    60.131    0.19      
sturdy-ang(ang)     1.13      2.678     4.126     2.117     3.674     9.543     14.462    64.485    0.19      
focal-ang(ang)      1.251     2.932     3.973     1.206     4.097     7.341     13.232    68.183    0.19      
beakl19bis(std)     1.403     5.12      4.248     2.523     1.886     6.032     7.466     73.537    0.19      
kuntem(ang)         1.45      3.038     4.559     2.347     4.609     11.732    7.321     67.159    0.19      
anymak:end(ang)     1.496     4.585     4.248     1.245     3.051     7.219     6.81      73.561    0.19      
ctgap-ang(ang)      1.682     2.056     4.266     1.007     2.74      8.381     12.406    69.677    0.19      
apt-V3(ang)         1.951     2.778     3.918     1.407     5.072     8.486     14.175    64.428    0.19      
colemak-dh(ang)     1.977     2.92      4.995     2.712     6.174     9.947     13.359    60.131    0.19      
dvorak(std)         2.21      3.271     4.671     1.66      6.213     4.362     7.219     72.799    0.0       
qwerty(ang)         2.476     3.428     8.286     7.727     12.706    10.736    2.496     54.36     0.19      
qwerty(std)         2.963     5.062     8.466     7.73      11.572    9.749     2.313     54.36     0.19
The mode in which the layout was analyzed is indicated in parentheses after the layout name. Values ​​are given as percentages.
## Some of my least favorite combinations
- Full scissors - "-3" – except for combinations where the index finger is down and the middle finger is up
- Half scissors (pinky, ring) - "-3"
- sfb(0u)(pinky) - "-3"
- sfb(0u)(index, middle, ring) - "-1"
- sfb(1u)(pinky) - "-3"
- sfb(1u)(index, middle, ring) - "-1"
- sfb(2u)(pinky) - "-3"
- sfb(2u)(index, middle, ring) - "-2"
- **rolls(pinky, middle) - "-2", "-3"**
- lsb - "0", "-1"
I don't demonize SFB (except for pinkies) and I don't think they are the most awkward combinations.
## Using ABA
After cloning the repository, simply navigate to the folder containing the `analyze.py` file and run it (no additional dependencies or virtual environments required):
`python analyze.py`
All layouts for each language will be analyzed. Comparison tables for each language will appear in the terminal and will be saved to the file `lang/results` (where `lang` is the language name). Detailed results for each layout will not be output to the terminal, but will be saved to a file in the `lang/results_all` folder. The threshold for displaying a bigram in the full report is set to 0.005% and can be easily changed in the script file.
If a particular layout isn't included in the analysis, simply copy the existing layout file and edit it. Don't forget to specify the analysis mode `std` or `ang` in the layout file. Both modes can be specified (separated by a space).
The analyzer only includes English and Russian layouts, but you can add any language for analysis by creating a folder with the name of the language and adding the layout files to it. Then add the language to the list of languages ​​in the analyze.py script. You will also need to create a file with the list of bigrams and their frequencies.
The analyzer only supports the ANSI keyboard, but it can be used with any keyboard with any number of keys. Simply create a new keyboard folder, number the keys sequentially for each hand, and, based on this numbering, construct matrices of efforts and add them to the corresponding files (`left`, `right`), from where the analyzer reads them. The folder structure should be the same as for `ANSI` folder. Next, copy `analyze.py` to the keyboard folder and run it.
