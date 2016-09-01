import nuke
import nukescripts
import nuke.rotopaint as rp

class Tracker2Roto(nukescripts.PythonPanel):
    def __init__(self, src, dst):
        nukescripts.PythonPanel.__init__(self, 'Tracker2Roto')
        self.trNode = src
        self.rpNode = dst
        self.curvesKnob = self.rpNode['curves']
        self.rootLayer = self.rpNode['curves'].rootLayer
        self.layers =  self.getData(self.rootLayer)
        self.layerNames = []
        self.transform = ''

        #set Root first in list
        self.layerNames = self.layers.keys()
        self.layerNames.remove(self.rootLayer.name)
        self.layerNames.insert(0, self.rootLayer.name)

        # Header
        self.headerKnob = nuke.Text_Knob('','', 'Tracker to Roto')
        self.addKnob(self.headerKnob)

        # Divider
        self.dividerKnob = nuke.Text_Knob('')
        self.addKnob(self.dividerKnob)

        # Translate knob
        self.tKnob = nuke.Bitmask_Knob('translate','Translate',['x','y'])
        self.tKnob.setDefaultValue([3])
        self.addKnob(self.tKnob)

        # Rotate knob
        self.rKnob = nuke.Bitmask_Knob('rotate','Rotate',[''])
        self.rKnob.setDefaultValue([1])
        self.addKnob(self.rKnob)

        # Scale knob
        self.sKnob = nuke.Bitmask_Knob('scale','Scale',['w','h'])
        self.sKnob.setDefaultValue([3])
        self.addKnob(self.sKnob)

        # Center knob
        self.cKnob = nuke.Bitmask_Knob('center','Center',['x','y'])
        self.cKnob.setDefaultValue([0])
        self.cKnob.setTooltip('Center of rotation and scaling.')
        self.addKnob(self.cKnob)

        # Divider 2
        self.dividerKnob2 = nuke.Text_Knob('')
        self.addKnob(self.dividerKnob2)

        # Layers enumeration knob
        self.layersKnob = nuke.Enumeration_Knob('layer', 'Layer:', [])
        self.addKnob(self.layersKnob)

        # Divider 3
        self.dividerKnob3 = nuke.Text_Knob('')
        self.addKnob(self.dividerKnob3)

        # Copy link button
        self.linkButton = nuke.PyScript_Knob( "Link")
        self.linkButton.setFlag(nuke.STARTLINE)
        self.addKnob(self.linkButton)

        # Copy values button
        self.copyButton = nuke.PyScript_Knob( "Bake" )
        self.addKnob(self.copyButton)

        # CANCEL
        self.cancelButton = nuke.Script_Knob( "              Close              " )
        self.cancelButton.setFlag(nuke.STARTLINE)
        self.addKnob(self.cancelButton)

        # Hide OK button
        self.okButton = nuke.Script_Knob( "OK" )
        self.okButton.setFlag(nuke.INVISIBLE)

    def link(self):
        """Link values from tracker node to rotopaint."""

        # Link to Translate knob
        if self.tKnob.value():
            a = rp.AnimCurve()
            parentName = self.trNode.knob('translate').fullyQualifiedName()
            value = self.tKnob.value()
            if value == 'x' or value == 'all':    # x                
                a.expressionString = 'parent.%s.%s' % (parentName, 'x')
                a.useExpression = True
                self.transform.setTranslationAnimCurve(0 ,a)
            if value == 'y' or value == 'all':    # y
                a.expressionString = 'parent.%s.%s' % (parentName, 'y')
                a.useExpression = True
                self.transform.setTranslationAnimCurve(1 ,a)

        # Link to Rotate knob
        if self.rKnob.value():
            a = rp.AnimCurve()
            parentName = self.trNode.knob('rotate').fullyQualifiedName()      
            a.expressionString = 'parent.%s' % (parentName)
            a.useExpression = True
            self.transform.setRotationAnimCurve(2 ,a)

        # Link to Scale knob
        if self.sKnob.value():
            a = rp.AnimCurve()
            parentName = self.trNode.knob('scale').fullyQualifiedName()
            value = self.sKnob.value()
            if value == 'w' or value == 'all':    # w             
                a.expressionString = 'parent.%s.%s' % (parentName, 'w')
                a.useExpression = True
                self.transform.setScaleAnimCurve(0 ,a)
            if value == 'h' or value == 'all':    # h
                a.expressionString = 'parent.%s.%s' % (parentName, 'h')
                a.useExpression = True
                self.transform.setScaleAnimCurve(1 ,a)

        # Link to Center knob
        if self.cKnob.value():
            a = rp.AnimCurve()
            parentName = self.trNode.knob('center').fullyQualifiedName()
            value = self.cKnob.value()
            if value == 'x' or value == 'all':    # x              
                a.expressionString = 'parent.%s.%s' % (parentName, 'x')
                a.useExpression = True
                self.transform.setPivotPointAnimCurve(0 ,a)
            if value == 'y' or value == 'all':    # y
                a.expressionString = 'parent.%s.%s' % (parentName, 'y')
                a.useExpression = True
                self.transform.setPivotPointAnimCurve(1 ,a)

    def copyValue(self):
        """Copy values from tracker node to rotopaint."""

        # Values to Translate knob
        if self.tKnob.value():
            value = self.tKnob.value()
            knobName = 'translate'
            knob = self.trNode[knobName]
            if value == 'x' or value == 'all':  
                    if knob.isAnimated(0):
                        a = self.copyAnim(knobName,'x')
                    else:                                     # Is constant
                        a = rp.AnimCurve()
                        a.constantValue = knob.x()
                    self.transform.setTranslationAnimCurve(0, a)
            if value == 'y' or value == 'all': 
                    if knob.isAnimated(1):
                        a = self.copyAnim(knobName,'y')
                    else:                                     # Is constant
                        a = rp.AnimCurve()
                        a.constantValue = knob.y()
                    self.transform.setTranslationAnimCurve(1, a)

        # Values to Rotate knob
        if self.rKnob.value():
            knobName = 'rotate'
            knob = self.trNode[knobName]
            if knob.isAnimated():
                a = self.copyAnim(knobName,'x')
            else:                                     # Is constant
                a = rp.AnimCurve()
                a.constantValue = knob.value()
            self.transform.setRotationAnimCurve(2, a)

        # Values to Scale knob
        if self.sKnob.value():
            value = self.sKnob.value()
            knobName = 'scale'
            knob = self.trNode[knobName]
            if value == 'w' or value == 'all':  
                if knob.isAnimated(0):
                    a = self.copyAnim(knobName,'x')
                else:
                    a = rp.AnimCurve()
                    a.constantValue = knob.x()
                self.transform.setScaleAnimCurve(0, a)
            if value == 'h' or value == 'all':  
                if knob.isAnimated(1):
                    a = self.copyAnim(knobName,'y')
                else:
                    a = rp.AnimCurve()
                    a.constantValue = knob.y()
                self.transform.setScaleAnimCurve(1, a)
        
        # Values to Center knob
        if self.cKnob.value():
            value = self.cKnob.value()
            knobName = 'center'
            knob = self.trNode[knobName]
            if value == 'x' or value == 'all':  
                if knob.isAnimated(0):
                    a = self.copyAnim(knobName,'x')
                else:
                    a = rp.AnimCurve()
                    a.constantValue = knob.x()
                self.transform.setPivotPointAnimCurve(0, a)
            if value == 'y' or value == 'all':
                if knob.isAnimated(1): 
                    a = self.copyAnim(knobName,'y')
                else:
                    a = rp.AnimCurve()
                    a.constantValue = knob.y()
                self.transform.setPivotPointAnimCurve(1, a)

    def copyAnim(self, knob, axis):
        """Copy animation from knob. Return animation curve.

        Arguments:
        knob -- tracker knob ('translate', 'rotate', etc...) 
        axis -- coordinate axis ('x', 'y')."""

        a = rp.AnimCurve()
        if not self.trNode[knob].hasExpression():
            if axis == 'x':  
                animCurve = self.trNode[knob].animation(0)       
            elif axis == 'y':
                if len(self.trNode[knob].animations()) > 1:
                    animCurve = self.trNode[knob].animation(1)
                if len(self.trNode[knob].animations()) == 1:
                    animCurve = self.trNode[knob].animation(0)
            first, last = animCurve.knob().getKeyList()[0], animCurve.knob().getKeyList()[-1]
        
            for frame in range(first, last+1):
                a.addKey(frame, animCurve.evaluate(frame))
        else:
            nuke.message("Knob '%s' has expression. Use 'copy link' instead 'bake values'" % (knob))
        return a

    
    def getLayers(self, layer, hashTable):
        if isinstance(layer, rp.Layer):
            for element in layer:
                hashTable[element.name] = element
                self.getLayers(element, hashTable)

    def getData(self, root):
        """Get layers and shapes from roto/rotopaint node. Return dictionary {'name':object}.

        args -- root layer in roto/rotopaint node"""
        layers = {root.name : root}
        self.getLayers(root, layers)
        return layers

    def knobChanged( self, knob ):
        self.layersKnob.setValues(self.layerNames)
        self.transform = self.layers[self.layersKnob.value()].getTransform()

        if knob == self.linkButton :  
            self.link()
            self.hide()
        elif knob == self.copyButton :
            try:
                self.copyValue()
            except AttributeError as er:
                pass
            self.hide()


def select(classes):
    """Return list of nodes"""
    return sum([nuke.selectedNodes(x) for x in classes], [])


def tracker2Roto():
    src = select(['Tracker3', 'Tracker4'])
    dst = select(['RotoPaint', 'Roto'])
    if len(dst) != 1 or len(src) != 1:
        nuke.message("Please select two nodes: Tracker, Roto|RotoPaint.")
    else:
        p = Tracker2Roto(src[0], dst[0])
        p.showModalDialog()
        dst[0]['curves'].changed()
