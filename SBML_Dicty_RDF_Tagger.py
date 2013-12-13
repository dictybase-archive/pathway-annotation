from libsbml import *
reader = SBMLReader()
document = reader.readSBMLFromFile('ChemotaxisPathway.xml')
model = document.getModel()

def set_speciesRDF(model):
	for i in range(model.getNumSpecies()):
		species = model.getSpecies(i)
		annotation = species.getAnnotation()
		set_RDF(annotation,species)
		
						
def set_RDF(annotation,node):
	term=CVTerm()
	term.setQualifierType(BIOLOGICAL_QUALIFIER)
	term.setBiologicalQualifierType(BQB_IS)
	DDB_ID=get_DDB_ID(node,mapping_doc)
	Uniprot_ID=get_Uniprot_ID(node,mapping_doc)
	term.addResource('http://identifiers.org/dictybase.gene/'+DDB_ID)
	term.addResource('http://identifiers.org/uniprot/'+Uniprot_ID)
	node.addCVTerm(term)
	CVTerms=RDFAnnotationParser.createCVTerms(node)
	RDF=RDFAnnotationParser.createRDFAnnotation()
	RDF.addChild(CVTerms)
	annotation.addChild(RDF)

def get_DDB_ID(node,filename):
	name=node.getName()
	mapping=read_dataset(filename)
	ID=mapping[mapping.index(name)+1]
	if ID=='NA':
		ID=''
	return ID
	
def get_Uniprot_ID(node,filename):
	name=node.getName()
	mapping=read_dataset(filename)
	ID=mapping[mapping.index(name)+2]
	if ID=='NA':
		ID=''
	return ID

def read_dataset(filename):
	with open(filename) as file:
		return file.read().replace('\r','\n').replace('\n','\t').split('\t')
		
mapping_doc='DictyChemotaxisSemanticMapping.txt'
	
set_speciesRDF(model)
writeSBMLToFile(document, 'ChemotaxisPathway.xml')