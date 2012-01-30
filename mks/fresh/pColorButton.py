"""This file has been ported from fresh library by Azevedo Filippe aka PasNox

See information at https://github.com/pasnox/fresh and 
API docks at http://api.monkeystudio.org/fresh/
"""

from PyQt4.QtCore import pyqtSignal, QSize
from PyQt4.QtGui import QColor, QColorDialog, QIcon, QPixmap, QToolButton

def tr(text):
    return text

class pColorButton(QToolButton):
    
    colorChanged = pyqtSignal(QColor)
    
    def __init__(self, colorOrParent, *args):
        if isinstance(colorOrParent, QColor):
            QToolButton.__init__(self, *args)
            self.setColor( colorOrParent )
        else:
            QToolButton.__init__(self, colorOrParent, *args)
            self.setColor(QColor())
        
        self.clicked.connect(self._q_clicked)
        self.setIconSize( QSize( 16, 16 ) )

    def color(self):
        return self._color

    def setColor(self, color ):
        self._color = color
        
        c = self._color
        texts = ["RGBA #%02x%02x%02x%02x" % (c.red(), c.green(), c.blue(), c.alpha()),
                 "RGBA %d, %d, %d, %d" % (c.red(), c.green(), c.blue(), c.alpha())]
            
        self.setText( texts[0] )
        self.setToolTip( '\n'.join(texts))
        
        pixmap = QPixmap(self.iconSize())
        pixmap.fill(self._color)

        self.setIcon( QIcon(pixmap) )
        
        self.colorChanged.emit( self._color )


    def _q_clicked(self):
        color = QColorDialog.getColor( self._color,
                                       self.window(),
                                       tr( "Choose a color" ),
                                       QColorDialog.ShowAlphaChannel)
        
        if  color.isValid():
            self.setColor( color )