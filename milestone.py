import matplotlib.pyplot as plt
from datetime import date
import numpy as np
import yaml
import os

# reference: https://mentalitch.com/key-events-in-rock-and-roll-history/

def create_milestone(dates, labels, as_file=None):
    fig, ax = plt.subplots(figsize=(15, 4), constrained_layout=True)

    min_date = date(np.min(dates).year, np.min(dates).month, np.min(dates).day-5)
    max_date = date(np.max(dates).year, np.max(dates).month, np.max(dates).day+5)

    ax.set_ylim(-2, 1.75)
    ax.set_xlim(min_date, max_date)

    # ax.axhline(0, xmin=0.05, xmax=0.95, c='grey', zorder=4)

    ax.scatter(dates, np.zeros(len(dates)), s=120, c='grey', zorder=2)
    ax.scatter(dates, np.zeros(len(dates)), s=30, c='black', zorder=3)

    label_offsets = np.zeros(len(dates))
    label_offsets[::2] = 0.35
    label_offsets[1::2] = -0.7

    for i, (l0, l1, d) in enumerate(zip(labels[0], labels[1], dates)):
        ax.text(d, label_offsets[i], l0, ha='center', fontweight='bold', color='green',fontsize=12)
        ax.text(d, label_offsets[i], l1, ha='center', fontweight='bold', color='black',fontsize=12)

    stems = np.zeros(len(dates))
    stems[::2] = 0.3
    stems[1::2] = -0.3
    markerline, stemline, baseline = ax.stem(dates, stems, use_line_collection=True)
    plt.setp(markerline, marker=',', color='grey')
    plt.setp(stemline, linestyle='--', color='grey')

    # hide lines around chart
    for spine in ["left", "top", "right", "bottom"]:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set(bounds=0)
        # pass
    
    # hide tick labels
    ax.set_xticks([])
    ax.set_yticks([])
    
    # ax.set_title('Important Milestones in Rock and Roll', fontweight="bold", fontfamily='serif', fontsize=16, 
    #                 color='royalblue')

    if as_file:
        if not os.path.exists(path=f'output'):
            os.mkdir(path=f'output')
        
        plt.savefig(f'output/{as_file}', bbox_inches='tight')

def parse_yaml(url):
    with open(url, 'r') as f:
        dat = yaml.safe_load(f)

    for d in dat:
        events = dat[d]['event']
        dates  = [eval(dt) for dt in dat[d]['date']]

        # date_labels = [f'{d:%^b %Y}\n' for l, d in zip (events, dates)]
        date_labels = [f'{d:%^b %Y}\n' for d in dates]
        task_labels = [f'{l.upper()}' for l in events]

        create_milestone(dates=dates, labels=[date_labels, task_labels], as_file=f'{d}.jpg')

parse_yaml(url='milestone.yaml')