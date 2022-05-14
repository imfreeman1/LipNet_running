import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

import os

def show_video_subtitle(frames, subtitle):
    fig, ax = plt.subplots()
    fig.show()

    text = plt.text(0.5, 0.1, "", 
        ha='center', va='center', transform=ax.transAxes, 
        fontdict={'fontsize': 15, 'color':'white', 'fontweight': 500})
    text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),
        path_effects.Normal()])

    subs = subtitle.split()
    inc = max(len(frames)/(len(subs)+1), 0.01)

    img = None
    for i, frame in enumerate(frames):
        sub = " ".join(subs[:int(i/inc)])

        text.set_text(sub)

        if img is None:
            img = plt.imshow(frame)
        else:
            img.set_data(frame)

        i = f'{i}'.zfill(2)
        save_path = os.path.join(os.getcwd(), f'results/result_{i}.png')
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        plt.subplots_adjust(left = 0, bottom = 0, right = 1, top = 1, hspace = 0, wspace = 0)
        plt.savefig(filename=save_path, bbox_inches='tight', pad_inches=0)
        
        fig.canvas.draw()