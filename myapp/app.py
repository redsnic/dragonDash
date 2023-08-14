import matplotlib.pyplot as plt
import numpy as np
from shiny import ui, render, App, reactive
from shiny.types import ImgData
from shinywidgets import output_widget, render_widget
from htmltools import TagList

# Create some random data

kwargs = {
    "class" : "maindiv"
}

app_ui = ui.page_fixed(
    ui.tags.style(
        """
        body {
            background-image: url(https://img.freepik.com/premium-vector/japanese-vintage-elements-seamless-pattern-with-angry-poisonous-snake-dangerous-fantasy-dragon-chrysanthemum-sakura-flowers_225004-2582.jpg)
        }
        div {
            background-color: #FFFFFF
        }
        .maindiv {
            opacity:1;color:black;box-shadow:0px 0px 20px 20px #888888;background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)
        }
        .modal.show{
            background-image: url(https://img.freepik.com/premium-vector/japanese-vintage-elements-seamless-pattern-with-angry-poisonous-snake-dangerous-fantasy-dragon-chrysanthemum-sakura-flowers_225004-2582.jpg)
        }
        .modal-content{
            border-color:#444444;border-width:2px;border-style:solid;opacity:1;color:black;box-shadow:0px 0px 20px 20px #888888;
        }
        """
    ),
    ui.HTML('<br>'),
    ui.HTML('<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/ETH_Z%C3%BCrich_Logo_black.svg/1024px-ETH_Z%C3%BCrich_Logo_black.svg.png" alt="ETH logo", height="50px">'),
    ui.HTML('<hr>'),
    ui.HTML("<H1><b>How to pimp your dragon</b></H1>"),
    ui.HTML('<hr>'),
    ui.markdown("""
        Some scientist have discovered that dragon eggs can be exposed to different conditions to make the newborn dragons to be perfectly adapted to 
        different natural enviroment. Even if they understood in principle what conditions should be met they still don't know how to handle the eggs
        properly, can you help them?
                
        You have recieved a post-it note with some instructions on how to use the dragon egg incubator interface:
                
        1. Set up the target environment in the **Environment** section. This will help you in understanding the target expression the genes. 
        2. The **Incubator controls** panel gives you access to the working parameters for the egg's environment. Your goal is to find the right ones!
        3. One you are done setting the parameters, you can use the **Start incubation** button to apply them. You will see how the expression of the genes will
           change right away in the **Monitor** section.
        4. With the **Check your egg** button you can see if you managed to hatch the egg and, if that is the case, see the dragon itself!

        Time to work!  
    """),
    ui.HTML("<hr>"),
    ui.HTML('<h4>Target environment</h4>'),
    ui.input_select("env", None,
                dict(forest="forest", ocean="ocean", volcano="volcano", desert='desert', arctic="arctic")
            ),
    ui.output_text("dragon_description", inline=True),
    ui.HTML('<hr>'),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.HTML('<h3>Incubator controls</h3>'),
            #ui.HTML('<hr>'),
            ui.input_slider("f_hot", "Incubation temperature (Celsius)", 0, 50, value=36, step=50/100),
            ui.input_slider("humidity", "Humidity (%)", 0, 100, value=30, step=1),
            ui.input_slider("thermocline", "Day/Night temperature difference (0 to 1)", 0, 1, value=0.5, step=0.01),
            ui.input_slider("diet", "Nutrient supplement (Kcal)", 0, 2000, value=600, step=2000/100),
            ui.input_slider("sunscreen", "Light exposure (0 total darkness, 1 full lighting)", 0, 1, value=0.5, step=0.01),
            ui.input_action_button("run", "Start incubation"),
            ui.HTML('<hr>'),
            ui.input_action_button("show", "Check your egg", class_="btn-primary"),
        ),
        ui.panel_main(
            ui.HTML('<h3>Gene expression monitor</h3>'),
            #ui.HTML('<hr>'),
            ui.output_plot("plot", height = '100%'),
            #output_widget("plot", height = '100%'),
            #ui.HTML('<hr>'),
            #ui.output_ui("dragon_image"),
            #ui.output_ui("open_dialog")
            style="border-color:#444444;border-width:2px;border-style:solid;box-shadow:5px 0px 5px -5px #AAAAAA;",
        )
    ),
    ui.HTML('<hr>'),
    ui.HTML('<p style="color:#555555">Scientifica 2023 - CTSB group, D-BSSE</p>'),
    ui.HTML('<br>'),
    ui.HTML('<br>'),
    **kwargs
    
)

I = {
    "red" : 0,
    "yellow" : 1,
    "blue" : 2,
    "green" : 3,
    "fur" : 4,
    "feathers" : 5,
    "scales" : 6
}

setpoints_dict = {}
setpoints_dict["volcano"] = {
    "red" : (0.7, 0.9),
    "yellow" : (0.2, 0.6),
    "blue" : (0.0, 0.1),
    "green" : (0.0, 0.1),
    "fur" : (0.0, 0.1),
    "feathers" : (0.0, 0.1),
    "scales" : (0.6, 0.8),
}
setpoints_dict["forest"] = {
    "red" : (0.2, 0.3),
    "yellow" : (0.0, 0.1),
    "blue" : (0.175, 0.25),
    "green" : (0.4, 0.6),
    "fur" : (0.0, 0.1),
    "feathers" : (1.1, 1.25),
    "scales" : (0.5, 0.7),
}
setpoints_dict["ocean"] = {
    "red" : (0., 0.1),
    "yellow" : (0.00, 0.1),
    "blue" : (0.35, 0.45),
    "green" : (0.0, 0.1),
    "fur" : (0.1, 0.3),
    "feathers" : (0.05, 0.15),
    "scales" : (0.6, 0.8),
}
setpoints_dict["desert"] = {
    "red" : (0.2, 0.9),
    "yellow" : (0.8, 1),
    "blue" : (0., 0.3),
    "green" : (0., 0.3),
    "fur" : (0., 0.1),
    "feathers" : (0., 0.1),
    "scales" : (0.2, 0.4),
}
setpoints_dict["arctic"] = {
    "red" : (0.0, 0.1),
    "yellow" : (0.0, 0.1),
    "blue" : (0.0, 0.2),
    "green" : (0.0, 0.1),
    "fur" : (0.25, 0.35),
    "feathers" : (0., 0.1),
    "scales" : (0.0, 0.1),
}

setpoints_dict_alt = {} # TODO
setpoints_dict_alt["volcano"] = { # diamond/crystal dragon
    "red" : (0., 0.1),     # what if the dragon was in a cave within his volcano?
    "yellow" : (0., 0.1),
    "blue" : (0.0, 0.1),
    "green" : (0.0, 0.1),
    "fur" : (0.0, 0.1),
    "feathers" : (0.0, 0.1),
    "scales" : (0., 0.1),  # bring everythin to <0.1
}
setpoints_dict_alt["forest"] = { # leaf/wood dragon
    "red" : (0., 0.1), # what if we would use only the green pigment?
    "yellow" : (0.0, 0.1),
    "blue" : (0.0, 0.1), #
    "green" : (0.8, 1), #
    "fur" : (0.0, 0.1),
    "feathers" : (1.1, 1.25),
    "scales" : (0., 0.1),
}
setpoints_dict_alt["ocean"] = { # asian dragon
    "red" : (0., 0.1),  # what would happen if we balanced fur and scales while keeping the blue pigment?
    "yellow" : (0.0, 0.1),
    "blue" : (0.15, 0.5),
    "green" : (0.0, 0.1),
    "fur" : (0.3, 0.5), # balance fur/feathers/scales
    "feathers" : (0., 0.1), 
    "scales" : (0.3, 0.5), 
}
setpoints_dict_alt["desert"] = { # copper dragon
    "red" : (0.9, 1), # what if both red and yellow pigments were maximally expressed?
    "yellow" : (0.8, 1),
    "blue" : (0., 0.3),
    "green" : (0., 0.3),
    "fur" : (0., 0.1),
    "feathers" : (0., 0.1),
    "scales" : (0.2, 0.4),
}
setpoints_dict_alt["arctic"] = { # ice dragon
    "red" : (0.0, 0.1),  # what if we add some blue pigment while removing fur, feathers and scales?
    "yellow" : (0.0, 0.1),
    "blue" : (0.1, 0.3), # we want some blue 
    "green" : (0.0, 0.1),
    "fur" : (0., 0.1),   # but very little of all other genes
    "feathers" : (0., 0.1),
    "scales" : (0.0, 0.1),
}

descrpttions = {
    "volcano" : "Volcano dragons can cope with extreme high temperatures. Their coulour helps them to blend in with the lava. There is a rumor that some of them live in caves hidden within volcanos, where nothing else can survive [Secret].",
    "forest"  : "Forest dragons are adapted to live among the vegetation of their habitat. Their green colour helps them to blend in with the leaves. It is said that some variants can produce only green pigments [Secret].",
    "ocean"   : "Ocean dragons live both over and under water. \n[Secret] Some of them have both scales and feathers, but this combination also changes their shape.",
    "desert"  : "Desert dragons can survive the hostile conditions of the desert. Based on the pigments they express, some of them can look like sand, while others have a metallic appearance [Secret].",
    "arctic"  : "Artic dragons can only survive at sub-zero temperatures. They are usually white, but some of them can express blue pigments to seem as made of ice [Secret].",
}

dragon_urls = {
    "volcano" : "https://lh3.googleusercontent.com/drive-viewer/AITFw-zyuwT1Zz9rs90pQhfxeGu7kIsyK_uuiUi3S4r72TguQjGKB56oR3m4s2ZNpwBKXvoDeksjORnuK9ByW02egLpGli-Yjg=s1600",
    "forest"  : "https://lh3.googleusercontent.com/drive-viewer/AITFw-zMnjWPE-ls0BVlyXZj6_A7X_YLP_OL7cRNoGdluuRQSPGySLcP2nKw9Ms4MtHsKeFTfWabRx2O2Mvs3CNLl6cyk5HIWw=s1600",
    "ocean"   : "https://lh3.googleusercontent.com/drive-viewer/AITFw-wOxMaSDFnUsLGHjqpl1pcCA9U-gpLNQl8lMa0C9xBRYnrE0sEqY_ROmUw97aCRTm1PXDkFCkEUENjZn-iHA3-ydRhyLQ=s1600",
    "desert"  : "https://lh3.googleusercontent.com/drive-viewer/AITFw-yImnNgBpsFyIcqQ6Z4AGC0eXpothT8IDvS1qK6W3un1CXrpxgUfdGn5aBKh_wGq2CXx9LTcvkyS1ViE-TOQPZvgXGmRg=s1600",
    "arctic"  : "https://lh3.googleusercontent.com/drive-viewer/AITFw-x9fujdnfjDdgTdVqoV8KQwHDyUTuTDhvNoHBeRcf66ga_xzyyhNfpzrEoX5cb8F2F7GT2IafS0Ma85bLyLHX5K-yaung=s1600",
}

dragon_urls_alt = { # TODO
    "volcano" : "https://lh3.googleusercontent.com/drive-viewer/AITFw-zyuwT1Zz9rs90pQhfxeGu7kIsyK_uuiUi3S4r72TguQjGKB56oR3m4s2ZNpwBKXvoDeksjORnuK9ByW02egLpGli-Yjg=s1600",
    "forest"  : "https://lh3.googleusercontent.com/drive-viewer/AITFw-zMnjWPE-ls0BVlyXZj6_A7X_YLP_OL7cRNoGdluuRQSPGySLcP2nKw9Ms4MtHsKeFTfWabRx2O2Mvs3CNLl6cyk5HIWw=s1600",
    "ocean"   : "https://lh3.googleusercontent.com/drive-viewer/AITFw-wOxMaSDFnUsLGHjqpl1pcCA9U-gpLNQl8lMa0C9xBRYnrE0sEqY_ROmUw97aCRTm1PXDkFCkEUENjZn-iHA3-ydRhyLQ=s1600",
    "desert"  : "https://lh3.googleusercontent.com/drive-viewer/AITFw-yImnNgBpsFyIcqQ6Z4AGC0eXpothT8IDvS1qK6W3un1CXrpxgUfdGn5aBKh_wGq2CXx9LTcvkyS1ViE-TOQPZvgXGmRg=s1600",
    "arctic"  : "https://lh3.googleusercontent.com/drive-viewer/AITFw-x9fujdnfjDdgTdVqoV8KQwHDyUTuTDhvNoHBeRcf66ga_xzyyhNfpzrEoX5cb8F2F7GT2IafS0Ma85bLyLHX5K-yaung=s1600",
}

colors = {
    "red" : "red",
    "yellow" : "gold",
    "blue" : "blue",
    "green" : "green",
    "fur" : "C0",
    "feathers" : "C1",
    "scales" : "C5"
}
    
delta = 1 
kappa = 0.05
k1 = 1
k2 = 1
eta = 200

# general Euler method implementation
def euler_np(x_0, derivative, step, finalTime):
    x = x_0
    while finalTime > 0:
        x = x + step*derivative(x) # single step
        finalTime -= step
    return x

def euler_step(x, derivative, step_size):
    return x + step_size*derivative(x) # single step

def eval_setpoint(setpoint, x):
    for k,v in setpoint.items():
        if x[I[k]] < v[0]:
            return False
        if x[I[k]] > v[1]:
            return False
    return True

def server(input, output, session):
    import numpy as np
    import matplotlib.pyplot as plt
    old_data = reactive.Value(None)

    
    def system(x):
        y = np.zeros_like(x)
        # y = x
        y[I["red"]] = input.sunscreen()* input.f_hot()/50 - delta*x[I["red"]] 
        y[I["yellow"]] = input.sunscreen()*input.thermocline() - delta*x[I["yellow"]] - eta*x[I["yellow"]] * x[I["blue"]]
        y[I["blue"]] = input.sunscreen()*input.humidity()/100 - delta*x[I["blue"]] - eta*x[I["yellow"]] * x[I["blue"]]
        y[I["green"]] = eta*x[I["yellow"]] * x[I["blue"]] - delta*x[I["green"]]
        #
        y[I["fur"]] = input.diet()/1000 * k1 * (kappa/(kappa + x[I["red"]] + x[I["yellow"]] + x[I["blue"]] + x[I["green"]])) - delta*x[I["fur"]]
        y[I["feathers"]] = input.diet()/1000 *2*x[I["green"]] - delta*x[I["feathers"]]
        y[I["scales"]] = input.diet()/1000 * (x[I["red"]]+x[I["yellow"]]+x[I["blue"]])*k2 - delta * x[I["scales"]]
        return y

    @output
    @render.plot
    #@render_widget
    @reactive.event(input.run, input.env, ignore_none=True)
    def plot():
        # simulation
        global setpoints_dict
        setpoints = setpoints_dict[input.env()]

        x_0 = np.array([0,0,0,0,0,0,0])
        euler_np(x_0, system, 0.01, 1)

        xs = [x_0]
        ts = 0.01
        size = 1000
        for i in range(size-1):
            xs.append(euler_step(xs[-1], system, ts))

        # plotting

        import matplotlib as mpl
        mpl.rcParams['figure.dpi'] = 300

        fig = plt.figure()
        
        for (pos, l) in enumerate(["red", "blue", "yellow", "green"]):
            ax = plt.subplot2grid((2,12), (0,pos*3), colspan=3)
            ax.grid(True)
            i = I[l]
            ax.plot(np.linspace(0,1,size), [ x[i] for x in xs], label=f"{l}", color=colors[l])
            ax.hlines(sum(setpoints[l])/2, 0, 1, color=colors[l], linestyle="dotted")
            ax.axhspan(setpoints[l][0], setpoints[l][1], 0, 1, facecolor=colors[l], alpha=0.2)
            if pos==0:
                ax.set_ylabel("Expression level")
            #ax.legend()
            ax.set_title(f"{l} color gene")
            ax.set_ylim((0,1.2))

        
        for (pos, l) in enumerate(["fur", "feathers", "scales"]):
            ax = plt.subplot2grid((2,12), (1,pos*4), colspan=4)
            ax.grid(True)
            i = I[l]
            ax.plot(np.linspace(0,1,size), [ x[i] for x in xs], label=f"{l}", color=colors[l])
            ax.hlines(sum(setpoints[l])/2, 0, 1, color=colors[l], linestyle="dotted")
            ax.axhspan(setpoints[l][0], setpoints[l][1], 0, 1, facecolor=colors[l], alpha=0.2)
            ax.set_xlabel("Time")
            if pos==0:
                ax.set_ylabel("Expression level")
            ax.set_title(f"{l} growth gene")
            ax.set_ylim((0,1.2))

        #fig.suptitle("**System's dynamics**")
        line = plt.Line2D((0.5,1),(-.5,-.5), color='k', linewidth=3)
        fig.add_artist(line)
        fig.tight_layout()
        return fig   

    @reactive.Effect
    @reactive.event(input.show, ignore_none=True)
    def _():
        global setpoints_dict
        setpoints = setpoints_dict[input.env()]

        global setpoints_dict_alt
        setpoints_alt = setpoints_dict_alt[input.env()]

        x_0 = np.array([0,0,0,0,0,0,0])
        euler_np(x_0, system, 0.01, 1)

        xs = [x_0]
        ts = 0.01
        size = 1000
        for i in range(size-1):
            xs.append(euler_step(xs[-1], system, ts))

        if eval_setpoint(setpoints, xs[-1]):
            global dragon_urls
            m = ui.modal(
                ui.HTML(f'<div style="text-align:center;background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)"><h3></h3><img src="{dragon_urls[input.env()]}" alt="dragon" style="width:80%;text-align:center;height:90%"></div>'),
                title="Congratulations! Here is your dragon!",
                easy_close=True,
                footer="Click outside of the box to return to the incubator settings.",
                size='l',
                fade=False,
                style="background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)",
            )
            ui.modal_show(m) 
        if eval_setpoint(setpoints_alt, xs[-1]):
            # add here alternative setpoints (if we make them)
            global dragon_urls_alt
            m = ui.modal(
                ui.HTML(f'<div style="text-align:center;background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)"><h3></h3><img src="{dragon_urls_alt[input.env()]}" alt="dragon" style="width:80%;text-align:center;height:90%"></div>'),
                title="Wow! You found a secret dragon!",
                easy_close=True,
                footer="Press outside of the box to return to the incubator settings.",
                size='l',
                fade=False,
                style="background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)",
            )
            ui.modal_show(m) 
        else: 
            m = ui.modal(
                ui.HTML('<div style="text-align:center;background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)"><h3></h3><img src="https://lh3.googleusercontent.com/drive-viewer/AITFw-zRUCixU9Ub3CFs7y2iCwstJ4hW8Ol1qPVYXpX0Y8bYYAPq0T5f8nqjRik5RnWOnj5MQzf_wphFZJQiNSlYyPpEZhHomQ=s1600" alt="EGG" style="width:80%;text-align:center;height:90%"></div>'),
                title="Too bad, the egg didn't hatch! Try again!",
                easy_close=True,
                footer="Press outside of the box to return to the incubator settings.",
                size='l',
                fade=False,
                style="background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)",
            )
            ui.modal_show(m) 
        

    @output
    @render.text
    @reactive.event(input.env, ignore_none=True)
    def dragon_description():
        global descrpttions
        if input.env() is None:
            return "Select an Environment"
        else:
            return f"{descrpttions[input.env()]}" # add here the description of the environment


app = App(app_ui, server)