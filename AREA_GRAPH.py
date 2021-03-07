from manim import *
import numpy as np

class Area(Scene):
    def construct(self):

        #Just add always_redraw(lambda : ) to add updaters with valuetrackers on shit....

        plane_config = dict(
            axis_config = { 
                "include_tip": True, "include_numbers" : True,
                "include_ticks" : True, "line_to_number_buff" : 0.05,
                "stroke_color" : WHITE, "stroke_width": 0.5,
                "number_scale_val" : 0.4,
                "tip_scale": 0.5,
            },
            x_axis_config = {
                "exclude_zero_from_default_numbers": True,
                "label_direction" : DOWN, "stroke_color" : WHITE,
                "x_min" : 0, "x_max" : 2, "unit_size": 1, 
                "numbers_to_show": range(0, 3, 1),
            },
            y_axis_config = {
                "exclude_zero_from_default_numbers": True,
                "label_direction" : UR, "stroke_color" : WHITE,
                "x_min" : 0, # not y_min
                "x_max" : 13,  # not y_max
                "unit_size": 4/13, "numbers_to_show": range(0, 11, 2),
                #unit size = 4/13, since 4 manim units up to 13 graph units up
            },
            background_line_style = {
                "stroke_width" : 1, "stroke_opacity" : 0.75,
                "stroke_color" : GREEN_C,
            }  
        )
        plane = NumberPlane(**plane_config)

        # shift origin to desired point
        new_origin = LEFT*6+DOWN*3
        plane.shift(new_origin)

        # rotate y labels
        for label in plane.y_axis.numbers:
            label.rotate(-PI/2)

        k = ValueTracker(0)  #my valuetracker for all my shit

        ##DEFINING MY FUNCTIONS, GRAPHS, TITLES
        graph = plane.get_graph(lambda x : np.pi*x**2, x_min = 0, x_max = 2, color = PINK)
        graph_lab = MathTex("A(r)=\pi{r}^{2}").set_width(1).next_to(graph, UR, buff=0.2)
        deriv = plane.get_graph(lambda x : 2*np.pi*x)

        title = Text("ក្រាបក្រឡាផ្ទៃ", font="Khmer OS Siemreap", color=PINK).scale(0.6).next_to(plane, UP, buff=0.5)
        und = Underline(title)

        #WANT TO PUT SLOPES AND HORIZ LINES ON GRAPH, so define them.
        def get_secant_line(x):
            p1 = plane.input_to_graph_point(x, graph)
            p2 = plane.input_to_graph_point(x+0.1, graph)
            secant = Line(p1, p2, color = RED)
            secant.scale_in_place(1.5 / secant.get_length())
            return secant

        def get_horiz_line(x):
            return DashedLine(
                plane.coords_to_point(0, graph.underlying_function(x)),
                plane.coords_to_point(x, graph.underlying_function(x)),
                color = YELLOW_C)

        def get_dot(x):
            return Dot().move_to(plane.coords_to_point(x, graph.underlying_function(x)))

        #ADDING THE MOBJECTS TO THE SCENE
        secant = always_redraw(lambda : get_secant_line(x = k.get_value()))
        horiz_line = always_redraw(lambda : get_horiz_line(x = k.get_value()))
        dot = always_redraw(lambda : get_dot(x = k.get_value()))

        circ = always_redraw(lambda : 
        Circle(fill_color = PINK, fill_opacity = 0.5,
        stroke_color = RED, stroke_width = 5,
        radius = k.get_value()).move_to(RIGHT*3+UP*1.5))

        radius = Line(circ.get_center(), circ.get_top(), stroke_color = RED)
        radius.add_updater(lambda x : x.become(
            Line(circ.get_center(), circ.get_top(), stroke_color = RED)))
        
        r_tex = MathTex("r").set_color(RED).next_to(radius, RIGHT, buff=0.1)
        r_tex.add_updater(lambda x : x.next_to(radius, RIGHT, buff=0.1))

        #FOR THE BOTTOM RIGHT CORNER, VALUE UPDATERS
        area_text = Text("ក្រឡាផ្ទៃ = ", font="Khmer OS Siemreap", color=GREEN_B).scale(0.7).shift(DOWN*2+RIGHT)
        area_value = DecimalNumber(num_decimal_places = 3).scale(0.7).next_to(area_text, RIGHT
        ).set_color(GREEN_B, BLUE_C)
        area_value.add_updater(lambda x : x.set_value(
            graph.underlying_function(k.get_value())
        ))  #Alternatively, could use always_redraw to the area_value and add in the set_value method

        perim_text = Text("បរិមាត្រ = ", font="Khmer OS Siemreap", color=RED).scale(0.7).next_to(area_text, DOWN, buff=0.75)
        perim_value = DecimalNumber(num_decimal_places = 3).scale(0.7).next_to(perim_text, RIGHT
        ).set_color(RED)
        perim_value.add_updater(lambda x : x.set_value(
            deriv.underlying_function(k.get_value())))
        
        self.play(LaggedStart(Write(plane), Write(title), ShowCreation(und),
        ShowCreation(graph), Write(graph_lab)), run_time=5, lag_ratio = 0.75)
        self.add(circ)
        self.play(Write(area_text), Write(perim_text))
        self.add(area_value, perim_value, secant, horiz_line, circ, radius, r_tex, dot)
        self.play(k.animate.set_value(2), run_time=10)
        self.wait()
        self.play(k.animate.set_value(1.5), run_time=5)
        self.play(k.animate.set_value(0.5), run_time=5)
        self.wait()


