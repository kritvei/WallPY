
import matplotlib.pyplot as plt
from rcParams import *
import sys
import attributes as attr

# sys.path.append(sys.path[0] + "\\..\\IO")
# from ..IO.classes import CypherBatch, CypherFile



class Ax:

    default_kwargs = {
        "xlabel": "",
        "ylabel": "",
        "legend": False,
        "labels": [],
        "scalebar": False,
        "colorbar": False,
        "values": None,
        "vmin": 0,
        "vmax": None,
        "vmax_std": None,
        "origin": "lower",
    } #TODO: Find the necessary kwargs

    def __init__(self, fig, **kwargs):

        if "ax" in kwargs:
            self.ax = kwargs["ax"]
        else:
            self.ax = fig.add_subplot() #TODO: Will have to depend on figure etc. 


        self.fig = fig
        self.kwargs = kwargs

        for key, value in self.default_kwargs.items():
            if key not in self.kwargs:
                self.kwargs[key] = value
        
        self.set_labels()
        return
    
    def set_labels(self):
        self.ax.set_xlabel(self.kwargs["xlabel"])
        self.ax.set_ylabel(self.kwargs["ylabel"])
        return
    
    def update_kwargs(self, **kwargs):

        for key, value in kwargs.items():
            self.kwargs[key] = value
        return
    
    def plot_cAFM(self, datafile, key:str="CR", **kwargs): #TODO: Fix imports
        """
        Plots a cAFM scan.
        """

        self.update_kwargs(**kwargs)

        #Figure out something universal for this.

        if self.kwargs["values"] is not None:
            values = self.kwargs["values"]*1e12
        else:
            values = datafile[key]*1e12
        
        if self.kwargs["vmax_std"] is not None:
            vmax_std = self.kwargs["vmax_std"]
            vmax = np.std(values)*vmax_std
        else:
            vmax = None
        
        im = self.ax.imshow(values, vmax=vmax, origin=self.kwargs["origin"])      
        self.ax.axis("off")
        self.fig.colorbar(im, ax=self.ax, label="Current (pA)") #TODO: Fix the label. Or this is a bit hard-coded. See if more general is possible eventually.
        self.set_labels()
        attr.add_scalebar(self.ax, datafile.x_res)
        return
    

    
    def plot_inset(self, datafile, key:str="CR", **inset_kwargs):

        default_kwargs = {
                "x1": 0,
                "y1": 0,
                "x2": 10,
                "y2": 10,
                "left_x": 0,
                "left_y": 0,
                "width": 0.5,
                "height": 0.5,
                "indicate": True,
                "values": None,
            }
        
        for kwarg_key, kwarg_value in default_kwargs.items():
            if kwarg_key not in inset_kwargs:
                inset_kwargs[kwarg_key] = kwarg_value

        if inset_kwargs["values"] is not None:
            values = inset_kwargs["values"] #*1e12
        else:
            values = datafile[key] #*1e12
        
        if self.kwargs["vmax_std"] is not None:
            vmax_std = self.kwargs["vmax_std"]
            vmax = np.std(values)*vmax_std
        else:
            vmax = None
        
        im = self.ax.imshow(values, vmax=vmax, origin="lower")      
        self.ax.axis("off")
        self.fig.colorbar(im, ax=self.ax, label="Value") #TODO: Fix the label in kwargs or something.
        attr.add_scalebar(self.ax, datafile.x_res)


        axins = self.ax.inset_axes([inset_kwargs["left_x"], inset_kwargs["left_y"], inset_kwargs["width"], inset_kwargs["height"]])
        axins.imshow(values, vmax=vmax, origin="lower")
        axins.set_xticks([])
        axins.set_yticks([])
        axins.set_xlim(inset_kwargs["x1"], inset_kwargs["x2"])
        axins.set_ylim(inset_kwargs["y1"], inset_kwargs["y2"])
        if inset_kwargs["indicate"]:
            rp, lines = self.ax.indicate_inset_zoom(axins, edgecolor="black", lw=1)
            for l in lines:
                l.set_linestyle("--")
                l.set_color("black")
                l.set_linewidth(1)

                # if l.get_visible():
                #     l.set_visible(False)
                # else:
                #     l.set_visible(True)
            # lines.set_linewidth(2)


        
        return

