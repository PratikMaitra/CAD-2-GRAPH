control+shift+m to preview on Atom
#### extract_graph_from_dxf

##### definitions
* CAD file: Computer-aided design file. 2D CAD files are referred to as drawings.
* DXF: AutoCAD DXF is a CAD data file format.
* SVG: Scalable Vector Graphics is an XML-based vector image format for two-dimensional graphics
* XML: a markup language similar to HTML, but without predefined tags to use
* YAML: YAML Ain't Markup Language (YAML) is a serialization language. Key-Value Pairs and Dictionaries

##### questions
* how to read svg file as a graph object in networkx? first convert it to GML format?
* what is a dxf file with walls and doors?
* what is a dxf file with label information?
* there is no return statement in the function. YAML file is saved instead.

##### purpose
* Converts an architecture CAD file in .dxf format into a graph object and save as SVG format

##### input
* dxf file name
* Name of the dxf file with label information
* Name of the output svg file

##### output
* a graph representation of the CAD file

===========================================================

#### dx.readfile("path to .dxf file")

##### input
* path to .dxf files

##### output
* ezdxf.drawing.Drawing object

==========================================================

#### dxf_reader.hospital_dxf.DXF

##### purpose
* define and generate DXF class and object

##### DXF object

###### input
* floor_architecture : Drawing
* floor_labels : Drawing
* step_size : int or None

###### instance vars
* floor_architecture
* floor_labels
* step_size
* offsets = [canvas_width_min-100, canvas_length_min-100]
* new_canvas_dimensions = [canvas_limits[0]-self.offsets[0],canvas_limits[1]-self.offsets[1]]
* walls (sharp object)?
* doors (sharp object)?
* room_labels (?)

###### local vars of constructor
* canvas_limits
* offsets
* they are returned by get_canvas_size()

==================================================

#### dxf_reader.hospital_dxf.get_canvas_size

##### purpose
?

##### input
* drawing: Drawing
* relevant_layers: List[str]

##### output
* canvas_limits, offsets :Tuple[List[int], List[int]]


===================================================

#### dxf_reader.dxf_to_shapely_objects. get_shapely_objects_from_relevant_layers

##### purpose
* 
