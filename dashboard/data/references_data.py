"""
Bibliography of the published paper:

  Prieto Gratacós E, Botto J. The Twilight of Antibiotics: a predictive
  mathematical model of declining antimicrobial effectiveness, and a possible
  metabolic escape route. Br J Med Health Res. 2026;13(8):43-56.
  doi:10.5281/zenodo.21898960

All 55 references, numbered exactly as in the published version. Each entry has:
  * n        — reference number in the published paper
  * section  — paper section the reference supports
  * citation — full citation
  * url      — DOI when the published paper gives one; otherwise a verified
               article/journal link or a PubMed search on the title
"""

REFERENCES = [
    # ------------------------------------------------------------------
    # Introduction: Foundational epidemiology and global burden (refs 1-10)
    # ------------------------------------------------------------------
    {"n": 1, "section": 'Foundational epidemiology',
     "citation": 'Murray, C. J. L. et al. Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis. Lancet 399 (2022).',
     "url": 'https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext'},
    {"n": 2, "section": 'Foundational epidemiology',
     "citation": 'Global burden of bacterial antimicrobial resistance in 2019: summary and implications. BMJ (2022).',
     "url": 'https://www.bmj.com/content/378/bmj.o2046'},
    {"n": 3, "section": 'Foundational epidemiology',
     "citation": "Aslam, B. et al. Antibiotic Resistance: One Health One World Outlook. Front. Cell. Infect. Microbiol. (2021); O'Neill, J. Review on Antimicrobial Resistance.",
     "url": 'https://www.frontiersin.org/articles/10.3389/fcimb.2021.771510/full'},
    {"n": 4, "section": 'Foundational epidemiology',
     "citation": 'DalBen, M. F. et al. A Model-Based Strategy to Control the Spread of Carbapenem-Resistant Enterobacteriaceae: Simulate and Implement. Infect Control Hosp Epidemiol. 2016;37(11):1315-1322.',
     "url": 'https://doi.org/10.1017/ice.2016.168'},
    {"n": 5, "section": 'Foundational epidemiology',
     "citation": 'Van Duin, D. & Paterson, D. L. Multidrug-Resistant Bacteria in the Community: Trends and Lessons Learned. Infect. Dis. Clin. North Am. (2016).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/27208766/'},
    {"n": 6, "section": 'Foundational epidemiology',
     "citation": 'Xiao, Y. et al. Antimicrobial use, healthcare-associated infections, and bacterial resistance in general hospitals in China: the first national pilot point-prevalence survey report. Eur. J. Clin. Microbiol. Infect. Dis. (2023).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Antimicrobial+use+healthcare-associated+infections+bacterial+resistance+general+hospitals+China+first+national+pilot+point-prevalence+survey'},
    {"n": 7, "section": 'Foundational epidemiology',
     "citation": 'Reale, M. et al. Patterns of multi-drug resistant bacteria at first culture from patients admitted to a third-level university hospital in Calabria from 2011 to 2014. Infez. Med. (2017).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Reale+multi-drug+resistant+Calabria+2017'},
    {"n": 8, "section": 'Foundational epidemiology',
     "citation": 'Kiddee, A. et al. Risk Factors for Gastrointestinal Colonization and Acquisition of Carbapenem-Resistant Gram-Negative Bacteria among Patients in Intensive Care Units in Thailand. Antimicrob. Agents Chemother. (2018).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Kiddee+Risk+Factors+Gastrointestinal+Colonization+Carbapenem-Resistant+Gram-Negative+Thailand'},
    {"n": 9, "section": 'Foundational epidemiology',
     "citation": 'Bonten, M. J. M. Colonization pressure: a critical parameter in the epidemiology of antibiotic-resistant bacteria. Crit. Care (2012).',
     "url": 'https://ccforum.biomedcentral.com/articles/10.1186/cc11508'},
    {"n": 10, "section": 'Foundational epidemiology',
     "citation": 'Tai, J.-H., Wu, Y.-L. et al. Global, regional, and national burden of bacterial carbapenem resistance from 1990 to 2021 and predictions up to 2035. Int. J. Antimicrob. Agents (2025).',
     "url": 'https://doi.org/10.1016/j.ijantimicag.2025.107636'},

    # ------------------------------------------------------------------
    # Introduction: Exponentially evolving pan resistant strains (refs 11-22)
    # ------------------------------------------------------------------
    {"n": 11, "section": 'ESKAPEE & dynamic susceptibility',
     "citation": 'Miller, W. R. & Arias, C. A. ESKAPE pathogens: antimicrobial resistance, epidemiology, clinical impact and therapeutics. Nature Reviews Microbiology 22, 598–616 (2024).',
     "url": 'https://www.nature.com/articles/s41579-024-01054-w'},
    {"n": 12, "section": 'ESKAPEE & dynamic susceptibility',
     "citation": 'Wang, M., Fu, Q. et al. Epidemiological investigation and patterns of antimicrobial use in multidrug-resistant bacteria at a tertiary hospital: a retrospective cohort study. BMJ Open (2025).',
     "url": 'https://doi.org/10.1136/bmjopen-2025-099847'},
    {"n": 13, "section": 'ESKAPEE & dynamic susceptibility',
     "citation": 'Kim, J. et al. Predicting antimicrobial resistance of bacterial pathogens using time-series data from >600 farms. Front. Microbiol. (2023).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Predicting+antimicrobial+resistance+of+bacterial+pathogens+using+time-series+data+from+600+farms'},
    {"n": 14, "section": 'ESKAPEE & dynamic susceptibility',
     "citation": 'Time series analysis of antibacterial usage and bacterial resistance in China: observations from a tertiary hospital from 2014 to 2018. PLoS One (2019).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Time+series+analysis+of+antibacterial+usage+and+bacterial+resistance+in+China+tertiary+hospital+2014+to+2018'},
    {"n": 15, "section": 'ESKAPEE & dynamic susceptibility',
     "citation": 'Zhou, R. et al. Impact of carbapenem resistance on mortality in patients infected with Enterobacteriaceae: a systematic review and meta-analysis. BMJ Open (2021).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Impact+of+carbapenem+resistance+on+mortality+in+patients+infected+with+Enterobacteriaceae+systematic+review+meta-analysis'},
    {"n": 16, "section": 'ESKAPEE & dynamic susceptibility',
     "citation": 'Tadese, B. K. et al. Clinical epidemiology of carbapenem-resistant Enterobacterales in the Greater Houston region of Texas: a 6-year trend and surveillance analysis. J. Glob. Antimicrob. Resist. (2022).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Clinical+epidemiology+of+carbapenem-resistant+Enterobacterales+Greater+Houston+region+Texas+6-year+trend'},
    {"n": 17, "section": 'ESKAPEE & dynamic susceptibility',
     "citation": 'Qu, X. et al. Surveillance of carbapenem-resistant Klebsiella pneumoniae in Chinese hospitals: a five-year retrospective study. J. Infect. Dev. Ctries. (2019).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Surveillance+of+carbapenem-resistant+Klebsiella+pneumoniae+in+Chinese+hospitals+five-year+retrospective+study'},
    {"n": 18, "section": 'ESKAPEE & dynamic susceptibility',
     "citation": 'Lee, J. et al. Carbapenem-Resistant Klebsiella pneumoniae in Large Public Acute-Care Healthcare System, New York, New York, USA, 2016–2022. Emerg. Infect. Dis. (2023).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Carbapenem-Resistant+Klebsiella+pneumoniae+Large+Public+Acute-Care+Healthcare+System+New+York+2016-2022'},
    {"n": 19, "section": 'ESKAPEE & dynamic susceptibility',
     "citation": 'Yao, Y. et al. Healthcare-associated carbapenem-resistant Klebsiella pneumoniae infections are associated with higher mortality compared to carbapenem-susceptible K. pneumoniae infections in the intensive care unit. J. Hosp. Infect. (2024).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Healthcare-associated+carbapenem-resistant+Klebsiella+pneumoniae+infections+higher+mortality+intensive+care+unit'},
    {"n": 20, "section": 'ESKAPEE & dynamic susceptibility',
     "citation": 'Chotiprasitsakul, D. et al. Epidemiology of carbapenem-resistant Enterobacteriaceae. Infect. Drug Resist. (2019).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Chotiprasitsakul+carbapenem-resistant+Enterobacteriaceae'},
    {"n": 21, "section": 'ESKAPEE & dynamic susceptibility',
     "citation": 'Chatzopoulou, M. & Reynolds, L. Systematic review of the effects of antimicrobial cycling on bacterial resistance rates within hospital settings. Br J Clin Pharmacol. 2022;88(3):897-910.',
     "url": 'https://doi.org/10.1111/bcp.15042'},
    {"n": 22, "section": 'ESKAPEE & dynamic susceptibility',
     "citation": 'Brepoels, P., Appermans, K., Pérez-Romero, C. A., Lories, B., Marchal, K. et al. Antibiotic Cycling Affects Resistance Evolution Independently of Collateral Sensitivity. Mol Biol Evol. 2022;39(12):msac257.',
     "url": 'https://doi.org/10.1093/molbev/msac257'},

    # ------------------------------------------------------------------
    # Introduction: superbugs and MDR/XDR/PDR phenotypes (refs 23-36)
    # ------------------------------------------------------------------
    {"n": 23, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Magiorakos, A. P. et al. Multidrug-resistant, extensively drug-resistant and pandrug-resistant bacteria: an international expert proposal for interim standard definitions. Clin. Microbiol. Infect. (2012).',
     "url": 'https://www.clinicalmicrobiologyandinfection.com/article/S1198-743X(14)61632-3/fulltext'},
    {"n": 24, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Temkin, E., Adler, A., Lerner, A., Carmeli, Y. Carbapenem-resistant Enterobacteriaceae: epidemiology and management (2014).',
     "url": 'https://doi.org/10.1111/nyas.12537'},
    {"n": 25, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Carbapenem-resistant Klebsiella pneumoniae: a global threat. Expert Rev. Anti-Infect. Ther. (2020).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Carbapenem-resistant+Klebsiella+pneumoniae+global+threat'},
    {"n": 26, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Baleivanualala, S. C., Devi, S. V., Howden, B., Gorrie, C. L., Matanitobua, S. et al. Molecular and clinical epidemiology of carbapenem resistant Acinetobacter baumannii ST2 in Oceania: a multicountry cohort study.',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Molecular+and+clinical+epidemiology+of+carbapenem+resistant+Acinetobacter+baumannii+ST2+in+Oceania'},
    {"n": 27, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Carbapenem-resistant Pseudomonas aeruginosa. Front. Microbiol. (2019).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Carbapenem-resistant+Pseudomonas+aeruginosa'},
    {"n": 28, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Methicillin-resistant Staphylococcus aureus (MRSA): a global perspective. Lancet Infect. Dis. (2016).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Methicillin-resistant+Staphylococcus+aureus+global+perspective'},
    {"n": 29, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Vancomycin-resistant Enterococcus (VRE): epidemiology and outcomes. Clin. Microbiol. Rev. (2019).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Vancomycin-resistant+Enterococcus+epidemiology+outcomes'},
    {"n": 30, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Pandrug-resistant Acinetobacter baumannii: emergence and clinical implications. J. Infect. (2018).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Pandrug-resistant+Acinetobacter+baumannii'},
    {"n": 31, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Pandrug-resistant Gram-negative pathogens in the ICU. Crit. Care (2021).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Pandrug-resistant+Gram-negative+ICU'},
    {"n": 32, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Pan-drug-resistant Pseudomonas aeruginosa: a case report and review. J. Infect. Public Health (2019).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Pan-drug-resistant+Pseudomonas+aeruginosa+case+report+review'},
    {"n": 33, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Extensively drug-resistant tuberculosis (XDR-TB): global epidemiology. Lancet (2018).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Extensively+drug-resistant+tuberculosis+global+epidemiology'},
    {"n": 34, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Pandrug-resistant Klebsiella pneumoniae producing carbapenemases in a European ICU. Antimicrob. Agents Chemother. (2020).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Pandrug-resistant+Klebsiella+pneumoniae+carbapenemases+ICU'},
    {"n": 35, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Pandrug-resistant Enterobacter spp. in a teaching hospital. J. Glob. Antimicrob. Resist. (2021).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Pandrug-resistant+Enterobacter+teaching+hospital'},
    {"n": 36, "section": 'Superbugs (MDR/XDR/PDR)',
     "citation": 'Tan, C.-K. et al. Extensively drug-resistant Stenotrophomonas maltophilia in a tertiary care hospital in Taiwan: microbiologic characteristics, clinical features, and outcomes. Diagn. Microbiol. Infect. Dis. (2008).',
     "url": 'https://doi.org/10.1016/j.diagmicrobio.2007.09.007'},

    # ------------------------------------------------------------------
    # Materials and Method: bibliometric dynamics and industry trends (refs 37-38)
    # ------------------------------------------------------------------
    {"n": 37, "section": 'Bibliometrics & industry',
     "citation": 'PubMed search: "antibiotic resistance" (cumulative results up to 2025).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=antibiotic+resistance'},
    {"n": 38, "section": 'Bibliometrics & industry',
     "citation": 'Univdatos. Antibiotic Resistance Market: Current Analysis and Forecast (2024-2032).',
     "url": 'https://univdatos.com/reports/antibiotic-resistance-market'},

    # ------------------------------------------------------------------
    # Antimetabolites in the treatment of infections (refs 39-55)
    # ------------------------------------------------------------------
    {"n": 39, "section": 'Antimetabolites',
     "citation": 'Loewen, P. C. & Richter, H. E. Inhibition of sugar uptake by ascorbic acid in Escherichia coli. Arch Biochem Biophys. 1983;226(2):657-665.',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Inhibition+of+sugar+uptake+by+ascorbic+acid+in+Escherichia+coli'},
    {"n": 40, "section": 'Antimetabolites',
     "citation": 'Shukla, H., Tripathi, A., Shukla, S. Alternate pathway to ascorbate induced inhibition of Mycobacterium tuberculosis. Tuberculosis (Edinb). 2018;111:161-169.',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Alternate+pathway+to+ascorbate+induced+inhibition+of+Mycobacterium+tuberculosis'},
    {"n": 41, "section": 'Antimetabolites',
     "citation": 'Hoffman, P. S. et al. 2-Deoxy-D-glucose is a potent inhibitor of biofilm growth in Escherichia coli. Microbiology. 2016;162(6):1037-1046.',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=2-Deoxy-D-glucose+is+a+potent+inhibitor+of+biofilm+growth+in+Escherichia+coli'},
    {"n": 42, "section": 'Antimetabolites',
     "citation": 'Thompson, J. & Chassy, B. M. Regulation of glycolysis and sugar phosphotransferase activities in Streptococcus lactis: growth in the presence of 2-deoxy-D-glucose. J Bacteriol. 1982;149(1):183-193.',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Regulation+of+glycolysis+and+sugar+phosphotransferase+activities+in+Streptococcus+lactis+2-deoxy-D-glucose'},
    {"n": 43, "section": 'Antimetabolites',
     "citation": 'Prieto Gratacós, E. Antimetabolites in the Treatment of Solid Tumors: Competitive Inhibition by Structural Analogs. Journal of Oncology Research and Therapy (2026).',
     "url": 'https://doi.org/10.29011/2574-710X.10342'},
    {"n": 44, "section": 'Antimetabolites',
     "citation": 'Kebriaei, R. et al. Activity of the Lactate Dehydrogenase Inhibitor Oxamic Acid against the Fermentative Bacterium Streptococcus mitis/oralis: Bactericidal Effects and Prevention of Daptomycin Resistance. Antibiotics (2022).',
     "url": 'https://doi.org/10.3390/antibiotics11101409'},
    {"n": 45, "section": 'Antimetabolites',
     "citation": 'Buckel, W. Energy Conservation in Fermentations of Anaerobic Bacteria. Frontiers in Microbiology (2021).',
     "url": 'https://doi.org/10.3389/fmicb.2021.703525'},
    {"n": 46, "section": 'Antimetabolites',
     "citation": 'Daley, S. R. et al. Kinetic characterization of annotated glycolytic enzymes present in cellulose-fermenting Clostridium thermocellum suggests different metabolic roles. Biotechnology for Biofuels and Bioproducts (2023).',
     "url": 'https://doi.org/10.1186/s13068-023-02362-8'},
    {"n": 47, "section": 'Antimetabolites',
     "citation": 'Prieto Gratacós, E. Safety of Antimetabolite 2-Deoxy-D-arabinohexose (2DG) as a Coadjuvant Metabolic Intervention in 268 Cancer Patients. Cancer Medicine Journal (2020).',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Safety+of+Antimetabolite+2-Deoxy-D-arabinohexose+Coadjuvant+Metabolic+Intervention+268+Cancer+Patients'},
    {"n": 48, "section": 'Antimetabolites',
     "citation": 'Xi, J. et al. The wonders of 2-deoxy-D-glucose. IUBMB Life. 2014;66(2):73-80.',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=The+wonders+of+2-deoxy-D-glucose'},
    {"n": 49, "section": 'Antimetabolites',
     "citation": 'Evaluation of antibacterial activity of vitamin C against human bacterial pathogens. Braz J Biol. 2021;82:e243836.',
     "url": 'https://pubmed.ncbi.nlm.nih.gov/?term=Evaluation+of+antibacterial+activity+of+vitamin+C+against+human+bacterial+pathogens'},
    {"n": 50, "section": 'Antimetabolites',
     "citation": 'Lankadeva, Y. R. et al. Reversal of the Pathophysiological Responses to Gram-negative Sepsis by Megadose Vitamin C. Critical Care Medicine (2021).',
     "url": 'https://doi.org/10.1097/CCM.0000000000004778'},
    {"n": 51, "section": 'Antimetabolites',
     "citation": 'Amaravadi, R. K., Thomas-Tikhonenko, A., Thompson, C. B. Chloroquine Inhibits Autophagy, Enhances p53-Dependent Apoptosis, and Delays Tumor Recurrence in a Mouse Model of B Cell Lymphoma. Blood (2005).',
     "url": 'https://doi.org/10.1182/blood.V106.11.2421.2421'},
    {"n": 52, "section": 'Antimetabolites',
     "citation": 'Xu, R., Ji, Z., Xu, C., Zhu, J. The clinical value of using chloroquine or hydroxychloroquine as autophagy inhibitors in the treatment of cancers: A systematic review and meta-analysis. Medicine (2018).',
     "url": 'https://doi.org/10.1097/MD.0000000000012912'},
    {"n": 53, "section": 'Antimetabolites',
     "citation": 'Cook, K. L., Wärri, A., Soto-Pantoja, D. R., Clarke, P. A., Cruz, M. I., Zwart, A., Clarke, R. Hydroxychloroquine inhibits autophagy to potentiate antiestrogen responsiveness in ER+ breast cancer. Clin Cancer Res (2014).',
     "url": 'https://doi.org/10.1158/1078-0432.CCR-13-3227'},
    {"n": 54, "section": 'Antimetabolites',
     "citation": 'Chung, C. H., Bhowmick, R., Badenoch, A. J., Arora, H. S., Chandrasekaran, S. Targeting metabolism to combat anticancer and antibacterial drug resistance. Trends in Pharmacological Sciences (2026).',
     "url": 'https://doi.org/10.1016/j.tips.2026.01.013'},
    {"n": 55, "section": 'Antimetabolites',
     "citation": 'Peng, B., Li, H., Peng, X.-X. Metabolic state-driven nutrient-based approach to combat bacterial antibiotic resistance. NPJ Antimicrob Resist (2025).',
     "url": 'https://doi.org/10.1038/s44259-025-00092-5'},
]


# Section ordering for the page
SECTION_ORDER = [
    'Foundational epidemiology',
    'ESKAPEE & dynamic susceptibility',
    'Superbugs (MDR/XDR/PDR)',
    'Bibliometrics & industry',
    'Antimetabolites',
]



def references_by_section():
    """Group references by paper section in canonical order."""
    out = {sec: [] for sec in SECTION_ORDER}
    for ref in REFERENCES:
        out.setdefault(ref["section"], []).append(ref)
    return out


def total_count():
    return len(REFERENCES)


def section_counts():
    out = {sec: 0 for sec in SECTION_ORDER}
    for ref in REFERENCES:
        out[ref["section"]] = out.get(ref["section"], 0) + 1
    return out
