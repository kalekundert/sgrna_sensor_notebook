**************************************
Test ligRNAs in Pseudomonas aeruginosa
**************************************

Methods
=======

Pick target sequences
---------------------
2018/07/17:

Jiuxin provided me with a list of target sequences for the folA gene.  I used 
ViennaRNA to predict which would be most likely to not interfere with the 
ligRNA (``./predict_spacer_quality.sh``).  Notably, the folA gene is very 
GC-rich (72%), so most of the spacers had pretty high predicted affinity for the 
ligRNA insert.  The promoter region appeared to be an exception, however.  The 
4 spacers I think would be the most promising to test would be fol1, fol2, 
fol3, and fol4::

    fol1
    Spacer: UCCACGAUGAGGUAACCCCA
    Insert: GUGGGAUACCAGCCGAAAGGCCCUUGGCAGCCUAC
    ΔG:     -10.8

    fol2
    Spacer: UGGGGUUACCUCAUCGUGGA
    Insert: GUGGGAUACCAGCCGAAAGGCCCUUGGCAGCCUAC
    ΔG:     -11.1

    fol3
    Spacer: GCCAUGGGGUUACCUCAUCG
    Insert: GUGGGAUACCAGCCGAAAGGCCCUUGGCAGCCUAC
    ΔG:     -15.5

    fol4
    Spacer: UAACCCCAUGGCACGACCGC
    Insert: GUGGGAUACCAGCCGAAAGGCCCUUGGCAGCCUAC
    ΔG:     -9.5

Strain construction
-------------------
2018/07/17:

I designed sequences containing the ligRNAs with the aforementioned spacers 
that could be cloned into the Rosenberg lab's sgRNA vector using Gibson 
assembly (``./make_gibson_inserts.py``).  Jiuxin noted that my sgRNA scaffold 
is different in two positions from theirs.  This difference is intentional, and 
is due to us using different optimized scaffolds.  We decided to use my 
scaffold, as the ligRNAs may be sensitive to mutations in the scaffold.

Jiuxin constructed the strains for me, and I don't know how he did it.  To 
start with, Jiuxin only cloned the fol1 constructs.  The fol1/on construct  did 
not grow well, presumably because leaky expression of the Cas9 system inhibited 
folA too strongly.  Jiuxin had not had this problem with his previous 
constructs.  The most likely explanation for the difference is the spacer (fol1 
vs fol9), since fol1 targets the promoter region and is therefore expected to 
repress more strongly.  It's also possible that the mutations in the scaffold 
were wholly or partly responsible for the defect.  For the MIC experiments, 
we'll use Jiuxin's fol9 sgRNA as our positive control.

Minimum inhibitory concentration (MIC) of trimethoprim (TMP)
------------------------------------------------------------
Trimethoprim (TMP) is an antibiotic that targets DHFR.  CRISPRi repression of 
folA increases the sensitivity of pseudomonas to TMP.  The minimum inhibitory 
concentration (MIC) of theophylline quantifies this sensitivity.  We are 
specifically testing the theophylline affects the MIC for the ligRNA 
constructs.

For reference, here is published MIC data for P. aeruginosa [Peters2018]:

.. figure:: published_mic.svg

We are doing the experiment in two steps.  First, we are setting up a plate 
with a variety of TMP concentrations to determine the MIC for each construct.  
Second, we will measure growth curves for each of these concentrations to get 
more presentable data.

.. update:: 2018/10/12
   
   The only reason it was neccesary to do these steps separately was that the 
   Rosenberg lab didn't have a plate reader capable of incubating and 
   measuring.  The JBD lab does have such a plate reader though, so I'm now 
   doing both steps simultaneously.  See the `Growth Curves`_ section below.

1. Grow overnight cultures of each ligRNA construct (fol1/on, fol1/off, 
   fol1/rxb/11/1, fol1/mhf/30) in 3 mL LB.

2. For each culture, setup serial dilutions of TMP with and without 
   theophylline (in duplicate):

   - Measure OD600 of the culture.

   - Prepare media master mixes with and without 2x theophylline:

      - 8866.7 µL media (can't remember name or recipe)
      - 633.3 µL water (apo) or 30 mM theophylline (holo)

   - Dilute culture to OD600=0.05 in each media master mix.

   - Prepare 64 µg/mL (2x) TMP (in media).

      - I don't know the specific recipe.

   - Create 7 2x dilutions of TMP:

      - Put 4 mL 2x TMP in a tube.
      - Put 2 mL media in 6 other tubes.
      - Perform a serial dilution, transferring 2 mL on each step.

   - Pipet 100 µL of the 2x TMP dilution to the appropriate wells of a clear 
     round-bottom 96-well plate.

   - Pipet 100 µL of the culture (with or without 2x theophylline) into the 
     appropriate wells of the same plate.

- Incubate at 37°C for 15h with shaking at 350 rpm.

- Measure OD600 for each well.

It seems that both rxb/11/1 and mhf/30 affect the MIC of TMP in a 
theophylline-dependent manner.

rxb/11/1: Difference is subtle, affected by normalization of data.  

The controls are really fucked:

- on appears to have the worst repression of everything.  This may be 
  attributable to using the different spacer.

- off seems to be more repressing that mhf/30.

.. figure:: 20180913_pseudomonas_endpoint_mic.svg 
   
.. figure:: 20180913_pseudomonas_endpoint_mic_wells.svg 

Growth curves
-------------

Below is the basic protocol I used to setup the MIC assays.  Deviations from 
this protocol are explained for each data set below:

.. literalinclude:: 20181012_tmp_mic_assay.txt

2018/09/25:

In this experiment, I used 0.5 mM theo (rather than 1 mM) in an attempt to be 
really conscientious about avoiding theophylline toxicity.  Despite this, the 
positive control cultures with 8.0 µg/mL TMP or higher still (sometimes) seem 
to be affected by theophylline.  The effect is inconsistent, though:

- 8 µg/mL: The effect is slight, but theophylline is somewhat toxic.
- 16 µg/mL: The effect is inverted: the cultures grow faster in the presence of 
  theophylline, which doesn't make sense.  I'm inclined to attribute this to 
  the cells just taking a long time to enter log phase, and that transition 
  being somewhat stochastic.
- 32 µg/mL: The effect is just visible, because the apo cultures start growing 
  just at 24h.

The effect of theophylline on the ligRNAs is also slight and inconsistent:

- rxb/11/1, 16 µg/mL: Noticeable effect, but in the opposite direction as 
  expected.  It's noteworthy that the controls also appear to flipped for this 
  well, making me suspicious that I flipped the apo and holo conditions 
  somehow.  I double-checked my analysis scripts, and they seem to be right.  
  It's possible that I pipetted the wells wrong, but that would mean I made a 
  mistake and compensated for it, and I definitely don't remember doing that.

- rxb/11/1, 32 µg/mL: A fairly strong effect, with the caveat that the cells in 
  both conditions are clearly sick, and the previous TMP concentration showed 
  the exact opposite effect.

- mhf/30, 16 µg/mL: A very weak effect, and it's weird that the ligRNA traces 
  are outside the bounds established by the controls.  Again, I would probably 
  attribute this to sick cells and some stochasticity in when cells enter log 
  phase, but it's not encouraging.

- mhf/30, 32 µg/mL: A larger effect, but still outside the bounds of the 
  controls.  Note also that the effect of the ligRNA in this case is the same 
  as the assumed toxicity of adding theophylline.

.. figure:: 20180925_pseudomonas_tmp_titration.svg

   Solid lines represent 0.5 mM theophylline (rather than the usual 1 mM).  
   Grey lines represent the controls, navy lines represent rxb/11/1, and teal 
   lines represent mhf/30.

2018/10/10:

In this experiment, I made an effort to better follow the canonical MIC assay 
described by [Weigand2008]_.  In particular, this meant:

a. Diluting the cells to OD=0.0025 rather than OD=0.05.
b. Starting cultures directly from plates, and from a lawn, rather than making 
   overnight cultures for single colonies and doing a 2h out-growth step.
c. Not shaking the plate during the incubation.

I deviated from the Weigand2008_ protocol in putting 50 µL mineral oil on top 
of each well.  Weigand2008_ calls for incubating the plate in a box with a wet 
paper towel to prevent evaporation, but isn't practical in the plate reader 
(Weigand2008_ also calls for just measuring OD once, by eye, after 24h, but I 
want growth curves.)  So I decided that it'd be better to have oil preventing 
evaporation, even though the oil also reduces oxygenation.

These results don't make any sense:

- The plate reader stopped recording data after ~13h.  I don't know why.

- TMP inhibits growth, but there's no difference between the controls or any of 
  the ligRNAs.

- For low concentration of TMP, growth is much slower than in the previous 
  experiment.

I think these weird results are related to (b) and (c) above, so I'm going to 
go back to my old protocol in those regards.  I'm going to keep (a) because I 
saw more growth than Peters2018_ in my previous experiment, and a larger 
innoculum could explain that.

.. figure:: 20181010_pseudomonas_mic_1mM_theo.svg

Results
=======
Pseudomonas is relatively tolerant to theophylline.  A growth defect is 
apparent at 4 mM, and a smaller defect is present at 2 mM and 1 mM.  Below 
that, no defect is detectable.

.. figure:: pa14_theo_toxicity_growth_curve.jpg

   I'm not sure what the difference between the left and right plots are.  I 
   also don't know what P3-aFolA means.  The indicated concentrations (in mM) 
   refer to theophylline.

References
==========
.. [Peters2018] :doi:`10.1101/315499`
.. [Weigand2008] :doi:`10.1038/nprot.2007.521`




