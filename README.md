# pooling_design_python
# The file, freemuxlet_pooling.py, is heavily commented with regard to purpose and functionality.
# The summary which exists at the top of the aforementioned file will be recapitulated here:
  # Purpose: To efficiently produce a balanced pooling structure for freemuxlet-based scRNAseq experiments.
  # These experiments require that only one sample from a given participant is present in a given pool, and that all of the samples from a participant appear in a unique combination of all available pools.
  # This program takes as input a .xlsx file with the first column identifying the participant, and the second column identifying the sample.
  # The column must have a header in row one but the exact text of the header is not important.
  # Any .xlsx file that is in the same directory as this program can be selected as the source file.
  # The output is a .xlsx file that details the pooling strategy.
  # The value of this program is that it will balance features of each participant and or each sample so they are distributed evenly across the pools.
  # If additional features are to be considered they should be included as columns beyond the two that are required for the program to function.
  # Sample specific features must have column heads that contain the word 'sample' (not case specific).
  # Participant specific features must have column heads that contain the word 'participant' (not case specific).
  # This balancing is accomplished by scoring distinct combinations and permutations of possible pool assignments for each participant and associated sample respectively.
  # The score is increase by the presence of other samples in the pool that have the same attributes of those being considerd for addition to the pool.
  # After all possible combinations and permutations have been checked. The combo or perm with the lowest score is selected.
  
# Example input .xlsx file array:
          #Column 1       #Column 2      #Column 3      #Column 4
# Row 1   #Participant       #Sample      #sample_atr    #participant_atr
# Row 2       #P1             #1-1         #screening        #Male
# Row 3       #P1             #1-2           #week 1         #Male
# Row 4       #P2             #2-1         #screening       #Female
# Row 5       #P2             #2-1           #week 1        #Female
