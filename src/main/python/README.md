Instructions for running the python script to generate the HTML for a tournament.

1. you will need the 'Tournament ID' when running the script
   a) you can look up the ID at the USCF website using the following url 
      https://www.uschess.org/msa/AffDtlTnmtHst.php?A5008948/ 

2. run the script like this:
 
   cd {PROJECT_ROOT}/src/main/python
   export PYTHONPATH=.
   python3 root/main.py web 123456
   (use the actual tournament id instead of 123456)

   or, better still, run the script and redirect the output to a file:
   python3 root/main.py web 123456 > LateSummer.html

3. you can copy the majority of the html into the WCC blog as a post (you don't need 
   the \<html> tags or the \<head> section).
   you can also view the resulting page in your browser (to see if all looks well) 

