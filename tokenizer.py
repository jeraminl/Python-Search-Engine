'''
tokenizer.py

Takes care of filtering the html content for relevant tags and tokenizing them.

this class will use NLTK as a library to help with the tokenizing

'''
import nltk
import json
import os.path
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer as PS
from nltk.corpus import stopwords
import re

class Tokenizer:
    def __init__(self):
        self.cleaner = Cleaner(scripts = True, javascript = True, style = True, \
            meta = True, annoying_tags = True, embedded = True, page_structure = False, \
            kill_tags = ['img', 'CDATA', 'form'], remove_tags = ['a','div'], remove_unknown_tags = True, comments = True)
        self.cleanerBody = Cleaner( page_structure = False, kill_tags = ['h1','h2','h3','h4','h5','h6'])
        self.stopwords = set(stopwords.words('english'))
        self.ps = PS()




    def parseHTML(self, content):

        cleaned = self.cleaner.clean_html(content)

        cleanedBody = self.cleanerBody.clean_html(cleaned)
        #print(cleanedBody)
        soup = BeautifulSoup(cleaned, 'lxml')
        soupBody = BeautifulSoup(cleanedBody,'lxml')
        #print(soup)
        if soup.html != None:
            title = self.getTitle(soup)
            heading = self.getHeadings(soup)
            body = self.getBody(soupBody)
            #print(title)
            #print(heading)
            #print(body)
            return (title, heading, body)


    def getTitle(self, soup):
        try:
            title = soup.title.getText().lower()
            #print(title)
            tokens = RegexpTokenizer(r'[a-z]+').tokenize(title)
            stemmed = [self.ps.stem(t) for t in tokens]
            filtered = [t for t in stemmed if not t in self.stopwords ]
            #print(filtered)
            return filtered
            #print(tokens)
        except AttributeError:
            pass
            #print('No <title> tag in this file')



    def getHeadings(self, soup):
        result = []
        for i in range(1,3):
            try:
                headerList = soup.find_all("h"+str(i))
                for h in headerList:
                    replaced = re.sub('<[/*a-zA-Z0-9]*>', ' ', str(h).lower())
                    #print(replaced)
                    tokens = RegexpTokenizer(r'[a-z]+').tokenize(replaced)
                    stemmed = [self.ps.stem(t) for t in tokens]
                    filtered = [t for t in stemmed if not t in self.stopwords ]
                    result.extend(filtered)
                    #print(filtered)
                    return filtered
            except AttributeError:
                pass


    def getBody(self, soup):
        try:

            replaced = re.sub('<[/*a-zA-Z0-9]*>', ' ', str(soup.body).lower())
            #print(replaced)
            tokens = RegexpTokenizer(r'[a-z]+').tokenize(replaced)
            stemmed = [self.ps.stem(t) for t in tokens]
            filtered = [t for t in stemmed if not t in self.stopwords ]
            #print(filtered)
            return filtered
        except AttributeError:
            pass



'''
below is a test for creating tokens
'''



if __name__ == "__main__":
    t = Tokenizer()
    html = '''
            <html><title>Function GO Term <br> transferase activity  <br> And related genes </title>
            <h2>Function GO Term transferase activity  and related genes </h2><br>Total 510<br>
            Page number 6 * 	<a href="f2_94_5.html"> Previous Page </a> * <a href="f2_94_7.html">Next Page</a><br><br> <a href="f2_94_1.html">1 </a> |  <a href="f2_94_2.html">2 </a> |  <a href="f2_94_3.html">3 </a> |  <a href="f2_94_4.html">4 </a> |  <a href="f2_94_5.html">5 </a> |  <a href="f2_94_6.html">6 </a> |  <a href="f2_94_7.html">7 </a> |  <a href="f2_94_8.html">8 </a> |  <a href="f2_94_9.html">9 </a> |  <a href="f2_94_10.html">10 </a> |  <a href="f2_94_11.html">11 </a> |  <a href="f2_94_12.html">12 </a> |  <a href="f2_94_13.html">13 </a> |  <a href="f2_94_14.html">14 </a> |  <a href="f2_94_15.html">15 </a> |  <a href="f2_94_16.html">16 </a> |  <a href="f2_94_18.html">18</a>
            <hr><table>
            <tr><td>Gene Name</td><td>ORF Name</td><td><b>Function GO Term</b></td><td>Process GO Term</td><td>Component GO Term</td><td>Interacting Genes</td><td>Description</td><td>Gene Product</td><td>Phenotype</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0003661">GCD14</a></td><td>YJL125C</td><td><b>tRNA methyltransferase activity</b></td><td>tRNA methylation</td><td>nucleus</td><td>YER179W	YFL052W	YNL062C	</td><td>General Control Derepression</td><td>subunit of tRNA(1-methyladenosine) methyltransferase, along with Gcd10p</td><td>3-Aminotriazole resistance; unconditional slow growth</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0002691">GCN2</a></td><td>YDR283C</td><td><b>protein kinase activity</b></td><td>protein amino acid phosphorylation*</td><td>cytosolic ribosome (sensu Eukarya)</td><td>YNL213C	YOR308C	YKL173W	YBR055C	YBL074C	YGR091W	YPR178W	YLR409C	</td><td>Derepression of GCN4 expression</td><td>eukaryotic initiation factor 2 alpha (eIF2-alpha) kinase</td><td>Null mutant is viable, unable to grow on medium containing 3-aminotriazole (3-AT), a competitive inh</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0003484">GCN5</a></td><td>YGR252W</td><td><b>histone acetyltransferase activity</b></td><td>histone acetylation*</td><td>SAGA complex</td><td>YOR225W	YDR448W	YPL254W	YDR176W	YOL148C	YBR081C	YHR099W	YMR319C	YMR223W	YHR041C	YNL236W	YCL010C	YGL112C	YBR253W	YDR167W	YPL016W	YOR290C	YBR289W	YHR030C	</td><td>functions in the Ada and SAGA (Spt/Ada) complexes to acetylate nucleosomal histones</td><td>histone acetyltransferase</td><td>Null mutant is viable, sensitive to intra-S-phase DNA damage, and grows poorly on minimal media.</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0006388">GDB1</a></td><td>YPR184W</td><td><b>4-alpha-glucanotransferase activity*</b></td><td>glycogen catabolism</td><td>cellular_component unknown</td><td>YFR017C	YER054C	YJL141C	</td><td>Glycogen debranching enzyme; the enzyme that debranches the glycogen having a glucanotranferase + 1-</td><td></td><td>Null mutant is viable but unable to degrade glycogen.</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0001587">GFA1</a></td><td>YKL104C</td><td><b>glutamine-fructose-6-phosphate transaminase (isomerizing) activity</b></td><td>cell wall chitin biosynthesis</td><td>cellular_component unknown</td><td>YDR127W	YPL111W	YDR062W	YMR308C	YER095W	YBL087C	YHR200W	YDR170C	YLR058C	YKL081W	YBR238C	YNL313C	YDR311W	YPR110C	YBR274W	YBR217W	YKL161C	YDL029W	YGL081W	YGR040W	</td><td>catalyzes first step in hexosamine pathway required for biosynthesis of cell wall precursors</td><td>glucoseamine-6-phosphate synthase|glutamine_fructose-6-phosphate amidotransferase</td><td>Null mutant is viable, glucosamine auxotroph</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0002915">GIN4</a></td><td>YDR507C</td><td><b>protein kinase activity</b></td><td>protein amino acid phosphorylation*</td><td>bud neck</td><td>YJR076C	YHR107C	YKR048C	YCR002C	YLR314C	YAL027W	YMR139W	YBR125C	YNL271C	</td><td>Growth inhibitory gene</td><td>serine/threonine kinase (putative)</td><td>Null mutant is viable, exhibits a mild elongated bud phenotype and some cell clumping</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0001766">GLG1</a></td><td>YKR058W</td><td><b>glycogenin glucosyltransferase activity</b></td><td>glycogen biosynthesis</td><td>cellular_component unknown</td><td></td><td>self-glucosylating initiator of glycogen synthesis; similar to mammalian glycogenin</td><td>glycogen synthesis initiator</td><td>Null mutant is viable; disruption of both GLG1 and GLG2 renders cells unable to synthesize glycogen</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0003673">GLG2</a></td><td>YJL137C</td><td><b>glycogenin glucosyltransferase activity</b></td><td>glycogen biosynthesis</td><td>cellular_component unknown</td><td>YLR258W	YMR212C	YJL137C	YFR015C	</td><td>self-glucosylating initiator of glycogen synthesis; similar to mammalian glycogenin</td><td>glycogen synthesis initiator</td><td>Null mutant is viable; disruption of both GLG2 and GLG2 renders cells unable to synthesize glycogen</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0000545">GLK1</a></td><td>YCL040W</td><td><b>glucokinase activity</b></td><td>carbohydrate metabolism</td><td>cytosol</td><td>YML099C	YCL040W	YDR516C	YBR040W	YNL189W	</td><td>Glucose phosphorylation</td><td>glucokinase</td><td>Null mutant is viable with no discernible difference from wild-type; hxk1, hxk2, glk1 triple null mu</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0001877">GNA1</a></td><td>YFL017C</td><td><b>glucosamine 6-phosphate N-acetyltransferase activity</b></td><td>UDP-N-acetylglucosamine biosynthesis</td><td>cellular_component unknown</td><td>YGL070C	YNL189W	YOL059W	YOR362C	YER102W	YDR429C	YDL071C	YDR070C	</td><td>involved in UDP-N-acetylglucosamine biosynthesis</td><td>glucosamine-phosphate N-acetyltransferase</td><td>Null mutatn is inviable</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0005847">GNT1</a></td><td>YOR320C</td><td><b>acetylglucosaminyltransferase activity</b></td><td>N-linked glycosylation</td><td>Golgi medial cisterna</td><td></td><td>N-acetylglucosaminyltransferase transferase capable of modification of N-linked glycans in the Golgi</td><td>N-acetylglucosaminyltransferase</td><td></td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0006364">GPH1</a></td><td>YPR160W</td><td><b>glycogen phosphorylase activity</b></td><td>glycogen catabolism</td><td>cytoplasm</td><td>YPL204W	YHR196W	YPR111W	YER054C	YML058W	YNL250W	YDL043C	YGR092W	YDR419W	YBR055C	YMR106C	YGL115W	YER133W	YKL166C	YAL017W	</td><td>Releases glucose-1-phosphate from glycogen</td><td>glycogen phosphorylase</td><td>Null mutant is viable; haploid cells contain higher levels of intracellular glycogen</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0002710">GPI11</a></td><td>YDR302W</td><td><b>phosphoethanolamine N-methyltransferase activity</b></td><td>GPI anchor biosynthesis</td><td>endoplasmic reticulum</td><td></td><td>Glycosylphosphatidylinositol (GPI) assembly</td><td></td><td></td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0003954">GPI13</a></td><td>YLL031C</td><td><b>phosphoethanolamine N-methyltransferase activity</b></td><td>GPI anchor biosynthesis</td><td>endoplasmic reticulum</td><td>YHL015W	</td><td>Glycosylphosphatidylinositol (GPI) biosynthesis</td><td></td><td>Null mutant is inviable; Gpi13p-depleted strains accumulate a GPI precursor whose glycan headgroup c</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0001775">GPT2</a></td><td>YKR067W</td><td><b>glycerol-3-phosphate O-acyltransferase activity</b></td><td>phospholipid biosynthesis</td><td>cytoplasm*</td><td>YFR051C	YGL137W	</td><td>Encodes a Glycerol-3-phosphate acyltransferase</td><td></td><td></td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0001911">GSY1</a></td><td>YFR015C</td><td><b>glycogen (starch) synthase activity</b></td><td>glycogen metabolism</td><td>cellular_component unknown</td><td>YDR259C	YLR258W	YOR047C	YFR015C	YJL137C	YHR008C	YER077C	YER133W	YBR160W	YGL081W	</td><td>Highly similar to GSY2. GSY2 is the predominantly expressed glycogen synthase</td><td>glycogen synthase (UDP-glucose-starch glucosyltransferase)</td><td>Null mutant is viable. Mutant lacking both GSY1 and GSY2 is viable but lacks glycogen synthase activ</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0004248">GSY2</a></td><td>YLR258W</td><td><b>glycogen (starch) synthase activity</b></td><td>glycogen metabolism</td><td>cytoplasm</td><td>YLR258W	YIL045W	YLR273C	YFR015C	YJL137C	YJL020C	YER054C	YER177W	YOR026W	YER133W	YBR274W	</td><td>Highly similar to GSY1. GSY2 is the predominantly expressed glycogen synthase. Activity is probably</td><td>glycogen synthase (UDP-glucose-starch glucosyltransferase)</td><td>Null mutant is viable. Mutant lacking both GSY1 and GSY2 is viable but lacks glycogen synthase activ</td></tr><tr bgcolor="#CCFFCC"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0001477">GTT1</a></td><td>YIR038C</td><td><b>glutathione transferase activity</b></td><td>glutathione metabolism</td><td>endoplasmic reticulum</td><td>YIR038C	YLL060C	YCL025C	YDL089W	YDR120C	YDR371W	YEL017W	YER022W	YGL225W	YGR121C	YGR149W	YGR191W	YHR123W	YHR190W	YIL023C	YJL097W	YLR026C	YLR088W	YML048W	YMR119W	YNL234W	YOL065C	YPL020C	</td><td>Glutathione Transferase</td><td>glutathione transferase</td><td>Null mutant is viable, heat shock sensitive at stationary phase</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0003983">GTT2</a></td><td>YLL060C</td><td><b>glutathione transferase activity</b></td><td>glutathione metabolism</td><td>cell</td><td>YIR038C	</td><td>Glutathione Transferase</td><td>glutathione transferase</td><td>Null mutant is viable, heat shock sensitive in stationary phase</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0002862">GUK1</a></td><td>YDR454C</td><td><b>guanylate kinase activity</b></td><td>GMP metabolism</td><td>cellular_component unknown</td><td>YDR262W	</td><td>guanylate kinase</td><td>guanylate kinase</td><td>Null mutant is inviable</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0001024">GUT1</a></td><td>YHL032C</td><td><b>glycerol kinase activity</b></td><td>glycerol metabolism</td><td>cellular_component unknown</td><td>YKR026C	</td><td>Glycerol utilization</td><td>converts glycerol to glycerol-3-phosphate|glyerol kinase</td><td>Null mutant is viable but is unable to grow on glycerol</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0003701">HAL5</a></td><td>YJL165C</td><td><b>protein kinase activity</b></td><td>cation homeostasis</td><td>cellular_component unknown</td><td>YOL103W	</td><td>Protein kinase homolog, mutant is salt and pH sensitive</td><td></td><td></td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0005922">HAT1</a></td><td>YPL001W</td><td><b>H3/H4 histone acetyltransferase activity</b></td><td>chromatin silencing at telomere*</td><td>nucleus*</td><td>YOR361C	YMR309C	YEL056W	YBR079C	YLL022C	YBR009C	YBR272C	YBL023C	YNL230C	YLR103C	</td><td>histone acetyltransferase</td><td>histone acetyltransferase</td><td>Null mutant is viable</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0000782">HAT2</a></td><td>YEL056W</td><td><b>H3/H4 histone acetyltransferase activity</b></td><td>chromatin silencing at telomere*</td><td>nucleus*</td><td>YPL001W	YNL030W	YHR183W	YLL022C	YDR233C	YBR272C	YLR200W	YGR078C	YLR103C	</td><td>subunit of histone acetyltransferase; may regulate activity of Hat1p, the catalytic subunit of histo</td><td>histone acetyltransferase subunit</td><td>Null mutant is viable</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0002640">HEM1</a></td><td>YDR232W</td><td><b>5-aminolevulinate synthase activity</b></td><td>heme biosynthesis</td><td>mitochondrial matrix</td><td></td><td>First enzyme in heme biosynthetic pathway</td><td>5-aminolevulinate synthase</td><td>Null mutant is viable; auxotroph for heme and methionine</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0002364">HEM3</a></td><td>YDL205C</td><td><b>hydroxymethylbilane synthase activity</b></td><td>heme biosynthesis</td><td>cellular_component unknown</td><td></td><td>catalyzes the third step in heme biosynthesis</td><td>phorphobilinogen deaminase (uroporphyrinogen synthase)</td><td>auxotroph for heme and methionine</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0000857">HIS1</a></td><td>YER055C</td><td><b>ATP phosphoribosyltransferase activity</b></td><td>histidine biosynthesis</td><td>cell</td><td></td><td>involved in the first step of histidine biosynthesis</td><td>ATP phosphoribosyltransferase</td><td>Null mutant is viable and requires histidine</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0001378">HIS5</a></td><td>YIL116W</td><td><b>histidinol-phosphate transaminase activity</b></td><td>histidine biosynthesis</td><td>cell</td><td></td><td>responsive to control of general amino acid biosynthesis</td><td>histidinol-phosphate aminotransferase</td><td>Null mutant is viable and requires histidine</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0000452">HIS7</a></td><td>YBR248C</td><td><b>imidazoleglycerol phosphate synthase activity</b></td><td>histidine biosynthesis</td><td>cell</td><td>YOL102C	</td><td>glutamine amidotransferase:cyclase, also called imidazole glycerol phosphate synthase</td><td>glutamine amidotransferase:cyclase|imidazole glycerol phosphate synthase (synonym)</td><td>Null mutant is viable and requires histidine</td></tr><tr bgcolor="whitesmoke"><td><a href="http://db.yeastgenome.org/cgi-bin/SGD/singlepageformat?sgdid=S0000238">HMT1</a></td><td>YBR034C</td><td><b>protein-arginine N-methyltransferase activity</b></td><td>mRNA-nucleus export*</td><td>nucleus</td><td>YDR432W	YMR048W	YGR118W	YDR249C	YER017C	YGR165W	YGR181W	YIL061C	YNL078W	</td><td>hnRNP methyltransferase</td><td>arginine methyltransferase|mono- and asymmetrically dimethylating enzyme</td><td>Null mutant is viable, hmt1 npl3-1 mutants are inviable</td></tr>
        '''

    t.parseHTML(html)
