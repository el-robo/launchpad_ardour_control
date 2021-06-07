from button import Button
import midi_device as midi

color_degen = {
    midi.color.red_full: midi.color.red_low,
    midi.color.red_low: midi.color.off,
    midi.color.amber_full: midi.color.amber_low,
    midi.color.amber_low: midi.color.off,
    midi.color.green_full: midi.color.green_low,
    midi.color.green_low: midi.color.off
}

class State:
    width = 8
    height = 8
            
    def __init__( self ):
        self.buttons = [ midi.color.off for i in range( Button.max_x * Button.max_y ) ]

    def iterate_buttons( self ):
        for y in range( Button.max_y ):
            for x in range( Button.max_x ):
                yield Button(x,y)
    
    def value( self, button ):
        return self.buttons[ button.y * Button.max_x + button.x ]

    def set( self, button, value ):
        if button.in_range():
            self.buttons[ button.y * Button.max_x + button.x ] = value

    def fill( self, color ):
        for button in self.iterate_buttons():
            self.set( button, color )

    def diff( self, state ):
        changed = []
        
        for button in self.iterate_buttons():
            if self.value(button) != state.value(button):
                changed.append(button)

        return changed

    def merge( self, state ): # TODO: this doesn't work

        for button in self.iterate_buttons():
            value = state.value( button )

            if value is not midi.color.off:
                self.set( button, value )
                continue

            # own_value = self.value( button )

            # if own_value:

    def apply( self, state ):
        changed = self.diff( state )

        for button in changed:
            value = state.value( button )
            midi.set_led( button.x, button.y, value )

        if len( changed ):
            self.buttons = [ value for value in state.buttons ]
