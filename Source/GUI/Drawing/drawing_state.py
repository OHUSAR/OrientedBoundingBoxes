class DrawingState:
    FIRST = 1
    SECOND = 2
    DONE = 3

    @staticmethod
    def drawing_color(state):
        return {1: 'salmon3', 2: 'chartreuse2'}[state]