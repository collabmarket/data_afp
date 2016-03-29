# Run all the scripts

def yesno(prompt = 'Continue?', default = 'y')
    alt = 'n' if default == 'y'
    alt = 'y' if default == 'n'
    q = "#{prompt}  [#{default}]/#{alt}: "
    input = [(print q), gets.rstrip.downcase][1]
    input = default if input.empty?
    return input == 'y'
end
run_hist = yesno("Update historical?", 'n')
run_year = yesno("Update this year?", 'n')
run_month = yesno("Update this month?", 'y')
run_python = yesno("Curate data?", 'y')
run_nb = yesno("Update notebooks?", 'y')

load './vc_historical.rb' if run_hist
load './vc_this_year.rb' if run_year
load './vc_this_month.rb' if run_month
%x( python cleancsv.py ) if run_python
%x( python curator.py ) if run_python
%x( jupyter nbconvert --to notebook --execute A-E_AFP.ipynb ) if run_nb
%x( jupyter nbconvert --to notebook --execute ValoresCuotaAFP.ipynb ) if run_nb

