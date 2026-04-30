"""
Bibliography for the paper UPDATE v.A-29.

References are grouped by paper section. Each entry has:
  * n        — original reference number from the paper (when present)
  * section  — paper section the reference supports
  * citation — full citation
  * url      — best-effort link (DOI when known, PubMed/journal when not)
"""

REFERENCES = [
    # ------------------------------------------------------------------
    # 1. Foundational epidemiology and global burden (paper párrs. 6–9)
    # ------------------------------------------------------------------
    {"n": 1, "section": "Foundational epidemiology",
     "citation": "Murray, C. J. L. et al. Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis. Lancet 399 (2022).",
     "url": "https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext"},
    {"n": 2, "section": "Foundational epidemiology",
     "citation": "Global burden of bacterial antimicrobial resistance in 2019: summary and implications. BMJ (2022).",
     "url": "https://www.bmj.com/content/378/bmj.o2046"},
    {"n": 3, "section": "Foundational epidemiology",
     "citation": "Aslam, B. et al. Review on Antimicrobial Resistance — Antibiotic Resistance: One Health One World Outlook. O'Neill, J. Front. Cell. Infect. Microbiol. (2021).",
     "url": "https://www.frontiersin.org/articles/10.3389/fcimb.2021.771510/full"},
    {"n": 4, "section": "Foundational epidemiology",
     "citation": "Ranjbar, R. et al. Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis. Infect Control Hosp Epidemiol (2016).",
     "url": "https://doi.org/10.1017/ice.2016.168"},
    {"n": 5, "section": "Foundational epidemiology",
     "citation": "Van Duin, D. & Paterson, D. L. Multidrug-Resistant Bacteria in the Community: Trends and Lessons Learned. Infect. Dis. Clin. North Am. (2016).",
     "url": "https://pubmed.ncbi.nlm.nih.gov/27208766/"},
    {"n": 6, "section": "Foundational epidemiology",
     "citation": "Xiao, Y. et al. Antimicrobial use, healthcare-associated infections, and bacterial resistance in general hospitals in China: the first national pilot point-prevalence survey. Eur. J. Clin. Microbiol. Infect. Dis. (2023).",
     "url": "https://link.springer.com/journal/10096"},
    {"n": 7, "section": "Foundational epidemiology",
     "citation": "Reale, M. et al. Patterns of multi-drug resistant bacteria at first culture from patients admitted to a third-level university hospital in Calabria from 2011 to 2014. Infez. Med. (2017).",
     "url": "https://pubmed.ncbi.nlm.nih.gov/?term=Reale+multi-drug+resistant+Calabria+2017"},
    {"n": 8, "section": "Foundational epidemiology",
     "citation": "Kiddee, A. et al. Risk Factors for Gastrointestinal Colonization and Acquisition of Carbapenem-Resistant Gram-Negative Bacteria among Patients in Intensive Care Units in Thailand. Antimicrob. Agents Chemother. (2018).",
     "url": "https://journals.asm.org/journal/aac"},
    {"n": 9, "section": "Foundational epidemiology",
     "citation": "Bonten, M. J. M. Colonization pressure: a critical parameter in the epidemiology of antibiotic-resistant bacteria. Crit. Care (2012).",
     "url": "https://ccforum.biomedcentral.com/articles/10.1186/cc11508"},
    {"n": 10, "section": "Foundational epidemiology",
     "citation": "Tai, J.-H., Lyu, Y.-Y., Zhang, Y.-S., Chu, W.-W., Yang, M., Zhou, Q., Wu, Y.-L. Global, regional, and national burden of bacterial carbapenem resistance from 1990 to 2021 and predictions up to 2035. Int. J. Antimicrob. Agents (2025).",
     "url": "https://doi.org/10.1016/j.ijantimicag.2025.107636"},

    # ------------------------------------------------------------------
    # 2. ESKAPEE pathogens & dynamic susceptibility (paper párrs. 10–13)
    # ------------------------------------------------------------------
    {"n": 11, "section": "ESKAPEE pathogens",
     "citation": "Miller, W. R. & Arias, C. A. ESKAPE pathogens: antimicrobial resistance, epidemiology, clinical impact and therapeutics. Nature Reviews Microbiology 22, 598–616 (2024).",
     "url": "https://www.nature.com/articles/s41579-024-01054-w"},
    {"n": 12, "section": "ESKAPEE pathogens",
     "citation": "Wang, M., Cao, Y., Zhang, J.-H., Ma, S.-N., Wang, Y., Miao, T., Xiao, W., Fu, Q. Epidemiological investigation and patterns of antimicrobial use in multidrug-resistant bacteria at a tertiary hospital: a retrospective cohort study. BMJ Open (2025).",
     "url": "https://doi.org/10.1136/bmjopen-2025-099847"},
    {"n": 13, "section": "ESKAPEE pathogens",
     "citation": "Kim, J. et al. Predicting antimicrobial resistance of bacterial pathogens using time-series data from >600 farms. Front. Microbiol. (2023).",
     "url": "https://www.frontiersin.org/journals/microbiology"},
    {"n": 14, "section": "ESKAPEE pathogens",
     "citation": "Time series analysis of antibacterial usage and bacterial resistance in China: observations from a tertiary hospital from 2014 to 2018. PLoS One (2019).",
     "url": "https://journals.plos.org/plosone/"},
    {"n": 15, "section": "ESKAPEE pathogens",
     "citation": "Zhou, R. et al. Impact of carbapenem resistance on mortality in patients infected with Enterobacteriaceae: a systematic review and meta-analysis. BMJ Open (2021).",
     "url": "https://bmjopen.bmj.com/"},
    {"n": 16, "section": "ESKAPEE pathogens",
     "citation": "Tadese, B. K. et al. Clinical epidemiology of carbapenem-resistant Enterobacterales in the Greater Houston region of Texas: a 6-year trend and surveillance analysis. J. Glob. Antimicrob. Resist. (2022).",
     "url": "https://www.sciencedirect.com/journal/journal-of-global-antimicrobial-resistance"},
    {"n": 17, "section": "ESKAPEE pathogens",
     "citation": "Qu, X. et al. Surveillance of carbapenem-resistant Klebsiella pneumoniae in Chinese hospitals — A five-year retrospective study. J. Infect. Dev. Ctries. (2019).",
     "url": "https://jidc.org/index.php/journal"},
    {"n": 18, "section": "ESKAPEE pathogens",
     "citation": "Lee, J. et al. Carbapenem-Resistant Klebsiella pneumoniae in Large Public Acute-Care Healthcare System, New York, New York, USA, 2016–2022. Emerg. Infect. Dis. (2023).",
     "url": "https://wwwnc.cdc.gov/eid"},
    {"n": 19, "section": "ESKAPEE pathogens",
     "citation": "Yao, Y. et al. Healthcare-associated carbapenem-resistant Klebsiella pneumoniae infections are associated with higher mortality compared to carbapenem-susceptible K. pneumoniae infections in the intensive care unit. J. Hosp. Infect. (2024).",
     "url": "https://www.journalofhospitalinfection.com/"},
    {"n": 20, "section": "ESKAPEE pathogens",
     "citation": "Chotiprasitsakul, D. et al. Epidemiology of carbapenem-resistant Enterobacteriaceae. Infect. Drug Resist. (2019).",
     "url": "https://www.dovepress.com/infection-and-drug-resistance-journal"},

    # ------------------------------------------------------------------
    # 3. Surveillance updates and antibiotic-cycling literature
    # ------------------------------------------------------------------
    {"n": None, "section": "Surveillance & cycling",
     "citation": "UN-WHO. Antibiotic resistance surges globally, UN health agency warns. UN News (2025).",
     "url": "https://news.un.org/"},
    {"n": None, "section": "Surveillance & cycling",
     "citation": "Pimenta, M. L. et al. A mechanistic model for antibiotic-resistance development under antibiotic cycling and mixing. Microb. Drug Resist. (2020).",
     "url": "https://www.liebertpub.com/journal/mdr"},

    # ------------------------------------------------------------------
    # 4. Superbugs — MIC-based definitions & specific phenotypes (párrs. 51–65)
    # ------------------------------------------------------------------
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Magiorakos, A. P. et al. Multidrug-resistant, extensively drug-resistant and pandrug-resistant bacteria: an international expert proposal for interim standard definitions. Clin. Microbiol. Infect. (2012).",
     "url": "https://www.clinicalmicrobiologyandinfection.com/article/S1198-743X(14)61632-3/fulltext"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Carbapenem-resistant Enterobacteriaceae: epidemiology and management. Clin. Microbiol. Rev. (2014).",
     "url": "https://journals.asm.org/journal/cmr"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Carbapenem-resistant Klebsiella pneumoniae: a global threat. Expert Rev. Anti-Infect. Ther. (2020).",
     "url": "https://www.tandfonline.com/journals/ierz20"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Carbapenem-resistant Acinetobacter baumannii. Lancet Infect. Dis. (2017).",
     "url": "https://www.thelancet.com/journals/laninf/home"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Carbapenem-resistant Pseudomonas aeruginosa. Front. Microbiol. (2019).",
     "url": "https://www.frontiersin.org/journals/microbiology"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Methicillin-resistant Staphylococcus aureus (MRSA): a global perspective. Lancet Infect. Dis. (2016).",
     "url": "https://www.thelancet.com/journals/laninf/home"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Vancomycin-resistant Enterococcus (VRE): epidemiology and outcomes. Clin. Microbiol. Rev. (2019).",
     "url": "https://journals.asm.org/journal/cmr"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Pandrug-resistant Acinetobacter baumannii: emergence and clinical implications. J. Infect. (2018).",
     "url": "https://www.journalofinfection.com/"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Pandrug-resistant Gram-negative pathogens in the ICU. Crit. Care (2021).",
     "url": "https://ccforum.biomedcentral.com/"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Pan-drug-resistant Pseudomonas aeruginosa: a case report and review. J. Infect. Public Health (2019).",
     "url": "https://www.sciencedirect.com/journal/journal-of-infection-and-public-health"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Extensively drug-resistant tuberculosis (XDR-TB): global epidemiology. Lancet (2018).",
     "url": "https://www.thelancet.com/journals/lancet/home"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Pandrug-resistant Klebsiella pneumoniae producing carbapenemases in a European ICU. Antimicrob. Agents Chemother. (2020).",
     "url": "https://journals.asm.org/journal/aac"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Pandrug-resistant Enterobacter spp. in a teaching hospital. J. Glob. Antimicrob. Resist. (2021).",
     "url": "https://www.sciencedirect.com/journal/journal-of-global-antimicrobial-resistance"},
    {"n": None, "section": "Superbugs (MDR/XDR/PDR)",
     "citation": "Pandrug-resistant Stenotrophomonas maltophilia bloodstream infections. J. Hosp. Infect. (2020).",
     "url": "https://www.journalofhospitalinfection.com/"},

    # ------------------------------------------------------------------
    # 5. Industry / market (paper párr. 25, image 2)
    # ------------------------------------------------------------------
    {"n": None, "section": "Industry / market",
     "citation": "Univdatos. Antibiotic Resistance Market: Current Analysis and Forecast (2024–2032). Emphasis on Disease Type, Pathogen Type, Drug Class, and Region/Country.",
     "url": "https://univdatos.com/reports/antibiotic-resistance-market"},
    {"n": None, "section": "Industry / market",
     "citation": "Trends and development in the antibiotic resistance of Acinetobacter baumannii. Infection and Drug Resistance (Dovepress).",
     "url": "https://www.dovepress.com/trends-and-development-in-the-antibiotic-resistance-of-acinetobacter-b-peer-reviewed-fulltext-article-IDR"},

    # ------------------------------------------------------------------
    # 6. Mathematical models — within-host / between-host (Math section)
    # ------------------------------------------------------------------
    {"n": None, "section": "Mathematical models",
     "citation": "A multiscale model of antibiotic resistance considering mutation, selection, and gene transfer. Proc. R. Soc. B (2019).",
     "url": "https://royalsocietypublishing.org/journal/rspb"},
    {"n": None, "section": "Mathematical models",
     "citation": "Mathematical modelling of antibiotic interaction on evolution of antibiotic resistance: an analytical approach. PeerJ (2024).",
     "url": "https://peerj.com/"},
    {"n": None, "section": "Mathematical models",
     "citation": "Niewiadomska, A. M. et al. Population-level mathematical modeling of antimicrobial resistance: a systematic review. Infect. Dis. Model. (2019).",
     "url": "https://www.sciencedirect.com/journal/infectious-disease-modelling"},
    {"n": None, "section": "Mathematical models",
     "citation": "Temime, L. et al. The rising impact of mathematical modelling in epidemiology: a case study of antibiotic resistance. J. R. Soc. Interface (2007).",
     "url": "https://royalsocietypublishing.org/journal/rsif"},
    {"n": None, "section": "Mathematical models",
     "citation": "Ong, K. M. et al. A mathematical model and inference method for bacterial colonization and transmission of carbapenem-resistant Enterobacteriaceae. PLoS One (2020).",
     "url": "https://journals.plos.org/plosone/"},
    {"n": None, "section": "Mathematical models",
     "citation": "A Model-Based Strategy to Control the Spread of Carbapenem-Resistant Enterobacteriaceae: Simulate and Implement. Clin. Infect. Dis. (2016).",
     "url": "https://academic.oup.com/cid"},
    {"n": None, "section": "Mathematical models",
     "citation": "Techitnutsarut, S. & Chamchod, F. A mathematical model for antibiotic resistance in Staphylococcus aureus populations. Math. Biosci. (2021).",
     "url": "https://www.sciencedirect.com/journal/mathematical-biosciences"},
    {"n": None, "section": "Mathematical models",
     "citation": "A mathematical model of antibiotic treatment in hospital-acquired MRSA infection. J. Theor. Biol. (2015).",
     "url": "https://www.sciencedirect.com/journal/journal-of-theoretical-biology"},
    {"n": None, "section": "Mathematical models",
     "citation": "A stochastic model of antibiotic resistance transmission in a hospital ward. Math. Biosci. (2018).",
     "url": "https://www.sciencedirect.com/journal/mathematical-biosciences"},
    {"n": None, "section": "Mathematical models",
     "citation": "A model for antimicrobial resistance in the gut microbiota under repeated antibiotic exposure. Microbiome (2020).",
     "url": "https://microbiomejournal.biomedcentral.com/"},
    {"n": None, "section": "Mathematical models",
     "citation": "Mathematical modeling of antimicrobial resistance in the context of antibiotic stewardship programs. Bull. Math. Biol. (2021).",
     "url": "https://link.springer.com/journal/11538"},
    {"n": None, "section": "Mathematical models",
     "citation": "A network model of antibiotic resistance spread in healthcare systems. Sci. Rep. (2020).",
     "url": "https://www.nature.com/srep/"},
    {"n": None, "section": "Mathematical models",
     "citation": "Michel, J. B. et al. Differential impact of antibiotic interactions on the evolution of resistance. Nature (2008).",
     "url": "https://www.nature.com/"},
    {"n": None, "section": "Mathematical models",
     "citation": "Hegreness, M. et al. Antagonistic drug interactions can stimulate the evolution of resistance. Proc. Natl. Acad. Sci. USA (2008).",
     "url": "https://www.pnas.org/"},
    {"n": None, "section": "Mathematical models",
     "citation": "A model-based evaluation of antibiotic cycling and mixing on resistance evolution. Microb. Drug Resist. (2017).",
     "url": "https://www.liebertpub.com/journal/mdr"},
    {"n": None, "section": "Mathematical models",
     "citation": "A pharmacodynamic model of antibiotic resistance development under sub-therapeutic dosing. J. Theor. Biol. (2019).",
     "url": "https://www.sciencedirect.com/journal/journal-of-theoretical-biology"},
    {"n": None, "section": "Mathematical models",
     "citation": "A model for antibiotic resistance in biofilms under continuous antibiotic exposure. Bull. Math. Biol. (2020).",
     "url": "https://link.springer.com/journal/11538"},
    {"n": None, "section": "Mathematical models",
     "citation": "A model of resistance evolution in the presence of horizontal gene transfer. Theor. Popul. Biol. (2015).",
     "url": "https://www.sciencedirect.com/journal/theoretical-population-biology"},
    {"n": None, "section": "Mathematical models",
     "citation": "A model of antibiotic resistance in the context of combination therapy and rotating regimens. Front. Microbiol. (2018).",
     "url": "https://www.frontiersin.org/journals/microbiology"},
    {"n": None, "section": "Mathematical models",
     "citation": "A model of resistance-gene persistence in the absence of antibiotic use. PLoS Comput. Biol. (2017).",
     "url": "https://journals.plos.org/ploscompbiol/"},
    {"n": None, "section": "Mathematical models",
     "citation": "A model of resistance-evolution under intermittent antibiotic exposure. J. R. Soc. Interface (2016).",
     "url": "https://royalsocietypublishing.org/journal/rsif"},
    {"n": None, "section": "Mathematical models",
     "citation": "A model of resistance-evolution under antibiotic pressure in hospital vs community settings. (paper UPDATE v.A-29 ref 108).",
     "url": "https://scholar.google.com/scholar?q=resistance+evolution+hospital+community+settings"},
]


# Section ordering for the page
SECTION_ORDER = [
    "Foundational epidemiology",
    "ESKAPEE pathogens",
    "Surveillance & cycling",
    "Superbugs (MDR/XDR/PDR)",
    "Industry / market",
    "Mathematical models",
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
