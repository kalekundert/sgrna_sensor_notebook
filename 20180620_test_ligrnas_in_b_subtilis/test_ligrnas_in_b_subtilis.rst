***************************
Test ligRNAs in B. subtilis
***************************

We make the claim in the paper that our system may be useful in bacteria 
without facile genetic controls.  The reviewers asked that we back up this 
claim by testing in a bacterial species other than E. coli.  We chose B.  
subtilis (Bs) because it is a model organism and the Carol Gross lab has agreed 
to help get me off the ground with it.  But it's also a good choice because 
it's a gram-positive species, while E. coli (Ec) is gram-negative, so the two 
species are often assumed to be representative of bacteria as a whole (even 
though our collaborators is the Gross lab caution that this is probably less 
true than it seems).

Methods
=======

Cloning
-------
The Gross lab has a B. subtilis strain that expresses the exact same 
super-folder GFP sequence that I've been using in bacteria.  That's convenient 
for me, because it allows us to use the same guides as before.  I'll begin by 
just using g1 (g2 doesn't seem to work very well).  If I have problems, I can 
come back and think more about which guides I want to use.

I got a B. subtilis sgRNA plasmid from the Gross lab.  I'm going to clone my 
ligRNAs using gBlocks and restriction cloning.  Unfortunately the MCS on this 
plasmid kinda sucks.  All the restriction sites that are present 5' of the 
sgRNA are also present 3' of it, so I have no option but to use the same 
restriction site on both sides of the insert.  This means that I'll get 
fragments inserted in both directions, so I'll have to pick extra colonies to 
account for that.  I decided to use HindIII, since it will allow me to order 
the smallest gBlocks.

It's worth noting that I decided against using inverse PCR because I would've 
had to do three reactions: one to install the spacer, one to install the Dang 
scaffold, and one to install the specific designs.  I could've also just 
ordered one gBlock (e.g. g1/on) and used inverse PCR to clone the designs, but 
ordering all the gBlocks will be the fastest way to make these constructs, and 
I think that's the most important consideration.

:download:`gblocks.xlsx`

2018/06/27:

- Miniprep pJMP3 (the backbone).  Yield: 269.2 ng/µL.

2018/06/28:

.. literalinclude:: restriction_cloning.txt

.. note::

   The above reaction has 10 U of HindIII, which is what was recommended by 
   NEB.  Since I don't often do restriction digests, I wanted to do a quick 
   calculation to make sure that 10 U would be enough:

   - `1 U of HindIII-HF digests 1 µg of λ DNA in 1h at 37°C 
     <https://www.neb.com/products/R3104-HindIII-HF#Product%20Information>`_

   - λ DNA is `48,502 bp long <http://www.bioinformatics.nl/molbi/SCLResources/lambda.htm>`_ and has 
     `6 HindIII sites <http://www.bioinformatics.nl/molbi/SCLResources/LambdaBE_restrct_alphab.htm>`_.

   - My backbone is 7263 bp and has 2 HindIII sites.  

   - (1 µg pJMP3) × (N bp / 1 μg) × (2 HindIII sites / 7263 bp pJMP3) × 
     (48,502 bp λ DNA / 6 HindIII sites) × (1 µg λ DNA / N bp) × (1 U at 
     37°C for 1h / 1 μg λ DNA) = 2.23 U at 37°C for 1h.

   10 U should be plenty.

If I have trouble with this, order primers to linearize the backbone and do 
Gibson.  Or order BsrGI and PmeI, but primers would be cheaper.  Why didn't I 
just think to do Gibson in the first place?


