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

language = "de"

locale = {
#### ENGLISH TRANSLATION ####
    "en" : {
        "title" : "How to pimp your dragon",
        # main_text is in markdown format
        "main_text" : """ 
Some scientist have discovered that dragon eggs can be exposed to different conditions to make the newborn dragons perfectly adapted to 
different natural enviroment. Even though they understood the principle of the conditions that should be met, they still don't know how to handle the eggs
properly. Can you help them?
        
You have recieved a note with some instructions on how to use the dragon egg incubator interface:
        
1. Set up the target environment in the **Environment** section. This will help you understand the target expression the genes. 
2. The **Incubator controls** panel provides you with access to the working parameters for the egg's environment. Your goal is to find the right ones so that the egg will hatch!
3. Once you are done setting the parameters, you can use the **Start incubation** button to apply them. You will observe how the expression of the genes will
    change immediately in the **Monitor** section. The intervals show the target expression that you should reach for each gene at the final time.
4. By clicking the **Check your egg** button, you can see if you managed to hatch the egg and, if that is the case, see the dragon itself!
5. For each environment there is an hidden dragon variant that you can find by playing with the parameters. Can you follow the hints and find them all?

Time to get to work!   
        """,
        "env_selector" : dict(forest="forest", ocean="ocean", volcano="volcano", desert='desert', arctic="arctic"),
        "incubator_UI" : dict(
            title="Incubator controls",
            f_hot="Incubation temperature (Celsius)",
            humidity="Humidity (%)",
            thermocline="Day/Night temperature difference (0 to 1)",
            diet="Nutrient supplement (Kcal)",
            sunscreen="Light exposure (0 total darkness, 1 full lighting)",
            run="Start incubation",
            show="Check your egg"
        ),
        "monitor_UI" : dict(
            title="Gene expression monitor",
        ),
        "monitor_plots" : dict(
            time="Time",
            expression="Expression level",
        ),
        "colors/features" : dict(
            red="Red color gene",
            yellow="Yellow color gene",
            blue="Blue color gene",
            green="Green color gene",
            fur="Fur growth factor",
            feathers="Feathers growth factor",
            scales="Scale growth factor",
        ),
        "modal" : dict(
            success="Congratulations! Here is your dragon!",
            failure="Too bad, the egg didn't hatch! Try again!",
            special="Wow! You found a secret dragon!",
            info="Press outside of the box to return to the incubator settings.",
        ),
        "environments" : dict(
            title = "Target environment",            
            volcano = "Volcano dragons can cope with extreme high temperatures. Their coulour helps them to blend in with the lava. There is a rumor that some of them live in caves hidden within volcanos, where nothing else can survive [Secret].",
            forest  = "Forest dragons are adapted to live among the vegetation of their habitat. Their green colour helps them to blend in with the leaves. It is said that some variants can produce only green pigments [Secret].",
            ocean   = "Ocean dragons live both over and under water and they are always blue in color. \n Some of them have a balanced amount of scales and fur, but this combination also changes their shape [Secret].",
            desert  = "Desert dragons can survive the hostile conditions of the desert. Based on the pigments they express, some of them can look like sand, while others have a metallic appearance that resembles copper [Secret].",
            arctic  = "Artic dragons can only survive at sub-zero temperatures. They are usually white, but some of them can express a small amount of blue pigments to seem as made of ice [Secret].",
        ),
    },
#### GERMAN TRANSLATION ####
    "de" : { # TODO
        "title" : "How to pimp your dragon",
        # main_text is in markdown format
        "main_text" : """ 
Wissenschaftler haben herausgefunden, dass Dracheneier verschiedenen Bedingungen ausgesetzt werden können, um die neugeborenen Drachen perfekt an unterschiedliche Umgebungen anzupassen.
Aber selbst wenn sie im Prinzip verstanden haben, was das Endresultat sein soll, wissen sie immer noch nicht, wie sie die Eier ausbrueten müssen um die entsprechenden
Resultate zu erreichen. 
Kannst du ihnen helfen? 
Du hast eine Nachricht mit einigen Anweisungen zur Verwendung des Drachenei-Brutschranks erhalten: 

1. Wähle die Zielumgebung im Abschnitt **Umgebung** aus. Dann werden dir die Ziel-Level der Gene angezeigt. 
2. Über das Bedienfeld **Inkubatorsteuerung** hast du Zugriff auf die Einstellungen für die Umgebung des Eies. Dein Ziel ist es, die richtigen zu finden, damit das Ei schlüpfen kann! 
3. Sobald du mit dem Einstellen der Parameter fertig bist, kannst du die Schaltfläche **Inkubation starten** verwenden, um sie anzuwenden. Im Abschnitt **Beobachtung** kannst du dann die Auswirkungen der Bruteinstellungen auf die Genablesung sehen. Die markierten Intervalle zeigen die Ziellevel an, die du für jedes Gen erreichen solltest. 
4. Mit der Schaltfläche **Überprüfe dein Ei** kannst du sehen, ob du es geschafft hast, das Ei auszubrüten, und wenn das der Fall ist, auch den Drachen selbst! 
5. Für jede Umgebung gibt es eine versteckte Drachenvariante, die du finden kannst, indem du mit den Einstellungen spielst. Kannst du den Hinweisen folgen und sie alle finden?

Mach dich an die Arbeit und hilf den Wissenschaftlern die Drachen anzupassen!
        """,
        "env_selector" : dict(forest="Wald", ocean="Ozean", volcano="Vulkan", desert='Wüste', arctic="Arktis"),
        "incubator_UI" : dict(
            title="Brutschrankparameter",
            f_hot="Temperatur (Celsius)",
            humidity="Luftfeuchtigkeit (%)",
            thermocline="Temperaturunterschied Tag/Nacht (0 to 1)",
            diet="Nährstoffe (Kcal)",
            sunscreen="Licht (0 komplette Dunkelheit, 1 helles Licht)",
            run="Ausbrüten",
            show=" Überprüfe dein Ei"
        ),
        "monitor_UI" : dict(
            title="Proteinlevel-Anzeige",
        ),
        "monitor_plots" : dict(
            time="Zeit",
            expression="Proteinlevel",
        ),
        "colors/features" : dict(
            red="Gen für rote Farbe",
            yellow="Gen für gelbe Farbe",
            blue="Gen für blaue Farbe",
            green="Gen für grüne Farbe",
            fur="Gen für Fell",
            feathers="Gen für Federn",
            scales="Gen für Schuppen",
        ),
        "modal" : dict(
            success="Herzlichen Glückwunsch! Hier ist dein Drache!",
            failure="Schade, dein Drache ist nicht geschlüpft. Versuche es noch einmal!",
            special="Wow! Du hast einen geheimen Drachen gefunden!",
            info="Klicke ausserhalb des Bildes um zu den Brutkasteneinstellungen zurückzugelangen.",
        ),
        "environments" : dict(
            title = "Zielumgebung",            
            volcano = "Vulkandrachen können mit extrem hohen Temperaturen umgehen. Ihre Farbe hilft ihnen, mit der Lava zu verschmelzen. Es geht das Gerücht um, dass einige von ihnen in Höhlen leben, die in Vulkanen versteckt sind, wo nichts anderes überleben kann [Geheimtipp].",
            forest  = "Walddrachen sind an die Vegetation ihres Lebensraums angepasst. Ihre grüne Farbe hilft ihnen, mit den Blättern zu verschmelzen. Es wird gesagt, dass einige Varianten nur grüne Pigmente erzeugen können [Geheimtipp].",
            ocean   = "Ozeandrachen leben sowohl über als auch unter Wasser und haben immer eine blaue Farbe. \n Einige von ihnen haben eine ausgewogene Menge an Schuppen und Fell, aber diese Kombination verändert auch ihre Form [Geheimtipp].",
            desert  = "Wüstendrachen können die lebensfeindlichen Bedingungen der Wüste überleben. Aufgrund ihrer Pigmente können einige von ihnen wie Sand aussehen, während andere ein metallisches Aussehen haben, das Kupfer ähnelt [Geheimtipp].",
            arctic  = "Polardrachen können nur bei Minusgraden überleben. Sie sind normalerweise weiß, aber einige von ihnen können eine kleine Menge blauer Pigmente ausdrücken, um den Anschein zu erwecken, als wären sie aus Eis [Geheimtipp].",
        ),
    },
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
         /* Dropdown Button (from w3school)*/
        .dropbtn {
        background-color: #4287f5;
        color: white;
        padding: 16px;
        font-size: 16px;
        border: none;
        width: 100%;
        }

        /* The container <div> - needed to position the dropdown content */
        .dropdown {
        position: absolute;
        display: inline-block;
        }

        /* Dropdown Content (Hidden by Default) */
        .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f1f1f1;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
        z-index: 1;
        }

        /* Links inside the dropdown */
        .dropdown-content a {
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
        }

        /* Change color of dropdown links on hover */
        .dropdown-content a:hover {background-color: #ddd;}

        /* Show the dropdown menu on hover */
        .dropdown:hover .dropdown-content {display: block; z-index: 1; position:fixed; width:inherit}

        /* Change the background color of the dropdown button when the dropdown content is shown */
        .dropdown:hover .dropbtn {background-color: #214382;} 
        """
    ),
    ui.HTML('<br>'),
    ui.HTML('<div>'),
    ui.HTML('<div style="overflow:hidden;background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)">'),
    ui.HTML('<div style="width: 80%;position:relative; float:left; background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)">'),
    ui.HTML('<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/ETH_Z%C3%BCrich_Logo_black.svg/1024px-ETH_Z%C3%BCrich_Logo_black.svg.png" alt="ETH logo", height="50px">'),
    ui.HTML('</div>'),
    #ui.HTML('<div style="width: 20%;position:relative; float:right;background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)">'),
    ui.HTML("""
        
        <div class="dropdown">
        <button class="dropbtn">Language/Sprache</button>
        <div class="dropdown-content" style="width:inherit; position:relative">
            <a href="/eng/index.html">English</a>
            <a href="/ger/index.html">Deutsch</a>
        </div>
        </div>
            
            """),
    ui.HTML('</div>'),
    #ui.HTML('</div>'),
    ui.HTML('</div>'),
    ui.HTML('<hr>'),
    ui.HTML(f"<H1><b>{locale[language]['title']}</b></H1>"),
    ui.HTML('<hr>'),
    ui.markdown(locale[language]["main_text"]),
    ui.HTML("<hr>"),
    ui.HTML(f'<h4>{locale[language]["environments"]["title"]}</h4>'),
    ui.input_select("env", None,
                dict(forest=locale[language]["env_selector"]["forest"], ocean=locale[language]["env_selector"]["ocean"], volcano=locale[language]["env_selector"]["volcano"], desert=locale[language]["env_selector"]["desert"], arctic=locale[language]["env_selector"]["arctic"])
            ),
    ui.output_text("dragon_description", inline=True),
    ui.HTML('<hr>'),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.HTML(f'<h3>{locale[language]["incubator_UI"]["title"]}</h3>'),
            #ui.HTML('<hr>'),
            ui.input_slider("f_hot", locale[language]["incubator_UI"]["f_hot"], 0, 50, value=36, step=50/100),
            ui.input_slider("humidity", locale[language]["incubator_UI"]["humidity"], 0, 100, value=30, step=1),
            ui.input_slider("thermocline", locale[language]["incubator_UI"]["thermocline"], 0, 1, value=0.5, step=0.01),
            ui.input_slider("diet", locale[language]["incubator_UI"]["diet"], 0, 2000, value=600, step=2000/100),
            ui.input_slider("sunscreen", locale[language]["incubator_UI"]["sunscreen"], 0, 1, value=0.5, step=0.01),
            ui.input_action_button("run", locale[language]["incubator_UI"]["run"]),
            ui.HTML('<hr>'),
            ui.input_action_button("show", locale[language]["incubator_UI"]["show"], class_="btn-primary"),
        ),
        ui.panel_main(
            ui.HTML(f'<h3>{locale[language]["monitor_UI"]["title"]}</h3>'),
            ui.output_plot("plot", height = '100%'),
            style="border-color:#444444;border-width:2px;border-style:solid;box-shadow:5px 0px 5px -5px #AAAAAA;",
        )
    ),
    ui.HTML('<hr>'),
    ui.HTML('<p style="color:#555555">Scientifica 2023 - CTSB group, D-BSSE</p>'),
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

dragon_urls = {
    "volcano" : "https://lh3.googleusercontent.com/drive-viewer/AITFw-zyuwT1Zz9rs90pQhfxeGu7kIsyK_uuiUi3S4r72TguQjGKB56oR3m4s2ZNpwBKXvoDeksjORnuK9ByW02egLpGli-Yjg=s1600",
    "forest"  : "https://lh3.googleusercontent.com/drive-viewer/AITFw-zMnjWPE-ls0BVlyXZj6_A7X_YLP_OL7cRNoGdluuRQSPGySLcP2nKw9Ms4MtHsKeFTfWabRx2O2Mvs3CNLl6cyk5HIWw=s1600",
    "ocean"   : "https://lh3.googleusercontent.com/drive-viewer/AITFw-wOxMaSDFnUsLGHjqpl1pcCA9U-gpLNQl8lMa0C9xBRYnrE0sEqY_ROmUw97aCRTm1PXDkFCkEUENjZn-iHA3-ydRhyLQ=s1600",
    "desert"  : "https://lh3.googleusercontent.com/drive-viewer/AITFw-yImnNgBpsFyIcqQ6Z4AGC0eXpothT8IDvS1qK6W3un1CXrpxgUfdGn5aBKh_wGq2CXx9LTcvkyS1ViE-TOQPZvgXGmRg=s1600",
    "arctic"  : "https://lh3.googleusercontent.com/drive-viewer/AITFw-x9fujdnfjDdgTdVqoV8KQwHDyUTuTDhvNoHBeRcf66ga_xzyyhNfpzrEoX5cb8F2F7GT2IafS0Ma85bLyLHX5K-yaung=s1600",
}

dragon_urls_alt = { # TODO
    "volcano" : "https://lh3.googleusercontent.com/drive-viewer/AITFw-x1iZPrYZ-HJoSbm0W3j6Mw2OdvyLi8azqXLqIHc4STwQYAx030ePYWrP93Y_cU9huu5L9v9rON75K8CXaogWkEQc2WMw=s1600",
    "forest"  : "https://lh3.googleusercontent.com/drive-viewer/AITFw-y4ghWSOyb1dOjOMnhqvpIJG1-3D3PzQamdvaH1IAc5qPQxLv10qmTUFOWX4ihNcIfD7u9DyBWw2iOnnJlpy9CC-NJITQ=s1600",
    "ocean"   : "https://lh3.googleusercontent.com/drive-viewer/AITFw-yxunUZqrokfrrIWLj63zLKL1mIev-4vngrSOT6eCQLC8RMN48IFWZh6bX1mK03TP9ze5obj02CVIC0wgPj_7Vs1S7yUQ=s1600",
    "desert"  : "https://lh3.googleusercontent.com/drive-viewer/AITFw-wTn-q2vl-vMr_3Tt37ZItDqk5Pl-XIwxPXF9jUiNPZLxqAWdwu2czmCvDpfO6CmfezzWS3M4bufegavnpIT2F7PGXDtg=s1600",
    "arctic"  : "https://lh3.googleusercontent.com/drive-viewer/AITFw-wsBZE_wL3G81MbCNUaGg9bLWHbnxrvWCRhzixR8TakceCeDpF7tSOkz2xScM8E7FP0mQ8RyM_poBO_EvAHFUyFPZ7-AA=s1600",
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
        global locale
        global language
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
        global locale
        global language
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
                ax.set_ylabel(locale[language]["monitor_plots"]["expression"])
            #ax.legend()
            ax.set_title(locale[language]["colors/features"][l])
            ax.set_ylim((0,1.2))

        
        for (pos, l) in enumerate(["fur", "feathers", "scales"]):
            ax = plt.subplot2grid((2,12), (1,pos*4), colspan=4)
            ax.grid(True)
            i = I[l]
            ax.plot(np.linspace(0,1,size), [ x[i] for x in xs], label=f"{l}", color=colors[l])
            ax.hlines(sum(setpoints[l])/2, 0, 1, color=colors[l], linestyle="dotted")
            ax.axhspan(setpoints[l][0], setpoints[l][1], 0, 1, facecolor=colors[l], alpha=0.2)
            ax.set_xlabel(locale[language]["monitor_plots"]["time"])
            if pos==0:
                ax.set_ylabel(locale[language]["monitor_plots"]["expression"])
            ax.set_title(locale[language]["colors/features"][l])
            ax.set_ylim((0,1.2))

        #fig.suptitle("**System's dynamics**")
        line = plt.Line2D((0.5,1),(-.5,-.5), color='k', linewidth=3)
        fig.add_artist(line)
        fig.tight_layout()
        return fig   

    @reactive.Effect
    @reactive.event(input.show, ignore_none=True)
    def _():
        global locale
        global language
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
                title=locale[language]["modal"]["success"],
                easy_close=True,
                footer=locale[language]["modal"]["info"],
                size='l',
                fade=False,
                style="background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)",
            )
            ui.modal_show(m) 
        elif eval_setpoint(setpoints_alt, xs[-1]):
            # add here alternative setpoints (if we make them)
            global dragon_urls_alt
            m = ui.modal(
                ui.HTML(f'<div style="text-align:center;background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)"><h3></h3><img src="{dragon_urls_alt[input.env()]}" alt="dragon" style="width:80%;text-align:center;height:90%"></div>'),
                title=locale[language]["modal"]["special"],
                easy_close=True,
                footer=locale[language]["modal"]["info"],
                size='l',
                fade=False,
                style="background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)",
            )
            ui.modal_show(m) 
        else: 
            m = ui.modal(
                ui.HTML('<div style="text-align:center;background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)"><h3></h3><img src="https://lh3.googleusercontent.com/drive-viewer/AITFw-zRUCixU9Ub3CFs7y2iCwstJ4hW8Ol1qPVYXpX0Y8bYYAPq0T5f8nqjRik5RnWOnj5MQzf_wphFZJQiNSlYyPpEZhHomQ=s1600" alt="EGG" style="width:80%;text-align:center;height:90%"></div>'),
                title=locale[language]["modal"]["failure"],
                easy_close=True,
                footer=locale[language]["modal"]["info"],
                size='l',
                fade=False,
                style="background-image:url(https://static.vecteezy.com/system/resources/previews/000/584/379/original/abstract-white-paper-textured-background-for-design-your-work-texture-vector.jpg)",
            )
            ui.modal_show(m) 
        

    @output
    @render.text
    @reactive.event(input.env, ignore_none=True)
    def dragon_description():
        global locale
        global language
        if input.env() is None:
            return locale[language]["environments"]["title"]
        else:
            return locale[language]["environments"][input.env()] # add here the description of the environment


app = App(app_ui, server)