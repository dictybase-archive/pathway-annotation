from libsbml import *
reader = SBMLReader()
document = reader.readSBMLFromFile('CMP_7918.xml')
model = document.getModel()

def set_species(model):
	for i in range(model.getNumSpecies()):
		species = model.getSpecies(i)
		annotation = species.getAnnotation()
		map_species_name(species,annotation)
	
def set_metaID(document,model):
	metaIdZfill=7
	document.setMetaId('metaid_'+'1'.zfill(metaIdZfill))
	model.setMetaId('metaid_'+'2'.zfill(metaIdZfill))
	numCompartments=model.getNumCompartments()
	for g in range(numCompartments):
		compartment = model.getCompartment(g)
		compartment.setMetaId('metaid_'+str(g+3).zfill(metaIdZfill))
	numSpecies=model.getNumSpecies()
	for h in range(numSpecies):
		species = model.getSpecies(h)
		species.setMetaId('metaid_'+str(h+3+numCompartments).zfill(metaIdZfill))
	for i in range(model.getNumReactions()):
		reaction = model.getReaction(i)
		reaction.setMetaId('metaid_'+str(i+3+numCompartments+numSpecies).zfill(metaIdZfill))
	
def map_species_name(species,annotation):
	annotationString = species.getAnnotationString()
	abbrevStart = annotationString.find('abbreviation="') + len('abbreviation="')
	abbrevEnd = annotationString.find('"', abbrevStart)
	Species.setName(species, annotationString[abbrevStart:abbrevEnd])
		
def set_reactions(model):
	for i in range(model.getNumReactions()):
		r = model.getReaction(i)
		annotation = r.getAnnotationString()
		signStart = annotation.find('sign="') + len('sign="')
		signEnd = annotation.find('"', signStart)
		Reaction.setName(r, annotation[signStart:signEnd])

def convert_L3v1(document):
	convertObj = SBMLLevelVersionConverter()
	propsObj = SBMLConverter.getDefaultProperties(convertObj)
	SBMLConverter.setDocument(convertObj, document)
	SBMLConverter.setProperties(convertObj, propsObj)
	SBMLConverter.convert(convertObj)

def get_Version(document):
	print(document.getLevel())
	print(document.getVersion())
	
set_species(model)
set_reactions(model)
set_metaID(document,model)
convert_L3v1(document)
writeSBMLToFile(document, 'ChemotaxisPathway.xml')