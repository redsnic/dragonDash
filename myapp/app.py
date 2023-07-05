import matplotlib.pyplot as plt
import numpy as np
from shiny import ui, render, App, reactive
from shiny.types import ImgData

# Create some random data
t = np.linspace(0, 2 * np.pi, 1024)
data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]

app_ui = ui.page_fixed(
    ui.HTML('<img src="https://ethz.ch/staffnet/de/service/kommunikation/corporate-design/logo/_jcr_content/par/image_65377674/image.imageformat.1286.403278616.png" alt="ETH logo", height="50px">'),
    ui.HTML('<hr>'),
    ui.h1("How to pimp your dragon"),
    ui.HTML('<hr>'),
    ui.markdown("""
        Use this interface to tune the environment of your dragon. When you are done press the 'Generate' button to see what happens!

        This is a list 
        * a 
        * b 
        * c 
        * d
    """),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_radio_buttons("env", "Target environment",
                dict(forest="forest", ocean="ocean", volcano="volcano", desert='desert')
            ),
            ui.input_radio_buttons("subtype", "Target subtype",
                dict(forest="feathered", ocean="scaled")
            ),
            ui.input_slider("f_hot", "F-hot", 0, 1, value=0, step=0.01),
            ui.input_slider("humidity", "Humidity exposure", 0, 1, value=0, step=0.01),
            ui.input_slider("thermocline", "Thermocline", 0, 1, value=0, step=0.01),
            ui.input_slider("diet", "Diet", 0, 1, value=0, step=0.01),
            ui.input_slider("sunscreen", "Light exposure", 0, 1, value=0, step=0.01),
            ui.input_action_button("run", "Compute dynamics"),
            ui.HTML('<hr>'),
            ui.input_action_button("show", "Show dragon", class_="btn-primary"),
            
        ),
        ui.panel_main(
            #ui.HTML('<h3>System\' dynamics</h3>'),
            ui.output_plot("plot", height = '100%'),
            #ui.HTML('<hr>'),
            #ui.output_ui("dragon_image"),
            #ui.output_ui("open_dialog")
        )
    ),
    ui.HTML('<hr>'),
    ui.HTML('Scientifica 2023 - CTSB group, D-BSSE'),
    ui.HTML('<br>'),
    ui.HTML('<br>')
)


   


def server(input, output, session):


    @output
    @render.plot
    @reactive.event(input.subtype, input.run, input.env, ignore_none=True)
    def plot():
        # extra
        import numpy as np
        import matplotlib.pyplot as plt

        # general Euler method implementation
        def euler_np(x_0, derivative, step, finalTime):
            x = x_0
            while finalTime > 0:
                x = x + step*derivative(x) # single step
                finalTime -= step
            return x

        def euler_step(x, derivative, step_size):
            return x + step_size*derivative(x) # single step

        I = {
            "red" : 0,
            "yellow" : 1,
            "blue" : 2,
            "green" : 3,
            "fur" : 4,
            "feathers" : 5,
            "scales" : 6
        }

        # TODO decide many setpoints...
        setpoints = {
            "red" : (0.3, 0.4),
            "yellow" : (0.2, 0.5),
            "blue" : (0.15, 0.18),
            "green" : (0.5, 0.3),
            "fur" : (0.1, 0.2),
            "feathers" : (0.3, 0.4),
            "scales" : (0.12, 0.2),
        }

        colors = {
            "red" : "C0",
            "yellow" : "C1",
            "blue" : "C2",
            "green" : "C3",
            "fur" : "C0",
            "feathers" : "C1",
            "scales" : "C2"
        }


        delta = 1 
        kappa = 0.3
        k1 = 1
        k2 = 1

        def system(x):
            y = np.zeros_like(x)
            # y = x
            y[I["red"]] = input.f_hot() - delta*x[I["red"]]
            y[I["yellow"]] = input.thermocline() - delta*x[I["yellow"]] - x[I["yellow"]] * x[I["blue"]]
            y[I["blue"]] = input.humidity() - delta*x[I["blue"]] - x[I["yellow"]] * x[I["blue"]]
            y[I["green"]] = x[I["yellow"]] * x[I["blue"]] - delta*x[I["green"]]
            #
            y[I["fur"]] = k1 * (kappa/(kappa + x[I["red"]] + x[I["yellow"]] + x[I["blue"]] + x[I["green"]])) - delta*x[I["fur"]]
            y[I["feathers"]] = x[I["green"]] - delta*x[I["feathers"]]
            y[I["scales"]] = x[I["red"]]*x[I["yellow"]]*x[I["blue"]]*k2 - delta * x[I["scales"]]
            return y

        x_0 = np.array([0,0,0,0,0,0,0])

        euler_np(x_0, system, 0.01, 1)

        xs = [x_0]
        ts = 0.01
        size = 1000
        for i in range(size-1):
            xs.append(euler_step(xs[-1], system, ts))

        fig, (ax1, ax2) = plt.subplots(2)

        for l in ["red", "blue", "yellow", "green"]:
            i = I[l]
            ax1.plot(np.linspace(0,1,size), [ x[i] for x in xs], label=f"{l}", color=colors[l])
            ax1.hlines(sum(setpoints[l])/2, 0, 1, color=colors[l], linestyle="dotted")
            ax1.axhspan(setpoints[l][0], setpoints[l][1], 0, 1, facecolor=colors[l], alpha=0.01)

        for l in ["fur", "feathers", "scales"]:
            i = I[l]
            ax2.plot(np.linspace(0,1,size), [ x[i] for x in xs], label=f"{l}", color=colors[l])
            ax2.hlines(sum(setpoints[l])/2, 0, 1, color=colors[l], linestyle="dotted")
            ax2.axhspan(setpoints[l][0], setpoints[l][1], 0, 1, facecolor=colors[l], alpha=0.01)

        fig.suptitle("System's dynamics")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Concentrations")
        ax1.legend()
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Concentrations")
        ax2.legend()
        return fig   

    @reactive.Effect
    @reactive.event(input.show, ignore_none=True)
    def _():
        m = ui.modal(
            ui.HTML('<div style="text-align:center"><h3></h3><img src="https://media.istockphoto.com/id/494839519/vector/knight-fighting-dragon.jpg?s=612x612&w=0&k=20&c=GUnR0APRVkiuFiREW2Psr0CkBKDaK6Bkkes5mmXENYQ=" alt="dragon" style="width:80%;text-align:center;height:90%"></div>'),
            title="Here is your dragon!",
            easy_close=True,
            footer=None,
            size='xl'
        )
        ui.modal_show(m) 


app = App(app_ui, server)